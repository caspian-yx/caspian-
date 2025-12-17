-- 医药销售管理系统数据库创建脚本

-- 1. 删除旧数据库（如果存在）
DROP DATABASE IF EXISTS pharmacy_db;

-- 2. 创建新数据库
CREATE DATABASE pharmacy_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 3. 使用数据库
USE pharmacy_db;

-- 数据库创建完成，接下来运行 data_init.py 初始化表结构和测试数据
