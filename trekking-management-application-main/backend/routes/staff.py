import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import User
from models.trek import Trek
from models.booking import Booking

staff_bp = Blueprint('staff', __name__)

def staff_required():
    current_user = json.loads(get_jwt_identity())
    if current_user['role'] != 'staff':
        return None
    return current_user

# Staff dashboard
@staff_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    current_user = staff_required()
    if not current_user:
        return jsonify({'message': 'Staff access required'}), 403

    # Get treks assigned to this staff member
    assigned_treks = Trek.query.filter_by(assigned_staff_id=current_user['id']).all()

    result = []
    for trek in assigned_treks:
        booking_count = Booking.query.filter_by(trek_id=trek.id, status='Booked').count()
        result.append({
            'id': trek.id,
            'name': trek.name,
            'location': trek.location,
            'difficulty': trek.difficulty,
            'status': trek.status,
            'available_slots': trek.available_slots,
            'total_slots': trek.total_slots,
            'registered_trekkers': booking_count
        })

    return jsonify({
        'assigned_treks': result,
        'total_assigned': len(result)
    }), 200


# Update trek slots and status
@staff_bp.route('/treks/<int:trek_id>', methods=['PUT'])
@jwt_required()
def update_trek(trek_id):
    current_user = staff_required()
    if not current_user:
        return jsonify({'message': 'Staff access required'}), 403

    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({'message': 'Trek not found'}), 404

    # Only assigned staff can update
    if trek.assigned_staff_id != current_user['id']:
        return jsonify({'message': 'You are not assigned to this trek'}), 403

    data = request.get_json()
    trek.available_slots = data.get('available_slots', trek.available_slots)
    trek.status = data.get('status', trek.status)

    db.session.commit()
    return jsonify({'message': 'Trek updated successfully'}), 200


# View participants for a trek
@staff_bp.route('/treks/<int:trek_id>/participants', methods=['GET'])
@jwt_required()
def get_participants(trek_id):
    current_user = staff_required()
    if not current_user:
        return jsonify({'message': 'Staff access required'}), 403

    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({'message': 'Trek not found'}), 404

    if trek.assigned_staff_id != current_user['id']:
        return jsonify({'message': 'You are not assigned to this trek'}), 403

    bookings = Booking.query.filter_by(trek_id=trek_id, status='Booked').all()
    result = []
    for booking in bookings:
        result.append({
            'booking_id': booking.id,
            'user_id': booking.user_id,
            'user_name': booking.user.name,
            'user_email': booking.user.email,
            'booking_date': booking.booking_date.strftime('%Y-%m-%d'),
            'status': booking.status
        })

    return jsonify({
        'trek_name': trek.name,
        'participants': result,
        'total': len(result)
    }), 200


# Mark trek as started/completed
@staff_bp.route('/treks/<int:trek_id>/status', methods=['PUT'])
@jwt_required()
def update_trek_status(trek_id):
    current_user = staff_required()
    if not current_user:
        return jsonify({'message': 'Staff access required'}), 403

    trek = Trek.query.get(trek_id)
    if not trek:
        return jsonify({'message': 'Trek not found'}), 404

    if trek.assigned_staff_id != current_user['id']:
        return jsonify({'message': 'You are not assigned to this trek'}), 403

    data = request.get_json()
    new_status = data.get('status')

    allowed_statuses = ['Open', 'Closed', 'Completed']
    if new_status not in allowed_statuses:
        return jsonify({'message': f'Status must be one of {allowed_statuses}'}), 400

    trek.status = new_status

    # If trek completed, mark all bookings as completed
    if new_status == 'Completed':
        bookings = Booking.query.filter_by(trek_id=trek_id, status='Booked').all()
        for booking in bookings:
            booking.status = 'Completed'

    db.session.commit()
    return jsonify({'message': f'Trek status updated to {new_status}'}), 200
