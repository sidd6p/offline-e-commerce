from re import L
from flask import Flask
from files.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
loginManager = LoginManager()
loginManager.login_view = 'seller.login'
loginManager.login_message = "You need to Log-In first"
loginManager.login_message_category = 'warning'

def createApp(congigClass = Config):
    app = Flask(__name__)
    app.config.from_object(congigClass)
    db.init_app(app)
    loginManager.init_app(app)

    from files.buyer.routes import buyer
    from files.seller.routes import seller
    from files.general.routes import general
    app.register_blueprint(buyer)
    app.register_blueprint(seller)
    app.register_blueprint(general)
    with app.app_context():
        db.create_all()
    
    return app