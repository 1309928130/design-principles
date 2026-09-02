from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from app_2 import app, db  # Import your app instance and db

migrate = Migrate(app, db)


