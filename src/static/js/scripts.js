
const allFilePath = document.getElementById("formFileAll");
const dailyFilePath = document.getElementById("formFileDaily");
const singleReportTab = $("#singleReportTab");
const multipleReportTab = $("#multipleReportTab");
const singleParse = $("#singleParse");
const multipleParse = $("#multipleParse");

const sheetTable = $("#sheetTable");
const employeeSheetChecks = $(".employeeSheetCheck");
const dateConstraint = $('#dateConstraint');
const supCodeChecks = $(".supCodeCheck");
const subDeptChecks = $(".subDeptCheck");
const emailRadioButtons = $(".emailRadioButton");
const sheetsDeleteButtons = $(".sheets-delete-button");

const downloadReportButton = $("#downloadReportButton");
const visualizeDateConstraint = $('#visualize-date-picker');

const allTotalChart = $("#allTotalChart");
const softwareImmPieChart = $("#SoftwareImmPieChart");
const hardwareImmPieChart = $("#HardwareImmPieChart");
const softwareEmailPieChart = $("#SoftwareEmailPieChart");
const hardwareEmailPieChart = $("#HardwareEmailPieChart");
const softwareLaterPieChart = $("#SoftwareLaterPieChart");
const hardwareLaterPieChart = $("#HardwareLaterPieChart");
const softwareBarChart = $('#SoftwareBarChart');
const hardwareBarChart = $('#HardwareBarChart')

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

singleReportTab.click(() => {
    singleReportTab.addClass("active");
    multipleReportTab.removeClass("active");
    singleParse.prop("hidden", false);
    multipleParse.prop("hidden", true);
});

multipleReportTab.click(() => {
    singleReportTab.removeClass("active");
    multipleReportTab.addClass("active");
    singleParse.prop("hidden", true);
    multipleParse.prop("hidden", false);
});

//#endregion

//#region SHEET TABLE FUNCTIONS

