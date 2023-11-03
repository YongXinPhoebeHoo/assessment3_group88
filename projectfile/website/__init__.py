#import flask - from the package import class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime
import os

db = SQLAlchemy()

# Creates a web application
# a web server running on this application
def create_app():
    app = Flask(__name__)
    Bootstrap5(app)
    Bcrypt(app)
    app.secret_key = 'somesecretkey'
    #initialize db with flask app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    db.init_app(app)
    UPLOAD_FOLDER = '/static/mg'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    #initialize the login manager
    login_manager = LoginManager()
    # set the name of the login function that lets user login
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # user loader function takes userid and returns User
    # Importing inside the create_app function avoids circular references
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(int(user_id))

    from . import views
    app.register_blueprint(views.main_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

    from . import events
    app.register_blueprint(events.eventbp)
    
    @app.errorhandler(404) 
    def not_found(e): 
      return render_template("404.html", error=e)
    
    @app.context_processor
    def get_context():
      year = datetime.datetime.today().year
      return dict(year=year)

    return app