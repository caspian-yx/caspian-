# caspian-
上传个人所完成的简单项目

# 医药销售管理系统

## 项目简介

这是一个基于 Flask 框架开发的**医药销售管理系统**（Pharmacy Sales Management System），用于管理药品、供应商、采购、销售、库存等业务流程。系统采用 B/S 架构，提供完整的 Web 界面操作。

### 核心特性

- 🏥 **药品管理**：药品信息、分类、单位管理
- 📦 **采购管理**：供应商管理、采购入库、审核流程
- 💰 **销售管理**：销售出库、客户管理
- 🏢 **仓库管理**：多仓库支持、库存盘点
- 📊 **统计报表**：入库统计、库存汇总
- 💾 **数据库管理**：数据导入导出、备份恢复
- 🔐 **用户认证**：登录验证、密码管理、会话管理

---

## 技术栈

### 后端技术
- **Flask 2.x**：轻量级 Web 框架
- **Flask-SQLAlchemy**：ORM 框架
- **PyMySQL**：MySQL 数据库驱动
- **Werkzeug**：密码哈希加密

### 前端技术
- **Bootstrap 5**：响应式 UI 框架
- **Jinja2**：模板引擎
- **原生 JavaScript**：交互逻辑

### 数据库
- **MySQL 8.0+**：关系型数据库
- **字符集**：UTF-8MB4（支持中文和特殊字符）

---

## 数据库设计

### ER 图概览

系统包含 12 个核心数据表，主要关系如下：

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│  Supplier   │       │   Purchase   │       │  Warehouse  │
│  供应商     │──────▶│   采购单     │◀──────│   仓库      │
└─────────────┘       └──────────────┘       └─────────────┘
                             │
                             ▼
                     ┌──────────────┐
                     │PurchaseDetail│
                     │  采购明细    │
                     └──────────────┘
                             │
                             ▼
                      ┌─────────────┐
                      │  Medicine   │◀──┐
                      │   药品      │   │
                      └─────────────┘   │
                             │          │
                             ▼          │
                      ┌──────────────┐  │
                      │  SaleDetail  │  │
                      │  销售明细    │  │
                      └──────────────┘  │
                             │          │
                             ▼          │
                      ┌─────────────┐   │
                      │    Sale     │   │
                      │   销售单    │   │
                      └─────────────┘   │
                                        │
                      ┌─────────────────┘
                      │
               ┌──────────────┐
               │MedicineCategory│
               │   药品分类     │
               └──────────────┘
