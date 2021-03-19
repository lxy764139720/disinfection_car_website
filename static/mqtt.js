namespace = '/disinfection_car';
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

socket.on('connect', function () {
    socket.emit('connect_message', {data: 'connected!'});
});

socket.on('mqtt_message', function (msg) {
    console.log('mqtt_message')
    console.log(msg);
});

function subscribe() {
    console.log("click subscribe");
    socket.emit('subscribe', {topic: 'warning'});
}

function publish() {
    console.log("click publish");
    socket.emit('publish', {topic: 'warning', message: 'battery warning'});
}
