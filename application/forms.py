from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField

class PostForm(FlaskForm):
    topic = StringField("Käyttäjä", [validators.Length(min=3)])
    message = TextAreaField("Message", [validators.InputRequired(message="Viestissä pitää olla sisältöä")], render_kw={"cols": 40, "rows": 3})

    class Meta:
        csrf = False
