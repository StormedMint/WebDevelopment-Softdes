document.addEventListener("DOMContentLoaded", () => {


    // Clear old selected user when page loads
    fetch("/clear_selected_user", {
        method: "POST"
    });


    const idInput = document.querySelector("input[name='id']");
    const fnameInput = document.querySelector("input[name='fname']");
    const lnameInput = document.querySelector("input[name='lname']");
    const accountTypeInput = document.querySelector("input[name='account_type']");
    const courseSectionInput = document.querySelector("input[name='course_section']");

    document.querySelectorAll(".user-row tr").forEach(row => {

        row.addEventListener("click", () => {

            const cells = row.querySelectorAll("td");

            // Prevent error when clicking the "No users found" row
            if (cells.length < 5) {
                return;
            }

            idInput.value = cells[0].innerText.trim();

            // Para ma-store sa session yung current selected ID
            fetch("/set_selected_user", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: "user_id=" + encodeURIComponent(cells[0].innerText.trim())
            });
            fnameInput.value = cells[1].innerText.trim();
            lnameInput.value = cells[2].innerText.trim();
            accountTypeInput.value = cells[3].innerText.trim();
            courseSectionInput.value = cells[4].innerText.trim();

            // Keep ID and Account Type readonly
            idInput.removeAttribute("readonly")
            fnameInput.removeAttribute("readonly");
            lnameInput.removeAttribute("readonly");
            courseSectionInput.removeAttribute("readonly");

    function capitalizeWords(input) {
        input.value = input.value
            .toLowerCase()
            .replace(/\b[a-z]/g, char => char.toUpperCase());
    }

    fnameInput.addEventListener("input", () => {
        fnameInput.value = fnameInput.value.replace(/[^a-zA-Z\s]/g, '');
        capitalizeWords(fnameInput);
    });

    lnameInput.addEventListener("input", () => {
        lnameInput.value = lnameInput.value.replace(/[^a-zA-Z\s]/g, '');
        capitalizeWords(lnameInput);
    });

    courseSectionInput.addEventListener("input", () => {
        courseSectionInput.value = courseSectionInput.value
            .replace(/[^a-zA-Z0-9-\s]/g, '')
            .toUpperCase();
    });
        });

    });

});
