# Home Assistant Helper Collection

[![Validate](https://github.com/DerOetzi/home-assistant-helper-collection/actions/workflows/validate.yml/badge.svg)](https://github.com/DerOetzi/home-assistant-helper-collection/actions/workflows/validate.yml)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/DerOetzi?label=Sponsor)](https://github.com/sponsors/DerOetzi)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-ffdd00?logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/deroetzik)

Eine Sammlung wiederverwendbarer Home-Assistant-Assets: Blueprints (Automationen), ein Blueprint-Script, Lovelace-CSS-Snippets, Template-Sensoren und begleitende Standalone-Tools. Dieses Repo enthält **keine** Custom-Integration mehr (siehe unten) — für Custom Components gibt es jeweils eigene Repositories, z.B. [home-assistant-meals_and_groceries](https://github.com/DerOetzi/home-assistant-meals_and_groceries).

## Inhalt

| Ordner       | Beschreibung                                              |
|--------------|------------------------------------------------------------|
| `blueprints/`| Automation-Blueprints (direkt über die Blueprint-Import-URL in Home Assistant importierbar) |
| `script/`    | Blueprint-Scripts                                          |
| `css/`       | CSS-Snippets für Lovelace-Karten (z.B. via `card-mod`)      |
| `templates/` | Wiederverwendbare Template-Sensor-Definitionen              |
| `tools/`     | Standalone-Skripte außerhalb von Home Assistant selbst (z.B. auf einem Raspberry Pi), die per MQTT o.ä. mit HA zusammenspielen |

## Nutzung

- **Blueprints**: In Home Assistant unter Einstellungen → Automatisierungen & Szenen → Blueprints → Blueprint importieren die Raw-URL der jeweiligen `.yaml`-Datei aus `blueprints/` einfügen.
- **CSS**: Dateien aus `css/` als `local`-Ressource einbinden bzw. per `card-mod` referenzieren.
- **Templates**: Inhalte aus `templates/` in die eigene `templates:`-Konfiguration übernehmen bzw. per `!include` einbinden.
- **Tools**: Python-Skripte aus `tools/` laufen unabhängig von Home Assistant auf eigener Hardware; Konfiguration jeweils über Umgebungsvariablen (siehe Docstring im jeweiligen Skript).

## Hinweis zur Integration

Bis vor Kurzem enthielt dieses Repo unter `custom_components/deroetzi_helpers/` eine kleine, experimentelle Custom Integration. Sie wurde entfernt, da HACS pro Repository nur eine Integration verwaltet und Custom Components hier künftig grundsätzlich in eigenen, dedizierten Repositories gepflegt werden.
