var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

socket.on('connect', function () {
    socket.emit('connect_message', {data: 'connected!'});
    subscribe();
});

// 接收消毒车位置参数并显示
socket.on('odom', function (msg) {
    display(msg);
});

socket.on('no_mask_warning', function () {
    toastr.warning("发现未佩戴口罩人员！");
    var no_mask = parseInt(document.getElementById("no_mask").innerText);
    document.getElementById("no_mask").innerText = (no_mask + 1).toString();
})

function subscribe() {
    console.log("click subscribe");
    socket.emit('subscribe', {topic: 'odom'});
}

function publish() {
    console.log("click publish");
    socket.emit('publish', {topic: 'odom', message: 'battery warning'});
}

function unsubscribe() {
    console.log("click unsubscribe");
    socket.emit('unsubscribe', {topic: 'odom', message: ''})
}

function toast() {
    console.log("click toast");
    socket.emit('toast');
}

function hideControl() {
    document.getElementsByClassName("change_camera_direction")[0].style.visibility = "hidden";//隐藏
}

function displayControl() {
    document.getElementsByClassName("change_camera_direction")[0].style.visibility = "visible";//显示
}

function left_direction() {
    console.log("left");
    socket.emit('direction', {topic: 'cmd', message: 4});
}

function forward_direction() {
    console.log("forward");
    socket.emit('direction', {topic: 'cmd', message: 2});
}

function stop_direction() {
    console.log("stop");
    socket.emit('direction', {topic: 'cmd', message: 5});
}

function backward_direction() {
    console.log("backward");
    socket.emit('direction', {topic: 'cmd', message: 8});
}

function right_direction() {
    console.log("right");
    socket.emit('direction', {topic: 'cmd', message: 6});
}

function send_cmd(cmd) {
    // var message = new Paho.MQTT.Message("<" + cmd + " > "); //"<1>", "<2>", ...
    console.log(cmd);
    // message.destinationName = "610_cmd"; //topic
    for (var i = 0; i < 5; i++) {
        // cmd_client.send(message);
        socket.emit('publish', {topic: 'cmd', message: cmd});
    }
}

document.onkeydown = function (event) {
    if (document.getElementsByClassName("change_camera_direction")[0].style.visibility === "visible") {
        // 手动模式
        if (event.key === 'ArrowLeft') { // 按左箭头
            left_direction();
        }
        if (event.key === 'ArrowUp') { // 按上箭头
            forward_direction();
        }
        if (event.key === ' ') { // 按空格
            stop_direction();
        }
        if (event.key === 'ArrowDown') { // 按下箭头
            backward_direction();
        }
        if (event.key === 'ArrowRight') { // 按右箭头
            right_direction();
        }
    }
};
