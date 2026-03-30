
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
const selectDate = document.getElementById('selected-date')

dateWrapper.addEventListener('click', function (e) {
    const dateCard = e.target.closest('.date-card');
    if (!dateCard) return;

    document.querySelector('.date-card.active')?.classList.remove('active');
    dateCard.classList.add('active');
    selectDate.value = dateCard.dataset.date;

    roomTypesContainer.querySelector('.room-type.active')?.classList.remove('active');
    selectRoom.value = '';

    console.info("Ngày đã chọn:", selectDate.value);
});
///// END DATE SWIPER

const roomTypesContainer = document.querySelector('.room-types');
const selectRoomType = document.getElementById('selected-room-type')
const roomsContainer = document.querySelector('.rooms');
const selectRoom = document.getElementById('selected-room')

roomTypesContainer.addEventListener('click', function(e) {
    const room_type = e.target.closest('.room-type');
    if (!room_type) return;

    roomTypesContainer.querySelector('.room-type.active')?.classList.remove('active');
    room_type.classList.add('active');
    selectRoomType.value = room_type.dataset.type;
    console.info("Loại phòng đã chọn:", selectRoomType.value);

    fetch(`/api/get-rooms/${selectRoomType.value}`, {
        method: 'get'
    }).then(res => res.json()).then(data => {
        if (data.success) {
            roomsContainer.innerHTML = ''
            if (data.rooms.length <= 0)
                roomsContainer.innerHTML =
                `<p class="text-info">Hiện chưa có phòng phù hợp!</p>`
            else {
                data.rooms.forEach(item => {
                    roomsContainer.innerHTML += `
                    <div class="room d-type" data-room="${item.id}">${item.number}</div>`
                })
            }
        }
    })
});
///// END ROOM TYPE PICK

const screeningsContainer = document.querySelector('.screenings')

roomsContainer.addEventListener('click', function(e) {
    const room = e.target.closest('.room');
    if (!room) return;

    roomsContainer.querySelector('.room.active')?.classList.remove('active');
    room.classList.add('active');
    selectRoom.value = room.dataset.room;
    console.info("Phòng đã chọn:", selectRoom.value);

    fetch(`/api/get-screenings?movie_id=1&room_id=${selectRoom.value}&watch_date=${selectDate.value}`, {
        method: 'get'
    }).then(res => res.json()).then(data => {
        console.info(data)
        if (data.success) {
            screeningsContainer.innerHTML = ''
            if (data.screenings.length <= 0)
                screeningsContainer.innerHTML =
                `<p class="text-info">Hiện chưa có suất chiếu phù hợp!</p>`
            else {
                data.screenings.forEach(item => {
                    screeningsContainer.innerHTML += `
                    <div class="screening d-type" data-screening="${item.id}">
                        <div class="time">${item.start_time} ~ ${item.end_time}</div>
                        <div class="price">(${item.base_price.toLocaleString()}đ)</div>
                    </div>`
                })
            }
        }
    })
});
/////END ROOM PICK

const selectScreening = document.getElementById('selected-screening')
const seatsContainer = document.getElementById('seat-map');

screeningsContainer.addEventListener('click', function(e) {
    const screening = e.target.closest('.screening');
    if (!screening) return;

    screeningsContainer.querySelector('.screening.active')?.classList.remove('active');
    screening.classList.add('active');
    selectScreening.value = screening.dataset.screening;
    console.info("Suất chiếu đã chọn:", selectScreening.value);

    fetch(`/api/get-seats/${selectScreening.value}`, {
        method: 'get'
    }).then(res => res.json()).then(data => {
        console.info(data)
        if (data.success) {
            seatsContainer.innerHTML = ''
            if (data.seats.length <= 0)
                seatsContainer.innerHTML =
                `<p class="text-info">Hiện chưa có ghế phù hợp!</p>`
            else {
                for (let row in data.seats) {
                    let rowContainer = `<div class='seat-row'>Hàng ${row}`;
                    data.seats[row].forEach(seat => {
                        rowContainer += `
                            <div class='seat ${seat.status}' data-seat="${seat.id}">
                                ${seat.number}
                            </div>`;
                    });
                    rowContainer += `</div>`;
                    seatsContainer.innerHTML += rowContainer;
                }
            }
        }
    })
});
/////END SCREENING PICK

const selectSeat = document.getElementById('selected-seat')

seatsContainer.addEventListener('click', function(e) {
    const seat = e.target.closest('.seat');
    if (!seat) return;
    const seatCount = document.querySelectorAll('.seat.selected').length;
    if (seatCount >= 8) {
        alert("Bạn chỉ được chọn tối đa 8 ghế!");
        return;
    }

    if (seat.classList.contains('seat')) {
        seat.classList.toggle('selected');
    }
    selectSeat.value = seat.dataset.seat;
    console.info("Ghế đã đã chọn:", selectSeat.value);

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
    selectDate.value = document.querySelector('.date-card.active').dataset.date;
    console.info("Ngày đã chọn:", selectDate.value);
});