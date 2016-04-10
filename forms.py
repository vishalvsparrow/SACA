from flask.ext.wtf import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField('Username',validators = [DataRequired("Please enter your username")])
    password = PasswordField('Password',validators=[DataRequired("Password cannot be left blank")])



