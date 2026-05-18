fetch("/get_capacity_data")

function updateCapacityColor(card, current, capacity) {
    card.classList.remove("low-capacity", "moderate-capacity", "full-capacity");

    if (capacity <= 0) {
        card.classList.add("low-capacity");
        return;
    }

    const percent = (current / capacity) * 100;

    if (percent >= 100) {
        card.classList.add("full-capacity");
    } 
    else if (percent >= 75) {
        card.classList.add("moderate-capacity");
    } 
    else {
        card.classList.add("low-capacity");
    }
}

function updateCapacityData() {
    fetch(capacityDataUrl)
        .then(response => response.json())
        .then(data => {
            data.rooms.forEach(room => {
                const card = document.querySelector(`.room-card[data-area="${room.area}"]`);

                if (!card) {
                    return;
                }

                const currentSpan = card.querySelector(".current-count");
                const maxSpan = card.querySelector(".max-count");

                if (currentSpan) {
                    currentSpan.textContent = room.current;
                }

                if (maxSpan) {
                    maxSpan.textContent = room.capacity;
                }

                updateCapacityColor(card, Number(room.current), Number(room.capacity));
            });
        })
        .catch(error => {
            console.error("Error updating capacity data:", error);
        });
}

document.addEventListener("DOMContentLoaded", () => {
    updateCapacityData();
    setInterval(updateCapacityData, 2000);
});