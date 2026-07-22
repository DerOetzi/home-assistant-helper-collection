"""USB HID barcode scanner bridge → MQTT.

Runs on a small host (e.g. a Raspberry Pi) with a USB HID barcode
scanner attached. Grabs the scanner as an exclusive input device,
decodes the German-keyboard-layout keystrokes it emits, and publishes
each completed scan (Enter-terminated) as its own MQTT message —
publishes on every scan, not just on value change, so the same barcode
can be scanned repeatedly in a row (pair with a `mqtt` trigger, e.g.
`barcode_scan_dispatcher.yaml` in this repo's `blueprints/`, rather
than a `state` trigger on a derived sensor).

Also publishes Home Assistant MQTT discovery for an availability-aware
sensor exposing the last scanned code.

Environment variables (all optional, defaults are placeholders — set
these for your actual broker/credentials):
    MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD
"""

from evdev import InputDevice, categorize, ecodes, list_devices
import paho.mqtt.client as mqtt
import logging
import sys
import signal
import time
import json
import socket
import select
import os

# Substring matched against evdev device names to find the scanner.
DEVICE_NAME_PART = "USB SCANNER"

MQTT_HOST = os.getenv("MQTT_HOST", "mqtt.example.local")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

MQTT_TOPIC_BARCODE = "scanner/kitchen/barcode"
MQTT_TOPIC_STATUS = "scanner/kitchen/status"

HA_DISCOVERY_PREFIX = "homeassistant"
HA_SENSOR_ID = "kitchen_barcode"
HA_SENSOR_NAME = "Kitchen Barcode Scanner"

LOG_LEVEL = logging.INFO

# US HID scancode -> (unshifted, shifted) character, for a German
# keyboard layout. The scanner reports positions via US HID keycodes;
# this maps those positions to what they'd type on a German QWERTZ
# keyboard (note the Y/Z swap).
KEYMAP_DE = {
    ecodes.KEY_A: ("a", "A"),
    ecodes.KEY_B: ("b", "B"),
    ecodes.KEY_C: ("c", "C"),
    ecodes.KEY_D: ("d", "D"),
    ecodes.KEY_E: ("e", "E"),
    ecodes.KEY_F: ("f", "F"),
    ecodes.KEY_G: ("g", "G"),
    ecodes.KEY_H: ("h", "H"),
    ecodes.KEY_I: ("i", "I"),
    ecodes.KEY_J: ("j", "J"),
    ecodes.KEY_K: ("k", "K"),
    ecodes.KEY_L: ("l", "L"),
    ecodes.KEY_M: ("m", "M"),
    ecodes.KEY_N: ("n", "N"),
    ecodes.KEY_O: ("o", "O"),
    ecodes.KEY_P: ("p", "P"),
    ecodes.KEY_Q: ("q", "Q"),
    ecodes.KEY_R: ("r", "R"),
    ecodes.KEY_S: ("s", "S"),
    ecodes.KEY_T: ("t", "T"),
    ecodes.KEY_U: ("u", "U"),
    ecodes.KEY_V: ("v", "V"),
    ecodes.KEY_W: ("w", "W"),
    ecodes.KEY_X: ("x", "X"),
    ecodes.KEY_Y: ("z", "Z"),
    ecodes.KEY_Z: ("y", "Y"),
    ecodes.KEY_1: ("1", "!"),
    ecodes.KEY_2: ("2", '"'),
    ecodes.KEY_3: ("3", "§"),
    ecodes.KEY_4: ("4", "$"),
    ecodes.KEY_5: ("5", "%"),
    ecodes.KEY_6: ("6", "&"),
    ecodes.KEY_7: ("7", "/"),
    ecodes.KEY_8: ("8", "("),
    ecodes.KEY_9: ("9", ")"),
    ecodes.KEY_0: ("0", "="),
    ecodes.KEY_MINUS: ("ß", "?"),
    ecodes.KEY_EQUAL: ("´", "`"),
    ecodes.KEY_BACKSLASH: ("#", "'"),
    ecodes.KEY_LEFTBRACE: ("ü", "Ü"),
    ecodes.KEY_RIGHTBRACE: ("+", "*"),
    ecodes.KEY_SEMICOLON: ("ö", "Ö"),
    ecodes.KEY_APOSTROPHE: ("ä", "Ä"),
    ecodes.KEY_COMMA: (",", ";"),
    ecodes.KEY_DOT: (".", ":"),
    ecodes.KEY_SLASH: ("-", "_"),
    ecodes.KEY_SPACE: (" ", " "),
}

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

