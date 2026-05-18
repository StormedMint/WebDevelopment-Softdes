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

            const popup = document.getElementById("capacityPopup");
            const closePopup = document.getElementById("closePopup");

            closePopup.addEventListener("click", function () {
                popup.style.display = "none";
            });

            const selectedRoomName = document.getElementById("selectedRoomName");
            const selectedRoomCapacity = document.getElementById("selectedRoomCapacity");
            const selectedRoomInput = document.getElementById("selectedRoomInput");

            const selectedCurrentInput = document.getElementById("selectedCurrentInput");
            const selectedCapacityInput = document.getElementById("selectedCapacityInput");

            const capacityAmount = document.getElementById("capacityAmount");
            const capacityForm = document.getElementById("capacityForm");
            
            const capacityError = document.getElementById("capacityError");

            

            function showError(message) {
                capacityError.textContent = message;
                capacityError.style.display = "block";
            }

            function clearError() {
                capacityError.textContent = "";
                capacityError.style.display = "none";
            }

            roomCards.forEach(card => {
                card.addEventListener("click", function () {
                    const area = card.dataset.area;

                    const current = Number(card.querySelector(".current-count").textContent.trim());
                    const max = Number(card.querySelector(".max-count").textContent.trim());

                    if (!area) {
                        showError("This room has no data-area value.");
                        return;
                    }

                    selectedRoomName.textContent = area;
                    selectedRoomCapacity.textContent = `${current} / ${max}`;

                    selectedRoomInput.value = area;
                    selectedCurrentInput.value = current;
                    selectedCapacityInput.value = max;

                    capacityAmount.value = "";
                    clearError();

                    popup.style.display = "flex";
                });
            });

            

            capacityForm.addEventListener("submit", function (event) {
                clearError();

                const current = Number(selectedCurrentInput.value);
                const max = Number(selectedCapacityInput.value);
                const amount = Number(capacityAmount.value);

                const action = event.submitter.value; // add or deduct

                if (!capacityAmount.value || isNaN(amount) || amount <= 0) {
                    event.preventDefault();
                    showError("Invalid input. Please enter a number greater than 0.");
                    return;
                }

                if (action === "add") {
                    const newTotal = current + amount;

                    if (newTotal > max) {
                        event.preventDefault();
                        showError(`Invalid. You can only add up to ${max - current}.`);
                        return;
                    }
                }

                if (action === "deduct") {
                    const newTotal = current - amount;

                    if (newTotal < 0) {
                        event.preventDefault();
                        showError(`Invalid. You can only deduct up to ${current}.`);
                        return;
                    }
                }
            });

            capacityAmount.addEventListener("input", function () {
                this.value = this.value.replace(/[^0-9]/g, "");
                clearError();
            });

            closePopup.addEventListener("click", function () {
                popup.style.display = "none";
                clearError();
            });

            popup.addEventListener("click", function (event) {
                if (event.target === popup) {
                    popup.style.display = "none";
                    clearError();
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