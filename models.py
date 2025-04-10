from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    experience = db.Column(db.String(50)) 
    split = db.Column(db.String(50)) 
    gym_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    password = db.Column(db.String(100))