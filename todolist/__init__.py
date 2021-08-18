from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
 

db=SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todoapp.db'
    app.config['SECRET_KEY'] ='123456789'
    db.init_app(app)


    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
   
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app