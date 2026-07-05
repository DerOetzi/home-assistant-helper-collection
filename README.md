# Home Assistant Helper Collection

Eine Sammlung wiederverwendbarer Home-Assistant-Assets: Blueprints (Automationen), ein Blueprint-Script, Lovelace-CSS-Snippets und Template-Sensoren. Dieses Repo enthält **keine** Custom-Integration mehr (siehe unten) — für Custom Components gibt es jeweils eigene Repositories, z.B. [home-assistant-meals_and_groceries](https://github.com/DerOetzi/home-assistant-meals_and_groceries).

## Inhalt

| Ordner       | Beschreibung                                              |
|--------------|------------------------------------------------------------|
| `blueprints/`| Automation-Blueprints (direkt über die Blueprint-Import-URL in Home Assistant importierbar) |
| `script/`    | Blueprint-Scripts                                          |
| `css/`       | CSS-Snippets für Lovelace-Karten (z.B. via `card-mod`)      |
| `templates/` | Wiederverwendbare Template-Sensor-Definitionen              |

## Nutzung

- **Blueprints**: In Home Assistant unter Einstellungen → Automatisierungen & Szenen → Blueprints → Blueprint importieren die Raw-URL der jeweiligen `.yaml`-Datei aus `blueprints/` einfügen.
- **CSS**: Dateien aus `css/` als `local`-Ressource einbinden bzw. per `card-mod` referenzieren.
- **Templates**: Inhalte aus `templates/` in die eigene `templates:`-Konfiguration übernehmen bzw. per `!include` einbinden.

## Hinweis zur Integration

Bis vor Kurzem enthielt dieses Repo unter `custom_components/deroetzi_helpers/` eine kleine, experimentelle Custom Integration. Sie wurde entfernt, da HACS pro Repository nur eine Integration verwaltet und Custom Components hier künftig grundsätzlich in eigenen, dedizierten Repositories gepflegt werden.
