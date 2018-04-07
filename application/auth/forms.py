from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Käyttäjä", [validators.Length(min=3)])
    password = PasswordField("Salasana")
  
    class Meta:
        csrf = False


class RegisterForm(FlaskForm):
    username = StringField("Käyttäjä", [validators.Length(min=3, message='Käyttäjännimen pitää olla vähintään 3 merkkiä pitkä')])
    password = PasswordField("Salasana", [validators.Length(min=3, message='Salasanan pitää olla vähintään 3 merkkiä pitkä'), validators.EqualTo('passwordAgain', message='Salasanojen pitää olla samat')])
    passwordAgain = PasswordField("Salasana uudelleen")
    
    class Meta:
        csrf = False
