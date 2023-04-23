from bookspire import db


class User(db.Model):
    # schema for the User model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    books = db.relationship("Book", backref="user", cascade="all, delete", lazy=True)
    reviews = db.relationship("Review", backref="user", cascade="all, delete", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.username 


class Book(db.Model):
    # schema for the Book model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), unique=True, nullable=False)
    author = db.Column(db.String(20), nullable=False)
    year_of_publication = db.Column(db.Integer, nullable=False)
    synopsis = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    genre = db.Column(db.String, nullable=False)
    username = db.Column(db.String, db.ForeignKey("user.username", ondelete="CASCADE"), nullable=False)
    cover = db.Column(db.String, nullable=False)
    reviews = db.relationship("Review", backref="book", cascade="all, delete", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Title: {1} | Author: {2}".format(
            self.id, self.title, self.author
        )


class Review(db.Model):
    # schema for the Review model
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String, db.ForeignKey("book.title", ondelete="CASCADE"), nullable=False)
    username = db.Column(db.String, db.ForeignKey("user.username", ondelete="CASCADE"), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    review_score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.review_text