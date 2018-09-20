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

function visitsToData(visits, period, param, value) {
    var data = [[0, 0]];
    while (data[data.length - 1][0] < S_IN_D) {
        data.push([data[data.length - 1][0] + period * 60, 0])
    }
    for (var v = 0; v < visits.length; v++) {
        for (var d = 0; d < data.length; d++) {
            if ((visits[v].seconds >= data[d][0]) && (visits[v].seconds < data[d + 1][0])) {
                if ((!(param)) || (visits[v][param] == value)) {
                    data[d][1]++
                }

            }
        }
    }
    return data;
}

function clearRowBackgrounds() {
    $("tr").each(function() {
        $(this).removeAttr("style");
    });
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
            color: "#10ac84",
            data: data,
        }],
        plotOptions: {
            column: {
                grouping: false,
                groupPadding: 0.05,
                pointPadding: 0,
                gapSize: 0,
                pointPlacement: "between",
                borderWidth: 0
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
        var subtitle = chart.subtitle.element.innerHTML.slice(7, -8).split(": ");
        console.log(subtitle)
        while (chart.series.length != 0) {
            chart.series[0].remove();
        }
        if (subtitle.length != 2) {
            console.log("Just adding 1")
            chart.addSeries({data: data, type: "column", color: "#10ac84"});
        } else {
            console.log("Adding 2")
            var data2 = visitsToData(visits, parseInt($(this).val()), subtitle[0].toLowerCase(), subtitle[1]);
            chart.addSeries({data: data, type: "column", color: "#10ac8433"});
            chart.addSeries({data: data2, type: "column", color: "#10ac84"});
        }
    })

    $("#clearSecondSeries").click(function() {
        clearRowBackgrounds();
        chart.series[1].remove();
        $(this).addClass("invisible");
        chart.series[0].options.color = "#10ac84";
        chart.series[0].update(chart.series[0].options);
        chart.setTitle(null, {
             text: null
         });
    })

    $(".param-row").click(function() {
        var param = $(this).attr("data-param");
        var value = $(this).find("td:eq(0)").text();

        clearRowBackgrounds();
        $(this).css("background-color", "#10ac8455");

        if (chart.series.length > 1) {
            chart.series[1].remove();
        }
        chart.series[0].options.color = "#10ac8433";
        chart.series[0].update(chart.series[0].options);

        var interval = parseInt($("#chartIntervalSelector").val())

        data = visitsToData(visits, interval, param, value);
        chart.addSeries({data: data, type: "column", color: "#10ac84"});
        chart.setTitle(null, {
             text: param[0].toUpperCase() + param.slice(1) + ": " + value
         });

         $("#clearSecondSeries").removeClass("invisible");
    })
})
