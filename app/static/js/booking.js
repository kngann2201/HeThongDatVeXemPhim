const selected_info = {
    movieId: MOVIE_ID, date: null, roomTypeId: null, roomId: null,
    screeningId: null, startTime: null, seats: [], price: 0,
    remaining: 8, rooms: [], screenings: [], seatMap: {}
};

var swiper = new Swiper(".mySwiper", {
    slidesPerView: "auto",
    spaceBetween: 15
});

const $ = (id) => document.getElementById(id);

const hideAllFrom = (step) => {
    const steps = ['menu-rooms', 'menu-screenings', 'menu-seats', 'btn-submit'];
    let start = false;
    steps.forEach(s => { if(s === step) start = true; if(start) $(s)?.classList.add('d-none'); });
};

const resetStateFrom = (step) => {
    const steps = ['roomType', 'room', 'screening'];
    let start = false;

    steps.forEach(s => {
        if (s === step) start = true;
        if (!start) return;

        switch (s) {
            case 'roomType':
                selected_info.roomTypeId = null;
                document.querySelectorAll('.room-type.active')
                    .forEach(e => e.classList.remove('active'));
                break;

            case 'room':
                selected_info.roomId = null;
                document.querySelectorAll('.room.active')
                    .forEach(e => e.classList.remove('active'));
                break;

            case 'screening':
                selected_info.screeningId = null;
                selected_info.startTime = null;
                $('selected-screening').value = '';
                document.querySelectorAll('.screening.active')
                    .forEach(e => e.classList.remove('active'));
                break;
        }
    });
};

function resetBookingState() {
    selected_info.seats = [];
    selected_info.price = 0;
    $('selected-seat').value = "";
    $('btn-submit').classList.add('d-none');
    $('total-price').innerHTML = "";
}

const saveState = () => {
    localStorage.setItem('pending_booking', JSON.stringify({
        date: selected_info.date,
        roomTypeId: selected_info.roomTypeId,
        roomId: selected_info.roomId,
        screeningId: selected_info.screeningId
    }));
};

async function restoreState() {
    const saved = localStorage.getItem('pending_booking');
    if (!saved) return;
    const data = JSON.parse(saved);

    if (data.date) {
        selected_info.date = data.date;
        document.querySelector('.date-card.active')?.classList.remove('active');
        document.querySelector(`.date-card[data-date="${data.date}"]`)?.classList.add('active');
    }
    if (data.roomTypeId) {
        selected_info.roomTypeId = data.roomTypeId;
        await loadRooms(data.roomTypeId);
        document.querySelector(`.room-type[data-type="${data.roomTypeId}"]`)?.classList.add('active');
    }
    if (data.roomId) {
        selected_info.roomId = data.roomId;
        await loadScreenings();
        document.querySelector(`.room[data-room="${data.roomId}"]`)?.classList.add('active');
    }
    if (data.screeningId) {
        selected_info.screeningId = data.screeningId;
        await loadSeats(data.screeningId);
        document.querySelector(`.screening[data-screening="${data.screeningId}"]`)?.classList.add('active');
        const s = selected_info.screenings.find(i => i.id == data.screeningId);
        if (s) selected_info.price = s.base_price;
    }
    localStorage.removeItem('pending_booking');
}

async function loadRooms(typeId) {
    const res = await fetch(`/api/get-rooms/${typeId}`).then(r => r.json());
    if (res.success) {
        selected_info.rooms = res.rooms;
        $('menu-rooms').classList.remove('d-none');
        renderRooms();
    }
}

async function loadScreenings() {
    const {movieId, roomId, date} = selected_info;
    const res = await fetch(`/api/get-screenings?movie_id=${movieId}&room_id=${roomId}&watch_date=${date}`).then(r => r.json());
    if (res.success) {
        selected_info.screenings = res.screenings;
        $('menu-screenings').classList.remove('d-none');
        renderScreenings();
    }
}

async function loadSeats(screeningId) {
    const res = await fetch(`/api/get-seats/${screeningId}`).then(r => r.json());
    console.log("API RESPONSE:", res);
    if (res.success) {
        $('menu-seats').classList.remove('d-none');
        if (res.remaining <= 0) {
            $('menu-seats').classList.remove('d-none');
            $('seat-map').innerHTML = `
                <p class="text-danger text-center">
                    Bạn đã đạt giới hạn 8 ghế cho suất chiếu này
                </p>`;
//            $('btn-submit').classList.add('d-none');
            return;
        }
        selected_info.remaining = res.remaining;

        selected_info.seatMap = res.seats;
        const available = Object.values(res.seats).some(row =>
            row.some(seat => seat.status === "AVAILABLE")
        );

        if (!available) {
            $('seat-map').innerHTML = `<p class="text-danger">Suất chiếu này đã hết ghế!</p>`;
//            $('btn-submit').classList.add('d-none');
            return;
        }
        renderSeats();
//
//        const wrapper = document.querySelector('.seat-map-wrapper');
//        const overlay = $('login-overlay');
//        if (!IS_AUTHENTICATED) {
//            wrapper.classList.add('locked');
//            overlay.classList.remove('d-none');
//        } else {
//            wrapper.classList.remove('locked');
//            overlay.classList.add('d-none');
//        }
    }
}

function renderRooms() {
    const container = document.querySelector('.rooms');
    container.innerHTML = selected_info.rooms.map(r => `
        <div class="room d-type ${selected_info.roomId == r.id ? 'active' : ''}" data-room="${r.id}">${r.number}</div>
    `).join('') || '<p class="text-danger">Hiện không có phòng phù hợp!</p>';
}

