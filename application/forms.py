from flask_wtf import FlaskForm
from wtforms import StringField, validators

class PostForm(FlaskForm):
    message = StringField("Message", [validators.InputRequired(message="Viestissä pitää olla sisältöä")])

    class Meta:
        csrf = False
