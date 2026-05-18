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

    // Updates room color depending on capacity percentage
    function updateCapacityColor(card, current, capacity) {
        card.classList.remove("low-capacity", "moderate-capacity", "full-capacity");

        if (capacity <= 0) {
            card.classList.add("low-capacity");
            return;
        }

        const percentage = (current / capacity) * 100;

        if (percentage >= 100) {
            card.classList.add("full-capacity");
        }
        else if (percentage >= 75) {
            card.classList.add("moderate-capacity");
        }
        else {
            card.classList.add("low-capacity");
        }
    }

    // nilolock room if full na tas unlock pag may bawas
    function updateRoomLockStatus(card, current, capacity) {
        if (current >= capacity) {

            // disables room kasi full
            card.classList.add("disabled-room");

            // makes yung room di pwede click if bigla full
            if (card.classList.contains("selected-room")) {
                card.classList.remove("selected-room");
                selectedRoom = "";
                selectedAreaInput.value = "";
            }
        }
        else {

            // pag nabawas na clickable na ulit yun room
            card.classList.remove("disabled-room");
        }
    }

    // gets new value ng current then update gui
    function getCardCurrent(card) {
        return Number(card.querySelector(".current-count")?.textContent.trim());
    }

    // Gets the latest max capacity 
    function getCardCapacity(card) {
        return Number(card.querySelector(".max-count")?.textContent.trim());
    }

    // refresh every 2 sec for gui update
    function updateCapacityData() {
        fetch(capacityDataUrl)
            .then(response => response.json())
            .then(data => {
                data.rooms.forEach(room => {
                    const card = document.querySelector(`.room-card[data-area="${room.area}"]`);

                    if (!card) {
                        return;
                    }

                    const current = Number(room.current);
                    const capacity = Number(room.capacity);

                    const currentSpan = card.querySelector(".current-count");
                    const maxSpan = card.querySelector(".max-count");

                    if (currentSpan) {
                        currentSpan.textContent = current;
                    }

                    if (maxSpan) {
                        maxSpan.textContent = capacity;
                    }

                    updateCapacityColor(card, current, capacity);

                    // decides if unlock room or not
                    updateRoomLockStatus(card, current, capacity);
                });
            })
            .catch(error => {
                console.error("Error updating capacity data:", error);
            });
    }

    roomCards.forEach(card => {
        card.addEventListener("click", function () {
            const area = card.dataset.area;

            // kada click nag bebase sa new db values
            const current = getCardCurrent(card);
            const max = getCardCapacity(card);

            if (!max || isNaN(current) || isNaN(max)) {
                return;
            }

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

    if (roomSelectForm) {
        roomSelectForm.addEventListener("submit", function (event) {
            if (!selectedRoom) {
                event.preventDefault();
                alert("Please select one available room first.");
                return;
            }
        });
    }

    // First update when page loads
    updateCapacityData();

    // Updates the room cards every 2 seconds 
    setInterval(updateCapacityData, 2000);
});