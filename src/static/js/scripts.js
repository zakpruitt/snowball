
const allFilePath = document.getElementById("formFileAll");
const dailyFilePath = document.getElementById("formFileDaily");

const sheetTable = $("#sheetTable");
const employeeSheetChecks = $(".employeeSheetCheck");
const dateConstraint = $('#dateConstraint');
const supCodeChecks = $(".supCodeCheck");
const subDeptChecks = $(".subDeptCheck");
const emailRadioButtons = $(".emailRadioButton");

const downloadReportButton = $("#downloadReportButton");
const visualizeDateConstraint = $('#visualize-date-picker');

const allTotalChart = $("#allTotalChart");
const softwareImmPieChart = $("#SoftwareImmPieChart");
const hardwareImmPieChart = $("#HardwareImmPieChart");
const softwareEmailPieChart = $("#SoftwareEmailPieChart");
const hardwareEmailPieChart = $("#HardwareEmailPieChart");
const softwareLaterPieChart = $("#SoftwareLaterPieChart");
const hardwareLaterPieChart = $("#HardwareLaterPieChart");

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
    try {
        start = window.location.href.split('start=')[1].split('&')[0];
        end = window.location.href.split('end=')[1];
        loadGraphsWithTimeConstraint(start, end);
    } catch (e) {
        loadGraphs();
    }
    initializeVisualizeDatePicker();
});

visualizeDateConstraint && visualizeDateConstraint.on('apply.daterangepicker', function (ev, picker) {
    var startDate = picker.startDate.format('YYYY-MM-DD').toString();
    var endDate = picker.endDate.format('YYYY-MM-DD').toString();
    window.location.href = "/visualize?start=" + startDate + "&end=" + endDate;
});

downloadReportButton.on("click", function () {
    // var doc = new jsPDF('landscape');
    // var options = {
    //     'background': '#fff',
    // };


    // doc.addHTML($('#software-data')[0], 0, 0, options, function () {
    //     doc.addPage();
    // });
    // doc.addHTML($('#hardware-data')[0], 0, 0, options, function () {
    //     doc.addPage();
    // });
    // doc.addHTML($('#other-data')[0], 0, 0, options, function () {
    //     doc.save('sample-file.pdf');
    // });
});

function renderLineGraph(chart, endpoint, title, dis_legend = true) {
    fetch('/data/' + endpoint)
        .then(response => response.json())
        .then(data => {
            const config = {
                type: 'line',
                data: data,
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: title
                        },
                        legend: {
                            display: dis_legend
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

function renderPieChart(chart, endpoint, title, dis_legend = true) {
    fetch('/data/' + endpoint)
        .then(response => response.json())
        .then(data => {
            if (data.datasets[0].data.length == 0) {
                alert(chart.previousElementSibling.className.contains("no-data-display-message"));
            }
            const config = {
                type: 'pie',
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: title
                        },
                        legend: {
                            display: dis_legend
                        },
                        datalabels: {
                            display: function (context) {
                                return context.dataset.data[context.dataIndex] > 1;
                            }
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

function initializeVisualizeDatePicker() {
    var start;
    var end;
    try {
        start = window.location.href.split('start=')[1].split('&')[0];
        end = window.location.href.split('end=')[1];
        start = moment(start);
        end = moment(end);
    } catch (e) {
        $('#visualize-date-picker span').html("All Dates");
    }

    function cb(start, end) {
        $('#visualize-date-picker span').html(start.format('YYYY-MM-DD') + ' - ' + end.format('YYYY-MM-DD'));
    }

    visualizeDateConstraint.daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
            'Today': [moment(), moment()],
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()],
            'Last 30 Days': [moment().subtract(29, 'days'), moment()],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb);
    cb(start, end);
}

function loadGraphs() {
    allTotalChart && renderLineGraph(allTotalChart, 'all-count', 'All Count');
    softwareImmPieChart && renderPieChart(softwareImmPieChart, '/pie-data?sub_dept=S&category=imm', 'Software Immediate Distribution');
    hardwareImmPieChart && renderPieChart(hardwareImmPieChart, '/pie-data?sub_dept=H&category=imm', 'Hardware Immediate Distibutiuon');
    softwareEmailPieChart && renderPieChart(softwareEmailPieChart, '/pie-email-data?sub_dept=S', 'Software Email Distribution');
    hardwareEmailPieChart && renderPieChart(hardwareEmailPieChart, '/pie-email-data?sub_dept=H', 'Hardware Email Distribution');
    softwareLaterPieChart && renderPieChart(softwareLaterPieChart, '/pie-data?sub_dept=S&category=later', 'Software Later Distribution');
    hardwareLaterPieChart && renderPieChart(hardwareLaterPieChart, '/pie-data?sub_dept=H&category=later', 'Hardware Later Distibutiuon');
}

function loadGraphsWithTimeConstraint(start, end) {
    allTotalChart && renderLineGraph(allTotalChart, 'all-count', 'All Count');
    softwareImmPieChart && renderPieChart(softwareImmPieChart, '/pie-data?sub_dept=S&category=imm&start=' + start + '&end=' + end, 'Software Immediate Distribution');
    hardwareImmPieChart && renderPieChart(hardwareImmPieChart, '/pie-data?sub_dept=H&category=imm&start=' + start + '&end=' + end, 'Hardware Immediate Distibutiuon');
    softwareEmailPieChart && renderPieChart(softwareEmailPieChart, '/pie-email-data?sub_dept=S&start=' + start + '&end=' + end, 'Software Email Distribution');
    hardwareEmailPieChart && renderPieChart(hardwareEmailPieChart, '/pie-email-data?sub_dept=H&start=' + start + '&end=' + end, 'Hardware Email Distribution');
    softwareLaterPieChart && renderPieChart(softwareLaterPieChart, '/pie-data?sub_dept=S&category=later&start=' + start + '&end=' + end, 'Software Later Distribution');
    hardwareLaterPieChart && renderPieChart(hardwareLaterPieChart, '/pie-data?sub_dept=H&category=later&start=' + start + '&end=' + end, 'Hardware Later Distibutiuon');
}

//#endregion