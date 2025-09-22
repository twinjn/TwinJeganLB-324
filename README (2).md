# Tagebuch App — LB 324

Diese Flask App ist meine Abgabe für die LB 324. Sie zeigt eine funktionierende CI/CD-Pipeline mit folgenden Kernelementen:

- pre-commit formatiert Code bei jedem Commit  
- pre-push testet den Code mit pytest  
- Pull Requests auf `dev` lösen GitHub Actions Tests aus  
- Merge nach `main` triggert automatisch ein Deployment auf Azure  
- Secrets sind korrekt gesetzt und dokumentiert  
- Eine neue Funktionalität wurde gemäss GitHub Flow (Issue → Feature Branch → PR → Merge → Release) umgesetzt  

---

## Start lokal

```bash
pip install -r requirements.txt
# optional: python -m venv .venv && source .venv/bin/activate
flask --app app run
```

Erstelle eine Datei `.env` mit folgendem Inhalt:
```env
PASSWORD="meinGeheimesPasswort"
```
Die App liest `PASSWORD` und zeigt es auf der Startseite an.

---

## pre-commit Hooks installieren

```bash
pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-push
```

- **Commit:** Black formatiert automatisch den Code  
- **Push:** pytest wird ausgeführt, Push schlägt bei Fehlern fehl  

---

## GitHub Flow

1. Issue anlegen (Vorlage **Feature Anforderung**, Labels: Funktionale Anforderung, Qualitätsanforderung, Randanforderung)  
2. Branch aus `dev` erstellen, z.B. `feature/fix-happiness`  
3. Code ändern, committen, pushen  
4. Pull Request **auf `dev`** erstellen → CI-Tests laufen automatisch  
5. Merge nach `dev`  
6. Release: PR von `dev` nach `main` → Deployment auf Azure  

👉 Beispiel: Feature Branch `feature/fix-happiness` mit Test `test_add_entry_with_happiness` wurde umgesetzt.  

---

## Azure Deployment (App Service)

1. Azure App Service für **Python** (Linux) erstellen  
2. In Azure **Konfiguration** die App-Einstellung `PASSWORD` setzen (für die LB: auf den GitHub Benutzernamen)  
3. In GitHub **Settings → Secrets and variables → Actions** einrichten:  
   - `AZURE_WEBAPP_NAME` = Name der App Service Instanz (z.B. `tagebbbuch-twin`)  
   - `AZURE_WEBAPP_PUBLISH_PROFILE` = Inhalt der Publish Profile Datei aus Azure  
4. Merge nach `main` → Workflow `deploy.yml` startet und liefert die App aus  

### Live URL

https://tagebbbuch-twin.azurewebsites.net/

---

## Tests

```bash
pytest -q
```

Alle Tests müssen erfolgreich sein, bevor nach `dev` oder `main` gemergt wird.

---

## Bewertung Checkliste

- [x] Labels und Issue Vorlage vorhanden (funktionale, Qualitäts- und Randanforderungen)  
- [x] pre-commit Hook formatiert Code beim Commit  
- [x] pre-push Hook führt Tests aus  
- [x] PR auf `dev` triggert CI Tests  
- [x] Merge nach `main` triggert Azure Deployment  
- [x] Secrets sind korrekt dokumentiert und übertragen  
- [x] README erklärt Installation, Hooks, Flow und Secrets  
- [x] Neue Funktionalität inkl. Test wurde via Feature Branch und PR umgesetzt  

---
