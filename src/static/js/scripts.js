
const allFilePath = document.getElementById("formFileAll")
const dailyFilePath = document.getElementById("formFileDaily")
const sheetTable = $("#sheetTable")

$(document).ready(function () {
    sheetTable.dataTable({
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excel',
                text: '<i class="fas fa-file-excel"></i>',
                className: 'btn btn-outline btn-success export-btn'
            },
            {
                extend: 'pdf',
                text: '<i class="fas fa-file-pdf"></i>',
                className: 'btn btn-outline btn-danger export-btn'
            },
        ],
        "lengthMenu": [[15, -1], [15, "All"]],
    });

    $('input[name="dates"]').daterangepicker();
});

allFilePath.addEventListener("change", (e) => {
    var fr = new FileReader();
    fr.onload = function () {
        var text = fr.result;
        $("#taAll").text(text);
    }
    fr.readAsText(allFilePath.files[0]);
});

dailyFilePath.addEventListener("change", (e) => {
    var fr = new FileReader();
    fr.onload = function () {
        var text = fr.result;
        $("#taDaily").text(text);
    }
    fr.readAsText(dailyFilePath.files[0]);
});
