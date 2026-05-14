document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".item-row").forEach(row => {
        row.addEventListener("click", () => {

            const cells = row.querySelectorAll("td");

            document.querySelector("input[name='item_name']").value = cells[0].innerText;
            document.querySelector("input[name='description']").value = cells[1].innerText;
            document.querySelector("input[name='place']").value = cells[3].innerText;
            document.querySelector("input[name='finder_name']").value = cells[4].innerText;
            document.querySelector("input[name='phone']").value = cells[5].innerText;

        });
    });

});