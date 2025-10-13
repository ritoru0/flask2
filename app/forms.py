from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo

from app.models import User


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(min=5, max=100)])
    body = TextAreaField('Текст', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Сохранить')

    def validate_title(self, field):
        if "!" in field.data:
            raise ValidationError("нельзя ! в заголовке")

    def validate_body(self, field):
        if "!" in field.data:
            raise ValidationError("нельзя ! в заголовке")

    def validate(self, extra_validators=None):
        # сначала запустим стандартную валидацию
        if not super().validate(extra_validators):
            return False

        # теперь добавим свою логику
        if self.title.data.lower() == self.author.data.lower():
            self.title.errors.append("Заголовок не должен совпадать с именем автора.")
            return False

        return True

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято. Пожалуйста, выберите другое.')

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')