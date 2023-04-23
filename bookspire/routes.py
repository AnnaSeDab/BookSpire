from flask import render_template, request, redirect, url_for, flash
from bookspire import app, db
from bookspire.models import User, Book, Review


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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Check  if username already exists
        existing_user = User.query.filter(
            User.username == request.form.get("username").lower()).all()

        # If username exists - flash message & reload register page
        if existing_user:
            flash("This username already exists, please try another username.")
            return redirect(url_for("register"))

        # If username doesn't exist
        newuser = User(
            username=request.form.get("username").lower(),
            password=request.form.get("password"),
        )
        # Add to database
        db.session.add(newuser)
        db.session.commit()

        # Add the user to the session and redirect to the login page
        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template("register.html")
