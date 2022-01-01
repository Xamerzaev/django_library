$(document).ready(function () {

    function GetDataDashboard() {
        $.ajax({
            data: 'phase=' + $('#phase').val(),
            url: '/polls/dashboard/',
            dataType: 'json',
            async: false,
            complete: function (response) {
                values = response.responseJSON;
            }
        });
        return values
    }


    function CreateDashboard(values) {

        var colors = Highcharts.getOptions().colors,
            browserData = [],
            versionsData = [],
            i,
            dataLen = Object.keys(values).length,
            drillDataLen,
            brightness;

        // Build the data arrays
        var x = 0;
        for (i = 0; i < dataLen; i += 1) {

            if (values[i] != '') {

                browserData.push({
                    name: i,
                    y: values[i]['len'] * 10,
                    color: colors[x],
                    extra: 'Время:' + i + ' часов'
                });

                drillDataLen = Object.keys(values[i]).length;
                var jj = 0;
                for (var prop in values[i]) {
                    if (prop == 'len') {
                        continue
                    }
                    brightness = 0.2 - (jj / drillDataLen) / 5;

                    versionsData.push({
                        name: prop,
                        y: values[i][prop].length * 10,
                        color: Highcharts.Color(colors[x]).brighten(brightness).get(),
                        extra: 'Проголосовали: ' + values[i][prop]
                    });
                    jj += 1;
                }
                x += 1;
                if (x == 10) {
                    x = 0;
                }
            }

        }

        // Create the chart
        Highcharts.chart('container', {
            chart: {
                type: 'pie'
            },
            title: {
                text: 'Итоги голосования'
            },

            plotOptions: {
                pie: {
                    shadow: false,
                    center: ['50%', '50%']
                }
            },

            tooltip: {
                formatter: function () {
                    return '<b>' + this.point.extra + '</b>';
                }
            },

            series: [{
                name: 'Время',
                data: browserData,
                size: '60%',
                dataLabels: {
                    formatter: function () {
                        return this.y > 5 ? this.point.name : null;
                    },
                    color: '#ffffff',
                    distance: -100
                }
            }, {
                name: 'Мероприятия',
                data: versionsData,
                size: '80%',
                innerSize: '60%',
                dataLabels: {
                    formatter: function () {
                        // display only if larger than 1
                        return this.y > 1 ? 'Мероприятие: <b>' + this.point.name + '</b>' : null;
                    }
                },
                id: 'versions'
            }],
            responsive: {
                rules: [{
                    condition: {
                        maxWidth: 400
                    },
                    chartOptions: {
                        series: [{
                            id: 'versions',
                            dataLabels: {
                                enabled: false
                            }
                        }]
                    }
                }]
            }
        });

    }

    var values = GetDataDashboard();
    CreateDashboard(values);

});