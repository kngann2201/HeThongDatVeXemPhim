from datetime import timedelta

from app import app, db, login, admin
from flask import render_template, request, redirect, url_for, flash, jsonify
from app.decorators import anonymous_required
from flask_login import login_user, current_user, login_required, logout_user
from flask_mail import Message
import re
import dao
import cloudinary.uploader
import math
from datetime import date
from dateutil.relativedelta import relativedelta

@app.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    page_size = 8
    movies = dao.get_movies(page=page, page_size=page_size)
    total_movies = dao.count_movies()
    pages = math.ceil(total_movies / page_size)

    return render_template('index.html',
                           products=movies,
                           pages=pages,
                           current_page=page)

@app.route("/register", methods=['GET', 'POST'])
def register():
    err_msg = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        email=request.form.get('email')
        birthday = request.form.get('birthday')
        avatar= request.files.get('avatar')
        avatar_url = None
        if birthday:
            birthday = date.fromisoformat(birthday)
            today = date.today()
            age = relativedelta(today, birthday).years

            if age < 13:
                err_msg = "Bạn phải từ 13 tuổi trở lên để đăng ký tài khoản."
                return render_template('register.html', err_msg=err_msg)

            if age > 100:
                err_msg = "Ngày sinh không hợp lệ."
                return render_template('register.html', err_msg=err_msg)
        if avatar:
            res = cloudinary.uploader.upload(avatar)
            avatar_url = res.get('secure_url')

        if not birthday:
            err_msg = "Vui lòng chọn ngày sinh"
            return render_template('register.html', err_msg=err_msg)

        if not re.match(r'^(0)(3|5|7|8|9)\d{8}$', phone):
            err_msg = "Số điện thoại không hợp lệ"
            return render_template('register.html', err_msg=err_msg)

        if dao.is_username_exists(username):
            err_msg = "Tên đăng nhập đã tồn tại"
            return render_template('register.html', err_msg=err_msg)

        if dao.is_phone_exists(phone):
            err_msg = "Số điện thoại đã được sử dụng"
            return render_template('register.html', err_msg=err_msg)

        if len(password) < 8:
            err_msg = "Mật khẩu phải có ít nhất 8 ký tự"
            return render_template('register.html', err_msg=err_msg)

        if not re.search(r'[A-Z]', password) or not re.search(r'\d', password):
            err_msg = "Mật khẩu phải có chữ hoa và số"
            return render_template('register.html', err_msg=err_msg)

        if password != confirm:
            err_msg = "Mật khẩu không khớp!"
            return render_template('register.html', err_msg=err_msg)

        if not re.search(r'^\S+@\S+\.\S+$', email) or dao.is_email_exists(email):
            err_msg = "Không đúng định dạng hoặc email đã tồn tại"
            return render_template('register.html', err_msg=err_msg)
        try:
            dao.add_user(
                    username=username,
                    password=password,
                    full_name=full_name,
                    phone=phone,
                    email=email,
                    birthday=birthday,
                    avatar=avatar_url
            )
            return render_template("login.html", success=True)
        except Exception as ex:
            db.session.rollback()
            err_msg = "Hệ thống đang lỗi!"
            print(ex)
    return render_template('register.html', err_msg=err_msg)

@app.route("/login", methods=['GET', 'POST'])
@anonymous_required
def login_my_user():
    err_msg = None
    next_page = request.args.get('next') or request.form.get('next')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username, password)

        if user:
            login_user(user)
            if next_page:
                return redirect(next_page)
            else:
                return redirect('/')
        else:
            err_msg = "Username hoac password khong dung!!!"

    return render_template('login.html', err_msg=err_msg)

@login.user_loader
def get_user(user_id):
    user = dao.get_admin_by_id(user_id)
    if user:
        return user

    return dao.get_user_by_id(user_id)

@login.unauthorized_handler
def unauthorized_callback():
    flash("Bạn cần đăng nhập để tiếp tục!", "warning")
    return redirect('/login?next=' + request.path)

@app.route("/logout")
def logout_my_user():
    logout_user()
    return redirect('/login')

@app.route("/login-admin", methods=["post", "get"])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = dao.auth_admin(username, password)

        if user:
            login_user(user)
        else:
            err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return redirect("/admin")

@app.route("/booking/<movie_id>", methods=['GET', 'POST'])
def booking(movie_id):
    err_msg = None
    movie = dao.get_movie_by_id(movie_id)
    movie_types = dao.get_movie_types(movie_id)
    room_types = dao.get_room_types()

    return render_template('booking.html', err_msg=err_msg,
        movie=movie, movie_types=movie_types, room_types=room_types)

@app.route("/api/get-rooms/<room_type_id>", methods=['GET'])
def get_rooms(room_type_id):
    rooms = dao.get_room_by_type(room_type_id)
    print(rooms)
    rooms_data = []
    for r in rooms:
        rooms_data.append({
            "id": r.id,
            "number": r.number,
            "image": r.image,
            "active": r.active
        })
    return jsonify({"success": True, "rooms": rooms_data})

@app.route("/api/get-screenings", methods=['GET'])
def get_screenings():
    watch_date = request.args.get("watch_date")
    room_id = request.args.get("room_id")
    movie_id = request.args.get("movie_id")
    print(watch_date, room_id, movie_id)
    movie = dao.get_movie_by_id(movie_id)
    screenings = dao.get_movie_screenings(movie_id=movie_id, room_id=room_id, watch_date=watch_date)
    print(screenings)
    screenings_data = []
    for s in screenings:
        screenings_data.append({
            "id": s.id,
            "start_time": s.start_time.strftime('%H:%M'),
            "end_time": (s.start_time + timedelta(minutes=movie.duration)).strftime('%H:%M'),
            "base_price": s.base_price,
            "active": s.active
        })
    return jsonify({"success": True, "screenings": screenings_data})

@app.route("/api/get-seats/<screening_id>", methods=['GET'])
def get_seats(screening_id):
    seats = dao.get_seats_by_screening(screening_id=screening_id)
    print(seats)

    seats_data = {}
    for seat, status in seats:
        row = seat.row
        if row not in seats_data:
            seats_data[row] = []

        seats_data[row].append({
            "id": seat.id,
            "number": seat.number,
            "active": seat.active,
            "status": status.name
        })
    return jsonify({"success": True, "seats": seats_data})

@app.route("/pay", methods=['POST', 'GET'])
@login_required
def pay():
    return render_template("pay.html")

@app.route("/user/profile")
@login_required
def profile():
    return render_template('user/profile.html', user=current_user)

@app.route('/user/bookings')
@login_required
def history_booking():
    customer = current_user.customer
    bookings = customer.bookings if customer else []
    return render_template('user_bookings.html', bookings=bookings)



if __name__ == "__main__":
    app.run(debug=True, port=5001)
