import logging
from datetime import timedelta


class Config:
    # 调试模式
    DEBUG = True
    # session加密秘钥
    SECRET_KEY = "disinfection_car"
    # session过期时间
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)


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
