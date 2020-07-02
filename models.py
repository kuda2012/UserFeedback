from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Establish columns, set parameters for columns, and create table for users in database"""

    __tablename__ = 'users'

    username = db.Column(db.String(20), unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    feedback = db.relationship("Feedback", backref="user",
                               cascade="all, delete-orphan")

    @staticmethod
    def register(password):
        """Created a hashed password for potential new user"""

        hashed = bcrypt.generate_password_hash(password)

        hashed_utf8 = hashed.decode("utf8")

        return hashed_utf8

    # # start_authenticate

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
    # end_authenticate


class Feedback(db.Model):
    """Establish columns, set parameters for columns, and create table for feedback in database"""
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey("users.username"))