$(document).ready(function () {
    if (top.location.pathname.includes('/sheets')) {
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
    }
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

sheetsDeleteButtons.each(function (i, element) {
    element.addEventListener("click", (e) => {
        attrs = e.target.attributes;
        const callNumber = attrs.getNamedItem("callnumber").value;
        const dateCreated = attrs.getNamedItem("datecreated").value;
        
        // ajax request to /sheets/delete with callnumber and datecreated
        $.ajax({
            url: '/sheets/delete',
            type: 'POST',
            data: {
                callNumber: callNumber,
                dateCreated: dateCreated
            },
            success: function (data) {
                location.reload();
            },
            error: function(err) {
                alert("Error!");
            }
        });
    });
});

employeeSheetChecks.each(function (i, element) {
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
});

dateConstraint.on('apply.daterangepicker', function (ev, picker) {
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

subDeptChecks.each(function (i, element) {
    element.addEventListener("change", (e) => {
        if (e.target.checked) {
            subDeptFilter.addSearch(e.target.value);
        } else {
            subDeptFilter.removeSearch(e.target.value);
        }
        search(3, subDeptFilter.buildSearchString());
    })
});

supCodeChecks.each(function (i, element) {
    element.addEventListener("change", (e) => {
        if (e.target.checked) {
            supCodeFilter.addSearch(e.target.value);
        } else {
            supCodeFilter.removeSearch(e.target.value);
        }
        search(2, supCodeFilter.buildSearchString());
    })
});

emailRadioButtons.each(function (i, element) {
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
    if (top.location.pathname.includes('/visualize')) {
        try {
            start = window.location.href.split('start=')[1].split('&')[0];
            end = window.location.href.split('end=')[1];
            loadGraphsWithTimeConstraint(start, end);
        } catch (e) {
            loadGraphs();
        }
        visualizeDateConstraint && initializeVisualizeDatePicker();
    }
});

visualizeDateConstraint.on('apply.daterangepicker', function (ev, picker) {
    var startDate = picker.startDate.format('YYYY-MM-DD').toString();
    var endDate = picker.endDate.format('YYYY-MM-DD').toString();
    window.location.href = "/visualize?start=" + startDate + "&end=" + endDate;
});

downloadReportButton.on("click", function () {
    var pdfTitle;
    try {
        start = window.location.href.split('start=')[1].split('&')[0];
        end = window.location.href.split('end=')[1];
        pdfTitle = "Report " + start + " - " + end;
    } catch (e) {
        pdfTitle = "Report All Dates";
    }
    
    var divs = ["#software-data", "#hardware-data", "#other-data"]
    var pdf = new jsPDF('p', 'mm', [400, 470]);

    for (let i = 0; i <= divs.length; i++) {
        html2canvas($(divs[i])[0],
            {
                dpi: 300,
                scale: 1
            }).then(canvas => {
                pdf.addImage(canvas.toDataURL("images/png", 1), 'PNG', 26, 2);

                if (i == divs.length - 1) {
                    pdf.save(pdfTitle);
                } else {
                    pdf.addPage();
                }
            });
    }
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

function renderBarGraph(chart, endpoint, title, dis_legend = true) {
    fetch('/data/' + endpoint)
        .then(response => response.json())
        .then(data => {
            const config = {
                type: 'bar',
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
            if (data.datasets[0].data.length != 0) {
                var parent = chart.parent();
                var div = parent.children().first();
                div.remove();
            }
            const config = {
                type: 'pie',
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        title: {
                            display: true,
                            text: title
                        },
                        legend: {
                            display: dis_legend,
                            position: 'left'
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

    if (start && end) {
        cb(start, end);
    }
}

function loadGraphs() {
    renderLineGraph(allTotalChart, 'all-count', 'All Count');
    renderPieChart(softwareImmPieChart, '/pie-data?sub_dept=S&category=imm', 'Software Immediate Distribution');
    renderPieChart(hardwareImmPieChart, '/pie-data?sub_dept=H&category=imm', 'Hardware Immediate Distibutiuon');
    renderPieChart(softwareEmailPieChart, '/pie-email-data?sub_dept=S', 'Software Email Distribution');
    renderPieChart(hardwareEmailPieChart, '/pie-email-data?sub_dept=H', 'Hardware Email Distribution');
    renderPieChart(softwareLaterPieChart, '/pie-data?sub_dept=S&category=later', 'Software Later Distribution');
    renderPieChart(hardwareLaterPieChart, '/pie-data?sub_dept=H&category=later', 'Hardware Later Distibutiuon');
    renderBarGraph(softwareBarChart, '/bar-data?sub_dept=S', 'Software Counts (Per Employee ID)');
    renderBarGraph(hardwareBarChart, '/bar-data?sub_dept=H', 'Hardware Counts (Per Employee ID)');
}

function loadGraphsWithTimeConstraint(start, end) {
    renderLineGraph(allTotalChart, 'all-count', 'All Count');
    renderPieChart(softwareImmPieChart, '/pie-data?sub_dept=S&category=imm&start=' + start + '&end=' + end, 'Software Immediate Distribution');
    renderPieChart(hardwareImmPieChart, '/pie-data?sub_dept=H&category=imm&start=' + start + '&end=' + end, 'Hardware Immediate Distibutiuon');
    renderPieChart(softwareEmailPieChart, '/pie-email-data?sub_dept=S&start=' + start + '&end=' + end, 'Software Email Distribution');
    renderPieChart(hardwareEmailPieChart, '/pie-email-data?sub_dept=H&start=' + start + '&end=' + end, 'Hardware Email Distribution');
    renderPieChart(softwareLaterPieChart, '/pie-data?sub_dept=S&category=later&start=' + start + '&end=' + end, 'Software Later Distribution');
    renderPieChart(hardwareLaterPieChart, '/pie-data?sub_dept=H&category=later&start=' + start + '&end=' + end, 'Hardware Later Distibutiuon');
    renderBarGraph(softwareBarChart, '/bar-data?sub_dept=S&start=' + start + '&end=' + end, 'Software Counts');
    renderBarGraph(hardwareBarChart, '/bar-data?sub_dept=H&start=' + start + '&end=' + end, 'Hardware Counts');
}

//#endregion
