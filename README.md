# DerOetzi Helpers — Home Assistant Custom Integration

A custom integration for [Home Assistant](https://www.home-assistant.io/) providing a collection of virtual helper entities.

## Installation

### HACS (empfohlen)

1. HACS öffnen → Integrationen → Benutzerdefiniertes Repository hinzufügen
2. URL: `https://github.com/deroetzi/home-assistant-helper-collection`
3. Kategorie: Integration
4. Herunterladen und Home Assistant neu starten

### Manuell

1. Den Ordner `custom_components/deroetzi_helpers/` in den `custom_components/`-Ordner deiner HA-Installation kopieren
2. Home Assistant neu starten

## Konfiguration

1. **Einstellungen → Geräte & Dienste → Integration hinzufügen**
2. Nach „DerOetzi Helpers" suchen
3. Einen Namen eingeben und bestätigen

## Plattformen

| Plattform       | Beschreibung               |
|-----------------|----------------------------|
| `sensor`        | Berechnete Sensorwerte     |
| `switch`        | Virtuelle Schalter         |
| `binary_sensor` | Binäre Zustände            |
| `climate`       | Virtueller Klimaregler     |

## Entwicklung

```bash
# Abhängigkeiten installieren (für Linting/Tests)
pip install homeassistant

# Hassfest lokal ausführen
python -m script.hassfest
```
