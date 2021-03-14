from controller import create_app

app = create_app('dev')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(threaded=True, host="0.0.0.0")
