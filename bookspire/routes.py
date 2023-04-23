from flask import render_template, request, redirect, url_for
from bookspire import app, db
from bookspire.models import User, Book, Review
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def home():
    books = list(Book.query.order_by(Book.id).all())
    return render_template("index.html", books=books)


@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        book = Book(
            title=request.form.get("title"),
            author=request.form.get("author"),
            year_of_publication=request.form.get("year_of_publication"),
            synopsis=request.form.get("synopsis"),
            genre=request.form.get("genre"),
            username=request.form.get("username"),
            cover=request.form.get("cover"),
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_book.html")