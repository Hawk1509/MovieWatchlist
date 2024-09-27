from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from graphene import ObjectType, Schema, Field, String as GrapheneString

db = SQLAlchemy()

# Example model
class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# GraphQL schema
class UserType(ObjectType):
    id = GrapheneString()
    username = GrapheneString()

class Query(ObjectType):
    users = Field(UserType, username=GrapheneString())

    def resolve_users(self, info, username=None):
        if username:
            return User.query.filter_by(username=username).first()
        return User.query.all()

schema = Schema(query=Query)
