# app.py
from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, Team, Player, Venue, Match
from forms import TeamForm, ReportForm, VenueForm, MatchForm
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sports_team.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('list_teams'))

# Requirement 1: CRUD Interface for Teams
@app.route('/teams')
def list_teams():
    teams = Team.query.all()
    return render_template('teams.html', teams=teams)

@app.route('/teams/add', methods=['GET', 'POST'])
def add_team():
    form = TeamForm()
    if form.validate_on_submit():
        new_team = Team(
            name=form.name.data,
            coach=form.coach.data,
            founded_year=form.founded_year.data
        )
        db.session.add(new_team)
        try:
            db.session.commit()
            flash('Team added successfully!', 'success')
            return redirect(url_for('list_teams'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding team. Make sure the team name is unique.', 'danger')
    return render_template('add_team.html', form=form)

@app.route('/teams/edit/<int:team_id>', methods=['GET', 'POST'])
def edit_team(team_id):
    team = Team.query.get_or_404(team_id)
    form = TeamForm(obj=team)
    if form.validate_on_submit():
        team.name = form.name.data
        team.coach = form.coach.data
        team.founded_year = form.founded_year.data
        try:
            db.session.commit()
            flash('Team updated successfully!', 'success')
            return redirect(url_for('list_teams'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating team. Make sure the team name is unique.', 'danger')
    return render_template('edit_team.html', form=form, team=team)

@app.route('/teams/delete/<int:team_id>', methods=['POST'])
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    try:
        db.session.commit()
        flash('Team deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting team.', 'danger')
    return redirect(url_for('list_teams'))

# Requirement 2: Report Interface
@app.route('/report', methods=['GET', 'POST'])
def report():
    form = ReportForm()
    form.team.choices = [(-1, 'All Teams')] + [(team.id, team.name) for team in Team.query.all()]
    form.venue.choices = [(-1, 'All Venues')] + [(venue.id, venue.name) for venue in Venue.query.all()]
    
    report_data = None
    statistics = {}
    
    if form.validate_on_submit():
        query = Match.query

        if form.team.data != -1:
            query = query.filter_by(team_id=form.team.data)
        if form.venue.data != -1:
            query = query.filter_by(venue_id=form.venue.data)
        if form.start_date.data:
            query = query.filter(Match.date >= form.start_date.data)
        if form.end_date.data:
            query = query.filter(Match.date <= form.end_date.data)
        
        report_data = query.all()
        
        # Calculate statistics
        if report_data:
            total_duration = sum(match.duration for match in report_data)
            total_invited = sum(match.invited_count for match in report_data)
            total_accepted = sum(match.accepted_count for match in report_data)
            average_duration = total_duration / len(report_data)
            average_invited = total_invited / len(report_data)
            average_accepted = total_accepted / len(report_data)
            average_attendance = (total_accepted / total_invited) * 100 if total_invited > 0 else 0

            statistics = {
                'average_duration': round(average_duration, 2),
                'average_invited': round(average_invited, 2),
                'average_accepted': round(average_accepted, 2),
                'average_attendance': round(average_attendance, 2)
            }
        else:
            statistics = {
                'average_duration': 0,
                'average_invited': 0,
                'average_accepted': 0,
                'average_attendance': 0
            }
    
    return render_template('report.html', form=form, report_data=report_data, statistics=statistics)


@app.route('/venues')
def list_venues():
    venues = Venue.query.all()
    return render_template('venues.html', venues=venues)

@app.route('/venues/add', methods=['GET', 'POST'])
def add_venue():
    form = VenueForm()
    if form.validate_on_submit():
        new_venue = Venue(
            name=form.name.data,
            location=form.location.data,
            capacity=form.capacity.data
        )
        db.session.add(new_venue)
        try:
            db.session.commit()
            flash('Venue added successfully!', 'success')
            return redirect(url_for('list_venues'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding venue. Make sure the venue name is unique.', 'danger')
    return render_template('add_venue.html', form=form)

@app.route('/venues/edit/<int:venue_id>', methods=['GET', 'POST'])
def edit_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm(obj=venue)
    if form.validate_on_submit():
        venue.name = form.name.data
        venue.location = form.location.data
        venue.capacity = form.capacity.data
        try:
            db.session.commit()
            flash('Venue updated successfully!', 'success')
            return redirect(url_for('list_venues'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating venue. Make sure the venue name is unique.', 'danger')
    return render_template('edit_venue.html', form=form, venue=venue)

@app.route('/venues/delete/<int:venue_id>', methods=['POST'])
def delete_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    db.session.delete(venue)
    try:
        db.session.commit()
        flash('Venue deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting venue. Ensure no matches are associated with this venue.', 'danger')
    return redirect(url_for('list_venues'))

@app.route('/matches')
def list_matches():
    matches = Match.query.order_by(Match.date.desc(), Match.time.desc()).all()
    return render_template('matches.html', matches=matches)

@app.route('/matches/add', methods=['GET', 'POST'])
def add_match():
    form = MatchForm()
    form.team.choices = [(team.id, team.name) for team in Team.query.order_by('name')]
    form.venue.choices = [(venue.id, venue.name) for venue in Venue.query.order_by('name')]
    
    if form.validate_on_submit():
        new_match = Match(
            team_id=form.team.data,
            opponent=form.opponent.data,
            venue_id=form.venue.data,
            date=form.date.data,
            time=form.time.data,
            duration=form.duration.data,
            description=form.description.data,
            invited_count=form.invited_count.data,
            accepted_count=form.accepted_count.data
        )
        db.session.add(new_match)
        try:
            db.session.commit()
            flash('Match added successfully!', 'success')
            return redirect(url_for('list_matches'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding match. Please check the details and try again.', 'danger')
    return render_template('add_match.html', form=form)

@app.route('/matches/edit/<int:match_id>', methods=['GET', 'POST'])
def edit_match(match_id):
    match = Match.query.get_or_404(match_id)
    form = MatchForm(obj=match)
    form.team.choices = [(team.id, team.name) for team in Team.query.order_by('name')]
    form.venue.choices = [(venue.id, venue.name) for venue in Venue.query.order_by('name')]
    
    if form.validate_on_submit():
        match.team_id = form.team.data
        match.opponent = form.opponent.data
        match.venue_id = form.venue.data
        match.date = form.date.data
        match.time = form.time.data
        match.duration = form.duration.data
        match.description = form.description.data
        match.invited_count = form.invited_count.data
        match.accepted_count = form.accepted_count.data
        try:
            db.session.commit()
            flash('Match updated successfully!', 'success')
            return redirect(url_for('list_matches'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating match. Please check the details and try again.', 'danger')
    return render_template('edit_match.html', form=form, match=match)

@app.route('/matches/delete/<int:match_id>', methods=['POST'])
def delete_match(match_id):
    match = Match.query.get_or_404(match_id)
    db.session.delete(match)
    try:
        db.session.commit()
        flash('Match deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting match.', 'danger')
    return redirect(url_for('list_matches'))

if __name__ == '__main__':
    app.run(debug=True)
