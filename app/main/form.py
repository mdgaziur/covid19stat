from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CountryFinderForm(FlaskForm):
    country_field = StringField(
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField(
        'Search'
    )