from datetime import timedelta, datetime
import time

from alembic.util import status

from app import app, db, login, dao
from flask import render_template, request, redirect, url_for, flash, jsonify, session, get_flashed_messages
from app.decorators import anonymous_required
from flask_login import login_user, current_user, login_required, logout_user
import cloudinary.uploader
import math
import secrets
from app.models import SeatStatus, Payment, PaymentStatus, Movie, TicketStatus
from app.vnpay import build_payment_url


def register_app(app):
    @app.route("/")
    def index():

        keyword = request.args.get('kw','')
        type_id = request.args.get('type_id')
        page = request.args.get('page', 1, type=int)
        page_size = 8
        products = dao.get_movies(keyword=keyword, type_id=type_id)
        all_movies = dao.get_movies()
        total_movies = dao.count_movies()
        pages = math.ceil(total_movies / page_size)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_movies = all_movies[start:end]
        ranking_movies = sorted(all_movies, key=lambda x: x.get('ticket_count', 0), reverse=True)[:5]

        movie_types = dao.get_all_genres()

        return render_template('index.html',
                               products=products,
                               ranking_movies=ranking_movies,
                               pages=pages,
                               all_movies=paginated_movies,
                               current_page=page,
                               keyword=keyword,
                               movie_types=movie_types)

    @app.route("/register", methods=['GET', 'POST'])
    def register():
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
                flash("Mật khẩu không khớp!!","danger")
                return render_template('register.html', data=data)

            if avatar:
                res = cloudinary.uploader.upload(avatar)
                avatar_url = res.get('secure_url')
            try:
                dao.add_user(
                    username=username, password=password, full_name=full_name,
                    phone=phone, email=email, birthday=birthday, avatar=avatar_url
                )
                flash("Đăng ký thành công!!!", "success")
                return redirect(url_for('login_my_user'))
            except ValueError as v:
                flash(str(v), "danger")
            except Exception as ex:
                db.session.rollback()
                flash("Hệ thống đang lỗi, vui lòng thử lại sau!", "danger")
        return render_template('register.html', data=data)

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

    @app.route("/booking/<int:movie_id>", methods=['GET'])
    def booking(movie_id):
        movie = dao.get_movie_by_id(movie_id)
        if not movie:
            flash("Phim không tồn tại hoặc đã bị gỡ bỏ!", "fail")
            return redirect(url_for('index'))

        view = dao.ticket_count_by_movie_id(movie_id)
        movie_types = dao.get_movie_types(movie_id)
        room_types = dao.get_room_types()

        return render_template('booking.html',
            movie=movie, movie_types=movie_types, room_types=room_types, view=view)

    @app.route("/api/get-rooms/<int:room_type_id>", methods=['GET'])
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
        if not watch_date or not room_id or not movie_id:
            jsonify({"success": False, "message": "Thiếu thông tin để tìm suất chiếu!"})

        movie = dao.get_movie_by_id(movie_id)
        screenings = dao.get_movie_screenings(movie_id=movie_id, room_id=room_id, watch_date=watch_date)
        now = datetime.now()
        screenings = [s for s in screenings if s.start_time > now]
        print("DS suất chiếu từ phim đã chọn:", screenings)
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

    @app.route("/api/get-seats/<int:screening_id>", methods=['GET'])
    def get_seats(screening_id):
        print(screening_id)
        seats = dao.get_seats_by_screening(screening_id=screening_id)

        if not seats:
            return jsonify({"success": False, "message": "Không tìm thấy ghế phù hợp!"})

        user_used = 0
        if current_user.is_authenticated:
            user_used = dao.total_seat_per_screening(screening_id, current_user.id)
        remaining = max(0, 8 - user_used)

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
        return jsonify({"success": True, "seats": seats_data, "remaining": remaining})

    @app.route('/booking/submit', methods=['POST'])
    def booking_submit():
        seat_ids = request.form.get("seat")
        screening = request.form.get("screening")
        print("Bắt lỗi submit:")
        print(seat_ids)
        print(screening)

        if not seat_ids or not screening:
            print("Thiếu thông tin ghế hoặc suất chiếu!")
            flash("Hệ thống đang có lỗi, vui lòng thử lại sau ít phút!", "error")
            return redirect(url_for('index'))

        seat_ids = [int(id) for id in seat_ids.split(",")]
        print(f"DS ghế nhận được từ trang đặt vé: {seat_ids}, suất chiếu {screening}")

        now = datetime.now()
        scr = dao.get_screening_by_id(screening)
        if scr.start_time <= now:
            return "Phim đã bắt đầu, không thể đặt vé!"

        if scr.start_time - now < timedelta(minutes=10):
            return "Không thể đặt vé sát giờ chiếu!"

        try:
            screening_seats = dao.hold_seats(seat_ids, screening)
            print("DS ghế sẽ giữ chỗ trong 10p: ", screening_seats)

            if len(screening_seats) != len(seat_ids):
                return "Một số ghế không tồn tại trong suất chiếu này!"

            if dao.total_seat_per_screening(screening, current_user.id) + len(seat_ids) > 8:
                return "Vượt quá số ghế được đặt mỗi suất chiếu!"

            for s in screening_seats:
                if s.status == SeatStatus.BOOKED or (s.status == SeatStatus.HOLDING and s.holding_user_id != current_user.id):
                    return "Ghế đã được đặt!"

                else:
                    s.status = SeatStatus.HOLDING
                    s.hold_expired_at = datetime.now() + timedelta(minutes=10)
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

            txn_ref = f"{bill.id}_{int(time.time())}"
            dao.add_payment(bill_id=bill.id, txn_ref=txn_ref, amount=bill.total_amount)
            payment_url = build_payment_url(amount=bill.total_amount, txn_ref=txn_ref)
            return render_template('redirect_payment.html',
                                   payment_url=payment_url,
                                   bill=bill)

        except Exception as e:
            db.session.rollback()
            print("Lỗi khi đặt vé:", e)
            return redirect('/')

    @app.route("/payment/<int:bill_id>")
    @login_required
    def payment(bill_id):
        try:
            bill = dao.get_bill_by_id(bill_id)
            if not bill:
                return "Hóa đơn không tồn tại", 404
            payment = dao.get_payment_by_bill_id(bill_id)

            if not payment:
                txn_ref = f"{bill.id}_{int(time.time())}"
                payment = dao.add_payment(bill_id=bill_id, txn_ref=txn_ref, amount=bill.total_amount)
            else:
                txn_ref = payment.txn_ref

            payment_url = build_payment_url(amount=bill.total_amount, txn_ref=txn_ref)
            return redirect(payment_url)

        except Exception as e:
            print(f"Lỗi thanh toán: {e}")
            return redirect(url_for('index'))

    @app.route("/vnpay_return")
    def vnpay_return():
        res_code = request.args.get("vnp_ResponseCode")
        trans_id = request.args.get("vnp_TransactionNo")
        txn_ref = request.args.get("vnp_TxnRef")
        msg=None
        success = False

        print("Kết quả trả về từ VNPAY")
        print(res_code)
        print(trans_id)
        print(txn_ref)

        payment = Payment.query.filter_by(txn_ref=txn_ref).first()
        if not payment:
            return "Không tìm thấy thông tin thanh toán!"
        if payment.status != PaymentStatus.PENDING:
            return "Đã xử lý trước đó"

        payment.vnp_transaction_id = trans_id
        bill = payment.bill

        for ticket in bill.tickets:
            seat = ticket.screening_seat
            if seat.status != SeatStatus.HOLDING:
                dao.pay_fail(payment, bill)
                msg = 'Ghế đã bị huỷ trong khi thanh toán!'
                return redirect(url_for('payment_return', txn_ref=txn_ref, amount=payment.amount, msg=msg))
            if seat.hold_expired_at < datetime.now():
                dao.pay_fail(payment, bill)
                msg = "Ghế đã hết hạn! Vui lòng đặt mới và thanh toán trong thời gian quy định!"
                return redirect(url_for('payment_return', txn_ref=txn_ref, amount=payment.amount, msg=msg))
        if res_code != '00':
            dao.pay_fail(payment, bill)
            msg = 'Thanh toán thất bại!'
            return redirect(url_for('payment_return', txn_ref=txn_ref, amount=payment.amount, msg=msg))

        dao.pay_success(payment, bill)
        msg = 'Thanh toán thành công!'
        success = True
        return redirect(url_for('payment_return', txn_ref=txn_ref, amount=payment.amount, msg=msg, success=success))

    @app.route("/payment-return")
    def payment_return():
        txn_ref = request.args.get('txn_ref')
        amount = request.args.get('amount')
        amount = int(amount)
        msg = request.args.get('msg')
        success = request.args.get('success')
        return render_template("return_payment.html", txn_ref=txn_ref, amount=amount, msg=msg, success=success)


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
        data = dao.get_all_info_movie(current_user.id)
        return render_template('user/history_booking.html', bookings=data)

    @app.route("/user/history_watched")
    @login_required
    def history_watched():
        data = dao.get_info_movie(current_user.id, TicketStatus.USED)
        return render_template('user/history_watched.html', ticket_list=data)

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

    @app.route('/user/change_profile', methods=['GET', 'POST'])
    @login_required
    def change_profile():
        user = current_user

        if request.method == "POST":
            has_changed = False
            data = request.form

            # 1. Kiểm tra thay đổi văn bản
            if data.get("full_name") and user.full_name != data.get("full_name"):
                user.full_name = data.get("full_name")
                has_changed = True

            if data.get("birthday") and str(user.birthday) != data.get("birthday"):
                user.birthday = data.get("birthday")
                has_changed = True

            if data.get("email") and user.email != data.get("email"):
                user.email = data.get("email")
                has_changed = True

            if data.get("phone") and user.phone_number != data.get("phone"):
                user.phone_number = data.get("phone")
                has_changed = True

            # 2. Kiểm tra thay đổi ảnh đại diện
            avatar_file = request.files.get("avatar")
            if avatar_file and avatar_file.filename:
                try:
                    res = cloudinary.uploader.upload(avatar_file)
                    user.avatar = res['secure_url']
                    has_changed = True
                except Exception as e:
                    flash("Lỗi khi tải ảnh lên Cloudinary!", "danger")
                    return render_template("user/change_profile.html", customer=user)

            # 3. Thực thi lưu vào Database
            if has_changed:
                try:
                    db.session.commit()
                    flash("Cập nhật thông tin thành công!", "success")
                    # Dùng redirect để chuyển hướng hẳn sang trang profile
                    return redirect(url_for('profile'))
                except Exception as ex:
                    db.session.rollback()
                    flash("Lỗi hệ thống khi lưu dữ liệu!", "danger")
            else:
                flash("Bạn chưa thay đổi thông tin nào.", "warning")

        # Trường hợp GET hoặc POST nhưng không có thay đổi/bị lỗi
        return render_template("user/change_profile.html", customer=user)

    @app.route("/user/cancel-ticket/<int:ticket_id>", methods=['POST'])
    @login_required
    def cancel_ticket_route(ticket_id):
        try:
            dao.cancel_ticket(ticket_id, current_user.id)
            flash("Hủy vé thành công! Ghế đã được giải phóng.", "success")

        except Exception as e:
            flash(str(e), "danger")

        return redirect(url_for('history_booking_ticket'))

if __name__ == "__main__":
    from app import admin
    register_app(app=app)
    app.run(debug=True)
