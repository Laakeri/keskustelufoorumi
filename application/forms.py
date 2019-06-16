from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField

class PostForm(FlaskForm):
    topic = StringField("Aihe", [validators.Length(max=100)])

    message = TextAreaField("Message", [validators.InputRequired(message="Viestissä pitää olla sisältöä"), validators.Length(max=10000)], render_kw={"cols": 40, "rows": 3})

    class Meta:
        csrf = False

class DescForm(FlaskForm):
	description = TextAreaField("Kuvaus", render_kw={"cols": 40, "rows": 3})

	class Meta:
		csrf = False