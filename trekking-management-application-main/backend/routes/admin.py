import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db, cache
from models.user import User
from models.trek import Trek
from models.booking import Booking
from models.staff_profile import StaffProfile
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__)

def admin_required():
    current_user = json.loads(get_jwt_identity())
    return current_user if current_user['role'] == 'admin' else False


# PUBLIC endpoint - no login required
@admin_bp.route('/public/stats', methods=['GET'])
def public_stats():
    from collections import Counter
    all_bookings = Booking.query.all()
    trek_counts = Counter(b.trek_id for b in all_bookings if b.status != 'Cancelled')

    popular = []
    for trek_id, count in trek_counts.most_common(5):
        trek = Trek.query.get(trek_id)
        if trek:
            popular.append({
                'name': trek.name,
                'location': trek.location,
                'difficulty': trek.difficulty,
                'bookings': count
            })

    return jsonify({
        'total_treks': Trek.query.count(),
        'open_treks': Trek.query.filter_by(status='Open').count(),
        'completed_treks': Trek.query.filter_by(status='Completed').count(),
        'total_bookings': Booking.query.count(),
        'popular_treks': popular,
        'difficulty_distribution': {
            'Easy': Trek.query.filter_by(difficulty='Easy').count(),
            'Moderate': Trek.query.filter_by(difficulty='Moderate').count(),
            'Hard': Trek.query.filter_by(difficulty='Hard').count(),
        },
        'status_distribution': {
            'Pending': Trek.query.filter_by(status='Pending').count(),
            'Approved': Trek.query.filter_by(status='Approved').count(),
            'Open': Trek.query.filter_by(status='Open').count(),
            'Closed': Trek.query.filter_by(status='Closed').count(),
            'Completed': Trek.query.filter_by(status='Completed').count(),
        }
    }), 200


@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    if not admin_required():
        return jsonify({'message': 'Admin access required'}), 403

    return jsonify({
        'total_treks': Trek.query.count(),
        'total_users': User.query.filter_by(role='trekker').count(),
        'total_staff': User.query.filter_by(role='staff').count(),
        'total_bookings': Booking.query.count(),
        'open_treks': Trek.query.filter_by(status='Open').count(),
        'completed_treks': Trek.query.filter_by(status='Completed').count(),
    }), 200


@admin_bp.route('/treks', methods=['POST'])
@jwt_required()
def create_trek():
    if not admin_required():
        return jsonify({'message': 'Admin access required'}), 403

    data = request.get_json()
    if not data.get('name') or not data.get('location') or not data.get('difficulty'):
        return jsonify({'message': 'Name, location and difficulty are required'}), 400

    if data.get('difficulty') not in ['Easy', 'Moderate', 'Hard']:
        return jsonify({'message': 'Difficulty must be Easy, Moderate or Hard'}), 400

    if data.get('available_slots', 10) < 1:
        return jsonify({'message': 'Slots must be at least 1'}), 400

    from datetime import datetime
    trek = Trek(
        name=data['name'],
        location=data['location'],
        difficulty=data['difficulty'],
        duration=data.get('duration', 1),
        available_slots=data.get('available_slots', 10),
        total_slots=data.get('available_slots', 10),
        status='Pending',
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d') if data.get('start_date') else None,
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d') if data.get('end_date') else None
    )
    db.session.add(trek)
    db.session.commit()

    return jsonify({'message': 'Trek created successfully', 'trek_id': trek.id}), 201


@admin_bp.route('/treks', methods=['GET'])
@jwt_required()
def get_treks():
    if not admin_required():
        return jsonify({'message': 'Admin access required'}), 403

    treks = Trek.query.all()
    result = [{
        'id': t.id, 'name': t.name, 'location': t.location,
        'difficulty': t.difficulty, 'duration': t.duration,
        'available_slots': t.available_slots, 'total_slots': t.total_slots,
        'status': t.status, 'assigned_staff_id': t.assigned_staff_id,
        'start_date': t.start_date.strftime('%Y-%m-%d') if t.start_date else None,
        'end_date': t.end_date.strftime('%Y-%m-%d') if t.end_date else None,
        'assigned_staff_name': t.assigned_staff.name if t.assigned_staff else None
    } for t in treks]

    return jsonify(result), 200