```

### 核心数据表

| 表名 | 说明 | 主键 | 外键 |
|------|------|------|------|
| `medicine` | 药品信息表 | id | category_id, unit_id |
| `medicine_category` | 药品分类表 | id | - |
| `unit` | 计量单位表 | id | - |
| `supplier` | 供应商表 | id | - |
| `warehouse` | 仓库表 | id | - |
| `purchase` | 采购单表 | purchase_id | supplier_id, warehouse_id |
| `purchase_detail` | 采购明细表 | id | purchase_id, medicine_id |
| `sale` | 销售单表 | sale_id | warehouse_id |
| `sale_detail` | 销售明细表 | id | sale_id, medicine_id |
| `stock_check` | 盘点单表 | check_id | - |
| `stock_check_detail` | 盘点明细表 | id | check_id, medicine_id |
| `user` | 用户表 | id | - |

### 关键字段说明

#### Medicine（药品表）
```sql
- id: 主键
- name: 药品名称
- generic_name: 通用名称
- approval_number: 批准文号（唯一）
- specification: 规格（如：10mg*24片）
- dosage_form: 剂型
- manufacturer: 生产厂家
- category_id: 分类ID（外键）
- unit_id: 单位ID（外键）
- is_prescription: 是否处方药（0=OTC，1=处方药）
- stock: 当前库存
- min_stock: 最低库存预警
- retail_price: 零售价
- 唯一约束: (name, specification)
```

#### Purchase（采购单）
```sql
- purchase_id: 采购单号（主键，如：PC20231114001）
- supplier_id: 供应商ID
- warehouse_id: 仓库ID
- purchase_date: 采购日期
- total_amount: 总金额
- audit_status: 审核状态（0=待审核，1=已审核，2=已驳回）
```

#### User（用户表）
```sql
- id: 主键
- username: 用户名（唯一）
- password: 密码（哈希存储）
- real_name: 真实姓名
- role: 角色
- is_active: 是否启用
- last_login: 最后登录时间
```

---

## 项目结构

```
数据库课设/
├── app/                          # 应用主目录
│   ├── __init__.py              # 应用初始化
│   ├── models.py                # 数据模型（12个表）
│   ├── routes/                  # 路由模块
│   │   ├── __init__.py
│   │   ├── auth.py             # 用户认证（登录、登出、修改密码）
│   │   ├── main.py             # 主路由
│   │   ├── material.py         # 药品管理
│   │   ├── material_category.py # 药品分类管理
│   │   ├── unit.py             # 单位管理
│   │   ├── supplier.py         # 供应商管理
│   │   ├── warehouse.py        # 仓库管理
│   │   ├── inbound.py          # 采购入库管理
│   │   ├── outbound.py         # 销售出库管理
│   │   ├── stock.py            # 库存盘点管理
│   │   ├── report.py           # 报表统计
│   │   ├── api.py              # RESTful API
│   │   └── database.py         # 数据库管理（导入/导出）
│   ├── templates/               # Jinja2 模板
│   │   ├── index.html          # 主页
│   │   ├── login.html          # 登录页
│   │   ├── change_password.html # 修改密码页
│   │   ├── database_manage.html # 数据库管理页
│   │   ├── material_*.html     # 药品相关页面
│   │   ├── supplier_*.html     # 供应商相关页面
│   │   ├── inbound_*.html      # 入库相关页面
│   │   ├── outbound_*.html     # 出库相关页面
│   │   └── ...                 # 其他模板
│   └── static/                  # 静态资源
│       └── js/
│           └── index.js
├── backups/                     # 数据库备份目录
├── config.py                    # 配置文件
├── run.py                       # 应用启动入口
├── data_init.py                # 初始化测试数据
├── 创建数据库.sql              # 数据库创建脚本
├── 更新仓库唯一约束.sql        # 数据库更新脚本
└── README.md                    # 项目文档（本文件）
```

---

## 功能模块详解

### 1. 用户认证模块（auth.py）

#### 登录功能
- 路由：`/auth/login`
- 功能：
  - 用户名密码验证
  - 密码哈希验证（Werkzeug）
  - 会话管理（Session）
  - 最后登录时间记录
  - 登录失败友好提示

#### 登出功能
- 路由：`/auth/logout`
- 功能：清除会话，跳转登录页

#### 修改密码
- 路由：`/auth/change_password`
- 功能：
  - 验证原密码
  - 新密码长度验证（至少6位）
  - 两次密码一致性验证
  - 密码哈希存储

#### 初始化管理员
- 路由：`/auth/init_admin`
- 功能：创建默认管理员账户
- 默认账户：`admin / admin123`

#### 全局登录验证
- 使用 `@app.before_request` 装饰器
- 白名单机制（登录页、静态资源除外）
- 会话超时时间：1小时

### 2. 药品管理模块（material.py）

#### 药品列表
- 路由：`/material/list`
- 功能：
  - 分页显示药品
  - 多字段搜索（名称、分类、规格）
  - 库存预警标识

#### 新增药品
- 路由：`/material/add`
- 功能：
  - 必填字段验证（名称、规格、分类、单位）
  - 唯一性验证（名称+规格组合）
  - 友好错误提示
  - 表单数据保留

#### 编辑药品
- 路由：`/material/edit/<id>`
- 功能：
  - 数据回显
  - 唯一性验证
  - IntegrityError 和 DataError 处理

#### 删除药品
- 路由：`/material/delete/<id>`
- 功能：级联删除检查

### 3. 供应商管理模块（supplier.py）

#### 供应商列表
- 路由：`/supplier/list`
- 功能：
  - 显示供应商名称、许可证号、联系人、电话
  - 关键字搜索

#### 新增供应商
- 路由：`/supplier/add`
- 功能：
  - 名称唯一性验证
  - 许可证号唯一性验证
  - IntegrityError 友好提示
  - 错误时保留表单数据

### 4. 仓库管理模块（warehouse.py）

#### 仓库列表
- 路由：`/warehouse/list`
- 功能：显示仓库名称、位置、负责人、状态

#### 新增/编辑仓库
- 路由：`/warehouse/add`、`/warehouse/edit/<id>`
- 功能：
  - **名称必填且唯一**
  - **位置必填且唯一**
  - 启用/禁用状态管理
  - 重复验证友好提示

### 5. 采购入库模块（inbound.py）

#### 入库单列表
- 路由：`/inbound/list`
- 功能：
  - 关联供应商和仓库显示
  - 多字段搜索（单号、供应商、仓库）
  - 按日期倒序排列

#### 新增入库单
- 路由：`/inbound/add`
- 功能：
  - 自动生成单号（格式：IN+时间戳）
  - 选择供应商和仓库
  - 默认日期为当前日期
  - 初始状态为未审核

#### 编辑入库单（含明细）
- 路由：`/inbound/edit/<inbound_id>`
- 功能：
  - 修改主单信息
  - 动态添加/删除明细行
  - 审核通过自动增加库存
  - 金额自动计算（数量×单价）

### 6. 销售出库模块（outbound.py）

#### 出库单列表
- 路由：`/outbound/list`
- 功能：关联仓库显示，支持搜索

#### 新增出库单
- 路由：`/outbound/add`
- 功能：
  - 自动生成单号（格式：OUT+时间戳）
  - 选择部门和仓库
  - 选择出库药品

#### 编辑出库单（含明细）
- 路由：`/outbound/edit/<outbound_id>`
- 功能：
  - 库存充足性检查
  - 审核通过自动扣减库存
  - 自动获取零售价（`retail_price`）
  - 金额自动计算

### 7. 库存盘点模块（stock.py）

#### 库存列表
- 路由：`/stock/list`
- 功能：显示所有药品库存

#### 库存盘点
- 路由：`/stock/check`
- 功能：
  - 生成盘点单号
  - 记录系统库存和实际库存
  - 计算差异

#### 库存预警
- 功能：自动标识库存低于最低库存的药品

### 8. 数据库管理模块（database.py）⭐️

#### 数据库管理主页
- 路由：`/database/manage`
- 功能：
  - MySQL 状态检测（自动查找安装路径）
  - 备份文件列表（文件名、大小、时间）
  - 操作按钮（导出、导入、下载、删除）

#### 数据库导出
- 路由：`/database/export`
- 方案：**纯 Python + PyMySQL**（不依赖 mysqldump）
- 功能：
  - 遍历所有表导出表结构（CREATE TABLE）
  - 导出所有表数据（INSERT INTO）
  - 自动处理特殊字符转义
  - 生成标准 SQL 文件
  - 文件名格式：`pharmacy_db_backup_时间戳.sql`
  - 自动下载到本地

#### 数据库导入
- 路由：`/database/import`
- 方案：**纯 Python + PyMySQL**（不依赖 mysql 命令）
- 功能：
  - 上传 SQL 文件
  - 解析并执行 SQL 语句
  - 跳过注释行
  - 按分号分割语句
  - 错误容忍（某些语句失败不影响整体）

#### 备份文件下载
- 路由：`/database/download/<filename>`
- 功能：从 `backups/` 目录下载备份文件

#### 备份文件删除
- 路由：`/database/delete/<filename>`
- 功能：删除指定的备份文件

### 9. 统计报表模块（report.py）

#### 入库统计报表
- 路由：`/report/inbound`
- 功能：按供应商统计入库单数、总入库量、总金额

#### 库存汇总报表
- 路由：`/report/stock_summary`
- 功能：按仓库统计物资种类数、总库存、库存总价值

### 10. RESTful API 模块（api.py）

提供完整的 RESTful API 接口，支持：
- 药品 CRUD：`/api/materials`
- 供应商 CRUD：`/api/suppliers`
- 仓库 CRUD：`/api/warehouses`
- 入库单 CRUD：`/api/inbounds`
- 出库单 CRUD：`/api/outbounds`

---

## 安装与运行

### 环境要求

- Python 3.8+
- MySQL 8.0+
- pip 包管理器

### 安装步骤

#### 1. 克隆项目
```bash
cd 数据库课设
```

#### 2. 安装依赖
```bash
pip install flask flask-sqlalchemy pymysql werkzeug faker
```

#### 3. 创建数据库
```bash
# 在 MySQL 中执行
mysql -u root -p < 创建数据库.sql
```

或者在 MySQL 命令行中：
```sql
CREATE DATABASE pharmacy_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 4. 配置数据库连接

