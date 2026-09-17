from extensions import db
from datetime import datetime

class Trek(db.Model):
    __tablename__ = 'treks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # Easy / Moderate / Hard
    duration = db.Column(db.Integer, nullable=False)  # in days
    available_slots = db.Column(db.Integer, nullable=False)
    total_slots = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending/Approved/Open/Closed/Completed
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship: lets us do trek.assigned_staff to get the User object
    assigned_staff = db.relationship('User', backref='assigned_treks')

    def __repr__(self):
        return f"<Trek {self.name} ({self.status})>"