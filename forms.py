from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length
from wtforms.widgets import TextArea


class UserForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(), Length(max = 30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max = 30)])
    email = StringField("Email", validators=[Email(), InputRequired(), Length(max = 50)])
    username = StringField("Username", validators=[InputRequired(), Length(max = 20)])
    password = PasswordField("Password", validators=[InputRequired()])


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(),Length(max = 100)])
    content = TextAreaField("Content",  render_kw={
                            "rows": 10},  validators=[InputRequired()])
