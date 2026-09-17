from app import app
from extensions import db
from models.user import User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Create all tables
    db.create_all()
    print("Tables created successfully!")

    # Check if admin already exists
    admin = User.query.filter_by(email='admin@trekking.com').first()
    
    if not admin:
        # Create admin user
        admin = User(
            name='Admin',
            email='admin@trekking.com',
            password=generate_password_hash('admin123'),
            role='admin',
            contact='9999999999',
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")
        print("Email: admin@trekking.com")
        print("Password: admin123")
    else:
        print("Admin already exists. No new admin created.")