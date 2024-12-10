from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired, Email, NumberRange

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, DateField, TimeField, TextAreaField
from wtforms.validators import DataRequired, Email, NumberRange, Optional

class TeamForm(FlaskForm):
    name = StringField('Team Name', validators=[DataRequired()])
    coach = StringField('Coach Name', validators=[DataRequired()])
    founded_year = IntegerField('Founded Year', validators=[DataRequired(), NumberRange(min=1800, max=2100)])
    submit = SubmitField('Submit')

class ReportForm(FlaskForm):
    team = SelectField('Team', coerce=int, choices=[])
    venue = SelectField('Venue', coerce=int, choices=[])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Generate Report')
    
class VenueForm(FlaskForm):
    name = StringField('Venue Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Submit')
    
class MatchForm(FlaskForm):
    team = SelectField('Team', coerce=int, validators=[DataRequired()])
    opponent = StringField('Opponent Team', validators=[DataRequired()])
    venue = SelectField('Venue', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('Time', validators=[DataRequired()], format='%H:%M')
    duration = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=1)])
    description = TextAreaField('Description', validators=[Optional()])
    invited_count = IntegerField('Invited Count', validators=[DataRequired(), NumberRange(min=0)])
    accepted_count = IntegerField('Accepted Count', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')
