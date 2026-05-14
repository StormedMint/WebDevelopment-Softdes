document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".admin-row").forEach(row => {
        row.addEventListener("click", () => {

            const cells = row.querySelectorAll("td");

            const username = cells[0].innerText.trim();
            const password = cells[1].innerText.trim();
            const adminType = cells[2].innerText.trim();

            document.querySelector("input[name='username']").value = username;
            document.querySelector("input[name='password']").value = password;
            document.querySelector("input[name='type_admin']").value = adminType;

        });
    });

});