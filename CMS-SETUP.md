# NEO FOODS – Decap CMS Setup

Die Website ist für Decap CMS vorbereitet.

## Was bereits eingebaut ist

- `/admin/` als Decap-CMS-Oberfläche
- `content/speisekarte.json`
- `content/getraenkekarte.json`
- `content/eiskarte.json`
- `menu-cms.js` rendert die bestehenden Karten aus den CMS-Daten
- Upload-Ordner `uploads/`
- Das bestehende Design (`readable-menu.css`) bleibt erhalten

## Wichtig: einmalig GitHub-Login aktivieren

GitHub verlangt für den Decap-GitHub-Backend-Login einen OAuth-Server. Cloudflare Pages ist dafür **nicht** nötig.

### Stabile Variante: Netlify nur für OAuth verwenden

1. Bei Netlify ein Projekt für dieses GitHub-Repository anlegen. Die Website kann weiterhin auf GitHub Pages bleiben.
2. In GitHub unter **Settings → Developer settings → OAuth Apps** eine OAuth App anlegen.
3. Als Callback-URL verwenden: `https://api.netlify.com/auth/done`
4. Client ID + Client Secret in Netlify unter **Project configuration → Security → OAuth → Authentication Providers → GitHub** eintragen.
5. Den Netlify-Projektdomainnamen (z. B. `dein-projekt.netlify.app`) in `admin/config.yml` unter `backend.site_domain` eintragen und die Zeile auskommentieren.
6. Committen/pushen und dann öffnen: `https://tayyib1903.github.io/neo-foods-menu/admin/`

Alle Personen, die sich über den normalen GitHub-Backend anmelden, brauchen Schreibzugriff auf das Repository.

## Alternative

Decap Turbo kann die GitHub-Authentifizierung hosten. Dafür müsste `backend.name` auf `turbo-github` umgestellt und die Turbo Site-ID eingetragen werden. Turbo verwendet derzeit die Beta-Version von Decap CMS, daher ist in diesem Paket die normale GitHub-Variante vorbereitet.

## PDFs

Änderungen im CMS aktualisieren die HTML-Karten sofort nach dem GitHub-Pages-Deploy, aber **nicht** die vorhandenen PDF-Dateien (`speisekarte.pdf`, `getraenkekarte.pdf`, `eiskarte.pdf`).
