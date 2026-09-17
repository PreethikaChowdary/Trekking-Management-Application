from extensions import db

class StaffProfile(db.Model):
    __tablename__ = 'staff_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    bio = db.Column(db.String(300), nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default='Active')  # Active / Inactive

    # Relationship
    user = db.relationship('User', backref='staff_profile', uselist=False)

    def __repr__(self):
        return f"<StaffProfile for User:{self.user_id}>"
    