var S_IN_D = 24 * 60 * 60;

function secondsToString(s) {
    var hour = Math.floor(s / 3600);
    var minutes = Math.round((s - (hour * 3600)) / 60);
    var suffix = ((hour <= 11) || (hour == 24)) ? "am" : "pm";
    hour = hour > 12 ? hour - 12 : hour;
    hour = hour == 0 ? 12 : hour;
    minutes = minutes == 0 ? "" : ":" + (minutes < 10 ? "0" : "") + minutes
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
    // Update hit count at top of page
    var ips = new Set();
    for (var v = 0; v < visits.length; v++) {
        ips.add(visits[v].IP);
    }
    $(".hit-count").text(
        visits.length + " page visit" + (visits.length == 1 ? "" : "s") +
         " (" + ips.size + " unique IP" + (ips.size == 1 ? "" : "s") + ")"
     );

     $( "#datepicker" ).datepicker({onSelect:function(date) {
         var values = date.split("/");
         values = [values[2]].concat(values.slice(0, 2));
         window.location.href = "?day=" + values.join("-");

     }});

     $('.header-text').on('click', function() {
		$("#datepicker").slideToggle("fast")
	});

    // Frequency tables
    var histograms = $(".histograms")
    var params = ["Path", "Country", "City", "Source"];
    for (var p = 0; p < params.length; p++) {
        var counter = {}
        for (var v = 0; v < visits.length; v++) {
            if (visits[v][params[p].toLowerCase()] in counter) {
                counter[visits[v][params[p].toLowerCase()]]++
            } else {
                counter[visits[v][params[p].toLowerCase()]] = 1
            }
        }
        var data = Object.keys(counter).map(function(key) {
            return [key, counter[key]];
        }).sort(function(a, b) {return b[1] - a[1]});
        var table = $("<table/>").addClass("histogram");;
        $.each(data, function(rowIndex, r) {
            var row = $("<tr class='param-row' data-param='" + params[p].toLowerCase() + "'></tr>");
            $.each(r, function(colIndex, c) {
                row.append($("<td/>").text(c));
            });
            table.append(row);
        });
        table.prepend("<tr><th colspan='2'>" + params[p] + "</th></tr>")
        $(histograms).append(table);
    }

    // Chart
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
        yAxis: {
            title: {
                enabled: false
            },
            allowDecimals: false,
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


    // All hits
    var table = $("#allHitsTable");
    for (var v = 0; v < visits.length; v++) {
        $(table).append("<tr><td>" + secondsToString(visits[v].seconds) + "</td><td>" + visits[v].path + "</td><td>" + visits[v].city + "</td><td>" + visits[v].referer + "</td></tr>")
    }

    // Events
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

        $("html, body").animate({
            scrollTop: $("#visits-chart").parent().offset().top
        }, 800);
    })
})
