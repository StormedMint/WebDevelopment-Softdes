document.addEventListener("DOMContentLoaded", function () {
            const roomCards = document.querySelectorAll(".room-card");

            roomCards.forEach(card => {
                const currentText = card.querySelector(".current-count")?.textContent.trim();
                const maxText = card.querySelector(".max-count")?.textContent.trim();

                const current = Number(currentText);
                const max = Number(maxText);

                if (!max || isNaN(current) || isNaN(max)) {
                    return;
                }

                const percentage = (current / max) * 100;

                card.classList.remove("low-capacity", "moderate-capacity", "full-capacity");

                if (percentage >= 100) {
                    card.classList.add("full-capacity");
                } 
                else if (percentage >= 75) {
                    card.classList.add("moderate-capacity");
                } 
                else {
                    card.classList.add("low-capacity");
                }
            });
        });

document.addEventListener("DOMContentLoaded", function () {
    const roomCards = document.querySelectorAll(".room-card");
    const selectedAreaInput = document.getElementById("selectedAreaInput");
    const roomSelectForm = document.getElementById("roomSelectForm");

    const allowedRooms = [
        "Reading Area",
        "Internet Section",
        "Lounge Area",
        "Faculty Room",
        "Graduate Reading Area",
        "Undergraduate Reading Area"
    ];

    let selectedRoom = "";

    roomCards.forEach(card => {
        const area = card.dataset.area;

        const currentText = card.querySelector(".current-count")?.textContent.trim();
        const maxText = card.querySelector(".max-count")?.textContent.trim();

        const current = Number(currentText);
        const max = Number(maxText);

        if (!max || isNaN(current) || isNaN(max)) {
            return;
        }

        const percentage = (current / max) * 100;

        card.classList.remove("low-capacity", "moderate-capacity", "full-capacity");

        if (percentage >= 100) {
            card.classList.add("full-capacity");
        } 
        else if (percentage >= 75) {
            card.classList.add("moderate-capacity");
        } 
        else {
            card.classList.add("low-capacity");
        }

        if (current >= max) {
            card.classList.add("disabled-room");
        }

        card.addEventListener("click", function () {
            const isAllowed = allowedRooms.includes(area);
            const isFull = current >= max;

            if (!isAllowed) {
                alert("This is a Reservation Room, Ask for a Reservation Form");
                return;
            }

            if (isFull) {
                alert("This room is already full.");
                return;
            }

            roomCards.forEach(otherCard => {
                otherCard.classList.remove("selected-room");
            });

            card.classList.add("selected-room");
            selectedRoom = area;
            selectedAreaInput.value = area;
        });
    });

    roomSelectForm.addEventListener("submit", function (event) {
        if (!selectedRoom) {
            event.preventDefault();
            alert("Please select one available room first.");
            return;
        }
    });
});

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