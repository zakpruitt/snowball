
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
        dom: '<<Bft>ip>',
        // dom: 'lfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                customize: function(xlsx){
                    customFormating(xlsx);
                },
                
                
                text: '<i class="fas fa-file-excel"></i>',
                className: 'btn btn-outline btn-success'
                
            },
            {
                extend: 'pdf',
                text: '<i class="fas fa-file-pdf"></i>',
                className: 'btn btn-outline btn-danger'
            },
        ],
        "lengthMenu": [[15, -1], [15, "All"]],
    });

    dateConstraint.daterangepicker();
});

function customFormating(xlsx){
    var sheet = xlsx.xl.worksheets['sheet1.xml'];
    var count = 0;
    var columns = ['A','B','C','D','E','F','G','H','I']
    var skippedHeader = false;
    var skippedTitle = false;
    for (let i = 0; i<columns.length;i++){
        $('row c[r*="'+columns[i] +'"]', sheet).each(function(){
        if (skippedHeader&skippedTitle){
            if (count % 2 === 0){
                $(this).attr('s','35');
            }
            else{
                $(this).attr('s','40');
            }
            count++;

        }
        else if(skippedTitle){

            skippedHeader=true;
        }else{
            skippedTitle=true;
        }
    });
    skippedHeader = false;
    
}
}

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

employeeSheetChecks && employeeSheetChecks.each(function (i, element) {
    element.addEventListener("change", (e) => {
        if (e.target.checked) {
            alert('hello');
        }
    })
});

dateConstraint && dateConstraint.each(function (i, element) {
    element.addEventListener("change", (e) => {
        if (e.target.checked) {
            alert('hello');
        }
    })
});

subDeptChecks && subDeptChecks.each(function (i, element) {
    element.addEventListener("change", (e) => {
        if (e.target.checked) {
            var table = sheetTable.DataTable();
            table.column(3).search(e.target.value + "H|S",true,false).draw();
            // var array = table.column(3)
            //     .data()
            //     .filter(function (value, index) {
            //         return value === e.target.value;
            //     })
            //     .draw();

            // $.fn.dataTableExt.afnFiltering.push(
            //     function (oSettings, aData, iDataIndex) {
            //         return aData[3] === e.target.value;
            //     }
            // );

            // table.draw()
        } else {

        }
    })
});

supCodeChecks && supCodeChecks.each(function (i, element) {
    element.addEventListener("change", (e) => {
        if (e.target.checked) {
            var table = sheetTable.DataTable();
            table.search('').columns(2).search(e.target.value).draw();
        }
    })
});

emailRadioButtons && emailRadioButtons.each(function (i, element) {
    element.addEventListener("change", (e) => {
        if (e.target.checked) {
            alert('hello');
        }
    })
});


