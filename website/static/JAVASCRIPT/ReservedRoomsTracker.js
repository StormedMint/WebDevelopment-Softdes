document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".res-row").forEach(row => {
        row.addEventListener("click", () => {

            const cells = row.querySelectorAll("td");

            // ROOM (dropdown)
            const roomSelect = document.querySelector("select[name='room']");
            if (roomSelect) {
                roomSelect.value = cells[0].innerText.trim();
            }

            // DATE
            const rawDate = cells[1].innerText.trim();
            const dateInput = document.querySelector("input[name='date']");

            if (dateInput) {
                const d = new Date(rawDate);
                if (!isNaN(d)) {
                    dateInput.value = d.toISOString().split("T")[0];
                } else {
                    dateInput.value = rawDate; // fallback if already correct format
                }
            }

            // TIME (custom input)
            const timeInput = document.getElementById("timeInput");
            if (timeInput) {
                timeInput.value = cells[2].innerText.trim();
            }

            // REPRESENTATIVE
            const repInput = document.querySelector("input[name='representative']");
            if (repInput) {
                repInput.value = cells[3].innerText.trim();
            }

            // REASON
            const reasonInput = document.querySelector("input[name='reason']");
            if (reasonInput) {
                reasonInput.value = cells[4].innerText.trim();
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
        //formatting sa hour 2 digits
        let hour = String(h).padStart(2, '0');
        //formatting sa minutes + hour
        let time = `${hour}:${m}`;

        // magiging clickable siya
        let div = document.createElement("div");
        div.textContent = time;

        //kapag kinlick yung time, maiinput siya sa div
        div.onclick = () => {
            input.value = time;
            dropdown.style.display = "none";
        };

        dropdown.appendChild(div);
    }
}

input.onclick = () => {
    dropdown.style.display = "block";
};

document.addEventListener("click", (e) => {
    if (!input.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.style.display = "none";
    }
});