编辑 `run.py` 文件，修改数据库配置：
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://用户名:密码@localhost/pharmacy_db?charset=utf8mb4'
```

同时修改 `app/routes/database.py` 文件中的数据库配置：
```python
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'your_password'  # 如果没有密码，设置为空字符串 ''
DB_NAME = 'pharmacy_db'
```

#### 5. 初始化数据表和测试数据
```bash
python data_init.py
```

此脚本会自动创建所有数据表并生成测试数据：
- 5个药品分类
- 8个计量单位
- 50个药品
- 15个供应商
- 3个仓库
- 30个采购单
- 25个销售单
- 8个盘点单

#### 6. 启动应用
```bash
python run.py
```

访问：`http://localhost:5000`

#### 7. 初始化管理员账户

首次启动后，访问：`http://localhost:5000/auth/init_admin`

或在登录页面点击"初始化管理员账户"链接。

默认管理员账户：
- **用户名**：`admin`
- **密码**：`admin123`

---

## 使用指南

### 登录系统

1. 访问 `http://localhost:5000`，自动跳转到登录页
2. 输入用户名和密码
3. 登录成功后进入主页

### 修改密码

1. 点击右上角用户名下拉菜单
2. 选择"修改密码"
3. 输入原密码和新密码
4. 确认后需要重新登录

