import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models.user import User

auth_bp = Blueprint('auth', __name__)

# Register - only for trekkers
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Name, email and password are required'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400

    new_user = User(
        name=data['name'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        role='trekker',
        contact=data.get('contact', '')
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registration successful'}), 201


# Login - for all roles
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401

    if not user.is_active:
        return jsonify({'message': 'Your account has been deactivated'}), 403

    access_token = create_access_token(identity=json.dumps({
        'id': user.id,
        'email': user.email,
        'role': user.role,
        'name': user.name
    }))

    return jsonify({
        'access_token': access_token,
        'role': user.role,
        'name': user.name,
        'message': 'Login successful'
    }), 200


# Get current logged in user info
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    current_user = json.loads(get_jwt_identity())
    return jsonify(current_user), 200