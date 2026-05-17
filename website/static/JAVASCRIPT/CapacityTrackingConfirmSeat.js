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
