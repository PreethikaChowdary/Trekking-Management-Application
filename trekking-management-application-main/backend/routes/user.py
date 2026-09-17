import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db, cache
from models.user import User
from models.trek import Trek
from models.booking import Booking

user_bp = Blueprint('user', __name__)

def trekker_required():
    current_user = json.loads(get_jwt_identity())
    if current_user['role'] != 'trekker':
        return None
    return current_user


@user_bp.route('/treks', methods=['GET'])
@jwt_required()
def get_available_treks():
    difficulty = request.args.get('difficulty')
    location = request.args.get('location')
    duration = request.args.get('duration')

    if difficulty and difficulty not in ['Easy', 'Moderate', 'Hard']:
        return jsonify({'message': 'Difficulty must be Easy, Moderate or Hard'}), 400

    if duration:
        try:
            duration = int(duration)
            if duration < 1:
                return jsonify({'message': 'Duration must be at least 1 day'}), 400
        except ValueError:
            return jsonify({'message': 'Duration must be a number'}), 400

    query = Trek.query.filter_by(status='Open')
    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)
    if location:
        query = query.filter(Trek.location.ilike(f'%{location}%'))
    if duration:
        query = query.filter(Trek.duration == duration)

    treks = query.all()
    result = [{
        'id': t.id, 'name': t.name, 'location': t.location,
        'difficulty': t.difficulty, 'duration': t.duration,
        'available_slots': t.available_slots, 'total_slots': t.total_slots,
        'status': t.status,
        'start_date': t.start_date.strftime('%Y-%m-%d') if t.start_date else None,
        'end_date': t.end_date.strftime('%Y-%m-%d') if t.end_date else None
    } for t in treks]

    return jsonify(result), 200


@user_bp.route('/bookings', methods=['POST'])
@jwt_required()
def book_trek():
    current_user = trekker_required()
    if not current_user:
        return jsonify({'message': 'Trekker access required'}), 403

    user = User.query.get(current_user['id'])
    if not user or not user.is_active:
        return jsonify({'message': 'Your account has been deactivated'}), 403

    data = request.get_json()
    trek_id = data.get('trek_id')

    if not trek_id:
        return jsonify({'message': 'Trek ID is required'}), 400

    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({'message': 'Trek not found'}), 404

    if trek.status != 'Open':
        return jsonify({'message': 'Trek is not open for booking'}), 400

    if trek.available_slots <= 0:
        return jsonify({'message': 'No slots available for this trek'}), 400

    existing = Booking.query.filter_by(
        user_id=current_user['id'], trek_id=trek_id, status='Booked'
    ).first()
    if existing:
        return jsonify({'message': 'You have already booked this trek'}), 400

    booking = Booking(
        user_id=current_user['id'],
        trek_id=trek_id,
        status='Booked'
    )
    db.session.add(booking)
    trek.available_slots -= 1
    db.session.commit()

    return jsonify({
        'message': 'Trek booked successfully',
        'booking_id': booking.id
    }), 201


@user_bp.route('/bookings', methods=['GET'])
@jwt_required()
def get_my_bookings():
    current_user = trekker_required()
    if not current_user:
        return jsonify({'message': 'Trekker access required'}), 403

    bookings = Booking.query.filter_by(
        user_id=current_user['id']
    ).order_by(Booking.booking_date.desc()).all()

    result = [{
        'booking_id': b.id,
        'trek_id': b.trek_id,
        'trek_name': b.trek.name,
        'location': b.trek.location,
        'difficulty': b.trek.difficulty,
        'duration': b.trek.duration,
        'start_date': b.trek.start_date.strftime('%Y-%m-%d') if b.trek.start_date else None,
        'end_date': b.trek.end_date.strftime('%Y-%m-%d') if b.trek.end_date else None,
        'booking_date': b.booking_date.strftime('%Y-%m-%d'),
        'status': b.status,
        'trek_status': b.trek.status,
        'payment_status': b.payment_status
    } for b in bookings]

    return jsonify(result), 200


@user_bp.route('/bookings/<int:booking_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_booking(booking_id):
    current_user = trekker_required()
    if not current_user:
        return jsonify({'message': 'Trekker access required'}), 403

    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'message': 'Booking not found'}), 404

    if booking.user_id != current_user['id']:
        return jsonify({'message': 'Unauthorized'}), 403

    if booking.status != 'Booked':
        return jsonify({'message': 'Only active bookings can be cancelled'}), 400

    trek = Trek.query.get(booking.trek_id)
    if trek.status == 'Completed':
        return jsonify({'message': 'Cannot cancel a completed trek'}), 400

    booking.status = 'Cancelled'
    trek.available_slots += 1
    db.session.commit()

    return jsonify({'message': 'Booking cancelled successfully'}), 200


@user_bp.route('/export-history', methods=['POST'])
@jwt_required()
def trigger_export():
    current_user = trekker_required()
    if not current_user:
        return jsonify({'message': 'Trekker access required'}), 403

    try:
        from tasks.jobs import export_booking_history
        task = export_booking_history.delay(current_user['id'])
        return jsonify({
            'message': 'Export started! You will receive an email shortly.',
            'task_id': task.id
        }), 202
    except Exception as e:
        return jsonify({
            'message': 'Export service unavailable. Please try again later.'
        }), 503


@user_bp.route('/export-status/<task_id>', methods=['GET'])
@jwt_required()
def export_status(task_id):
    try:
        from tasks.jobs import celery
        task = celery.AsyncResult(task_id)
        return jsonify({
            'task_id': task_id,
            'status': task.status,
            'result': str(task.result)
        }), 200
    except Exception as e:
        return jsonify({'status': 'unavailable'}), 503


@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user = json.loads(get_jwt_identity())
    user = User.query.get(current_user['id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()

    if not data.get('name') or len(data.get('name', '').strip()) < 2:
        return jsonify({'message': 'Name must be at least 2 characters'}), 400

    user.name = data.get('name', user.name).strip()
    user.contact = data.get('contact', user.contact)
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200


@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user = json.loads(get_jwt_identity())
    user = User.query.get(current_user['id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'id': user.id, 'name': user.name,
        'email': user.email, 'contact': user.contact,
        'role': user.role, 'is_active': user.is_active
    }), 200


@user_bp.route('/treks/search', methods=['GET'])
@jwt_required()
def search_treks():
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify([]), 200

    treks = Trek.query.filter(
        Trek.name.ilike(f'%{query}%'),
        Trek.status == 'Open'
    ).all()

    result = [{
        'id': t.id, 'name': t.name, 'location': t.location,
        'difficulty': t.difficulty, 'duration': t.duration,
        'available_slots': t.available_slots, 'status': t.status,
        'start_date': t.start_date.strftime('%Y-%m-%d') if t.start_date else None,
    } for t in treks]

    return jsonify(result), 200