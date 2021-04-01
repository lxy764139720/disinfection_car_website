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
    socket.emit('subscribe', {topic: 'topic'});
}

function publish() {
    console.log("click publish");
    socket.emit('publish', {topic: 'topic', message: 'battery warning'});
}

function unsubscribe() {
    console.log("click unsubscribe");
    socket.emit('unsubscribe', {topic: 'topic', message: ''})
}

function hideControl() {
    document.getElementsByClassName("change_camera_direction")[0].style.visibility = "hidden";//隐藏
}

function displayControl() {
    document.getElementsByClassName("change_camera_direction")[0].style.visibility = "visible";//显示
}
