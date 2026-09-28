# NEO FOODS – Inhalte selbst bearbeiten


## Bearbeiten

Es gibt fünf deutsche Bereiche: **Speisekarte**, **Getränkekarte**, **Eiskarte**, **Angebote**, **NEO Moments**.

- Bei Karten eine Kategorie, Produktgruppe und anschließend das Produkt öffnen. Name, Preis, Zutaten und bestätigte Allergene eintragen. Preise im Format `5,50`, ohne Eurozeichen.
- Mit **Auf der Website anzeigen** Produkte, Kategorien, Angebote oder Videos vorübergehend ausblenden.
- Bei Eis wird der **Preis pro Kugel** auch auf der Startseite verwendet.
- Die Listen erlauben neue Einträge und eine neue Reihenfolge. Mindestens eine Kategorie pro Karte behalten.
- Unter **Angebote** Preis, Uhrzeit, Titel und Zusatz ändern. Alle ausgeblendeten Angebote verschwinden einschließlich des Navigationslinks.
- Unter **NEO Moments** Video, Vorschaubild, Überschrift und Beschreibung ändern. MP4 oder WebM, maximal 25 MB; kurze komprimierte Videos verwenden. Die angezeigte Dauer im kleinen Überschrift-Feld selbst anpassen.
- **Speichern** schreibt die Änderung ins Repository. GitHub Actions erstellt und veröffentlicht anschließend automatisch die Website. Das dauert üblicherweise etwas; maßgeblich ist das grüne Häkchen unter Actions. Die bisherige Veröffentlichung bleibt bei einem Buildfehler bestehen.

## PDFs

PDFs sind getrennte Dateien. Eine Änderung im Produktformular ändert die Website, **nicht automatisch die PDF**. Nach Preis- oder Allergenänderungen eine aktualisierte PDF über das Feld **PDF-Karte** hochladen oder **PDF-Download anzeigen** ausschalten. Die vorhandenen Dateien bleiben im Repository erhalten.

## Für spätere technische Änderungen

- Inhalte liegen in `content/*.json`; Formulare in `.pages.yml`.
- Das Startseitenlayout liegt in `templates/index.html`, das Kartenlayout in `scripts/build_site.py`; Gestaltung in den CSS-Dateien.
- `index.html` und die drei Karten im Repository sind nur der anfängliche statische Stand. Die veröffentlichte Fassung entsteht bei jedem Build in `_site`. Ab jetzt Inhalte im CMS ändern, nicht in diesen vier HTML-Dateien.
- Impressum, Datenschutz und Tischkarten werden unverändert aus ihren Dateien übernommen.
- Lokal prüfen: `python -m unittest discover -s tests -v`, dann `python scripts/build_site.py` und `python -m http.server 8000 --directory _site`.
- Der Build benötigt nur Python 3.12 und keine zusätzlichen Pakete. Nur öffentliche Webdateien gelangen nach `_site`, keine CMS-Konfiguration, Tests oder Buildskripte.
- Zur Rückkehr zum vorherigen System den Einrichtungs-Commit mit `git revert` zurücknehmen und die bisherige GitHub-Pages-Quelle (`main`, Root) wieder auswählen.
