from datetime import timedelta

from app import app, db, login, admin, mail
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from app.decorators import anonymous_required
from flask_login import login_user, current_user, login_required, logout_user
from flask_mail import Message
import re
import dao
import cloudinary.uploader
import math
from app.models import Movie
import secrets
@app.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    page_size = 8
    movies = dao.get_movies(page=page, page_size=page_size)
    total_movies = dao.count_movies()
    pages = math.ceil(total_movies / page_size)
    keyword = request.args.get('kw', '').strip()
    query = Movie.query

    if keyword:
        query = query.filter(Movie.title.icontains(keyword))
    movies = query.order_by(Movie.id.desc()).all()
    return render_template('index.html',
                           products=movies,
                           pages=pages,
                           current_page=page,
                           keyword=keyword)

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
        if password != confirm:
            err_msg = "Mật khẩu không khớp!"
            return render_template('register.html', err_msg=err_msg)
        if avatar:
            res = cloudinary.uploader.upload(avatar)
            avatar_url = res.get('secure_url')
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
            if next_page and next_page != "None" and next_page.startswith('/'):
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

@app.route("/user/history_booking")
@login_required
def history_booking_ticket():
    data = dao.get_info_movie(current_user.id)
    return render_template('user/history_booking.html', watched_list=data)

@app.route("/user/history_watched")
@login_required
def history_watched():
    data = dao.get_info_movie(current_user.id)
    return render_template('user/history_watched.html', watched_list=data)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        customer = dao.get_customer_by_email(identifier)

        if customer:
            if customer.email:
                otp = "".join([str(secrets.randbelow(10)) for _ in range(6)])
                session['reset_otp'] = otp
                session['reset_customer_id'] = customer.id
                if dao.send_reset_email(customer.email, otp):
                    flash(f'Mã xác nhận đã được gửi vào email: {customer.email}', 'info')
                    return redirect(url_for('verify_otp'))
                else:
                    flash('Lỗi hệ thống khi gửi email. Hãy thử lại!', 'danger')
        else:
            flash('Email không tồn tại!', 'danger')

    return render_template('forgot_password.html')


@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if 'reset_otp' not in session:
        return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        user_otp = request.form.get('otp')
        if user_otp == session.get('reset_otp'):
            flash('Xác thực thành công! Hãy nhập mật khẩu mới.', 'success')
            return redirect(url_for('reset_password'))
        else:
            flash('Mã OTP không chính xác!', 'danger')

    return render_template('verify_otp.html')


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_otp' not in session:
        return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password == confirm:
            customer_id = session.get('reset_customer_id')
            try:
                if dao.update_password(customer_id, password):
                    flash('Đổi mật khẩu thành công! Mời bạn đăng nhập.', 'success')
                    return redirect(url_for('login_my_user'))
                else:
                    flash('Không tìm thấy tài khoản hoặc lỗi database!', 'danger')

            except ValueError as e:
                flash(str(e), 'warning')
        else:
            flash('Mật khẩu xác nhận không khớp!', 'danger')

    return render_template('reset_password.html')
if __name__ == "__main__":
    app.run(debug=True, port=5001)
