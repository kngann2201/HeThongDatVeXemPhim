const state = {
    movieId: MOVIE_ID,
    date: null,
    roomTypeId: null,
    roomId: null,
    screeningId: null,
    seats: [],
    total: 0,
    price: 0,

    rooms: [],
    screenings: [],
    seatMap: {}
};

const roomTypesContainer = document.querySelector('.room-types');
const roomsContainer = document.querySelector('.rooms');
const screeningsContainer = document.querySelector('.screenings');
const seatsContainer = document.getElementById('seat-map');
const totalPrice = document.getElementById("total-price");


function renderRooms() {
    roomsContainer.innerHTML = '';

    if (!state.roomTypeId) {
        roomsContainer.innerHTML = `<p class="text-info">Chọn loại phòng để hiện thông tin này</p>`;
        return;
    }
    if (state.rooms.length === 0) {
        roomsContainer.innerHTML = `<p class="text-info">Hiện chưa có phòng phù hợp!</p>`;
        return;
    }
    state.rooms.forEach(r => {
        roomsContainer.innerHTML += `
            <div class="room d-type ${state.roomId == r.id ? 'active' : ''}" data-room="${r.id}">
                ${r.number}
            </div>`;
    });
}

function renderScreenings() {
    screeningsContainer.innerHTML = '';
    if (!state.roomId) {
        screeningsContainer.innerHTML = `<p class="text-info">Chọn phòng để xem suất chiếu</p>`;
        return;
    }
    if (state.screenings.length === 0) {
        screeningsContainer.innerHTML = `<p class="text-info">Hiện chưa có suất chiếu phù hợp!</p>`;
        return;
    }
    state.screenings.forEach(item => {
        screeningsContainer.innerHTML += `
        <div class="screening d-type ${state.screeningId == item.id ? 'active' : ''}" data-screening="${item.id}">
            <div class="time">${item.start_time} ~ ${item.end_time}</div>
            <div class="price">(${item.base_price.toLocaleString()}đ/vé)</div>
        </div>`;
    });
}
function renderSeats() {
    seatsContainer.innerHTML = '';
    if (!state.screeningId) {
        seatsContainer.innerHTML = `<p class="text-info">Chọn suất chiếu để xem sơ đồ ghế!</p>`;
        return;
    }

    for (let row in state.seatMap) {
        let rowHtml = `<div class='seat-row'>Hàng ${row}`;
        state.seatMap[row].forEach(seat => {
            const selected = state.seats.includes(String(seat.id));

            rowHtml += `
                <div class="seat ${seat.status} ${selected ? 'selected' : ''}"
                     data-seat="${seat.id}">
                    ${seat.number}
                </div>`;
        });

        rowHtml += `</div>`;
        seatsContainer.innerHTML += rowHtml;
    }
}
function updatePrice() {
    state.total = state.price*state.seats.length;
    if (state.total > 0) {
        totalPrice.innerHTML = `<h5 class="mb-3 px-2 text-success">Tổng tiền vé ước tính : ${state.total.toLocaleString()}đ</h5>`
    }
}

function render() {
    renderRooms();
    renderScreenings();
    renderSeats();
}
/////END STATE AND RENDER TEMPLATE


function getDayName(date, isToday) {
    if (isToday) return "Hôm nay";
    const days = ["CN", "Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7"];
    return days[date.getDay()];
}
var swiper = new Swiper(".mySwiper", {
    slidesPerView: "auto",
    spaceBetween: 15
});

const dateWrapper = document.getElementById('date-wrapper');
dateWrapper.addEventListener('click', function (e) {
    const dateCard = e.target.closest('.date-card');
    if (!dateCard) return;

    document.querySelector('.date-card.active')?.classList.remove('active');
    dateCard.classList.add('active');
    console.info("Ngày đã chọn:", dateCard.dataset.date);

    state.date = dateCard.dataset.date;
    state.roomTypeId = null;
    state.roomId = null;
    state.screeningId = null;
    state.seats = [];

    state.rooms = [];
    state.screenings = [];
    state.seatMap = {};

    render();
});
///// END DATE SWIPER


