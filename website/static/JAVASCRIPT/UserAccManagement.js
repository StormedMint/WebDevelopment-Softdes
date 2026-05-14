document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".user-row tr").forEach(row => {

        row.addEventListener("click", () => {

            const cells = row.querySelectorAll("td");

            const id = cells[0].innerText.trim();
            const fname = cells[1].innerText.trim();
            const lname = cells[2].innerText.trim();
            const account_type = cells[3].innerText.trim();
            const course_section = cells[4].innerText.trim();

            document.querySelector("input[name='id']").value = id;
            document.querySelector("input[name='fname']").value = fname;
            document.querySelector("input[name='lname']").value = lname;
            document.querySelector("input[name='account_type']").value = account_type;
            document.querySelector("input[name='course_section']").value = course_section;

        });

    });

});