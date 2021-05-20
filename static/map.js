var img = new Image();
var last_x = 546;
var last_y = 20;

function initDraw() {
    var canvas = document.getElementById('map');
    if (!canvas.getContext) return;
    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // var map = new Image();
    // var img = new Image();
    var goal = new Image();
    canvas.onmousedown = function (e) {
        if (mode === 'focus') {
            var canvas_position = getPointOnCanvas(canvas, e.pageX, e.pageY);
            canvas_x = canvas_position.x;
            canvas_y = canvas_position.y;
            ctx.drawImage(goal, canvas_x, canvas_y, 20, 20);
        }
    }
    // map.onload = function () {
    //     ctx.drawImage(map, 0, 0, 640, 440);
    // }
    // img.onload = function () {
    //     ctx.drawImage(img, 30, 30, 20, 20);
    // }
    // map.src = "../static/images/map.png";
    // img.src = "../static/images/location.png"; // 设置图片源地址
    goal.src = "../static/images/goal.png"
}

function getPointOnCanvas(canvas, x, y) {
    var bbox = canvas.getBoundingClientRect();
    return {
        x: x - bbox.left * (canvas.width / bbox.width),
        y: y - bbox.top * (canvas.height / bbox.height)
    };
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