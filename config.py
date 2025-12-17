import os

class Config:
    # 数据库连接配置（医药销售管理系统）
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/pharmacy_db?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)  # 会话加密
    # 强制关闭连接池，避免超时（针对Windows环境）
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}