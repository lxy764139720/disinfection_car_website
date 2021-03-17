from flask import session, redirect, url_for, render_template, Response, request, jsonify
from utils.camera import VideoCamera
from config import create_app

app = create_app('dev')

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


if __name__ == '__main__':
    app.run(threaded=True, host="0.0.0.0")
