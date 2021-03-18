namespace = '/disinfection_car';
var buttonSubscribe = document.getElementById("subscribe");
var buttonPublish = document.getElementById("publish");
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
console.log(location.protocol + '//' + document.domain + ':' + location.port);

socket.on('connect', function () {
    socket.emit('my_event', {data: 'I\'m connected!'});
});

socket.on('my_response', function (msg) {
    console.log(msg.count + ': ' + msg.data);
    // $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
});

function subscribe() {
    console.log("subscribe");
    socket.emit('my_event', {topic: 'hello'});
}

function publish() {
    console.log("publish");
    socket.emit('publish', {topic: 'hello', message: 'hi'});
}
