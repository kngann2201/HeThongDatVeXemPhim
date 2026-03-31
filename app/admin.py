from flask import redirect
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_login import logout_user, current_user
from app import app, db
from app.models import *


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

class MovieTypeDetailView(ModelView):
    column_searchable_list = ["movie.title", "type.name"]
    column_filters = ["movie.title", "type.name"]

admin = Admin(app=app, name="Quản lý rạp phim - CINEMA", theme=Bootstrap4Theme(), index_view=MyAdminIndexView())
admin.add_view(AuthenticatedView(Customer, db.session))
admin.add_view(AuthenticatedView(MovieType, db.session))
admin.add_view(AuthenticatedView(Movie, db.session))
admin.add_view(MovieTypeDetailView(MovieTypeDetail, db.session, name="Movie Type Details"))
admin.add_view(AuthenticatedView(RoomType, db.session))
admin.add_view(AuthenticatedView(Room, db.session))
admin.add_view(AuthenticatedView(Seat, db.session))
admin.add_view(AuthenticatedView(MovieScreening, db.session))
admin.add_view(AuthenticatedView(ScreeningSeat, db.session))
admin.add_view(AuthenticatedView(Ticket, db.session))
admin.add_view(AuthenticatedView(Bill, db.session))
admin.add_view(AuthenticatedView(Payment, db.session))
admin.add_view(MyLogoutView(name="Đăng xuất"))