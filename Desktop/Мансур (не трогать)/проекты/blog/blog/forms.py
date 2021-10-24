from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
import email_validator
from blog.models import User

class RegForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(message='Это поле обязательно!'), Email('Не правильно ввели свой email')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Это поле обязательно!')])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(message='Это поле обязательно!'), EqualTo('password')])
    submit = SubmitField ('Регистрация')

    def validate_email (self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError ('Пользователь с таким email уже существует!')

class PostForm(FlaskForm):
    title = StringField('Название рецепта', validators=[DataRequired()])
    content = TextAreaField('Рецепт', validators=[DataRequired()])
    image = FileField('Изображение', validators=[DataRequired()])
    submit = SubmitField('Поделиться')   