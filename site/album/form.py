from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField
from wtforms.validators import DataRequired, Length

class AuthForm(FlaskForm): 
    password = PasswordField('Password', validators=[DataRequired('请输入密码'), Length(8, 20)]) 
    mail = StringField('mail', validators=[DataRequired('请输入邮箱')]) 
    submit = SubmitField('submit')

class ColForm(FlaskForm): 
    name = StringField('name', validators=[DataRequired()]) 
    col_type = SelectField('type', validators=[DataRequired()] , choices=[('私密', '私密'),('共享', '共享')])
    submit = SubmitField('submit')

class ChangeForm(FlaskForm):
    old_password = PasswordField('oldPassword', validators=[DataRequired('请输入密码'), Length(8, 20)]) 
    new_password = PasswordField('newPassword', validators=[DataRequired('请输入密码'), Length(8, 20)]) 
    submit = SubmitField('submit')
