from flask import render_template, request, redirect, url_for
from bookspire import app, db
from bookspire.models import User, Book, Review


@app.route("/")
def home():
    return render_template("index.html")

