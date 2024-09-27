from flask import Flask
from flask_graphql import GraphQLView
from models import db, schema  # Assuming you have a schema defined in models.py

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize the database
db.init_app(app)

# Add GraphQL endpoint
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
