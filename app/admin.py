import cloudinary.uploader
from flask import redirect
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_login import logout_user, current_user
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from wtforms import FileField

from app import app, db
from app.models import *
from app import dao
import re
import hashlib

class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render('admin/index.html')

class MyLogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role==UserRole.ADMIN

class CustomerView(AuthenticatedView):
    column_searchable_list = ["full_name", "username"]
    column_filters = ["phone_number", "email"]

    form_excluded_columns = ["avatar"]
    form_extra_fields = {
        "avatar": FileField("Avatar")
    }

    def on_model_change(self, form, model, is_created):
        if dao.is_username_exists(form.username.data):
            existing = Customer.query.filter_by(phone_number=form.username.data).first()
            if existing.id != model.id:
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
            raise ValueError("Số điện thoại không hợp lệ,!")

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
    column_searchable_list = ["title"]
    column_filters = ["age_limit", "release_date"]

    form_excluded_columns = ["poster"]
    form_extra_fields = {
        "poster": FileField("Poster")
    }

    def on_model_change(self, form, model, is_created):
        if form.poster.data:
            res = cloudinary.uploader.upload(form.poster.data)
            file_path = res["secure_url"]
            model.poster = file_path
            form.poster.data = None

class MovieTypeDetailView(AuthenticatedView):
    column_filters = ["type.name", "movie.title"]

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

class RoomTypeView(AuthenticatedView):
    column_searchable_list = ["name"]
    column_list = ["name", "active", "created_at", "rooms"]

admin = Admin(app=app, name="Quản lý rạp phim - CINEMA", theme=Bootstrap4Theme(), index_view=MyAdminIndexView())
admin.add_view(CustomerView(Customer, db.session))
admin.add_view(AuthenticatedView(MovieType, db.session))
admin.add_view(MovieView(Movie, db.session))
admin.add_view(MovieTypeDetailView(MovieTypeDetail, db.session))
admin.add_view(RoomTypeView(RoomType, db.session))
admin.add_view(RoomView(Room, db.session))
admin.add_view(AuthenticatedView(Seat, db.session))
admin.add_view(AuthenticatedView(MovieScreening, db.session))
admin.add_view(AuthenticatedView(ScreeningSeat, db.session))
admin.add_view(AuthenticatedView(Ticket, db.session))
admin.add_view(AuthenticatedView(Bill, db.session))
admin.add_view(AuthenticatedView(Payment, db.session))
admin.add_view(MyLogoutView(name="Đăng xuất"))