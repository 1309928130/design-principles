from app_2 import app  # Import your Flask app
from models import db

# Ensure the app context is pushed
with app.app_context():
    db.create_all()
