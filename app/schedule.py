from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
from app.models import ScreeningSeat, SeatStatus, TicketStatus, PaymentStatus, Ticket, MovieScreening, Bill

def start_scheduler(app, db):
    scheduler = BackgroundScheduler()

    def release_expired_seats():
        with app.app_context():
            now = datetime.now()

            expired_seats = db.session.query(ScreeningSeat.id).filter(
                ScreeningSeat.status == SeatStatus.HOLDING,
                ScreeningSeat.hold_expired_at < now
            ).all()

            expired_tickets = db.session.query(Ticket.bill_id).filter(
                Ticket.screening_seat_id.in_(expired_seats)
            ).all()

            if not expired_tickets:
                return

            ids = [s.id for s in expired_seats]
            ScreeningSeat.query.filter(ScreeningSeat.id.in_(ids)).update({
                'status': SeatStatus.AVAILABLE,
                'holding_user_id': None
            }, synchronize_session=False)

            Ticket.query.filter(Ticket.screening_seat_id.in_(ids)).update({
                'status': TicketStatus.CANCELLED
            }, synchronize_session=False)

            bill_ids = {t.bill_id for t in expired_tickets if t.bill_id}
            Bill.query.filter(Bill.id.in_(bill_ids)).update({
                'status': PaymentStatus.FAILED
            }, synchronize_session=False)

            db.session.commit()

    def checkin_tickets():
        with app.app_context():
            now = datetime.now()
            ticket_ids = (db.session.query(Ticket.id)
                     .join(ScreeningSeat, Ticket.screening_seat_id == ScreeningSeat.id)
                     .join(MovieScreening, ScreeningSeat.screening_id == MovieScreening.id)
                     .filter(
                Ticket.status == TicketStatus.PAID,
                MovieScreening.start_time <= now
            ).all())
            ids = [t.id for t in ticket_ids]

            db.session.query(Ticket).filter(Ticket.id.in_(ids)).update(
                {'status': TicketStatus.USED},
                synchronize_session=False
            )
            db.session.commit()

    release_expired_seats()
    checkin_tickets()
    scheduler.add_job(release_expired_seats, 'interval', seconds=1)
    scheduler.add_job(checkin_tickets, 'interval', seconds=1)
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        scheduler.start()