@admin_bp.route('/treks/<int:trek_id>', methods=['PUT'])
@jwt_required()
def update_trek(trek_id):
    if not admin_required():
        return jsonify({'message': 'Admin access required'}), 403

    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({'message': 'Trek not found'}), 404

    data = request.get_json()

    if data.get('difficulty') and data['difficulty'] not in ['Easy', 'Moderate', 'Hard']:
        return jsonify({'message': 'Difficulty must be Easy, Moderate or Hard'}), 400

    from datetime import datetime
    trek.name = data.get('name', trek.name)
    trek.location = data.get('location', trek.location)
    trek.difficulty = data.get('difficulty', trek.difficulty)
    trek.duration = data.get('duration', trek.duration)
    trek.available_slots = data.get('available_slots', trek.available_slots)
    trek.total_slots = data.get('total_slots', trek.total_slots)
    trek.status = data.get('status', trek.status)
    if data.get('start_date'):
        trek.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    if data.get('end_date'):
        trek.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')

    db.session.commit()
    return jsonify({'message': 'Trek updated successfully'}), 200


@admin_bp.route('/treks/<int:trek_id>', methods=['DELETE'])
@jwt_required()
def delete_trek(trek_id):
    if not admin_required():
        return jsonify({'message': 'Admin access required'}), 403

    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({'message': 'Trek not found'}), 404

    db.session.delete(trek)
    db.session.commit()
    return jsonify({'message': 'Trek deleted successfully'}), 200


