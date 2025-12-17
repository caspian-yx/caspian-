from flask import Flask
from app import db  # 数据库实例（在app/__init__.py中初始化）
import os
import sys
from flask import Flask, render_template, session, redirect, url_for, request  # 添加 request 导入

# 初始化Flask应用
app = Flask(__name__,template_folder='app/templates')

# 数据库配置（医药销售管理系统）
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/pharmacy_db?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secure_secret_key'  # 用于flash消息和会话

# 会话配置
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 会话超时时间：1小时（单位：秒）
app.config['SESSION_COOKIE_NAME'] = 'pharmacy_session'  # 会话 Cookie 名称
app.config['SESSION_COOKIE_HTTPONLY'] = True  # 防止 JavaScript 访问 Cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF 防护

# 初始化数据库
db.init_app(app)

# 获取当前文件（run.py）的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 将项目根目录加入 Python 搜索路径
sys.path.insert(0, current_dir)

# 确保 routes 和其子模块中有 __init__.py 文件
try:
    from app.routes.main import main_bp  # 总导航
    from app.routes.material import material_bp  # 物资管理
    from app.routes.material_category import material_category_bp  # 物资分类
    from app.routes.supplier import supplier_bp  # 供应商管理
    from app.routes.inbound import inbound_bp  # 入库管理
    from app.routes.outbound import outbound_bp  # 出库管理
    from app.routes.warehouse import warehouse_bp  # 仓库管理
    from app.routes.unit import unit_bp  # 单位管理
    from app.routes.stock import stock_bp  # 库存管理
    from app.routes.database import database_bp  # 数据库管理
    from app.routes.auth import auth_bp  # 用户认证

except ImportError as e:
    print(f"导入路由模块时出错: {e}")
    sys.exit(1)

app.register_blueprint(main_bp)
app.register_blueprint(material_bp)
app.register_blueprint(material_category_bp)
app.register_blueprint(supplier_bp)
app.register_blueprint(inbound_bp)
app.register_blueprint(outbound_bp)
app.register_blueprint(warehouse_bp)
app.register_blueprint(unit_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(database_bp)
app.register_blueprint(auth_bp)

# 全局登录验证（在每次请求前执行）
@app.before_request
def check_login():
    # 白名单：不需要登录就能访问的路由
    whitelist = [
        'auth.login',           # 登录页面
        'auth.logout',          # 登出
        'auth.init_admin',      # 初始化管理员
        'static'                # 静态文件
    ]

    # 如果访问的是白名单中的路由，直接放行
    if request.endpoint in whitelist:
        return None

    # 如果访问静态文件，直接放行
    if request.path.startswith('/static/'):
        return None

    # 检查是否已登录
    if 'user_id' not in session:
        # 未登录，重定向到登录页
        return redirect(url_for('auth.login', next=request.url))

    return None

@app.route('/')
def index():
    return render_template('index.html') 
# 启动服务
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 确保数据库表存在
    app.run(host='0.0.0.0', port=5000, debug=True)  # 生产环境关闭debug