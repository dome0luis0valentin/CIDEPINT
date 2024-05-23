from datetime import datetime
from src.core.config.database import db

class UserInstitutionRole(db.Model):
    __tablename__ = 'user_institution_role'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    institution_id = db.Column(db.Integer, db.ForeignKey('institutions.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
    #user = db.relationship('User', backref='user_institution_role')
    
    #institution = db.relationship('Institution', backref='user_institution_role')
    #role = db.relationship('Role', backref='user_institution_role')