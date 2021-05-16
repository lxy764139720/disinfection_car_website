from flask import session, redirect, url_for, render_template, request, jsonify, make_response
from config import create_app

app, mqtt, socketio = create_app('pro')


# 主页
@app.route('/disinfection_car/home')
def index():
    # 模板渲染
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))
    return render_template("index.html")


# 登录
@app.route("/disinfection_car/login", methods=["GET", "POST"])
def login():
    username = session.get("username")

    if username:
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("login.html")
    # 获取参数
    username = request.form.get("username")
    password = request.form.get("password")
    # 校验参数
    if not all([username, password]):
        return render_template("login.html", errmsg="参数不足")

    # 校验对应的管理员用户数据
    if username == "admin" and password == "admin":
        # 验证通过
        session["username"] = username
        return redirect(url_for("index"))

    return render_template("login.html", errmsg="用户名或密码错误")


# 退出登录
@app.route("/disinfection_car/logout")
def logout():
    # 删除session数据
    session.pop("username", None)
    # 返回登录页面
    return redirect(url_for("login"))


@app.route('/rtmp_address')
def add_numbers():
    video_address = 'http://120.55.55.230:8181/live?port=1965&app=live&stream=cs'
    res = make_response(jsonify(result=video_address))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res


@socketio.on('connect_message')
def handle_my_custom_event(json_data):
    print('connect_message')
    print('已连接前端socket')


# 前端发来"订阅"消息，订阅odom主题
@socketio.on('subscribe')
def handle_subscribe(json_data):
    # data = json.loads(json_data)
    print('已订阅主题')
    mqtt.subscribe(json_data['topic'])


# 前端发来"发布"消息，转发到mqtt服务器
@socketio.on('publish')
def handle_publish(json_data):
    # data = json.loads(json_data)
    print('向MQTT发送消息：')
    print(json_data)
    mqtt.publish(json_data['topic'], json_data['message'])


@socketio.on('toast')
def handle_toast():
    socketio.emit('no_mask_warning')


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print('已连接MQTT服务器')
    mqtt.subscribe('warning')


# mqtt服务器发来消息，转发到前端
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(topic=message.topic, payload=message.payload.decode())
    print(message.topic, message.payload)
    if message.topic == 'odom':
        socketio.emit('odom', data=data)
    if message.topic == 'no_mask_warning':
        socketio.emit('no_mask_warning')
    if message.topic == 'car_sensor_temperature':
        socketio.emit('car_sensor_temperature', data=data)
    if message.topic == 'car_sensor_humidity':
        socketio.emit('car_sensor_humidity', data=data)
    if message.topic == 'car_sensor_capacity':
        socketio.emit('car_sensor_capacity', data=data)
    if message.topic == 'car_sensor_voltage':
        socketio.emit('car_sensor_voltage', data=data)


@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


if __name__ == '__main__':
    socketio.run(threaded=True, port=5000, host="0.0.0.0")
    # socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)
