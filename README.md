# Tagebuch App · LB 324

Kleine Flask App als Übungsablage für LB 324. Die Ablage zeigt
* neuen Feature Flow mit Issue  Feature Branch  PR auf dev  Release nach main  
* Tests mit pytest lokal und in GitHub Actions  
* Auslieferung auf Azure App Service  

---

## Live URL
https://tagebbbuch-twin.azurewebsites.net

---

## Projektziel in einem Satz
Benutzende können einen Texteingang im Tagebuch speichern und optional eine Stimmung als Emoji 😃 mitgeben.

---

## Tech Stack
* Python 3.12  Flask  
* pytest für Tests  
* pre commit Hooks  Formatierung und Test bei Push  
* GitHub Actions  PR CI auf dev  Deploy auf main  
* Azure App Service Linux  gunicorn  

---

## Ordnerstruktur
.github/workflows/ # pr ci und deploy
templates/ # index.html
tests/ # test_app.py
app.py # Flask App
requirements.txt # Abhängigkeiten inkl gunicorn
pytest.ini # pythonpath = .
.env.example # Vorlage für lokale Variablen

yaml
Code kopieren

---

## Lokal starten

bash
# einmalig Abhängigkeiten installieren
py -m pip install -r requirements.txt

# optional venv
# py -m venv .venv && .\.venv\Scripts\activate

# Tests lokal
py -m pytest -q

# App lokal starten
py -m flask --app app run
Hinweis Emoji eingeben
Windows Taste und Punkt drücken dann das Smiley wählen.

GitHub Flow in diesem Repo
Issue mit der Vorlage Feature Anforderung anlegen

Branch aus dev erstellen z B feature/happiness

Code bauen committen pushen

PR feature → dev erstellen PR CI läuft automatisch und zeigt pytest grün

Nach Review in dev mergen
den neuen Feature Ast nicht löschen so verlangt es die LB

Release PR dev → main Merge löst Build Test und Azure Deployment aus

CI Workflows
PR CI nur Tests auf dev
.github/workflows/pr-ci.yml

yaml
Code kopieren
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
Deploy auf Azure bei main
.github/workflows/deploy.yml baut testet und liefert auf Azure aus.

Azure Deployment
Azure App Service erstellt Python 3.12 Linux Region Switzerland North

Konfiguration → Anwendungseinstellungen PASSWORD gesetzt

Konfiguration → Allgemeine Einstellungen → Startbefehl

bash
Code kopieren
gunicorn --bind=0.0.0.0:$PORT --timeout 600 app:app
GitHub → Settings → Secrets and variables → Actions

AZURE_WEBAPP_NAME = tagebbbuch-twin

AZURE_WEBAPP_PUBLISH_PROFILE = gesamter XML Inhalt aus Veröffentlichungsprofil

Merge nach main löst den Deploy Workflow aus

pre commit Hooks
bash
Code kopieren
py -m pip install pre-commit
pre-commit install
pre-commit install --hook-type pre-push
bei jedem Commit formatiert black den Code

bei jedem Push läuft pytest

Tests
Die LB prüft die neue Funktion mit diesem Verhalten

POST auf /add_entry mit content und happiness

Antwort ist Redirect 302 auf /

der erste Eintrag in entries enthält Text und das Smiley

Implementierung in app.py Kurzsicht

python
Code kopieren
@app.route("/add_entry", methods=["POST"])
def add_entry():
    content = request.form.get("content", "").strip()
    happiness = request.form.get("happiness", "").strip()
    if content:
        entries.append(Entry(content=content, happiness=happiness or ""))
    return redirect(url_for("index"))
Evidenz
Issue #3 Eintrag mit Stimmung speichern
https://github.com/twinjn/TwinJeganLB-324/issues/3

PR feature → dev Tests grün
https://github.com/twinjn/TwinJeganLB-324/pull/9

Actions Lauf zum PR
HIER DEN LINK AUS PR CHECKS DETAILS EINFÜGEN

PR dev → main Deploy grün
https://github.com/twinjn/TwinJeganLB-324/pull/14

Actions Lauf zum Deploy
HIER DEN LINK AUS CHECKS DETAILS DES RELEASE PR EINFÜGEN

Live URL
https://tagebbbuch-twin.azurewebsites.net

Troubleshooting kurz
504 GatewayTimeout
Startbefehl wie oben setzen Deploy neu anstoßen Logstream prüfen

gunicorn nicht gefunden
gunicorn in requirements.txt aufnehmen neu deployen

ModuleNotFoundError app
Datei heißt app.py Flask Variable heißt app

Hinweis zu Secrets
Die Datei .env gehört nicht ins Repo. Bitte nur .env.example versionieren.
In Azure ist PASSWORD als App Einstellung gesetzt.
