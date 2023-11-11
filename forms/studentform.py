from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired


class StudentForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    gender = RadioField('Пол', choices=[('М', 'М'),
                                        ('Ж', 'Ж')],
                        default='2', validators=[DataRequired()])
    in_plan = BooleanField('В плане')
    submit = SubmitField('Сохранить')
