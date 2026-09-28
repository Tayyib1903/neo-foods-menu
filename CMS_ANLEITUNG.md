# NEO FOODS – Inhalte selbst bearbeiten

## Einmalige Einrichtung

1. Dieses Update in das Repository `Tayyib1903/neo-foods-menu` übernehmen und auf `main` pushen (Befehl im Chat).
2. Auf GitHub unter **Settings → Pages → Build and deployment → Source** die Option **GitHub Actions** auswählen.
3. Unter **Actions → NEO Website veröffentlichen → Run workflow → main** die Veröffentlichung starten. Nach dem grünen Häkchen ist die Seite aus den CMS-Daten online.
4. https://app.pagescms.org öffnen und mit dem GitHub-Konto anmelden, das das Repository verwaltet. Die Anmeldung und die Zustimmung zu den Bedingungen selbst durchführen.
5. Wenn Pages CMS die GitHub-App-Verbindung verlangt: nur das Repository **neo-foods-menu** auswählen und die angezeigten Berechtigungen prüfen und bestätigen. Danach Repository und Branch **main** öffnen.

Die Anmeldung und GitHub-Verbindung sind nicht im ZIP enthalten. Es werden keine Zugangsdaten im Repository gespeichert.

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

## Wenn eine Änderung nicht sichtbar ist

1. Unter GitHub **Actions** den neuesten Lauf ansehen. Bei Rot den Schritt „Inhalte und Darstellung prüfen“ bzw. „Website erstellen“ öffnen; dort steht z. B., welches Bild fehlt oder welcher Preis falsch formatiert ist.
2. Den Eintrag im CMS korrigieren und erneut speichern. Keine Dateien aus alten Update-ZIPs darüberkopieren.
3. Nach erfolgreicher Veröffentlichung die Seite neu laden. Bei alten Handy-Tabs hilft vorübergehend ein Versionszusatz, z. B. `?v=neu`.

## Für spätere technische Änderungen

- Inhalte liegen in `content/*.json`; Formulare in `.pages.yml`.
- Das Startseitenlayout liegt in `templates/index.html`, das Kartenlayout in `scripts/build_site.py`; Gestaltung in den CSS-Dateien.
- `index.html` und die drei Karten im Repository sind nur der anfängliche statische Stand. Die veröffentlichte Fassung entsteht bei jedem Build in `_site`. Ab jetzt Inhalte im CMS ändern, nicht in diesen vier HTML-Dateien.
- Impressum, Datenschutz und Tischkarten werden unverändert aus ihren Dateien übernommen.
- Lokal prüfen: `python -m unittest discover -s tests -v`, dann `python scripts/build_site.py` und `python -m http.server 8000 --directory _site`.
- Der Build benötigt nur Python 3.12 und keine zusätzlichen Pakete. Nur öffentliche Webdateien gelangen nach `_site`, keine CMS-Konfiguration, Tests oder Buildskripte.
- Zur Rückkehr zum vorherigen System den Einrichtungs-Commit mit `git revert` zurücknehmen und die bisherige GitHub-Pages-Quelle (`main`, Root) wieder auswählen.

Offizielle Dokumentation: https://pagescms.org/docs/quick-start/ und https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
