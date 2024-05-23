from datetime import datetime
#from src.core.board.database import db
from src.core.config.database import db

class Institution(db.Model):
    __tablename__ = "institutions"
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))
    contact_info = db.Column(db.String(255))
    address = db.Column(db.String(255))
    location = db.Column(db.String(255))
    web = db.Column(db.String(255))
    active = db.Column (db.Boolean, default=True)
    key_words = db.Column(db.Text)
    work_schedule = db.Column(db.Text)

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    #users = db.relationship('User', secondary='user_institution_role')
    #user_institution_role = db.relationship('UserInstitutionRole', back_populates='institutions')
    