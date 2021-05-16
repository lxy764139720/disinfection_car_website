var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
var mode = 'overall'; // overall：全面消杀，focus：重点消杀，manual：手动控制

socket.on('connect', function () {
    socket.emit('connect_message', {data: 'connected!'});
    subscribe();
});

// 接收消毒车位置参数并显示
socket.on('odom', function (msg) {
    display(msg);
});

socket.on('no_mask_warning', function (msg) {
    toastr.clear();
    toastr.warning("发现未佩戴口罩人员！");
    var no_mask = parseInt(document.getElementById("no_mask").innerText);
    document.getElementById("no_mask").innerText = (no_mask + 1).toString();
})

socket.on('car_sensor_temperature', function (msg) {
    var temperature_element = document.getElementById("temperature");
    var temperature = Math.round(parseFloat(msg.payload) / 100);
    if (temperature > 100)
        temperature = 100;
    temperature_element.innerText = temperature + '℃';
    temperature_element.style.width = temperature + '%';
})

socket.on('car_sensor_humidity', function (msg) {
    var humidity_element = document.getElementById("humidity");
    var humidity = Math.round(parseFloat(msg.payload) / 100);
    if (humidity > 100)
        humidity = 100;
    humidity_element.innerText = humidity + '%';
    humidity_element.style.width = humidity + '%';
})

socket.on('car_sensor_capacity', function (msg) {
    var humidity_element = document.getElementById("capacity");
    var capacity = Math.round(parseFloat(msg.payload) / 100);
    if (capacity > 100)
        capacity = 100;
    humidity_element.innerText = capacity + '%';
    humidity_element.style.width = capacity + '%';
})

socket.on('car_sensor_voltage', function (msg) {
    var battery_element = document.getElementById("chassis_power");
    var chassis_power = Math.round(parseFloat(msg.payload) / 100);
    if (chassis_power > 100)
        chassis_power = 100;
    battery_element.innerText = chassis_power + '%';
    battery_element.style.width = chassis_power + '%';
})

function subscribe() {
    console.log("click subscribe");
    socket.emit('subscribe', {topic: 'odom'});
    socket.emit('subscribe', {topic: 'no_mask_warning'});
    socket.emit('subscribe', {topic: 'car_sensor_temperature'});
    socket.emit('subscribe', {topic: 'car_sensor_humidity'});
    socket.emit('subscribe', {topic: 'car_sensor_capacity'});
    socket.emit('subscribe', {topic: 'car_sensor_voltage'});
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

function overallMode() {
    mode = 'overall';
    toastr.clear();
    toastr.success('已切换为全面消杀模式');
    initDraw();
    document.getElementsByClassName("control_direction")[0].style.visibility = "hidden";//隐藏
    send_cmd('f');
}

function focusMode() {
    mode = 'focus';
    toastr.clear();
    var focus_button = document.getElementById("focus_mode");
    if (focus_button.innerText === "重点消杀模式") {
        toastr.success('请在地图中点选确认', '已切换为重点消杀模式');
        focus_button.innerText = "确认消杀点位";
        document.getElementsByClassName("control_direction")[0].style.visibility = "hidden";//隐藏
    }
    else if (focus_button.innerText === "确认消杀点位") {
        toastr.success('已发送重点消杀点位', '已切换为重点消杀模式');
        focus_button.innerText = "重点消杀模式";
        document.getElementsByClassName("control_direction")[0].style.visibility = "hidden";//隐藏
    }
}

function manualMode() {
    mode = 'manual';
    toastr.clear();
    toastr.success('请使用鼠标或键盘进行控制', '已切换为人工控制模式');
    initDraw();
    document.getElementsByClassName("control_direction")[0].style.visibility = "visible";//显示
}

function openVideo() {
    console.log("open video");
    socket.emit('publish', {topic: 'cmdv', message: 'v'})
}

function left_direction() {
    toastr.clear();
    toastr.success('左转');
    console.log("left");
    socket.emit('publish', {topic: 'cmd', message: 4});
}

function forward_direction() {
    toastr.clear();
    toastr.success('前进');
    console.log("forward");
    socket.emit('publish', {topic: 'cmd', message: 2});
}

function stop_direction() {
    toastr.clear();
    toastr.success('停止');
    console.log("stop");
    socket.emit('publish', {topic: 'cmd', message: 5});
}

function backward_direction() {
    toastr.clear();
    toastr.success('后退');
    console.log("backward");
    socket.emit('publish', {topic: 'cmd', message: 8});
}

function right_direction() {
    toastr.clear();
    toastr.success('右转');
    console.log("right");
    socket.emit('publish', {topic: 'cmd', message: 6});
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
    if (document.getElementsByClassName("control_direction")[0].style.visibility === "visible") {
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
