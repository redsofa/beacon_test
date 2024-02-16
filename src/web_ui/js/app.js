// The source in this file are adapted from the two examples in the follwing URLs: 
//
// https://www.highcharts.com/demo/highcharts/gauge-dual
// https://github.com/stackhero-io/mqttWebsocketGettingStarted/blob/master/src/index.html
$(function(){
    const url = 'ws://jetson:9001/mqtt';
    const topic = 'i10';
    const username = 'admin';
    const password = 'admin';
    var cnt = 0;
    const client = mqtt.connect(url, { username, password });

    function drawTemperatureGauge(){
	return Highcharts.chart('chart', {
	    chart: {
		type: 'gauge',
		alignTicks: false,
		plotBackgroundColor: null,
		plotBackgroundImage: null,
		plotBorderWidth: 0,
		plotShadow: false,
	    },

	    title: {
		text: 'i10 Beacon'
	    },

	    pane: {
		startAngle: -150,
		endAngle: 150
	    },

	    yAxis: [{
		min: -50,
		max: 50,
		lineColor: 'red',
		tickColor: '#339',
		minorTickColor: '#339',
		offset: -25,
		lineWidth: 2,
		labels: {
		    distance: -20,
		    rotation: 'auto'
		},
		tickLength: 5,
		minorTickLength: 5,
		endOnTick: false
	    }, 
	    ],

	    series: [{
		name: 'Temp',
		data: [0],
		dataLabels: {
		    format: '<span style="color:#339">{y} &#176 Celcius</span><br/>',
		    backgroundColor: {
			linearGradient: {
			    x1: 0,
			    y1: 0,
			    x2: 0,
			    y2: 1
			},
			stops: [
			    [0, '#DDD'],
			    [1, '#FFF']
			]
		    }
		},
		tooltip: {
		    valueSuffix: ' Degrees'
		}
	    }]

	});
    }

    client.on('error', function (error) {
	consoleAdd('Error: ' + error);
    });

    client.on('close', function (){
	consoleAdd('Connection has been closed');
    });

    client.on('reconnect', function () {
	consoleAdd('Reconnecting...');
    });

    client.on('connect', function () {
        consoleAdd('Connected!');
	client.subscribe(topic, function (err, res) {
	    if (err) {
		consoleAdd('Error when subscribing to topic ' + topic + ': ' + err);
		return;
	    }
	})
    });

    client.on('message', function (topic, message) {
	cnt = cnt + 1
	consoleAdd( cnt + ' - Messages received on topic "' + topic + '"  - Message : ' + message);
	incAllPointsCount(cnt);
        const pMsg = JSON.parse(message);
	const point = tempGauge.series[0].points[0];
	point.update(pMsg.temp);
    });

    function incAllPointsCount(count){
        $('#all_points').text(count);
    }

    const consoleAdd = function (text) {
	const main = document.getElementById('mqtt_msg');
	main.innerHTML = text + '<br />';
	main.scrollTop = main.scrollHeight;
    }

    tempGauge = drawTemperatureGauge();
    consoleAdd('Connecting to MQTT server ' + url + '...');
});
