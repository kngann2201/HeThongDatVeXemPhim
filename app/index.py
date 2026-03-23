from app import app, db, login
from flask import render_template, request, redirect, url_for, flash
from app.decorators import anonymous_required
from flask_login import login_user, current_user, login_required, logout_user
import re
import dao
import cloudinary

@app.route("/")
def index():
    return render_template('index.html')

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

        if not re.match(r'^(0)(3|5|7|8|9)\d{8}$', phone):
            err_msg = "Số điện thoại không hợp lệ, phải gồm 10 kí tự. VD: 0123456789"
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
                    email=email )
            return render_template("register.html", success=True)
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
    return dao.get_user_by_id(user_id)

@login.unauthorized_handler
def unauthorized_callback():
    flash("Bạn cần đăng nhập để tiếp tục!", "warning")
    return redirect('/login?next=' + request.path)

@app.route("/logout")
def logout_my_user():
    logout_user()
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