@admin_bp.route('/staff', methods=['POST'])
@jwt_required()
def create_staff():
    if not admin_required():
        return jsonify({'message': 'Admin access required'}), 403

    data = request.get_json()
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Name, email and password are required'}), 400

    if len(data.get('password', '')) < 6:
        return jsonify({'message': 'Password must be at least 6 characters'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400

    staff = User(
        name=data['name'], email=data['email'],
        password=generate_password_hash(data['password']),
        role='staff', contact=data.get('contact', '')
    )
    db.session.add(staff)
    db.session.flush()

    profile = StaffProfile(
        user_id=staff.id,
        bio=data.get('bio', ''),
        experience_years=data.get('experience_years', 0)
    )
    db.session.add(profile)
    db.session.commit()

    return jsonify({'message': 'Staff created successfully', 'staff_id': staff.id}), 201


@admin_bp.route('/staff', methods=['GET'])
@jwt_required()
def get_staff():
    if not admin_required():
        return jsonify({'message': 'Admin access required'}), 403

    staff_list = User.query.filter_by(role='staff').all()
    result = [{
        'id': s.id, 'name': s.name, 'email': s.email,
        'contact': s.contact, 'is_active': s.is_active,
        'assigned_treks': [{'id': t.id, 'name': t.name} for t in s.assigned_treks]
    } for s in staff_list]

    return jsonify(result), 200


@admin_bp.route('/staff/<int:staff_id>', methods=['DELETE'])
@jwt_required()
def delete_staff(staff_id):
    if not admin_required():
        return jsonify({'message': 'Admin access required'}), 403

    staff = User.query.filter_by(id=staff_id, role='staff').first()
    if not staff:
        return jsonify({'message': 'Staff not found'}), 404

    # Remove staff from assigned treks
    Trek.query.filter_by(assigned_staff_id=staff_id).update(
        {'assigned_staff_id': None, 'status': 'Pending'}
    )

    # Delete staff profile
    StaffProfile.query.filter_by(user_id=staff_id).delete()

    # Delete staff user
    db.session.delete(staff)
    db.session.commit()

    return jsonify({'message': 'Staff deleted successfully'}), 200


@admin_bp.route('/treks/<int:trek_id>/assign-staff', methods=['PUT'])
@jwt_required()
def assign_staff(trek_id):
    if not admin_required():
        return jsonify({'message': 'Admin access required'}), 403

    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({'message': 'Trek not found'}), 404

    data = request.get_json()
    staff = User.query.filter_by(id=data.get('staff_id'), role='staff').first()
    if not staff:
        return jsonify({'message': 'Staff not found'}), 404

    if not staff.is_active:
        return jsonify({'message': 'Cannot assign inactive staff'}), 400

    trek.assigned_staff_id = staff.id
    trek.status = 'Approved'
    db.session.commit()

    return jsonify({'message': f'Staff {staff.name} assigned to trek {trek.name}'}), 200


@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    if not admin_required():
        return jsonify({'message': 'Admin access required'}), 403

    users = User.query.filter_by(role='trekker').all()
    result = [{
        'id': u.id, 'name': u.name, 'email': u.email,
        'contact': u.contact, 'is_active': u.is_active,
        'booking_count': Booking.query.filter_by(user_id=u.id).count()
    } for u in users]

    return jsonify(result), 200


@admin_bp.route('/users/<int:user_id>/deactivate', methods=['PUT'])
@jwt_required()
def deactivate_user(user_id):
    if not admin_required():
        return jsonify({'message': 'Admin access required'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.role == 'admin':
        return jsonify({'message': 'Cannot deactivate admin'}), 400

    user.is_active = not user.is_active
    db.session.commit()
    status = 'activated' if user.is_active else 'deactivated'
    return jsonify({'message': f'User {status} successfully', 'is_active': user.is_active}), 200


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    if not admin_required():
        return jsonify({'message': 'Admin access required'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.role == 'admin':
        return jsonify({'message': 'Cannot delete admin'}), 400

    Booking.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200


@admin_bp.route('/bookings', methods=['GET'])
@jwt_required()
def get_bookings():
    if not admin_required():
        return jsonify({'message': 'Admin access required'}), 403

    bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    result = [{
        'id': b.id,
        'user_id': b.user_id, 'user_name': b.user.name,
        'trek_id': b.trek_id, 'trek_name': b.trek.name,
        'booking_date': b.booking_date.strftime('%Y-%m-%d'),
        'status': b.status, 'payment_status': b.payment_status
    } for b in bookings]

    return jsonify(result), 200


@admin_bp.route('/search', methods=['GET'])
@jwt_required()
def search():
    if not admin_required():
        return jsonify({'message': 'Admin access required'}), 403

    q = request.args.get('q', '')
    if not q:
        return jsonify({'message': 'Search query is required'}), 400

    users = User.query.filter(User.name.ilike(f'%{q}%'), User.role == 'trekker').all()
    staff = User.query.filter(User.name.ilike(f'%{q}%'), User.role == 'staff').all()
    treks = Trek.query.filter(Trek.name.ilike(f'%{q}%')).all()

    return jsonify({
        'users': [{'id': u.id, 'name': u.name, 'email': u.email} for u in users],
        'staff': [{'id': s.id, 'name': s.name, 'email': s.email} for s in staff],
        'treks': [{'id': t.id, 'name': t.name, 'location': t.location, 'status': t.status} for t in treks]
    }), 200


@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    if not admin_required():
        return jsonify({'message': 'Admin access required'}), 403

    from collections import Counter
    all_bookings = Booking.query.all()
    trek_counts = Counter(b.trek_id for b in all_bookings if b.status != 'Cancelled')

    popular = []
    for trek_id, count in trek_counts.most_common(5):
        trek = Trek.query.get(trek_id)
        if trek:
            popular.append({'name': trek.name, 'location': trek.location,
                            'difficulty': trek.difficulty, 'bookings': count})

    difficulty_dist = {
        'Easy': Trek.query.filter_by(difficulty='Easy').count(),
        'Moderate': Trek.query.filter_by(difficulty='Moderate').count(),
        'Hard': Trek.query.filter_by(difficulty='Hard').count(),
    }

    return jsonify({
        'popular_treks': popular,
        'difficulty_distribution': difficulty_dist,
        'status_distribution': {
            'Pending': Trek.query.filter_by(status='Pending').count(),
            'Approved': Trek.query.filter_by(status='Approved').count(),
            'Open': Trek.query.filter_by(status='Open').count(),
            'Closed': Trek.query.filter_by(status='Closed').count(),
            'Completed': Trek.query.filter_by(status='Completed').count(),
        },
        'total_bookings': Booking.query.count(),
        'total_cancelled': Booking.query.filter_by(status='Cancelled').count(),
        'total_completed': Booking.query.filter_by(status='Completed').count(),
    }), 200