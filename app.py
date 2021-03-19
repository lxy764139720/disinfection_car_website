from flask import session, redirect, url_for, render_template, Response, request, jsonify
from utils.camera import VideoCamera
from config import create_app
import json
from flask import Flask, render_template

app, mqtt, socketio = create_app('dev')
video_camera = None
global_frame = None


@app.route('/')
def hello_world():
    return 'Hello World!'


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


# 视频流
@app.route('/disinfection_car/video_viewer')
def video_viewer():
    # 模板渲染
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


# # 录制状态
# @app.route('/disinfection_car/record_status', methods=['POST'])
# def record_status():
#     global video_camera
#     if video_camera is None:
#         video_camera = VideoCamera()
#
#     json = request.get_json()
#
#     status = json['status']
#
#     if status == "true":
#         video_camera.start_record()
#         return jsonify(result="started")
#     else:
#         video_camera.stop_record()
#         return jsonify(result="stopped")


# 获取视频流
def video_stream():
    global video_camera
    global global_frame

    if video_camera is None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.get_inferred_frame('', conf_thresh=0.5)

        if frame is not None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')


@socketio.on('connect_message')
def handle_my_custom_event(json_data):
    print('connect_message')
    print(json_data)


# @socketio.on('message')
# def handle_my_custom_event(data):
#     print("message")
#     print('received json: ' + data)
#
#
# @socketio.on('json')
# def handle_my_custom_event(json_data):
#     print("json")
#     print('received json: ' + str(json_data))


# 前端发来"订阅"消息，订阅topic主题
@socketio.on('subscribe')
def handle_subscribe(json_data):
    # data = json.loads(json_data)
    print('订阅')
    print(json_data)
    print(type(json_data))
    print(json_data['topic'])
    mqtt.subscribe(json_data['topic'])


# 前端发来"发布"消息，转发到mqtt服务器
@socketio.on('publish')
def handle_publish(json_data):
    # data = json.loads(json_data)
    print('发布')
    print(json_data)
    mqtt.publish(json_data['topic'], json_data['message'])


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print('on_connect')
    mqtt.subscribe('warning')


# mqtt服务器发来消息，转发到前端
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(message)
    socketio.emit('mqtt_message', data=data)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


if __name__ == '__main__':
    # app.run(threaded=True, host="0.0.0.0")
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)
