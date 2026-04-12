from app import app, db, login, admin, mail
from datetime import timedelta, datetime
import time
from app import app, db, login, admin
from flask import render_template, request, redirect, url_for, flash, jsonify, session, get_flashed_messages
from app.decorators import anonymous_required
from flask_login import login_user, current_user, login_required, logout_user
from flask_mail import Message
import re
import dao
import cloudinary.uploader
import math
import secrets
from dateutil.relativedelta import relativedelta
from app.models import SeatStatus, Payment, PaymentStatus, Movie
from app.vnpay import build_payment_url


@app.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    keyword = request.args.get('kw', '').strip()
    page_size = 8
    query = Movie.query
    if keyword:
        query = query.filter(Movie.title.icontains(keyword))

    total_movies = query.count()
    pages = math.ceil(total_movies / page_size)

    movies = query.order_by(Movie.id.desc()) \
        .offset((page - 1) * page_size) \
        .limit(page_size) \
        .all()

    msg = get_flashed_messages(with_categories=True)

    return render_template('index.html',
                           products=movies,
                           pages=pages,
                           current_page=page,
                           keyword=keyword,
                           msg=msg)


@app.route("/register", methods=['GET', 'POST'])
def register():
    err_msg = None
    data = {}

    if request.method == 'POST':
        data = request.form.to_dict()

        username = data.get('username')
        password = data.get('password')
        confirm = data.get('confirm_password')
        full_name = data.get('full_name')
        phone = data.get('phone')
        email = data.get('email')
        birthday = data.get('birthday')
        avatar = request.files.get('avatar')
        avatar_url = None

        if password != confirm:
            err_msg = "Mật khẩu không khớp!"
            return render_template('register.html', err_msg=err_msg, data=data)

        if avatar:
            res = cloudinary.uploader.upload(avatar)
            avatar_url = res.get('secure_url')
        try:
            dao.add_user(
                username=username, password=password, full_name=full_name,
                phone=phone, email=email, birthday=birthday, avatar=avatar_url
            )
            return render_template("login.html", success=True)
        except ValueError as v:
            err_msg = str(v)
        except Exception as ex:
            db.session.rollback()
            err_msg = "Hệ thống đang lỗi!"
            print(ex)

    return render_template('register.html', err_msg=err_msg, data=data)

@app.route("/login", methods=['GET', 'POST'])
@anonymous_required
def login_my_user():
    err_msg = None
    next_page = request.args.get('next') or request.form.get('next')
    data = {}

    if request.method == 'POST':
        data = request.form.to_dict()
        username = data.get('username')
        password = data.get('password')
        user = dao.auth_user(username, password)

        if user:
            login_user(user)
            if next_page and next_page != "None" and next_page.startswith('/'):
                return redirect(next_page)
            else:
                flash("Đăng nhập thành công!", "success")
                return redirect(url_for('index'))
        else:
            err_msg = "Username hoặc password không đúng!!!"

    return render_template('login.html', err_msg=err_msg, data=data)

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

@app.route("/login-admin", methods=["POST", "GET"])
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
    print(f"DS phòng theo loại phòng {room_type_id} đã chọn: {rooms}")
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
    print("Ngày xem:", watch_date)
    print("Id phòng đã chọn:",room_id)
    print("Id phim đã chọn:", movie_id)
    movie = dao.get_movie_by_id(movie_id)
    screenings = dao.get_movie_screenings(movie_id=movie_id, room_id=room_id, watch_date=watch_date)
    screenings = [s for s in screenings if s.start_time > datetime.now()]
    print("DS suất chiếu phim đã chọn:", screenings)
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

@app.route('/booking/submit', methods=['POST', 'GET'])
def booking_submit():
    if request.method == "POST":
        seat_ids = request.form.get("seat")
        screening = request.form.get("screening")
        session["booking_seats"] = seat_ids
        session["screening"] = screening

        # if not seat_ids:
        #     flash("Thiếu thông tin ghế", "error")
        #     return redirect(url_for('index'))
        #
        # if not screening:
        #     flash("Thiếu thông tin suất chiếu", "error")
        #     return redirect(url_for('index'))

        if not seat_ids or not screening:
            flash("Hệ thống đang có lỗi, vui lòng thử lại sau ít phút!", "error")
            return redirect(url_for('index'))

    else:
        seat_ids = session.get("booking_seats")
        screening = session.get("screening")
        if not seat_ids or not screening:
            flash("Hệ thống đang có lỗi, vui lòng thử lại sau ít phút!", "error")
            return redirect(url_for('index'))

    if not current_user.is_authenticated:
        return redirect(url_for("login_my_user", next=request.url))

    seat_ids = [int(id) for id in seat_ids.split(",")]
    print(f"DS ghế nhận được từ trang đặt vé: {seat_ids}, suất chiếu {screening}")
    now = datetime.now()
    expired_time = now + timedelta(minutes=5)

    try:
        screening_seats = dao.hold_seats(seat_ids, screening)
        print("DS ghế sẽ giữ chỗ trong 10p: ", screening_seats)
        if not screening_seats:
            return "Không tìm thấy ghế", 404

        for s in screening_seats:
            if s.status == SeatStatus.BOOKED:
                return "Ghế đã được đặt"

            if s.status == SeatStatus.HOLDING and s.hold_expired_at > now:
                return "Ghế đang được giữ"

        for s in screening_seats:
            s.status = SeatStatus.HOLDING
            s.hold_expired_at = expired_time
            s.holding_user_id = current_user.id

        total = 0
        bill = dao.add_bill(customer_id=current_user.id)
        for s in screening_seats:
            price = s.screening.base_price
            total += price
            dao.add_ticket(bill_id=bill.id, ss_id=s.id, price=price)
        bill.total_amount = total

        session.pop("booking_seats", None)
        db.session.commit()

        return redirect(url_for("payment", bill_id=bill.id))

    except Exception as e:
        db.session.rollback()
        print("Lỗi khi đặt vé:", e)
        return redirect('/')

@app.route("/payment/<bill_id>")
@login_required
def payment(bill_id):
    try:
        bill = dao.get_bill_by_id(bill_id)
        txn_ref = f"{bill.id}_{int(time.time())}"
        payment = dao.add_payment(bill_id=bill_id, txn_ref=txn_ref, amount=bill.total_amount)
        payment_url = build_payment_url(amount=payment.amount, txn_ref=txn_ref)
        return redirect(payment_url)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/vnpay_return")
def vnpay_return():
    res_code = request.args.get("vnp_ResponseCode")
    trans_id = request.args.get("vnp_TransactionNo")
    txn_ref = request.args.get("vnp_TxnRef")

    print("Kết quả trả về từ VNPAY")
    print(res_code)
    print(trans_id)
    print(txn_ref)

    payment = Payment.query.filter_by(txn_ref=txn_ref).first()

    if payment.status != PaymentStatus.PENDING:
        return "Đã xử lý trước đó"

    payment.vnp_transaction_id = trans_id
    bill = payment.bill

    if not payment:
        return 404
    if res_code != '00':
        dao.pay_fail(payment, bill)
        return redirect("/fail")

    dao.pay_success(payment, bill)

    return redirect("/")


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

@app.route('/user/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password == confirm:
            customer_id = current_user.id
            try:
                if dao.update_password(customer_id, password):
                    flash('Đổi mật khẩu thành công!', 'success')
                    return redirect(url_for('profile'))
            except ValueError as e:
                flash(str(e), 'warning')
        else:
            flash('Mật khẩu xác nhận không khớp!', 'danger')

    return render_template('user/change_password.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
