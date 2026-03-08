from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qualification = db.Column(db.String(50))
    interest = db.Column(db.String(50))
    tech_field = db.Column(db.String(50))
    weak_subject = db.Column(db.String(50))
    skills = db.Column(db.String(200))  # comma-separated
    personality = db.Column(db.String(50))
    goal = db.Column(db.String(50))

class Career(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    required_skills = db.Column(db.String(200))
    courses = db.Column(db.String(500))
    improvement_tips = db.Column(db.String(500))
    learning_platforms = db.Column(db.String(200))
    roadmap_steps = db.Column(db.String(500))