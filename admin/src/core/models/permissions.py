from datetime import datetime
from src.core.config.database import db
from enum import Enum

# class PermissionEnum(Enum):
#     USER_INDEX = 'user_index'
#     USER_NEW = 'user_new'
#     USER_DESTROY = 'user_destroy'
#     USER_UPDATE = 'user_update'
#     USER_SHOW = 'user_show'

#     SERVICE_INDEX = 'service_index'
#     SERVICE_NEW = 'service_new'
#     SERVICE_DESTROY = 'service_destroy'
#     SERVICE_UPDATE = 'service_update'
#     SERVICE_SHOW = 'service_show'

#     INSTITUTION_INDEX = 'institution_index'
#     INSTITUTION_NEW = 'institution_new'
#     INSTITUTION_DESTROY = 'institution_destroy'
#     INSTITUTION_UPDATE = 'institution_update'
#     INSTITUTION_SHOW = 'institution_show'

#     CONFIG_SHOW = 'config_show'
#     CONFIG_UPDATE = 'config_update'

permissions = {'User': ['user_index', 'user_new', 'user_destroy', 'user_update', 'user_show'],
                'Service': ['service_index', 'service_new', 'service_destroy', 'service_update', 'service_show'],
                'Institution': ['institution_index', 'institution_new', 'institution_destroy', 'institution_update', 'institution_show'],
                'Config': ['config_show', 'config_update']}

class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), unique=True)

    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Define the relationship to Role via RolePermissions
    roles = db.relationship('Role', secondary='role_permission', back_populates='permissions')



