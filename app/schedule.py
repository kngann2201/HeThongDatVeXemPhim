from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os

def start_scheduler(app, db):
    scheduler = BackgroundScheduler()

    def release_expired_seats():
        from app.models import ScreeningSeat, SeatStatus, TicketStatus, PaymentStatus

        with app.app_context():
            now = datetime.now()

            expired_seats = ScreeningSeat.query.filter(
                ScreeningSeat.status == SeatStatus.HOLDING,
                ScreeningSeat.hold_expired_at < now
            ).all()

            for s in expired_seats:
                s.status = SeatStatus.AVAILABLE
                s.holding_user_id = None
                for t in s.tickets:
                    t.status = TicketStatus.CANCELLED
                    t.bill.status = PaymentStatus.FAILED

            db.session.commit()

    scheduler.add_job(release_expired_seats, 'interval', minutes=0.8)
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        scheduler.start()