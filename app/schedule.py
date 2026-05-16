from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
from app.models import ScreeningSeat, SeatStatus, TicketStatus, PaymentStatus, Ticket, MovieScreening, Bill

def start_scheduler(app, db):
    scheduler = BackgroundScheduler()

    def release_expired_seats():
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

    def checkin_tickets():
        with app.app_context():
            now = datetime.now()
            tickets = (db.session.query(Ticket)
                       .join(ScreeningSeat, Ticket.screening_seat_id == ScreeningSeat.id)
                       .join(MovieScreening, ScreeningSeat.screening_id == MovieScreening.id)
                       .filter(
                Ticket.status == TicketStatus.PAID,
                MovieScreening.start_time <= now)
                       .all())

            for t in tickets:
                t.status = TicketStatus.USED

            db.session.commit()

    release_expired_seats()
    checkin_tickets()
    scheduler.add_job(release_expired_seats, 'interval', seconds=1)
    scheduler.add_job(checkin_tickets, 'interval', seconds=1)
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        scheduler.start()