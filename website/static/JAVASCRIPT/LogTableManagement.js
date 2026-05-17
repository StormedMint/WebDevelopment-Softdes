document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".log-row").forEach(row => {
        row.addEventListener("click", () => {

            const cells = row.querySelectorAll("td");

            document.querySelector("input[name='id']").value = cells[0].innerText;
            document.querySelector("input[name='fname']").value = cells[1].innerText;
            document.querySelector("input[name='lname']").value = cells[2].innerText;
            document.querySelector("input[name='account_type']").value = cells[3].innerText;
            document.querySelector("input[name='course_section']").value = cells[4].innerText;
            document.querySelector("input[name='date']").value = cells[5].innerText;

        });
    });

});
