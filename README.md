Tagebuch App · LB 324

Kleine Flask App als Übungsablage für LB 324.
Sie zeigt

- sauberen GitHub Flow mit Issue, Feature Branch, PR auf dev, Release auf main
- Tests mit pytest lokal und in GitHub Actions
- Auslieferung auf Azure App Service
- pre commit Hooks für Formatierung und Tests

---

## Live URL

https://tagebbbuch-twin.azurewebsites.net

---

## Ziel

Benutzende können Einträge erfassen und optional eine Stimmung als Emoji 😃 speichern.

---

## Tech Stack

- Python 3.12, Flask
- pytest
- pre commit Hooks, black
- GitHub Actions
- Azure App Service Linux, gunicorn

---

## Ordnerstruktur
`
.github/workflows/        PR CI und Deploy
templates/                index.html
tests/                    test_app.py
app.py                    Flask Anwendung
requirements.txt          Abhängigkeiten
pytest.ini                pythonpath = .
.pre-commit-config.yaml   Hooks Konfiguration
.env.example              Vorlage für lokale Variablen
``

---

## Schnellstart lokal

`bash
# einmalig Abhängigkeiten installieren
py -m pip install -r requirements.txt

# optional venv unter Windows
# py -m venv .venv && .\.venv\Scripts\activate

# Tests lokal
py -m pytest -q

# App lokal starten
py -m flask --app app run```

Lege dazu eine Datei **.env** an, zum Beispiel


PASSWORD="sehrGeheimesPasswort"`

Emoji Eingabe unter Windows
Windows Taste und Punkt drücken, dann Smiley wählen.

---

## GitHub Flow in diesem Repo

1. Issue mit Vorlage **Feature Anforderung** anlegen
2. Branch aus dev erstellen, zum Beispiel feature/happiness`
3. Code bauen, committen, pushen
4. PR **feature → dev** öffnen, PR CI läuft automatisch und prüft mit pytest
5. In dev` mergen
  den Feature Branch **nicht löschen**, so verlangt es die LB
6. Release PR **dev → main**, Merge auf `main` triggert das Deployment auf Azure

---

## CI Workflows

### PR CI: Tests für Pull Requests auf dev

Datei: .github/workflows/pr-ci.yml`

yaml
name: PR CI
on:
  pull_request:
    branches: ["dev"]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest -q


### Deploy auf Azure bei main

Datei: .github/workflows/deploy.yml`
nutzt das Azure Publish Profile, kein separates Azure Login nötig

yaml
name: Deploy to Azure on main
on:
  push:
    branches: ["main"]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest -q
      - uses: actions/upload-artifact@v4
        with:
          name: drop
          path: .

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: drop
      - uses: azure/webapps-deploy@v2
        with:
          app-name: ${{ secrets.AZURE_WEBAPP_NAME }}
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}


---

## Azure Deployment

1. Azure App Service erstellen
  Runtime **Python 3.12**, Linux, Region **Switzerland North**
2. In **Konfiguration → Anwendungseinstellungen** Variable `PASSWORD` setzen
3. In **Konfiguration → Allgemeine Einstellungen → Startbefehl** eintragen
  
  bash
  gunicorn --bind=0.0.0.0:$PORT --timeout 600 app:app
  
  
4. In GitHub unter **Settings → Secrets and variables → Actions** anlegen
  - AZURE_WEBAPP_NAME, zum Beispiel tagebbbuch-twin`
  - AZURE_WEBAPP_PUBLISH_PROFILE, kompletter XML Inhalt des Publish Profiles aus Azure
5. Merge nach main` löst den Deploy Workflow aus
  Live prüfen unter der URL oben

---

## Neue Funktion der LB

Der Test **test_add_entry_with_happiness** prüft

- POST auf /add_entry mit content und happiness`
- Status 302 Redirect auf /
- erster Eintrag in entries` enthält Text und das Emoji

Implementierung in app.py`

python
@app.route("/add_entry", methods=["POST"])
def add_entry():
    content = request.form.get("content", "").strip()
    happiness = request.form.get("happiness", "").strip()
    if content:
        entries.append(Entry(content=content, happiness=happiness or ""))
    return redirect(url_for("index"))


Anzeige in templates/index.html`

html
<form action="/add_entry" method="post">
  <input name="content" placeholder="Eintrag" required />
  <input name="happiness" placeholder="😊" />
  <button type="submit">Add</button>
</form>

<ul>
  {% for e in entries %}
    <li>{{ e.content }} — {{ e.happiness }}</li>
  {% endfor %}
</ul>
```

---

## pre commit Hooks

Installieren und aktivieren

bash
py -m pip install pre-commit black
pre-commit install
pre-commit install --hook-type pre-push
pre-commit run --all-files


Konfiguration in .pre-commit-config.yaml`

yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks:
      - id: black
        stages: [pre-commit]
        language_version: python3
  - repo: local
    hooks:
      - id: pytest
        name: pytest on pre-push
        entry: python -m pytest -q
        language: system
        pass_filenames: false
        stages: [pre-push]


Bei jedem Commit formatiert **black** den Code.
Beim Push führt der Hook **pytest** aus.

---

## Evidenz für die LB

- Issue: *Eintrag mit Stimmung speichern*
  https://github.com/twinjn/TwinJeganLB-324/issues/3
  
- PR **feature → dev** Tests grün
  ERSETZE DURCH DEINEN PR LINK
  
- Checks Seite dieses PR
  ERSETZE DURCH DEN LINK AUS PR CHECKS DETAILS
  
- PR **dev → main** Deploy grün
  ERSETZE DURCH DEINEN RELEASE PR LINK
  
- Deploy Lauf in Actions
  ERSETZE DURCH DEN LINK ZUM DEPLOY RUN
  
- Live URL
  https://tagebbbuch-twin.azurewebsites.net
  


