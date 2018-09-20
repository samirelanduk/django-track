var S_IN_D = 24 * 60 * 60;

function secondsToString(s) {
    var hour = Math.floor(s / 3600);
    var minutes = (s - (hour * 3600)) / 60;
    var suffix = ((hour <= 11) || (hour == 24)) ? "am" : "pm";
    hour = hour > 12 ? hour - 12 : hour;
    hour = hour == 0 ? 12 : hour;
    minutes = minutes == 0 ? "" : ":" + minutes
    return hour + minutes + " " + suffix;
}

function visitsToData(visits, period) {
    var data = [[0, 0]];
    while (data[data.length - 1][0] < S_IN_D) {
        data.push([data[data.length - 1][0] + period * 60, 0])
    }
    for (var v = 0; v < visits.length - 1; v++) {
        for (var d = 0; d < data.length; d++) {
            if ((visits[v].seconds > data[d][0]) && (visits[v].seconds < data[d + 1][0])) {
                data[d][1]++
            }
        }
    }
    return data;
}





$(document).ready(function() {

    var data = visitsToData(visits, 30);

    var chart = Highcharts.chart("visits-chart", {
        title: {
            text: today,
        },
        credits: {
            enabled: false
        },
        xAxis: {
            tickInterval: 3600,
            labels: {
                step: 3,
                formatter: function() {
                    return secondsToString(this.value)
                }
            },
            min: 0,
            max: S_IN_D,
            title: {
                enabled: true,
                text: "Time"
            },
        },
        series: [{
            type: "column",
            data: data,
        }],
        plotOptions: {
            column: {
                groupPadding: 0,
                pointPadding: 0,
                gapSize: 0,
                pointPlacement: "between"
            }
        },
        tooltip: {
            formatter: function() {
                var start = this.x;
                var end = this.series.xData[this.series.xData.indexOf(this.x) + 1]
                text = "<b>" + secondsToString(start) + " - " + secondsToString(end) + "</b>"
                text += "<br>" + this.y + " visit" + (this.y == 1 ? "" : "s")
                return text
            }
        },
        legend: {
            enabled: false
        },
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    xAxis: {
                        labels: {
                            step: 6
                        }
                    },
                }
            }]
        }
    });

    $("#chartIntervalSelector").change(function() {
        var data = visitsToData(visits, parseInt($(this).val()));
        chart.series[0].setData(data);
    })
})
