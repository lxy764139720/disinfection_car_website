import logging
from logging.handlers import RotatingFileHandler
import eventlet
from flask import Flask
from datetime import timedelta
from flask_mqtt import Mqtt
from flask_socketio import SocketIO


class Config:
    # 调试模式
    DEBUG = True
    # session加密秘钥
    SECRET_KEY = "disinfection_car"
    # session过期时间
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    TEMPLATES_AUTO_RELOAD = True
    MQTT_BROKER_URL = '106.15.92.226'
    MQTT_BROKER_PORT = 8083
    MQTT_USERNAME = ''
    MQTT_PASSWORD = ''
    MQTT_KEEPALIVE = 5
    MQTT_TLS_ENABLED = False


class DevelopmentConfig(Config):
    # 开发模式配置
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    # 上线配置
    # 关闭调试
    DEBUG = False
    LOG_LEVEL = logging.ERROR  # 日志级别


# 配置字典，键：配置
config_dict = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig
}


# 设置日志(目的是将flask默认的日志和自定义的日志保存到文件中)
def setup_log(log_level):
    # 设置日志的记录等级
    logging.basicConfig(level=log_level)  # 根据配置类型设置日志等级

    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(pathname)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


# 工厂函数: 由外界提供物料, 在函数内部封装对象的创建过程
def create_app(config_type):  # 封装web应用的创建过程
    eventlet.monkey_patch()
    # 根据类型取出对应的配置子类
    config_class = config_dict[config_type]
    app = Flask(__name__)
    app.config.from_object(config_class)
    mqtt = Mqtt(app)
    socketio = SocketIO(app)

    # 设置日志
    setup_log(config_class.LOG_LEVEL)

    return app, mqtt, socketio
