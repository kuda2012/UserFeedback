"""Example flask app that stores passwords hashed with Bcrypt. Yay!"""

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/")
def to_register():
    """Send to register page"""
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Create user if form entries are valid"""
    if "username" in session:
        user = User.query.filter_by(username=session["username"]).one()
        return redirect(f'/users/{user.username}')
    form = UserForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User.register(username, password)
        add_user = User(username=user.username, password=user.password,
                        first_name=first_name, last_name=last_name, email=email)
        db.session.add(add_user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash(f"Username and/or Email already taken, try a different one")
            return redirect("/register")
        session["username"] = add_user.username
        return redirect(f"/users/{add_user.username}")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """Login user if entries are correct"""
    if "username" in session:
        user = User.query.filter_by(username=session["username"]).one()
        return redirect(f'/users/{user.username}')
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            active_user = User.query.filter_by(username=user.username).one()
            session["username"] = active_user.username
            return redirect(f"/users/{active_user.username}")
        else:
            flash("Incorrect username or password")
            return redirect("/login")
    else:
        return render_template("login.html", form=form)


@app.route("/users/<username>")
def show_user_info(username):
    """Show user info and the titles of their feedback"""
    user = User.query.filter_by(username=username).one()
    if "username" not in session or session["username"] != user.username:
        return redirect("/login")
    else:
        user = User.query.filter_by(username=username).one()
        feedback = Feedback.query.filter_by(username=username).all()
        return render_template("user_info.html", user=user, feedback=feedback)


@app.route("/users/<username>/delete", methods=["GET", "POST"])
def delete_user(username):
    """Delete user and all of their feedback"""
    user = User.query.filter_by(username=username).one()
    print(user.username)
    if "username" not in session or session["username"] != user.username:
        return redirect("/login")
    else:
        db.session.delete(user)
        try:
            db.session.commit()
            session.pop("username")
        except:
            db.session.rollback()
            flash("Something went wrong")
            return redirect(f"users/{username}")
        return redirect("/logout")


@app.route("/feedback/<id>")
def get_feedback(id):
    """Show the title and content of the feedback"""
    feedback = Feedback.query.get_or_404(id)
    if "username" not in session or session["username"] != feedback.username:
        return redirect("/login")
    return render_template("show_feedback.html", feedback=feedback)


@app.route("/feedback/<fb_id>/delete", methods=["GET", "POST"])
def delete_feedback(fb_id):
    """Delete a given feedback"""
    feedback = Feedback.query.get_or_404(fb_id)
    user = User.query.filter_by(username=feedback.username).one()
    if "username" not in session or session["username"] != user.username:
        return redirect("/login")
    else:
        db.session.delete(feedback)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash("Something went wrong")
    return redirect(f"/users/{user.username}")


@app.route("/feedback/<fb_id>/update", methods=["GET", "POST"])
def update_feedback(fb_id):
    """Edit a feedback if all entries are correct"""
    feedback = Feedback.query.get_or_404(fb_id)
    user = User.query.filter_by(username=feedback.username).one()
    if "username" not in session or session["username"] != user.username:
        return redirect("/login")
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback.title = title
        feedback.content = content
        db.session.add(feedback)
        try:
            db.session.commit()
        except:
            flash("Something went wrong")
        return redirect(f"/users/{user.username}")
    else:
        return render_template("edit_feedback.html", form=form, user=user, feedback=feedback)


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def create_feedback(username):
    """Add feedback if all form entries are correct"""
    user = User.query.filter_by(username=username).one()
    if "username" not in session or session["username"] != user.username:
        return redirect("/login")
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content,
                            username=user.username)
        db.session.add(feedback)
        try:
            db.session.commit()
        except:
            flash("Something went wrong")
        return redirect(f"/users/{user.username}")
    else:
        return render_template("create_feedback.html", form=form, user=user)


@app.route("/logout", methods=["POST", "GET"])
def logout_user():
    """Logout user if username is in session"""
    if "username" in session:
        session.pop("username")
        return redirect("/login")
    else:
        return redirect("/")
