import csv
import io
import sys
import os
from datetime import datetime, timedelta
from flask import render_template_string
from flask_mail import Mail, Message
from celery import Celery
from celery.schedules import crontab


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create Celery instance
celery = Celery(
    'tasks',
    broker='redis://localhost:6379/1',
    backend='redis://localhost:6379/2'
)

celery.conf.beat_schedule = {
    'daily-trek-reminders': {
        'task': 'tasks.jobs.send_daily_reminders',
        'schedule': crontab(hour=8, minute=0),
    },
    'monthly-activity-report': {
        'task': 'tasks.jobs.send_monthly_report',
        'schedule': crontab(day_of_month=1, hour=6, minute=0),
    },
}
celery.conf.timezone = 'Asia/Kolkata'

REMINDER_TEMPLATE = """
<html><body style="font-family:Arial,sans-serif;padding:20px;">
  <h2 style="color:#585D27;">🏔️ Trek Reminder</h2>
  <p>Hi <strong>{{ name }}</strong>,</p>
  <p>Your trek <strong>{{ trek_name }}</strong> is coming up soon!</p>
  <table style="border-collapse:collapse;width:100%;">
    <tr><td style="padding:8px;border:1px solid #BCA890;"><b>Location</b></td>
        <td style="padding:8px;border:1px solid #BCA890;">{{ location }}</td></tr>
    <tr><td style="padding:8px;border:1px solid #BCA890;"><b>Start Date</b></td>
        <td style="padding:8px;border:1px solid #BCA890;">{{ start_date }}</td></tr>
    <tr><td style="padding:8px;border:1px solid #BCA890;"><b>Difficulty</b></td>
        <td style="padding:8px;border:1px solid #BCA890;">{{ difficulty }}</td></tr>
    <tr><td style="padding:8px;border:1px solid #BCA890;"><b>Duration</b></td>
        <td style="padding:8px;border:1px solid #BCA890;">{{ duration }} days</td></tr>
  </table>
  <p style="margin-top:20px;">Please be prepared and carry all necessary gear. Stay safe!</p>
  <p style="color:#888;font-size:12px;">— Trekking Management App Team</p>
</body></html>
"""

MONTHLY_REPORT_TEMPLATE = """
<html><body style="font-family:Arial,sans-serif;padding:20px;">
  <h2 style="color:#585D27;">📊 Monthly Trekking Activity Report</h2>
  <p>Report for <strong>{{ month_year }}</strong></p>
  <hr>
  <h3>Summary</h3>
  <table style="border-collapse:collapse;width:60%;">
    <tr style="background:#BCA890;">
      <th style="padding:10px;border:1px solid #ccc;text-align:left;">Metric</th>
      <th style="padding:10px;border:1px solid #ccc;text-align:left;">Count</th>
    </tr>
    <tr><td style="padding:8px;border:1px solid #ccc;">Treks Conducted</td>
        <td style="padding:8px;border:1px solid #ccc;">{{ treks_conducted }}</td></tr>
    <tr><td style="padding:8px;border:1px solid #ccc;">Total Bookings</td>
        <td style="padding:8px;border:1px solid #ccc;">{{ total_bookings }}</td></tr>
    <tr><td style="padding:8px;border:1px solid #ccc;">Unique Participants</td>
        <td style="padding:8px;border:1px solid #ccc;">{{ unique_participants }}</td></tr>
    <tr><td style="padding:8px;border:1px solid #ccc;">Cancelled Bookings</td>
        <td style="padding:8px;border:1px solid #ccc;">{{ cancelled_bookings }}</td></tr>
  </table>
  <h3 style="margin-top:20px;">🏆 Popular Treks This Month</h3>
  <table style="border-collapse:collapse;width:100%;">
    <tr style="background:#BCA890;">
      <th style="padding:10px;border:1px solid #ccc;">Trek Name</th>
      <th style="padding:10px;border:1px solid #ccc;">Location</th>
      <th style="padding:10px;border:1px solid #ccc;">Bookings</th>
    </tr>
    {% for trek in popular_treks %}
    <tr>
      <td style="padding:8px;border:1px solid #ccc;">{{ trek.name }}</td>
      <td style="padding:8px;border:1px solid #ccc;">{{ trek.location }}</td>
      <td style="padding:8px;border:1px solid #ccc;">{{ trek.bookings }}</td>
    </tr>
    {% endfor %}
  </table>
  <p style="color:#888;font-size:12px;margin-top:30px;">
    Generated on {{ generated_at }} — Trekking Management App
  </p>
</body></html>
"""

CSV_DONE_TEMPLATE = """
<html><body style="font-family:Arial,sans-serif;padding:20px;">
  <h2 style="color:#585D27;">✅ Your Booking History Export is Ready</h2>
  <p>Hi <strong>{{ name }}</strong>,</p>
  <p>Your trekking history CSV has been exported. Please find it attached.</p>
  <p style="color:#888;font-size:12px;">— Trekking Management App Team</p>
</body></html>
"""


def get_app():
    from app import app
    return app


