import cloudinary.uploader
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from flask import redirect
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_login import logout_user, current_user
from wtforms import FileField
from app.models import *
from app import dao
import re
import hashlib
from sqlalchemy import func, case

class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if current_user.is_authenticated and current_user.role==UserRole.ADMIN:
            stats = db.session.query(
                Movie.id,
                Movie.title,
                func.count(Ticket.id).label("total_tickets"),
                func.sum(
                    case(
                        (Ticket.status == TicketStatus.PAID, Ticket.price),
                        else_=0
                    )
                ).label("revenue"),
                func.sum(
                    case((Ticket.status == TicketStatus.HOLDING, 1), else_=0)
                ).label("holding"),
                func.sum(
                    case((Ticket.status == TicketStatus.PAID, 1), else_=0)
                ).label("paid"),
                func.sum(
                    case((Ticket.status == TicketStatus.CANCELLED, 1), else_=0)
                ).label("cancelled"),
            ).join(ScreeningSeat, Ticket.screening_seat_id == ScreeningSeat.id) \
                .join(MovieScreening, ScreeningSeat.screening_id == MovieScreening.id) \
                .join(Movie, MovieScreening.movie_id == Movie.id) \
                .group_by(Movie.id) \
                .order_by(func.count(Ticket.id).desc()) \
                .all()

            chart_stats = [row for row in stats if row.paid > 0]
            chart_stats = sorted(chart_stats, key=lambda x: x.revenue or 0, reverse=True)

            hot_movies = sorted(stats, key=lambda x: x.total_tickets or 0, reverse=True)
            hot_movies = hot_movies[:10]

            return self.render('admin/index.html', stats=stats, chart_stats=chart_stats, hot_movies=hot_movies)
        else:
            return self.render('admin/index.html', msg="Bạn không có quyền truy cập trang quản trị!")

class MyLogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.role==UserRole.ADMIN

class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role==UserRole.ADMIN

class CustomerView(AuthenticatedView):
    column_searchable_list = ["full_name", "username"]
    column_filters = ["phone_number", "email"]

    form_excluded_columns = ["avatar", "holding_seats", "bills"]
    form_extra_fields = {
        "avatar": FileField("Avatar")
    }

    def on_model_change(self, form, model, is_created):
        if dao.is_username_exists(form.username.data):
            existing = Customer.query.filter_by(username=form.username.data).first()
            if existing and existing.id != model.id:
                raise ValueError("Username đã tồn tại!")

        if form.password.data:
            if len(form.password.data) == 32 and re.fullmatch(r'[a-f0-9]{32}', form.password.data):
                pass
            else:
                if not re.search(r'[A-Z]', form.password.data) or not re.search(r'\d', form.password.data):
                    raise ValueError("Mật khẩu phải chứa kí tự in hoa và số!")
                model.password = hashlib.md5(form.password.data.encode('utf-8')).hexdigest()

        if not re.search(r'^\S+@\S+\.\S+$', form.email.data):
            raise ValueError("Email không đúnng định dạng!")

        if dao.is_email_exists(form.email.data):
            existing = Customer.query.filter_by(email=form.email.data).first()
            if existing.id != model.id:
                raise ValueError("Email đã tồn tại!")

        if not re.match(r'^(0)(3|5|7|8|9)\d{8}$', form.phone_number.data):
            raise ValueError("Số điện thoại không hợp lệ!")

        if dao.is_phone_exists(form.phone_number.data):
            existing = Customer.query.filter_by(phone_number=form.phone_number.data).first()
            if existing.id != model.id:
                raise ValueError("Số điện thoại đã tồn tại!")

        if form.avatar.data:
            res = cloudinary.uploader.upload(form.avatar.data)
            file_path = res["secure_url"]
            model.avatar = file_path
            form.avatar.data = None

