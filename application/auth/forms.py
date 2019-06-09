from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
    username = StringField("Käyttäjä", [validators.Length(min=3, max=40)])
    password = PasswordField("Salasana")
  
    class Meta:
        csrf = False


class RegisterForm(FlaskForm):
    username = StringField("Käyttäjä", [validators.Length(min=3, max=40, message='Käyttäjännimen pitää olla 3-40 merkkiä pitkä')])
    password = PasswordField("Salasana", [validators.Length(min=3, max=40, message='Salasanan pitää olla vähintään 3-40 merkkiä pitkä'), validators.EqualTo('passwordAgain', message='Salasanojen pitää olla samat')])
    passwordAgain = PasswordField("Salasana uudelleen")
    
    class Meta:
        csrf = False
