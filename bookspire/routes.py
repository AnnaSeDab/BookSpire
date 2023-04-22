from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import User, Book, Review

@app.route("/")
def home():
    return render_template("index.html")
