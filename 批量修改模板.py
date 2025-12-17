import os
import re

# 定义替换规则
replacements = {
    # 系统名称
    '仓库管理系统': '医药销售管理系统',
    '仓库物资管理系统': '医药销售管理系统',

    # 模块名称
    '物资管理': '药品管理',
    '物资分类': '药品分类',
    '物资信息': '药品信息',
    '物资名称': '药品名称',
    '物资列表': '药品列表',
    '物资编号': '药品编号',
    '新增物资': '新增药品',
    '编辑物资': '编辑药品',
    '删除物资': '删除药品',

    # 业务名称
    '入库管理': '采购管理',
    '入库单': '采购单',
    '入库日期': '采购日期',
    '入库数量': '采购数量',
    '新增入库': '新增采购',
    '入库明细': '采购明细',

    '出库管理': '销售管理',
    '出库单': '销售单',
    '出库日期': '销售日期',
    '出库数量': '销售数量',
    '新增出库': '新增销售',
    '出库明细': '销售明细',
    '领用部门': '客户名称',
}

def replace_in_file(file_path):
    """替换单个文件中的内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 执行所有替换
        for old, new in replacements.items():
            content = content.replace(old, new)

        # 如果内容有变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Modified: {file_path}")
            return True
        else:
            return False
    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
        return False

def batch_replace_templates():
    """批量替换templates目录下的所有HTML文件"""
    template_dir = os.path.join(os.path.dirname(__file__), 'app', 'templates')

    if not os.path.exists(template_dir):
        print(f"错误：模板目录不存在 {template_dir}")
        return

    print(f"开始扫描目录: {template_dir}")
    print("="*60)

    modified_count = 0
    total_count = 0

    # 遍历所有HTML文件
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                total_count += 1
                if replace_in_file(file_path):
                    modified_count += 1

    print("="*60)
    print(f"扫描完成！共扫描 {total_count} 个文件，修改了 {modified_count} 个文件")

if __name__ == '__main__':
    batch_replace_templates()
