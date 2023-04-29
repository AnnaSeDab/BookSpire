from flask import render_template, request, redirect, url_for, flash, session
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
            username=session["user"],
            cover=request.form.get("cover"),
            score=0,
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
            password=generate_password_hash(request.form.get("password")),
        )
        # Add to database let user know they are registered
        db.session.add(newuser)
        db.session.commit()
        flash('Registration successful!')

        # Add the user to the session and redirect to the main page
        session["user"] = request.form.get("username").lower()
        flash("Welcome, {}. You are now logged in!".format(
            request.form.get("username").capitalize()))
        return redirect(url_for("home"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = User.query.filter(
            User.username == request.form.get("username").lower()).all()

        # checks if username exists
        if existing_user:

            # checks if password matches then logs in user
            if check_password_hash(
                    existing_user[0].password,
                    request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username").capitalize()))
                return redirect(url_for("home"))
                flash('You are now logged in!')

            # invalid password
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        # username doesn't exist
        else:   
            flash("Incorrect Username and/or Password")

    return render_template("login.html")


@app.route("/logout")
# logs out user and flashed the message and redirect user to homepage
def logout():
    session.pop("user")
    flash("You have been logged out.")
    return render_template("index.html")


@app.route("/book/<int:book_id>")
def book(book_id):
    # loads in data about selected book with given id and list all reviews
    book = Book.query.get_or_404(book_id)
    reviews = list(Review.query.all())
    return render_template("book.html", book=book, reviews=reviews)


@app.route("/delete_book/<int:book_id>")
#deletes book
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book has been deleted!')
    return redirect(url_for("home"))


@app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == "POST":
        book.title = request.form.get("title")
        book.author = request.form.get("author")
        book.year_of_publication = request.form.get("year_of_publication")
        book.synopsis = request.form.get("synopsis")
        book.genre = request.form.get("genre")
        book.cover = request.form.get("cover")
        db.session.commit()
        return redirect(url_for("home"))

    #renders template with specific book's details loaded in
    return render_template("edit_book.html", book=book)


@app.route("/add_review/<int:book_id>", methods=["GET", "POST"])
def add_review(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == "POST":
        review = Review(
            book_id=book.id,
            review_title=request.form.get("review_title"),
            review_text=request.form.get("review_text"),
            review_score=request.form.get("review_score"),
            username=session["user"],
        )
        book.score = book.score + int(review.review_score)
        db.session.add(review)
        db.session.commit()
        return redirect(url_for("home"))
        
    return render_template("add_review.html", book=book)