log = logging.getLogger("scanner")
running = True


def stop(*_):
    global running
    running = False


def find_device():
    for path in list_devices():
        dev = InputDevice(path)
        if DEVICE_NAME_PART in dev.name:
            log.info("Found device: %s (%s)", dev.name, path)
            return dev
    return None


def publish_ha_discovery():
    payload = {
        "name": HA_SENSOR_NAME,
        "state_topic": MQTT_TOPIC_BARCODE,
        "availability_topic": MQTT_TOPIC_STATUS,
        "payload_available": "online",
        "payload_not_available": "offline",
        "unique_id": HA_SENSOR_ID,
        "device": {
            "identifiers": [HA_SENSOR_ID],
            "name": HA_SENSOR_NAME,
            "manufacturer": "Generic",
            "model": "USB HID Barcode Scanner",
            "sw_version": "2.0",
            "connections": [["hostname", socket.gethostname()]],
        },
    }
    topic = f"{HA_DISCOVERY_PREFIX}/sensor/{HA_SENSOR_ID}/config"
    mqttc.publish(topic, json.dumps(payload), qos=1, retain=True)


def on_connect(client, userdata, flags, reason_code, properties):
    # Called on EVERY successful (re)connect, not just the first start.
    # Important so HA discovery and the "online" status are reliably
    # re-set after a broker restart (retained messages may be lost).
    log.info("MQTT connected (rc=%s)", reason_code)
    client.publish(MQTT_TOPIC_STATUS, "online", qos=1, retain=True)
    publish_ha_discovery()


def on_disconnect(client, userdata, flags, reason_code, properties):
    log.warning("MQTT disconnected (rc=%s)", reason_code)


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

mqttc = mqtt.Client(client_id="barcode-scanner", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqttc.will_set(MQTT_TOPIC_STATUS, "offline", qos=1, retain=True)
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.reconnect_delay_set(min_delay=1, max_delay=30)

mqttc.connect_async(MQTT_HOST, MQTT_PORT, 60)
mqttc.loop_start()

while running:
    dev = find_device()

    if not dev:
        log.warning("Scanner not found, retrying...")
        time.sleep(2)
        continue

    try:
        dev.grab()
        log.info("Device grabbed")

        fd = dev.fd
        shift = False
        buffer = ""

        while running:
            r, _, _ = select.select([fd], [], [], 1)
            if not r:
                continue

            for event in dev.read():
                if event.type != ecodes.EV_KEY:
                    continue

                key = categorize(event)

                if key.scancode in (ecodes.KEY_LEFTSHIFT, ecodes.KEY_RIGHTSHIFT):
                    shift = key.keystate == key.key_down
                    continue

                if key.keystate != key.key_down:
                    continue

                if key.scancode == ecodes.KEY_ENTER:
                    if buffer:
                        mqttc.publish(MQTT_TOPIC_BARCODE, buffer, qos=1)
                        log.info("Barcode: %s", buffer)
                        buffer = ""
                    continue

                if key.scancode in KEYMAP_DE:
                    buffer += KEYMAP_DE[key.scancode][1 if shift else 0]

    except OSError as e:
        log.error("Device error: %s", e)
    except Exception as e:
        log.exception("Unexpected error: %s", e)
    finally:
        try:
            dev.ungrab()
            dev.close()
        except Exception:
            pass

        log.info("Reconnecting to scanner...")
        time.sleep(1)

mqttc.publish(MQTT_TOPIC_STATUS, "offline", qos=1, retain=True)
mqttc.loop_stop()
mqttc.disconnect()
