from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    coach = db.Column(db.String(100), nullable=False)
    founded_year = db.Column(db.Integer, nullable=False)

    players = db.relationship('Player', backref='team', cascade="all, delete-orphan")
    matches = db.relationship('Match', backref='team', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Team {self.name}>'

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<Player {self.name}>'

class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    location = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    matches = db.relationship('Match', backref='venue', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Venue {self.name}>'

class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    description = db.Column(db.String(200))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    opponent = db.Column(db.String(100), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id', ondelete='SET NULL'))
    invited_count = db.Column(db.Integer, default=0)
    accepted_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Match {self.team.name} vs {self.opponent} on {self.date}>'
