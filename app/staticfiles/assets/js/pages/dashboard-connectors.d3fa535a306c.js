'use strict';
document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function() {
        float_chart()
    }, 100);
    // [ campaign-scroll ] start
    var px = new PerfectScrollbar('.customer-scroll', {
        wheelSpeed: .5,
        swipeEasing: 0,
        wheelPropagation: 1,
        minScrollbarLength: 40,
    });
    var px = new PerfectScrollbar('.customer-scroll1', {
        wheelSpeed: .5,
        swipeEasing: 0,
        wheelPropagation: 1,
        minScrollbarLength: 40,
    });
    var px = new PerfectScrollbar('.customer-scroll2', {
        wheelSpeed: .5,
        swipeEasing: 0,
        wheelPropagation: 1,
        minScrollbarLength: 40,
    });
    var px = new PerfectScrollbar('.customer-scroll3', {
        wheelSpeed: .5,
        swipeEasing: 0,
        wheelPropagation: 1,
        minScrollbarLength: 40,
    });
    // [ campaign-scroll ] end
});

function float_chart() {
    // [ coversions-chart ] start
    (function () {
        var options1 = {
            chart: {
                type: 'bar',
                height: 65,
                sparkline: {
                    enabled: true
                }
            },
            dataLabels: {
                enabled: false
            },
            colors: ["#73b4ff"],
            fill: {
                type: 'gradient',
                gradient: {
                    shade: 'light',
                    type: "vertical",
                    shadeIntensity: 0,
                    gradientToColors: ["#4099ff"],
                    inverseColors: true,
                    opacityFrom: 0.99,
                    opacityTo: 0.99,
                    stops: [0, 100]
                },
            },
            plotOptions: {
                bar: {
                    columnWidth: '80%'
                }
            },
            series: [{
                data: [25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54, 25, 66, 41, 89, 63, 54, 25, 66, 41, 85, 63, 25, 44, 12, 36, 9, 54, 25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 25, 44, 12, 36, 9, 54]
            }],
            xaxis: {
                crosshairs: {
                    width: 1
                },
            },
            tooltip: {
                fixed: {
                    enabled: false
                },
                x: {
                    show: false
                },
                y: {
                    title: {
                        formatter: function(seriesName) {
                            return ''
                        }
                    }
                },
                marker: {
                    show: false
                }
            }
        }
        let coversions_chart1 = document.querySelector("#coversions-chart1");
        if ( coversions_chart1 ) {
            new ApexCharts(document.querySelector("#coversions-chart1"), options1).render();
        }        

        var options2 = {
            chart: {
                type: 'bar',
                height: 65,
                sparkline: {
                    enabled: true
                }
            },
            dataLabels: {
                enabled: false
            },
            colors: ["#59e0c5"],
            fill: {
                type: 'gradient',
                gradient: {
                    shade: 'light',
                    type: "vertical",
                    shadeIntensity: 0,
                    gradientToColors: ["#2ed8b6"],
                    inverseColors: true,
                    opacityFrom: 0.99,
                    opacityTo: 0.99,
                    stops: [0, 100]
                },
            },
            plotOptions: {
                bar: {
                    columnWidth: '80%'
                }
            },
            series: [{
                data: [25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54, 25, 66, 41, 89, 63, 54, 25, 66, 41, 85, 63, 25, 44, 12, 36, 9, 54, 25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 25, 44, 12, 36, 9, 54]
            }],
            xaxis: {
                crosshairs: {
                    width: 1
                },
            },
            tooltip: {
                fixed: {
                    enabled: false
                },
                x: {
                    show: false
                },
                y: {
                    title: {
                        formatter: function(seriesName) {
                            return ''
                        }
                    }
                },
                marker: {
                    show: false
                }
            }
        }
        let coversions_chart2 = document.querySelector("#coversions-chart2");
        if ( coversions_chart2 ) {
            new ApexCharts(document.querySelector("#coversions-chart2"), options2).render();
        }

        var options4 = {
            chart: {
                type: 'bar',
                height: 65,
                sparkline: {
                    enabled: true
                }
            },
            dataLabels: {
                enabled: false
            },
            colors: ["#ff869a"],
            fill: {
                type: 'gradient',
                gradient: {
                    shade: 'light',
                    type: "vertical",
                    shadeIntensity: 0,
                    gradientToColors: ["#ff5370"],
                    inverseColors: true,
                    opacityFrom: 0.99,
                    opacityTo: 0.99,
                    stops: [0, 100]
                },
            },
            plotOptions: {
                bar: {
                    columnWidth: '80%'
                }
            },
            series: [{
                data: [25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54, 25, 66, 41, 89, 63, 54, 25, 66, 41, 85, 63, 25, 44, 12, 36, 9, 54, 25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 25, 44, 12, 36, 9, 54]
            }],
            xaxis: {
                crosshairs: {
                    width: 1
                },
            },
            tooltip: {
                fixed: {
                    enabled: false
                },
                x: {
                    show: false
                },
                y: {
                    title: {
                        formatter: function(seriesName) {
                            return ''
                        }
                    }
                },
                marker: {
                    show: false
                }
            }
        }
        let coversions_chart4 = document.querySelector("#coversions-chart4");
        if ( coversions_chart4 ) {
            new ApexCharts(document.querySelector("#coversions-chart4"), options4).render();
        }
        
    })();
    // [ coversions-chart ] end
    // [ seo-card1 ] start
    (function () {
        var options1 = {
            chart: {
                type: 'area',
                height: 145,
                sparkline: {
                    enabled: true
                }
            },
            dataLabels: {
                enabled: false
            },
            colors: ["#ff5370"],
            fill: {
                type: 'gradient',
                gradient: {
                    shade: 'dark',
                    gradientToColors: ['#ff869a'],
                    shadeIntensity: 1,
                    type: 'horizontal',
                    opacityFrom: 1,
                    opacityTo: 0.8,
                    stops: [0, 100, 100, 100]
                },
            },
            stroke: {
                curve: 'smooth',
                width: 2,
            },
            series: [{
                data: [45, 35, 60, 50, 85, 70]
            }],
            yaxis: {
               min: 5,
               max: 90,
           },
            tooltip: {
                fixed: {
                    enabled: false
                },
                x: {
                    show: false
                },
                y: {
                    title: {
                        formatter: function(seriesName) {
                            return 'Ticket '
                        }
                    }
                },
                marker: {
                    show: false
                }
            }
        }
        let seo_card1 = document.querySelector("#seo-card1");
        if ( seo_card1 ) {
            new ApexCharts(seo_card1, options1).render();
        }        
    })();
    // [ seo-card1 ] end
    // [ customer-chart ] start
    (function () {
        var options = {
            chart: {
                height: 150,
                type: 'donut',
            },
            dataLabels: {
                enabled: false
            },
            plotOptions: {
                pie: {
                    donut: {
                        size: '75%'
                    }
                }
            },
            labels: ['Unassigned', 'Overdue'],
            series: [{{unassigned_incidents_count}}, {{open_incidents_thirty_days_count}}],
            legend: {
                show: false
            },
            tooltip: {
                theme: 'datk'
            },
            grid: {
                padding: {
                    top: 20,
                    right: 0,
                    bottom: 0,
                    left: 0
                },
            },
            colors: ["#4680ff", "#2ed8b6"],
            fill: {
                opacity: [1, 1]
            },
            stroke: {
                width: 0,
            }
        }
        let customer_chart = document.querySelector("#customer-chart");
        if ( customer_chart ) {
            var chart = new ApexCharts(customer_chart, options);
            chart.render();
        }
        var options1 = {
            chart: {
                height: 150,
                type: 'donut',
            },
            dataLabels: {
                enabled: false
            },
            plotOptions: {
                pie: {
                    donut: {
                        size: '75%'
                    }
                }
            },
            labels: ['NotUpdated', 'Older'],
            series: [20, 15],
            legend: {
                show: false
            },
            tooltip: {
                theme: 'dark'
            },
            grid: {
                padding: {
                    top: 20,
                    right: 0,
                    bottom: 0,
                    left: 0
                },
            },
            colors: ["#fff", "#2ed8b6"],
            fill: {
                opacity: [1, 1]
            },
            stroke: {
                width: 0,
            }
        }
        let customer_chart1 = document.querySelector("#customer-chart1");
        if ( customer_chart1 ) {
            var chart = new ApexCharts(customer_chart1, options1);
            chart.render();
        }
    })();
    // [ customer-chart ] end
//    // [ incidents-sla-chart ] start
//    (function () {
//        var options = {
//            ajax: {
//              "type": "GET",
//              "url": "{% url 'dashboards:ajax_incidents_graph' %}",
//              "headers": {
//                 "X-CSRFToken": "{{ csrf_token }}"
//              },
//              "error": function (xhr, error, thrown) {
//                alert("Error occurred:\n" + xhr.status + ": " + xhr.statusText);
//              }
//            },
//            chart: {
//                height: 230,
//                type: 'line',
//                toolbar: {
//                    show: false,
//                },
//            },
//            dataLabels: {
//                enabled: false
//            },
//            stroke: {
//                width: 2,
//                curve: 'smooth'
//            },
//            series: [{
//                name: 'Yes',
//                data: 'inc_count'
//            }, {
//                name: 'No',
//                data: 'inc_count'
//            }],
//            legend: {
//                position: 'top',
//            },
//            xaxis: {
//                type: 'datetime',
//                categories: ['2019', '2020', '2021', '2022', '2023'],
//                axisBorder: {
//                    show: false,
//                },
//                label: {
//                    style: {
//                        color: '#ccc'
//                    }
//                },
//            },
//            yaxis: {
//                show: true,
//                min: 10,
//                max: 70,
//                labels: {
//                    style: {
//                        color: '#ccc'
//                    }
//                }
//            },
//            colors: ['#73b4ff', '#59e0c5'],
//            fill: {
//                type: 'gradient',
//                gradient: {
//                    shade: 'light',
//                    gradientToColors: ['#4099ff', '#2ed8b6'],
//                    shadeIntensity: 0.5,
//                    type: 'horizontal',
//                    opacityFrom: 1,
//                    opacityTo: 1,
//                    stops: [0, 100]
//                },
//            },
//            markers: {
//                size: 5,
//                colors: ['#4099ff', '#2ed8b6'],
//                opacity: 0.9,
//                strokeWidth: 2,
//                hover: {
//                    size: 7,
//                }
//            },
//            grid: {
//                borderColor: '#cccccc3b',
//            }
//        }
//        var chart = new ApexCharts(document.querySelector("#incidents-sla-chart"), options);
//        chart.render();
//    })();
//    // [ incidents-sla-chart ] end
}
