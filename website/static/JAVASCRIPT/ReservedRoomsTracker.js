document.addEventListener("DOMContentLoaded", () => {

    const roomSelect = document.querySelector("select[name='room']");
    const dateInput = document.querySelector("input[name='date']");
    const timeInput = document.getElementById("timeInput");
    const repInput = document.querySelector("input[name='representative']");
    const reasonInput = document.querySelector("input[name='reason']");

    const addButton = document.getElementById("plus-button");

    document.querySelectorAll(".res-row").forEach(row => {
        row.addEventListener("click", () => {

            const cells = row.querySelectorAll("td");

            // Fill Room
            if (roomSelect) {
                roomSelect.value = cells[0].innerText.trim();

                // make select act like readonly
                roomSelect.style.pointerEvents = "none";
                roomSelect.style.opacity = "0.7";
                roomSelect.tabIndex = -1;
            }

            // Fill Date
            if (dateInput) {
                dateInput.value = cells[1].innerText.trim();
                dateInput.readOnly = true;
            }

            // Fill Time
            if (timeInput) {
                timeInput.value = cells[2].innerText.trim();
                timeInput.readOnly = true;
            }

            // Fill Representative
            if (repInput) {
                repInput.value = cells[3].innerText.trim();
                repInput.readOnly = true;
            }

            // Fill Reason
            if (reasonInput) {
                reasonInput.value = cells[4].innerText.trim();
                reasonInput.readOnly = true;
            }

            // Optional: prevent adding duplicate reservation after selecting row
            if (addButton) {
                addButton.disabled = true;
                addButton.style.opacity = "0.5";
                addButton.style.cursor = "not-allowed";
            }

            // store ID for delete/edit
            window.selectedReservationId = row.dataset.id;

        });
    });

});


// Kunin sa html yung elements
const dropdown = document.getElementById("timeDropdown");
const input = document.getElementById("timeInput");

// loop through 24hrs
for (let h = 0; h < 24; h++) {
    // loop for minutes
    for (let m of ["00", "30"]) {
        // formatting sa hour 2 digits
        let hour = String(h).padStart(2, '0');

        // formatting sa minutes + hour
        let time = `${hour}:${m}`;

        // magiging clickable siya
        let div = document.createElement("div");
        div.textContent = time;

        // kapag kinlick yung time, maiinput siya sa div
        div.onclick = () => {
            input.value = time;
            dropdown.style.display = "none";
        };

        dropdown.appendChild(div);
    }
}

input.onclick = () => {
    // Do not show dropdown after selecting a table row
    if (input.readOnly && input.value !== "") {
        return;
    }

    dropdown.style.display = "block";
};

document.addEventListener("click", (e) => {
    if (!input.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.style.display = "none";
    }
});

document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", function (e) {

        const select = this.querySelector("select");

        if (select && select.value === "all-rooms") {
            e.preventDefault();
            alert("Please select a valid room option.");
        }
    });
});