@celery.task(name='tasks.jobs.send_daily_reminders')
def send_daily_reminders():
    app = get_app()
    with app.app_context():
        from models.trek import Trek
        from models.booking import Booking
        from models.user import User
        mail = Mail(app)

        now = datetime.utcnow()
        upcoming_cutoff = now + timedelta(days=3)

        upcoming_treks = Trek.query.filter(
            Trek.start_date != None,
            Trek.start_date >= now,
            Trek.start_date <= upcoming_cutoff,
            Trek.status == 'Open'
        ).all()

        sent = 0
        for trek in upcoming_treks:
            bookings = Booking.query.filter_by(trek_id=trek.id, status='Booked').all()
            for booking in bookings:
                user = User.query.get(booking.user_id)
                if user and user.email:
                    try:
                        html_body = render_template_string(
                            REMINDER_TEMPLATE,
                            name=user.name,
                            trek_name=trek.name,
                            location=trek.location,
                            start_date=trek.start_date.strftime('%d %b %Y') if trek.start_date else 'TBD',
                            difficulty=trek.difficulty,
                            duration=trek.duration
                        )
                        msg = Message(
                            subject=f"🏔️ Reminder: Your trek '{trek.name}' is coming up!",
                            recipients=[user.email],
                            html=html_body
                        )
                        mail.send(msg)
                        sent += 1
                    except Exception as e:
                        print(f"Failed to send reminder to {user.email}: {e}")

        return f"Sent {sent} reminder(s)"


@celery.task(name='tasks.jobs.send_monthly_report')
def send_monthly_report():
    app = get_app()
    with app.app_context():
        from models.trek import Trek
        from models.booking import Booking
        from models.user import User
        mail = Mail(app)

        now = datetime.utcnow()
        first_day = datetime(now.year, now.month - 1 if now.month > 1 else 12, 1)
        last_day = datetime(now.year, now.month, 1)
        month_year = first_day.strftime('%B %Y')

        month_bookings = Booking.query.filter(
            Booking.booking_date >= first_day,
            Booking.booking_date < last_day
        ).all()

        total_bookings = len(month_bookings)
        cancelled_bookings = sum(1 for b in month_bookings if b.status == 'Cancelled')
        unique_participants = len(set(b.user_id for b in month_bookings))

        treks_conducted = Trek.query.filter(
            Trek.status == 'Completed',
            Trek.end_date >= first_day,
            Trek.end_date < last_day
        ).count()

        from collections import Counter
        trek_counts = Counter(b.trek_id for b in month_bookings)
        popular = []
        for trek_id, count in trek_counts.most_common(5):
            trek = Trek.query.get(trek_id)
            if trek:
                popular.append({
                    'name': trek.name,
                    'location': trek.location,
                    'bookings': count
                })

        html_body = render_template_string(
            MONTHLY_REPORT_TEMPLATE,
            month_year=month_year,
            treks_conducted=treks_conducted,
            total_bookings=total_bookings,
            unique_participants=unique_participants,
            cancelled_bookings=cancelled_bookings,
            popular_treks=popular,
            generated_at=now.strftime('%d %b %Y %H:%M')
        )

        admin = User.query.filter_by(role='admin').first()
        if admin:
            try:
                msg = Message(
                    subject=f"📊 Monthly Trekking Report — {month_year}",
                    recipients=[admin.email],
                    html=html_body
                )
                mail.send(msg)
                return f"Monthly report sent to {admin.email}"
            except Exception as e:
                return f"Failed to send report: {e}"

        return "No admin found"


@celery.task(name='tasks.jobs.export_booking_history')
def export_booking_history(user_id):
    app = get_app()
    with app.app_context():
        from models.user import User
        from models.trek import Trek
        from models.booking import Booking
        mail = Mail(app)

        user = User.query.get(user_id)
        if not user:
            return "User not found"

        bookings = Booking.query.filter_by(user_id=user_id).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            'Booking ID', 'Trek Name', 'Location', 'Difficulty',
            'Duration (days)', 'Start Date', 'End Date',
            'Booking Date', 'Booking Status'
        ])

        for b in bookings:
            trek = Trek.query.get(b.trek_id)
            writer.writerow([
                b.id,
                trek.name if trek else 'N/A',
                trek.location if trek else 'N/A',
                trek.difficulty if trek else 'N/A',
                trek.duration if trek else 'N/A',
                trek.start_date.strftime('%Y-%m-%d') if trek and trek.start_date else 'N/A',
                trek.end_date.strftime('%Y-%m-%d') if trek and trek.end_date else 'N/A',
                b.booking_date.strftime('%Y-%m-%d'),
                b.status
            ])

        csv_data = output.getvalue().encode('utf-8')

        try:
            html_body = render_template_string(CSV_DONE_TEMPLATE, name=user.name)
            msg = Message(
                subject="✅ Your Trekking History Export",
                recipients=[user.email],
                html=html_body
            )
            msg.attach(
                filename=f"booking_history_{user_id}.csv",
                content_type='text/csv',
                data=csv_data
            )
            mail.send(msg)
            return f"CSV sent to {user.email}"
        except Exception as e:
            return f"Failed to send CSV: {e}"