function renderScreenings() {
    const container = document.querySelector('.screenings');
    container.innerHTML = selected_info.screenings.map(s => `
        <div class="screening d-type ${selected_info.screeningId == s.id ? 'active' : ''}" data-screening="${s.id}" data-start="${s.start_time}">
            <div class="time">${s.start_time} ~ ${s.end_time}</div>
            <div class="price">(${s.base_price.toLocaleString()}đ)</div>
        </div>
    `).join('') || '<p class="text-danger">Hiện không có suất chiếu phù hợp!</p>';
}

function renderSeats() {
    let html = '';
    for (let row in selected_info.seatMap) {
        html += `<div class='seat-row'>Hàng ${row}` + selected_info.seatMap[row].map(seat => `
            <div class="seat ${seat.status} ${selected_info.seats.includes(String(seat.id)) ? 'selected' : ''}" data-seat="${seat.id}">${seat.number}</div>
        `).join('') + `</div>`;
    }
    $('seat-map').innerHTML = html;
}

function updatePrice() {
    const count = selected_info.seats.length;
    const price = selected_info.price;
    const total = count * price;

    if (count > 0) {
        $('total-price').innerHTML = `
            <div class="booking-summary animate__animated animate__fadeIn">
                <div class="summary-item">
                    <span>Số lượng ghế:</span>
                    <strong>${count} ghế</strong>
                </div>
                <div class="summary-item">
                    <span>Giá vé:</span>
                    <strong>${price.toLocaleString()}đ</strong>
                </div>
                <div class="summary-total">
                    <span>TỔNG TIỀN:</span>
                    <span>${total.toLocaleString()}đ</span>
                </div>
            </div>
        `;
    } else {
        $('total-price').innerHTML = '';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const wrapper = $('date-wrapper');
    for (let i = 0; i < 14; i++) {
        const d = new Date(); d.setDate(d.getDate() + i);
        const active = i === 0 ? 'active' : '';
        wrapper.innerHTML += `<div class="swiper-slide" style="width:auto">
            <div class="date-card ${active}" data-date="${d.toISOString().split('T')[0]}">
                <div class="day-num">${d.getDate()}/${d.getMonth()+1}</div>
                <div class="day-name">${i===0 ? "Hôm nay" : ["CN","T2","T3","T4","T5","T6","T7"][d.getDay()]}</div>
            </div>
        </div>`;
    }
    selected_info.date = document.querySelector('.date-card.active').dataset.date;
    restoreState();
});

$('date-wrapper').addEventListener('click', (e) => {
    const card = e.target.closest('.date-card');
    if (!card) return;
    document.querySelector('.date-card.active')?.classList.remove('active');
    card.classList.add('active');
    selected_info.date = card.dataset.date;
    resetStateFrom('roomType');
    hideAllFrom('menu-rooms');
    selected_info.roomTypeId = null;
});

document.querySelector('.room-types').addEventListener('click', (e) => {
    const btn = e.target.closest('.room-type');
    if (!btn) return;
    document.querySelector('.room-type.active')?.classList.remove('active');
    resetStateFrom('room');
    btn.classList.add('active');
    selected_info.roomTypeId = btn.dataset.type;
    hideAllFrom('menu-rooms');
    loadRooms(selected_info.roomTypeId);
    console.log(selected_info);
});

document.querySelector('.rooms').addEventListener('click', (e) => {
    const btn = e.target.closest('.room');
    if (!btn) return;
    resetStateFrom('screening');
    btn.classList.add('active');
    selected_info.roomId = btn.dataset.room;
    hideAllFrom('menu-screenings');
    loadScreenings();
});

document.querySelector('.screenings').addEventListener('click', (e) => {
    const btn = e.target.closest('.screening');
    if (!btn) return;
    resetStateFrom('seat');
    btn.classList.add('active');
    selected_info.screeningId = btn.dataset.screening;
    selected_info.startTime = btn.dataset.start;
    $('selected-screening').value = selected_info.screeningId;
    const s = selected_info.screenings.find(i => i.id == selected_info.screeningId);
    selected_info.price = s.base_price;

    if (!IS_AUTHENTICATED) {
        $('menu-seats').classList.remove('d-none');
        $('seat-map').innerHTML = `<div style="height:200px"></div>`;
        $('login-overlay').classList.remove('d-none');
        document.querySelector('.seat-map-wrapper').classList.add('locked');
        $('overlay-login-btn').href = `/login?next=${window.location.pathname}`;
    } else {
        $('login-overlay').classList.add('d-none');
        document.querySelector('.seat-map-wrapper').classList.remove('locked');
        loadSeats(selected_info.screeningId);
    }
});

$('seat-map').addEventListener('click', (e) => {
    const seat = e.target.closest('.seat');
    document.getElementById('btn-submit').classList.remove('d-none');
    if (!seat || seat.classList.contains('BOOKED') || seat.classList.contains('HOLDING')) return;

    const id = seat.dataset.seat;
    if (selected_info.seats.includes(id)) {
        selected_info.seats = selected_info.seats.filter(s => s !== id);
    } else {
        if (selected_info.seats.length >= selected_info.remaining) return alert("Bạn đã đạt giới hạn đặt ghế ở suất chiếu này!");
        selected_info.seats.push(id);
    }

    $('selected-seat').value = selected_info.seats.join(",");
    $('btn-submit').classList.toggle('d-none', selected_info.seats.length === 0);
    renderSeats();

    const total = selected_info.price * selected_info.seats.length;
    updatePrice()
});

$('overlay-login-btn').addEventListener('click', saveState);

$('btn-submit').addEventListener('click', (e) => {
    const now = new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit', hour12:false});
    const screeningDateTime = new Date(
        `${selected_info.date}T${selected_info.startTime}:00`
    );
    if (screeningDateTime <= now) {
        e.preventDefault();
        return alert("Suất chiếu đã bắt đầu!");
    }
    localStorage.removeItem('pending_booking');
});