document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".item-row").forEach(row => {
        row.addEventListener("click", () => {

            const cells = row.querySelectorAll("td");

            // Fill inputs
            document.querySelector("input[name='item_name']").value = cells[0].innerText.trim();
            document.querySelector("input[name='description']").value = cells[1].innerText.trim();
            document.querySelector("input[name='place']").value = cells[3].innerText.trim();
            document.querySelector("input[name='finder_name']").value = cells[4].innerText.trim();
            document.querySelector("input[name='phone']").value = cells[5].innerText.trim();

            // KUNIN STATUS SA TABLE
            const status = cells[6].innerText.trim();

            // SESELECT YUNG STATUS SA RADIO BUTTON
            const radios = document.querySelectorAll("input[name='status']");

            radios.forEach(radio => {
                radio.checked = (radio.value === status);
            });

        });
    });

});