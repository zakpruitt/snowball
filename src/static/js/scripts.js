
const allFilePath = document.getElementById("formFileAll")
const dailyFilePath = document.getElementById("formFileDaily")

const sheetTable = $("#sheetTable")
const employeeSheetChecks = $(".employeeSheetCheck")
const dateConstraint = $('#dateConstraint')
const supCodeChecks = $(".supCodeCheck")
const subDeptChecks = $(".subDeptCheck")
const emailRadioButtons = $(".emailRadioButton")


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

    dateConstraint.daterangepicker();
});

// PARSE FILE FUNCTIONS 

allFilePath && allFilePath.addEventListener("change", (e) => {
    var fr = new FileReader();
    fr.onload = function () {
        var text = fr.result;
        $("#taAll").text(text);
    }
    fr.readAsText(allFilePath.files[0]);
});

dailyFilePath && dailyFilePath.addEventListener("change", (e) => {
    var fr = new FileReader();
    fr.onload = function () {
        var text = fr.result;
        $("#taDaily").text(text);
    }
    fr.readAsText(dailyFilePath.files[0]);
});

// SHEET TABLE FUNCTIONS

employeeSheetChecks && employeeSheetChecks.each(function(i, element) {
    element.addEventListener("change", (e) => {
        if (e.target.checked) {
            alert('hello');
        }
    })
});

dateConstraint && dateConstraint.each(function(i, element) {
    element.addEventListener("change", (e) => {
        if (e.target.checked) {
            alert('hello');
        }
    })
});

subDeptChecks && subDeptChecks.each(function(i, element) {
    element.addEventListener("change", (e) => {
        if (e.target.checked) {
            alert('hello');
        }
    })
});

supCodeChecks && supCodeChecks.each(function(i, element) {
    element.addEventListener("change", (e) => {
        if (e.target.checked) {
            alert('hello');
        }
    })
});

emailRadioButtons && emailRadioButtons.each(function(i, element) {
    element.addEventListener("change", (e) => {
        if (e.target.checked) {
            alert('hello');
        }
    })
});


