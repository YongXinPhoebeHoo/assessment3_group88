from . import db
from datetime import datetime
from flask_login import UserMixin

# User table
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer,  primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True, nullable=False)
    email_id = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user')
    def __repr__(self):
        return f"Name: {self.name}"
    def get_id(self):
        return str(self.user_id)

# Evenets table
class Events(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255))
    event_description = db.Column(db.String(255))
    organiser_name = db.Column(db.String(255))
    host_info = db.Column(db.String(255))
    event_type = db.Column(db.String(255))
    event_category = db.Column(db.String(255))
    start_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_date = db.Column(db.Date)
    end_time = db.Column(db.Time)
    status = db.Column(db.String(9))
    location = db.Column(db.String(200))
    tickets = db.Column(db.Integer)
    cost = db.Column(db.String(200))
    image = db.Column(db.String(400))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    comments = db.relationship('Comment', backref='event')
    def __repr__(self):
        return f"Name: {self.event_name}"
    
# Comments table 
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    comment = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    def __repr__(self):
        return f"Comment: {self.text}"

# Bookings table
class Booking(db.Model):
    __tablename__ = 'bookings' 
    book_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    event_name = db.Column(db.String)
    no_tickets = db.Column(db.Integer)
    purchase_date = db.Column(db.DateTime)
    invoice_no = db.Column(db.String(60), unique=True)
    invoice_date = db.Column(db.DateTime)
    total_cost = db.Column(db.String)
    def __repr__(self):
        return f""