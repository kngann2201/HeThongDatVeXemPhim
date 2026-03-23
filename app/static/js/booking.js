const apiResponse = [
        { id: 1, row: "A", number: 1, status: "AVAILABLE" },
        { id: 2, row: "A", number: 2, status: "BOOKED" },
        { id: 3, row: "A", number: 3, status: "AVAILABLE" },
        { id: 4, row: "B", number: 1, status: "AVAILABLE" },
        { id: 6, row: "B", number: 3, status: "AVAILABLE" }
    ];

function renderSeats(data) {
    const seatMap = document.getElementById('seat-map');
    if (!seatMap) return;

    seatMap.innerHTML = '';

    const rows = data.reduce((acc, seat) => {
        if (!acc[seat.row]) acc[seat.row] = [];
        acc[seat.row].push(seat);
        return acc;
    }, {});

    Object.keys(rows).sort().forEach(rowName => {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'seat-row';

        const label = document.createElement('div');
        label.className = 'row-label';
        label.innerText = rowName;
        rowDiv.appendChild(label);

        rows[rowName].sort((a, b) => a.number - b.number).forEach(seat => {
            const seatDiv = document.createElement('div');
            seatDiv.className = `seat ${seat.status}`;
            seatDiv.dataset.id = seat.id;

            if (seat.status === "AVAILABLE") {
                seatDiv.onclick = () => {
                    const selectedCount = document.querySelectorAll('.seat.selected').length;
                    if (!seatDiv.classList.contains('selected') && selectedCount >= 8) {
                        alert("Bạn chỉ được chọn tối đa 8 ghế!");
                        return;
                    }
                    seatDiv.classList.toggle('selected');
                };
            }
            rowDiv.appendChild(seatDiv);
        });
        seatMap.appendChild(rowDiv);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    renderSeats(apiResponse);
});