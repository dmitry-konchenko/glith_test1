from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, IntegerField, StringField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job_title = StringField('Название работы', validators=[DataRequired()])
    team_leader = IntegerField('Айди лидера команды', validators=[DataRequired()])
    duration = StringField('Рабочие часы', validators=[DataRequired()])
    collaborations = StringField('Союзные команды', validators=[DataRequired()])
    is_job_finished = BooleanField('Работа закончена?')
    submit = SubmitField('Подтвердить')