### 药品管理

1. 在主页点击"药品管理"
2. 添加药品：填写名称、规格、分类、单位等信息
3. 编辑药品：点击"编辑"按钮修改信息
4. 删除药品：点击"删除"按钮

### 采购入库

1. 在主页点击"采购管理"
2. 添加采购单：选择供应商和仓库，填写采购日期
3. 编辑采购单：添加采购明细（药品、数量、单价）
4. 审核通过后，系统自动增加库存

### 销售出库

1. 在主页点击"销售管理"
2. 添加销售单：选择部门和仓库
3. 编辑销售单：添加销售明细（药品、数量）
4. 系统自动获取零售价并计算金额
5. 审核通过后，系统自动扣减库存

### 数据库备份与恢复

#### 导出数据库
1. 点击"数据库管理"
2. 点击"立即导出"按钮
3. 系统自动生成 SQL 文件并下载

#### 导入数据库
1. 点击"数据库管理"
2. 选择要导入的 SQL 文件
3. 点击"上传导入"
4. **注意**：导入会覆盖现有数据，建议先备份

---

## 核心技术实现

### 1. 密码安全

使用 Werkzeug 提供的密码哈希功能：
```python
from werkzeug.security import generate_password_hash, check_password_hash

# 设置密码
user.password = generate_password_hash(password)

# 验证密码
check_password_hash(user.password, input_password)
```

### 2. 会话管理

使用 Flask Session 管理用户登录状态：
```python
# 登录时设置会话
session.permanent = True
session['user_id'] = user.id
session['username'] = user.username

# 全局登录验证
@app.before_request
def check_login():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
```

会话配置：
- 超时时间：1小时
- Cookie 名称：`pharmacy_session`
- HttpOnly：防止 JavaScript 访问
- SameSite：CSRF 防护

### 3. 数据库导入导出

**纯 Python 实现**，不依赖 mysqldump 工具：

#### 导出原理
```python
import pymysql

# 连接数据库
connection = pymysql.connect(host, user, password, database)
cursor = connection.cursor()

# 获取所有表名
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

# 遍历每个表
for table in tables:
    # 导出表结构
    cursor.execute(f"SHOW CREATE TABLE `{table}`")
    create_sql = cursor.fetchone()[1]

    # 导出表数据
    cursor.execute(f"SELECT * FROM `{table}`")
    rows = cursor.fetchall()

    # 生成 INSERT 语句
    for row in rows:
        values = escape_values(row)
        sql = f"INSERT INTO `{table}` VALUES ({values});"
```

#### 导入原理
```python
# 读取 SQL 文件
with open(sql_file, 'r') as f:
    sql_content = f.read()

# 分割 SQL 语句
statements = sql_content.split(';')

# 逐条执行
for statement in statements:
    cursor.execute(statement)

connection.commit()
```

### 4. 唯一性约束验证

#### 数据库层面
```python
# models.py
class Supplier(db.Model):
    name = db.Column(db.String(100), unique=True)
    license_number = db.Column(db.String(50), unique=True)
```

#### 应用层面
```python
from sqlalchemy.exc import IntegrityError

try:
    db.session.commit()
except IntegrityError:
    db.session.rollback()
    flash('供应商名称或经营许可证号已存在', 'error')
```

### 5. 库存自动更新

#### 采购入库（增加库存）
```python
if inbound.audit_status == 1:  # 审核通过
    material = Material.query.get(material_id)
    material.stock += quantity
    db.session.commit()
```

#### 销售出库（扣减库存）
```python
if outbound.audit_status == 1:  # 审核通过
    material = Material.query.get(material_id)
    if material.stock >= quantity:
        material.stock -= quantity
        db.session.commit()
    else:
        flash('库存不足', 'error')
```

---

## 常见问题

### Q1: 数据库导出失败？

**A:** 系统使用纯 Python 方案，不依赖 mysqldump。如果仍然失败，请检查：
1. 数据库连接配置是否正确（`app/routes/database.py`）
2. 数据库密码是否正确
3. 数据库用户是否有权限

### Q2: 无法登录系统？

**A:** 请确保：
1. 已初始化管理员账户（访问 `/auth/init_admin`）
2. 数据库中 `user` 表已创建
3. 默认账户：`admin / admin123`

