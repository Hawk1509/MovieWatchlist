from flask import Blueprint
from models import User

api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return {'users': [user.username for user in users]}
