# Tagebbbuch App — LB 324 Üben

Diese kleine Flask App ist eine **Übungsablage** für LB 324. Sie erfüllt die Kernpunkte:
- pre-commit formatiert Code bei jedem Commit
- pre-push testet mit pytest
- PRs auf `dev` lösen GitHub Actions Tests aus
- Merge nach `main` liefert auf Azure aus (nachdem Secrets gesetzt sind)

## Start lokal

```bash
pip install -r requirements.txt
# optional: python -m venv .venv && source .venv/bin/activate
flask --app app run
```

Erstelle eine Datei `.env` mit:
```
PASSWORD="meinGeheimesPasswort"
```
Die App liest `PASSWORD` nur zur Demo aus und zeigt es auf der Startseite.

## pre-commit Hooks installieren

```bash
pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-push
```
- Black formatiert bei jedem Commit
- Pytest läuft bei jedem Push

## GitHub Flow kurz und knapp

1. Issue anlegen mit Vorlage **Feature Anforderung**
2. Branch aus `dev` erstellen, z.B. `feature/entry-happiness`
3. Code bauen, committen, pushen
4. Pull Request **auf `dev`** erstellen → Tests laufen automatisch
5. Nach Review in `dev` mergen
6. Release: PR von `dev` nach `main` → Merge nach `main` triggert Deployment

## Azure Deployment (App Service)

1. Azure App Service für **Python** erstellen (Linux)
2. In Azure **Konfiguration** die App‑Einstellung `PASSWORD` setzen. Beim LB Wunsch: setze es auf deinen GitHub Benutzernamen
3. In GitHub **Settings → Secrets and variables → Actions** anlegen:
   - `AZURE_WEBAPP_NAME` = Name der App Service Instanz (z.B. `tagebbbuch-twin`)
   - `AZURE_WEBAPP_PUBLISH_PROFILE` = Inhalt der Publish Profile Datei aus Azure (Download im Portal)
4. Auf `main` pushen oder PR mergen → Workflow deployt automatisch

### Live URL

Trage hier deine App URL ein, z.B.:  
`https://tagebbbuch-twin.azurewebsites.net/`

## Tests

```bash
pytest -q
```

## Bewertung Checkliste

- Labels und Issue Vorlage vorhanden
- pre-commit formatiert beim Commit
- pre-push testet
- PR auf `dev` triggert Tests
- Merge nach `main` triggert Azure Deployment
- README erklärt Installation, Hooks und Secrets
- Neue Funktionalität inkl. Test wurde via Feature Branch und PR umgesetzt
```
PR CI Test
