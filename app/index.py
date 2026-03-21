from app import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_mail import Message
import re
import dao
import cloudinary

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/booking", methods=['POST', 'GET'])
def booking():
    movie_id = 1
    err_msg = None
    room_types = dao.get_room_types()
    seats = dao.get_seats()
    return render_template('booking.html', movie_id=movie_id,
                           seats=seats, err_msg=err_msg, room_types=room_types)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
