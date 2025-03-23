from project import db,app
from flask_login import UserMixin

class soil_data(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(30))
    bearing_capacity = db.Column(db.String(20), nullable=False, default='default.jpg')
    ground_waterlevel_l = db.Column(db.String(30))
    ground_waterlevel_h = db.Column(db.String(30))

class found_data(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    foundation= db.Column(db.String(30))
    usage = db.Column(db.String(30))
    bearing_capacity_l = db.Column(db.String(20))
    bearing_capacity_h = db.Column(db.String(20))
    reason = db.Column(db.String(500))

with app.app_context():
     db.create_all()