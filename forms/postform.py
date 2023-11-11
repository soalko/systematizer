from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import PasswordField, StringField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    floor = StringField('Этаж', validators=[DataRequired()])
    am_m = IntegerField('Кол-во мальчиков')
    am_f = IntegerField('Кол-во девочек')
    submit = SubmitField('Сохранить')
