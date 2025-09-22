from flask import Flask, request, redirect, url_for, render_template
from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@dataclass
class Entry:
    content: str
    happiness: str

entries = []

@app.route("/")
def index():
    return render_template("index.html", entries=entries, password=os.getenv("PASSWORD", "not-set"))

@app.route("/add_entry", methods=["POST"])
def add_entry():
    content = request.form.get("content", "").strip()
    happiness = request.form.get("happiness", "").strip()
    if content:
        entries.append(Entry(content=content, happiness=happiness or "🙂"))
    return redirect(url_for("index"))
