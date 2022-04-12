
const allFilePath = document.getElementById("formFileAll");
const dailyFilePath = document.getElementById("formFileDaily");

const sheetTable = $("#sheetTable");
const employeeSheetChecks = $(".employeeSheetCheck");
const dateConstraint = $('#dateConstraint');
const supCodeChecks = $(".supCodeCheck");
const subDeptChecks = $(".subDeptCheck");
const emailRadioButtons = $(".emailRadioButton");

const allTotalChart = $("#allTotalChart");
const SoftwareImmLaterChart = $("#SoftwareImmLaterChart");
const HardwareImmLaterChart = $("#HardwareImmLaterChart");
//#region PARSE FILE FUNCTIONS 

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

//#endregion

//#region SHEET TABLE FUNCTIONS

$(document).ready(function () {
    sheetTable && sheetTable.dataTable({
        dom: '<<Bft>ip>',
        buttons: [
            {
                extend: 'excelHtml5',
                customize: function (xlsx) {
                    customFormating(xlsx);
                },
                title: '',
                text: '<i class="fas fa-file-excel"></i>',
                className: 'btn btn-outline btn-success',
            },
            {
                extend: 'pdf',
                text: '<i class="fas fa-file-pdf"></i>',
                className: 'btn btn-outline btn-danger'
            },
        ],
        "lengthMenu": [[15, -1], [15, "All"]],
    });

    dateConstraint && dateConstraint.daterangepicker();
});

function DTFilter() {
    this.searches = new Array();
}

DTFilter.prototype.addSearch = function (search) {
    this.searches.push(search);
}

DTFilter.prototype.removeSearch = function (search) {
    this.searches.splice(this.searches.indexOf(search), 1);
}

DTFilter.prototype.clearSearches = function (search) {
    this.searches = [];
}

DTFilter.prototype.buildSearchString = function () {
    var searchString = "";
    for (let i = 0; i < this.searches.length; i++) {
        searchString += this.searches[i].toString();
        if (i < this.searches.length - 1) {
            searchString += "|";
        }
    }
    return searchString;
}

const employeeFilter = new DTFilter();
const dateFilter = new DTFilter();
const subDeptFilter = new DTFilter();
const supCodeFilter = new DTFilter();

employeeSheetChecks && employeeSheetChecks.each(function (i, element) {
    element.addEventListener("change", (e) => {
        if (e.target.checked) {
            employeeFilter.addSearch(e.target.value);
            employeeFilter.addSearch(e.target.id);
        } else {
            employeeFilter.removeSearch(e.target.value);
            employeeFilter.removeSearch(e.target.id);
        }
        search([5, 6, 7], employeeFilter.buildSearchString());
        console.log(employeeFilter.buildSearchString());
    });

    employeeFilter.addSearch(element.value);
    employeeFilter.addSearch(element.id);
});

dateConstraint && dateConstraint.on('apply.daterangepicker', function (ev, picker) {
    // clear searches and show formatted value on picker
    dateFilter.clearSearches();
    $(this).val(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'));

    // get dates from picker
    var startDate = picker.startDate.format('MM-DD-YYYY').toString();
    var endDate = picker.endDate.format('MM-DD-YYYY').toString();

    // get all dates (inclusive) inbetween start and end. loop through them and add to filter.
    getDates(new Date(startDate), new Date(endDate)).forEach(date => {
        dateFilter.addSearch(date.toString());
    });

    // search
    search(1, dateFilter.buildSearchString());
});

subDeptChecks && subDeptChecks.each(function (i, element) {
    element.addEventListener("change", (e) => {
        if (e.target.checked) {
            subDeptFilter.addSearch(e.target.value);
        } else {
            subDeptFilter.removeSearch(e.target.value);
        }
        search(3, subDeptFilter.buildSearchString());
    })
});

supCodeChecks && supCodeChecks.each(function (i, element) {
    element.addEventListener("change", (e) => {
        if (e.target.checked) {
            supCodeFilter.addSearch(e.target.value);
        } else {
            supCodeFilter.removeSearch(e.target.value);
        }
        search(2, supCodeFilter.buildSearchString());
    })
});

emailRadioButtons && emailRadioButtons.each(function (i, element) {
    element.addEventListener("change", (e) => {
        if (e.target.checked) {
            search(4, e.target.value);
        }
    })
});

function search(colNum, searchString) {
    var table = sheetTable.DataTable();
    table.column(colNum).search(searchString, true, false).draw();
}

function getDates(startDate, stopDate) {
    var dateArray = [];
    var currentDate = moment(startDate);
    var stopDate = moment(stopDate);
    while (currentDate <= stopDate) {
        dateArray.push(moment(currentDate).format('YYYY-MM-DD'))
        currentDate = moment(currentDate).add(1, 'days');
    }
    return dateArray;
}

function customFormating(xlsx) {
    var sheet = xlsx.xl.worksheets['sheet1.xml'];

    var count = 0;
    $('row', sheet).each(function () {
        if (count % 2 == 0 && count > 1) {
            $(this).find("c").attr('s', '45');
        }
        else {
            $(this).find("c").attr('s', '25');
        }
        count++;
    });
    $('row:first c', sheet).attr('s', '42');
}

//#endregion

//#region VISUALIZE FUNCTIONS

$(document).ready(function () {
    allTotalChart && renderLineGraph(allTotalChart, 'all-count', 'All Count');
    SoftwareImmLaterChart && renderChart(SoftwareImmLaterChart,'imm_later_software', 'Software Immediate vs. Later', dis_legend=false);
    HardwareImmLaterChart && renderChart(HardwareImmLaterChart,'imm_later_hardware', 'Hardware Immediate vs. Later', dis_legend=false);

});

function renderLineGraph(chart, endpoint, title, dis_legend = true) {
    fetch('/data/' + endpoint)
        .then(response => response.json())
        .then(data => {
            const config = {
                type: 'line',
                data: data,
                options: {
                    scales:{
                        y:{
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: title
                        },
                        legend:{
                            display:dis_legend
                        }
                    }
                }
            };
        
            const newChart = new Chart(
                chart,
                config
            );
        });
}

function renderChart(chart,endpoint,title, dis_legend = true) {
    fetch('/data/' + endpoint)
        .then(response => response.json())
        .then(data => {
            const config = {
                type: 'bar',
                data: data,
                options: {
                    plugins: {
                        title: {
                            display: true,
                            text: title
                        },
                        legend:{
                            display:dis_legend
                        }
                    }
                }
            };
        
            const newChart = new Chart(
                chart,
                config
            );
        });
}

//#endregion