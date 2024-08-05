from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import Config
import psycopg2
from sqlalchemy_utils import database_exists, create_database

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()

def setup_database(app):
    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    db_name = db_url.split('/')[-1]

    # Create database if it doesn't exist
    if not database_exists(db_url):
        create_database(db_url)
        print(f"Database '{db_name}' created.")

    # Connect to the database
    conn = psycopg2.connect(db_url)
    conn.autocommit = False
    cursor = conn.cursor()

    try:
        # Check if the 'user' table exists
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'user')")
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            print("Creating 'user' table...")
            db.create_all()
            print("'user' table created.")
        else:
            print("'user' table already exists.")

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        setup_database(app)
    
    jwt.init_app(app)
    mail.init_app(app)

    from .api import api_bp
    app.register_blueprint(api_bp)

    return app