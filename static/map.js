var img = new Image();
var last_x = 546;
var last_y = 20;

function initDraw() {
    var canvas = document.getElementById('map');
    if (!canvas.getContext) return;
    var ctx = canvas.getContext("2d");
    var map = new Image();
    var img = new Image();
    map.onload = function () {
        ctx.drawImage(map, 0, 0, 640, 440);
    }
    img.onload = function () {
        ctx.drawImage(img, 546, 20, 20, 20);
    }
    map.src = "../static/images/map.png";
    img.src = "../static/images/location.png"; // 设置图片源地址
}

function display(msg) {
    console.log('odom');
    console.log(msg);
    // ((?<=<x:).+)(.+(?=,))
    // ((?<=,).+)(.+(?=>))
    var x = parseFloat(msg.payload.match(/((?<=<x).+)(.+(?=,))/));
    var y = parseFloat(msg.payload.match(/((?<=, y).+)(.+(?=>))/));

    var canvas = document.getElementById('map');
    if (!canvas.getContext) return;
    var ctx = canvas.getContext("2d");

    var x_img = 78.83 * x - 31.24;
    console.log("x:" + x.toString());
    var y_img = -61.59 * y - 0.324;
    console.log("y:" + y.toString());
    img.onload = function () {
        ctx.clearRect(last_x, last_y, 20, 20);
        ctx.drawImage(img, x_img, y_img, 20, 20);
        last_x = x_img;
        last_y = y_img;
    }
    img.src = "../static/images/location.png"; // 设置图片源地址
}