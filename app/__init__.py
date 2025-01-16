from flask import Flask
from app.database import db, init_db
from app.routes import bp as routes_bp
from flask_cors import CORS

def create_app():

    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    #init database

    db.init_app(app)
    with app.app_context():
        init_db()
    
    app.register_blueprint(routes_bp)
    return app