roomTypesContainer.addEventListener('click', function(e) {
    const room_type = e.target.closest('.room-type');
    if (!room_type) return;

    roomTypesContainer.querySelector('.room-type.active')?.classList.remove('active');
    room_type.classList.add('active');
    state.roomTypeId = room_type.dataset.type;

    state.roomId = null;
    state.screeningId = null;
    state.seats = [];
    state.screenings = [];
    state.seatMap = {};

    fetch(`/api/get-rooms/${state.roomTypeId}`, {
        method: 'get'
    }).then(res => res.json()).then(data => {
        console.info(data)
        if (data.success) {
            state.rooms = data.rooms;
            render();
        }
    })
});
///// END ROOM TYPE PICK AND RENDER ROOMS

roomsContainer.addEventListener('click', function(e) {
    const room = e.target.closest('.room');
    if (!room) return;

    console.info("Phòng đã chọn:", room.dataset.room);
    state.roomId = room.dataset.room;

    fetch(`/api/get-screenings?movie_id=${state.movieId}&room_id=${state.roomId}&watch_date=${state.date}`, {
        method: 'get'
    }).then(res => res.json()).then(data => {
        console.info(data)
        if (data.success) {
            state.screenings = data.screenings;
            render();
        }
    })
});
/////END ROOM PICK AND RENDER SCREENINGS


screeningsContainer.addEventListener('click', function(e) {
    const screening = e.target.closest('.screening');
    if (!screening) return;

    console.info("Suất chiếu đã chọn:", screening.dataset.screening);
    state.screeningId = screening.dataset.screening;
    document.getElementById("selected-screening").value = state.screeningId;

    const selected = state.screenings.find(s => s.id == state.screeningId);
    state.price = selected.base_price;
    console.info("Giá vé đã chọn:", state.price)

    fetch(`/api/get-seats/${state.screeningId}`, {
        method: 'get'
    }).then(res => res.json()).then(data => {
        console.info(data)
        if (data.success) {
            state.seatMap = data.seats;
            render();
        }
    })
});
/////END SCREENING PICK AND RENDER SEATMAP


seatsContainer.addEventListener('click', function(e) {
    const seat = e.target.closest('.seat');
    if (!seat) return;

    if (seat.classList.contains('BOOKED') || seat.classList.contains('HOLDING')) {
        return;
    }

    const seat_id = seat.dataset.seat;
    if (state.seats.includes(seat_id)) {
        state.seats = state.seats.filter(s => s !== seat_id);
    } else {
        if (state.seats.length >= 8) {
            alert("Bạn chỉ được chọn tối đa 8 ghế!");
            return;
        }
        state.seats.push(seat_id);
    }

    console.info("Các ghế đã đã chọn:", state.seats);
    document.getElementById("selected-seat").value = state.seats.join(",");

    render();
    updatePrice();

});
/////END SEAT PICK

document.addEventListener('DOMContentLoaded', () => {
    for (let i = 0; i < 14; i++) {
        const d = new Date();
        d.setDate(d.getDate() + i);
        const day = d.getDate();
        const month = d.getMonth() + 1;
        const formattedDay = `${day}/${month}`;

        const slide = `
            <div class="swiper-slide d-flex" style="width: auto;">
                <div class="date-card ${i === 0 ? 'active' : ''}" data-date="${d.toISOString().split('T')[0]}">
                    <div class="day-num">${formattedDay}</div>
                    <div class="day-name">${getDayName(d, i === 0)}</div>
                </div>
            </div>
        `;

        dateWrapper.innerHTML += slide;
    }
    state.date = document.querySelector('.date-card.active').dataset.date;
    console.info("Ngày đã chọn:", state.date);
});

document.querySelector("form").addEventListener("submit", function(e) {
    if (!state.screeningId) {
        alert("Vui lòng chọn suất chiếu!");
        e.preventDefault();
        return;
    }

    if (state.seats.length === 0) {
        alert("Vui lòng chọn ít nhất 1 ghế!");
        e.preventDefault();
        return;
    }
});