class MovieView(AuthenticatedView):
    column_list = ["title", "description", "duration", "age_limit", "release_date", "types"]
    column_searchable_list = ["title"]
    column_filters = ["age_limit", "release_date"]

    form_excluded_columns = ["poster", "movie_screenings", "movie_type_details"]

    def _format_types(view, context, model, name):
        return ", ".join([mtd.type.name for mtd in model.movie_type_details])

    column_formatters = {
        "types": _format_types
    }

    def _get_types(self):
        return db.session.query(MovieType).all()

    form_extra_fields = {
        "poster": FileField("Poster"),
        "movie_type_list": QuerySelectMultipleField(
            "Thể loại",
            query_factory=_get_types,
            get_label="name"
        )
    }

    def on_model_change(self, form, model, is_created):
        if form.poster.data:
            res = cloudinary.uploader.upload(form.poster.data)
            file_path = res["secure_url"]
            model.poster = file_path
            form.poster.data = None

        for mtd in list(model.movie_type_details):
            db.session.delete(mtd)
        db.session.flush()

        for t in form.movie_type_list.data:
            mtd = MovieTypeDetail(
                type_id=t.id,
                movie=model
            )
            model.movie_type_details.append(mtd)

    def on_form_prefill(self, form, id):
        movie = self.session.get(Movie, id)
        form.movie_type_list.data = [mtd.type for mtd in movie.movie_type_details]

class MovieTypeView(AuthenticatedView):
    column_searchable_list = ["name"]
    form_excluded_columns = ["movie_type_details"]

# class MovieTypeDetailView(AuthenticatedView):
#     column_filters = ["type.name", "movie.title"]

class RoomTypeView(AuthenticatedView):
    column_searchable_list = ["name"]
    column_list = ["name", "active", "created_at", "rooms"]

class RoomView(AuthenticatedView):
    column_searchable_list = ["number"]
    column_filters = ["room_type"]

    form_excluded_columns = ["image"]
    form_extra_fields = {
        "image": FileField("Image")
    }

    def on_model_change(self, form, model, is_created):
        if form.image.data:
            res = cloudinary.uploader.upload(form.image.data)
            file_path = res["secure_url"]
            model.image = file_path
            form.image.data = None

class SeatView(AuthenticatedView):
    column_filters = ["row", "number", "room"]

    form_excluded_columns = ["screening_seats"]

class MovieScreeningView(AuthenticatedView):
    form_excluded_columns = ["screening_seats"]

    def on_model_change(self, form, model, is_created):
        if not is_created:
            return

        db.session.flush()

        if form.room.data:
            room_id = form.room.data.id
            seats = Seat.query.filter_by(room_id=room_id).all()

            for seat in seats:
                exists = ScreeningSeat.query.filter_by(
                    seat_id=seat.id,
                    screening_id=model.id
                ).first()

                if not exists:
                    db.session.add(ScreeningSeat(
                        seat_id=seat.id,
                        screening_id=model.id
                    ))

class ScreeningSeatView(AuthenticatedView):
    form_excluded_columns = ["tickets"]

class TicketView(AuthenticatedView):
    column_list = ["bill.customer", "price", "status", "pay_time", "screening_seat", "active", "created_at"]
    form_excluded_columns = ["bill"]
    column_labels = {
        "bill.customer": "Customer"
    }

class BillView(AuthenticatedView):
    form_excluded_columns = ["tickets", "payments"]

class PaymentView(AuthenticatedView):
    column_list = ["bill.customer", "amount", "status", "txn_ref", "vnp_transaction_id", "active", "created_at"]
    form_excluded_columns = ["bill"]
    column_labels = {
        "bill.customer": "Customer"
    }


admin = Admin(app=app, name="Quản lý rạp phim - CINEMA", theme=Bootstrap4Theme(), index_view=MyAdminIndexView())
admin.add_view(CustomerView(Customer, db.session))
admin.add_view(MovieTypeView(MovieType, db.session))
admin.add_view(MovieView(Movie, db.session))
# admin.add_view(MovieTypeDetailView(MovieTypeDetail, db.session))
admin.add_view(RoomTypeView(RoomType, db.session))
admin.add_view(RoomView(Room, db.session))
admin.add_view(SeatView(Seat, db.session))
admin.add_view(MovieScreeningView(MovieScreening, db.session))
admin.add_view(ScreeningSeatView(ScreeningSeat, db.session))
admin.add_view(TicketView(Ticket, db.session))
admin.add_view(BillView(Bill, db.session))
admin.add_view(PaymentView(Payment, db.session))
admin.add_view(MyLogoutView(name="Đăng xuất"))