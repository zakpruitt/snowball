
const allFilePath = document.getElementById("formFileAll")
const dailyFilePath = document.getElementById("formFileDaily")
const sheetTable = $("#sheetTable")

$(document).ready(function () {
    sheetTable.dataTable({
        dom: 'Bfrtip',
        buttons: [
            'csv', 'excel', 'pdf'
        ],
        "lengthMenu": [[15, -1], [15, "All"]],
    });
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

