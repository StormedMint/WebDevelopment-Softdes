document.addEventListener("DOMContentLoaded", () => {

    const rows = document.querySelectorAll(".res-row");

    rows.forEach(row => {
        row.addEventListener("click", () => {

            document.querySelector("input[name='representative']").value =
                row.dataset.rep;

            document.querySelector("input[name='datetime']").value =
                row.dataset.datetime.replace(" ", "T");

            document.querySelector("textarea[name='reason']").value =
                row.dataset.reason;

            document.querySelector("select[name='room']").value =
                row.dataset.room;

            // store selected ID for delete
            window.selectedReservationId = row.dataset.id;
        });
    });
});