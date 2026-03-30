from datetime import timedelta
from app import app, db
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Message
import re
import dao
import cloudinary

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/booking", methods=['GET', 'POST'])
def booking():
    movie_id = 1
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

@app.route("/api/pay", methods=['POST'])
def pay():
    pass


if __name__ == "__main__":
    app.run(debug=True, port=5000)
