function response_handler() {

    var socket = io('http://' + document.domain + ':' + location.port);

    // listen for mqtt_message events
    // when a new message is received, log and append the data to the page
    socket.on('events', function (data) {
        console.log(data);
        var payload = JSON.parse(data);
        response_management(payload);

        //var text = '(' + data['topic'] + ' qos: ' + data['qos'] + ') ' + data['payload'];
        //$('#subscribe_messages').append(text + '<br><br>');
    });

    function init() {
        if (window.location.pathname == "/dashboard") {
            socket.emit('request_data', JSON.stringify({'operations': 'places'}));
            socket.emit('request_data', JSON.stringify({'operations': 'absolute_counting'}));
            socket.emit('request_data', JSON.stringify({'operations': 'counting_hour'}));
            socket.emit('request_data', JSON.stringify({'operations': 'counting_day'}));
        } else if (window.location.pathname == "/dashboard_spiagge") {
            socket.emit('request_data_spiagge', JSON.stringify({'operations': 'places'}));
            socket.emit('request_data_spiagge', JSON.stringify({'operations': 'absolute_counting'}));
            socket.emit('request_data_spiagge', JSON.stringify({'operations': 'counting_hour'}));
            socket.emit('request_data_spiagge', JSON.stringify({'operations': 'counting_day'}));
        }

    }

    init();

    function response_management(data) {
        switch (data['operation']) {
            case "places":
                places(data['payload']);
                break;
            case "absolute_counting":
                absolute_counting(data['payload']);
                break;
            case "counting_hour":
                counting_hour(data['payload']);
                break;
            case "counting_day":
                counting_day(data['payload']);
                break;

        }
    }


    function absolute_counting(data) {
        $("#hour").text(data['hour']);
        $("#day").text(data['day']);
        $("#week").text(data['week']);

        var value =parseInt(data['hour']);
        var max_value = parseInt(20000 / 20);

        if (value < max_value) {
            $('#covid-19').css('background-color', 'rgba(168, 224, 95,1)');
            $('#distancing-respect').text('Respected').css('color', 'rgba(5,114,78,1)');
            $('#covid-icon').css('color', 'rgba(5,114,78,1)')
        } else {
            $('#covid-19').css('background-color', 'rgba(200, 0, 0,1)');
            $('#distancing-respect').text('Overcrowded').css('color', 'rgb(83,2,2)');
            $('#covid-icon').css('color', 'rgb(83,2,2)')
        }

    }


    function places(data) {

        var polar_data = [];
        var polar_labels = [];

        data.forEach(function (e) {
            $("#place_table").append('<tr><th scope="row" style="color: lightgray;">' + e['position'] + '</th><td style="color: lightgray; font-size: 80%">' + e['address'] + '</td></tr>');
            polar_data.push(e['hints']);
            polar_labels.push('Place #' + e['position'])
        });

        var ctx_polar = document.getElementById('polar_places').getContext('2d');

        var data_chart = {
            labels: polar_labels,
            datasets: [{
                data: polar_data,
                backgroundColor: [
                    'rgba(108, 159, 67, 0.8)',
                    'rgba(14,174,255,0.8)',
                    'rgba(37,0,165,0.8)',
                    'rgba(49,100,171,0.8)',
                    'rgba(5,114,78,0.8)'
                ],
                borderColor: [
                    'rgba(108, 159, 67, 1)',
                    'rgba(14,174,255,1)',
                    'rgba(37,0,165,1)',
                    'rgba(49,100,171,1)',
                    'rgba(5,114,78,1)'
                ]
            }]
        };

        var chartOptions = {
            legend: {
                display: false
            },
            responsive: true,
            title: {
                display: true,
                text: 'Record in top 5 places'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            }

        };

        var polarAreaChart = new Chart(ctx_polar, {
            type: 'bar',
            data: data_chart,
            options: chartOptions
        });
    }


    function counting_hour(data) {
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data['labels'],
                datasets: [{
                    data: data['values'],
                    backgroundColor: [

                        'rgba(56, 120, 199, 0.8)',
                        'rgba(56, 120, 199, 0.8)',
                        'rgba(56, 120, 199, 0.8)',
                        'rgba(56, 120, 199, 0.8)',
                        'rgba(56, 120, 199, 0.8)',
                        'rgba(56, 120, 199, 0.8)',

                    ],
                    borderColor: [
                        'rgba(56, 120, 199, 1)',
                        'rgba(56, 120, 199, 1)',
                        'rgba(56, 120, 199, 1)',
                        'rgba(56, 120, 199, 1)',
                        'rgba(56, 120, 199, 1)',
                        'rgba(56, 120, 199, 1)',
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: 'Last Hour'
                },
                legend: {
                    display: false
                },

                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });

    }

    function counting_day(data) {
        var ctx2 = document.getElementById('day_chart').getContext('2d');
        var myLineChart2 = new Chart(ctx2, {
            type: 'line',
            data: {
                labels: data['labels'],
                datasets: [{
                    backgroundColor: 'rgba(56, 120, 199, 0.2)',
                    borderColor: 'rgba(56, 120, 199, 1)',
                    data: data['values'],
                }
                ]
            },
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: 'Last Day'
                },
                legend: {
                    display: false
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                },
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
                scales: {
                    yAxes: {
                        ticks: {
                            scaleOverride: true,
                            scaleSteps: Math.round(Math.max.apply(null, data['values']) / 3),
                            scaleStepWidth: Math.max.apply(null, data['values']),
                            scaleStartValue: 0
                        }
                    }
                }
            }
        });
    }


}