### Q3: 仓库名称/位置重复无法添加？

**A:** 这是正确的行为。系统要求：
- 仓库名称必须唯一
- 仓库位置必须唯一

如需更新数据库约束，执行 `更新仓库唯一约束.sql`。

### Q4: 入库单/出库单字段名错误？

**A:** 系统使用了兼容层映射：
- `Inbound` → `Purchase`（采购单）
- `InboundDetail` → `PurchaseDetail`（采购明细）
- `Outbound` → `Sale`（销售单）
- `OutboundDetail` → `SaleDetail`（销售明细）

字段别名：
- `inbound_id` → `purchase_id`
- `outbound_id` → `sale_id`
- `material_id` → `medicine_id`

### Q5: 如何清除浏览器会话测试登录？

**A:** 方法一（推荐）：
1. 按 F12 打开开发者工具
2. Application → Cookies → 删除 `pharmacy_session`
3. 刷新页面

方法二：使用隐私/无痕模式浏览。

---

## 开发规范

### 代码规范

- **Python**：遵循 PEP 8 规范
- **命名规范**：
  - 类名：大驼峰（PascalCase）
  - 函数/变量：小写下划线（snake_case）
  - 常量：大写下划线（UPPER_CASE）

### 数据库规范

- **表名**：小写下划线（如：`medicine_category`）
- **字段名**：小写下划线（如：`create_time`）
- **外键命名**：`关联表_id`（如：`supplier_id`）
- **字符集**：UTF-8MB4
- **存储引擎**：InnoDB

### Git 提交规范

```
feat: 新增功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建/工具链相关
```

---

## 项目亮点

1. ✅ **纯 Python 数据库备份方案**：不依赖外部工具，跨平台兼容
2. ✅ **完整的用户认证系统**：登录、登出、密码管理、会话管理
3. ✅ **友好的错误提示**：所有数据验证错误都有中文提示
4. ✅ **表单数据保留**：验证失败时自动保留用户输入
5. ✅ **自动库存管理**：审核通过自动更新库存
6. ✅ **唯一性约束验证**：数据库+应用层双重验证
7. ✅ **兼容层设计**：支持旧代码平滑迁移
8. ✅ **响应式设计**：Bootstrap 5，支持移动端访问
9. ✅ **MySQL 自动检测**：自动查找 MySQL 安装路径
10. ✅ **会话超时管理**：1小时自动过期，安全可靠

---

## 项目截图

### 登录页面
美观的渐变紫色主题，支持初始化管理员账户。

### 主页
卡片式布局，9大功能模块一目了然。

### 数据库管理页面
- MySQL 状态检测（绿色✅/红色❌）
- 备份文件列表
- 一键导出/导入

### 药品管理
- 列表视图
- 搜索功能
- 添加/编辑表单
- 必填字段标识

---

## 后续优化建议

1. **权限管理**：添加角色权限控制（管理员、操作员、查看者）
2. **操作日志**：记录所有增删改操作
3. **数据统计图表**：使用 ECharts 生成可视化报表
4. **导出 Excel**：支持导出数据为 Excel 格式
5. **批量操作**：支持批量删除、批量导入
6. **消息通知**：库存预警推送
7. **API 文档**：使用 Swagger 生成 API 文档
8. **单元测试**：添加 pytest 测试用例
9. **前后端分离**：使用 Vue.js 重构前端
10. **Docker 部署**：容器化部署方案

---

## 许可证

本项目仅用于学习和交流，不得用于商业用途。

---

## 联系方式

如有问题，请提交 Issue 或联系开发者。

---

## 更新日志

### v2.0 (2025-11-24)
- ✨ 新增：纯 Python 数据库导入导出功能
- ✨ 新增：用户认证系统（登录、登出、修改密码）
- ✨ 新增：全局登录验证
- ✨ 新增：会话管理（1小时超时）
- ✨ 新增：MySQL 自动检测功能
- 🐛 修复：仓库名称和位置唯一性约束
- 🐛 修复：供应商许可证号唯一性验证
- 🐛 修复：药品分类唯一性验证
- 🐛 修复：入库/出库字段名映射问题
- 🐛 修复：销售出库自动获取零售价
- 🐛 修复：金额自动计算功能
- 💄 优化：所有错误提示改为友好的中文提示
- 💄 优化：表单验证失败时保留用户输入
- 📝 更新：完整的开发文档

### v1.0 (初始版本)
- 基础的药品管理功能
- 供应商、仓库管理
- 采购入库、销售出库
- 库存盘点
- 统计报表

---


**技术栈**：Flask + MySQL + Bootstrap 5
**代码行数**：约 5000+ 行

