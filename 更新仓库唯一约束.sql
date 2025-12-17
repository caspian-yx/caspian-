-- 更新仓库表，为 location 字段添加唯一约束
-- 使用方法：在 MySQL 命令行或客户端中执行此脚本

USE pharmacy_db;

-- 1. 先检查是否有重复的位置（排除 NULL）
SELECT location, COUNT(*) as count
FROM warehouse
WHERE location IS NOT NULL
GROUP BY location
HAVING count > 1;

-- 2. 如果上面查询有结果，需要先手动处理重复数据
-- 例如：UPDATE warehouse SET location = CONCAT(location, '-', id) WHERE id IN (需要修改的id);

-- 3. 检查是否有 NULL 值的 location
SELECT COUNT(*) FROM warehouse WHERE location IS NULL OR location = '';

-- 4. 如果有空值，可以设置默认值或删除这些记录
-- UPDATE warehouse SET location = CONCAT('未知位置-', id) WHERE location IS NULL OR location = '';

-- 5. 确认没有重复和空值后，添加唯一约束
ALTER TABLE warehouse ADD UNIQUE INDEX uk_warehouse_location (location);

-- 验证约束是否添加成功
SHOW INDEX FROM warehouse;
