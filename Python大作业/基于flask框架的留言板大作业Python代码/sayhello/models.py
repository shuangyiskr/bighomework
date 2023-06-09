from datetime import datetime
from sayhello import db


class Message(db.Model):
    __tablename__ = 'liuyan'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    replies = db.relationship('Reply', backref='message', lazy='dynamic')

class Reply(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    message_id = db.Column(db.Integer, db.ForeignKey('liuyan.id'))
