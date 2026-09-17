from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from extensions import db, cache
from models.user import User
from models.trek import Trek
from models.booking import Booking
from models.staff_profile import StaffProfile
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.staff import staff_bp
from routes.user import user_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'trekking-secret-key-change-in-production'

    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300

    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = '24f2002054@ds.study.iitm.ac.in'
    app.config['MAIL_PASSWORD'] = 'zdxxlatxewuemlds'
    app.config['MAIL_DEFAULT_SENDER'] = '24f2002054@ds.study.iitm.ac.in'

    db.init_app(app)
    cache.init_app(app)
    CORS(app)
    JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(staff_bp, url_prefix='/api/staff')
    app.register_blueprint(user_bp, url_prefix='/api/user')

    @app.route('/')
    def home():
        return "Trekking Management App API is running!"

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)