import os
import sys
from faker import Faker
from datetime import datetime, timedelta
import random

# 导入项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import db
from app.models import (
    Medicine, MedicineCategory, Unit, Supplier,
    Warehouse, Purchase, PurchaseDetail,
    Sale, SaleDetail,
    StockCheck, StockCheckDetail
)
from run import app

# 初始化Faker（中文数据）
fake = Faker('zh_CN')

# 生成数据量配置
CATEGORY_COUNT = 5       # 药品分类
UNIT_COUNT = 8           # 单位
MEDICINE_COUNT = 50      # 药品
SUPPLIER_COUNT = 15      # 供应商
WAREHOUSE_COUNT = 3      # 仓库
PURCHASE_COUNT = 30      # 采购单
SALE_COUNT = 25          # 销售单
STOCK_CHECK_COUNT = 8    # 盘点单

def init_data():
    with app.app_context():
        # 1. 清空现有表并重建（谨慎使用！）
        db.drop_all()
        db.create_all()
        print("数据库表已重置")

        # 2. 生成药品分类
        categories = []
        category_names = ["西药", "中成药", "保健品", "医疗器械", "中药材"]
        for name in category_names:
            c = MedicineCategory(name=name, remark=f"{name}相关产品")
            db.session.add(c)
            categories.append(c)
        db.session.commit()
        print(f"生成 {len(categories)} 个药品分类")

        # 3. 生成单位
        units = []
        unit_names = ["盒", "瓶", "支", "片", "粒", "袋", "瓶装", "盘"]
        for name in unit_names:
            u = Unit(name=name, abbreviation=name[0])
            db.session.add(u)
            units.append(u)
        db.session.commit()
        print(f"生成 {len(units)} 个单位")

        # 4. 生成药品数据（确保 名称+规格 唯一）
        medicines = []
        medicine_names = [
            "阿莫西林胶囊", "头孢克肟片", "布洛芬缓释胶囊", "感冒灵颗粒", "板蓝根颗粒",
            "复方氨酚烷胺片", "维生素C片", "阿司匹林肠溶片", "氨溴索口服液", "左氧氟沙星片",
            "罗红霉素胶囊", "盐酸二甲双胍片", "硝苯地平缓释片", "阿托伐他汀钙片", "奥美拉唑肠溶胶囊"
        ]
        specifications = ["10mg*12片", "20mg*24片", "500mg*10粒", "100ml/瓶", "0.25g*20粒",
                         "0.5g*12片", "250mg*30粒", "10g*10袋", "5mg*28片", "0.1g*24粒"]
        dosage_forms = ["片剂", "胶囊", "颗粒", "注射液", "口服液", "软膏"]
        manufacturers = ["华北制药股份有限公司", "石药集团有限公司", "哈药集团制药厂",
                        "云南白药集团股份有限公司", "广州白云山制药股份有限公司"]

        # 使用集合记录已生成的 名称+规格 组合，避免重复
        generated_combinations = set()
        used_approval_numbers = set()

        for i in range(MEDICINE_COUNT):
            category = random.choice(categories)
            unit = random.choice(units)

            # 确保 名称+规格 组合唯一
            name_idx = i % len(medicine_names)
            spec_idx = i // len(medicine_names)  # 每个药品名称搭配不同规格

            name = medicine_names[name_idx]
            spec = specifications[spec_idx % len(specifications)]

            # 如果组合已存在，添加后缀区分
            combination_key = (name, spec)
            if combination_key in generated_combinations:
                spec = f"{spec}-{i}"  # 添加编号区分
            generated_combinations.add((name, spec))

            # 生成唯一的批准文号
            while True:
                approval_num = f"国药准字H{random.randint(10000000, 99999999)}"
                if approval_num not in used_approval_numbers:
                    used_approval_numbers.add(approval_num)
                    break

            m = Medicine(
                name=name,
                generic_name=f"{name.replace('片','').replace('胶囊','').replace('颗粒','')}",
                approval_number=approval_num,
                specification=spec,
                dosage_form=random.choice(dosage_forms),
                manufacturer=random.choice(manufacturers),
                category_id=category.id,
                unit_id=unit.id,
                is_prescription=random.choice([0, 1]),
                stock=random.randint(50, 500),
                min_stock=random.randint(10, 50),
                retail_price=round(random.uniform(10, 200), 2),
                create_time=fake.date_time_between(start_date='-1y', end_date='now'),
                remark=f"用于{random.choice(['感冒', '发热', '炎症', '高血压', '糖尿病'])}治疗"
            )
            db.session.add(m)
            medicines.append(m)
        db.session.commit()
        print(f"生成 {len(medicines)} 个药品（名称+规格唯一）")

        # 5. 生成医药供应商
        suppliers = []
        for _ in range(SUPPLIER_COUNT):
            s = Supplier(
                name=f"{fake.company()}医药公司",
                license_number=f"药经{random.randint(100000, 999999)}",  # 药品经营许可证号
                contact=fake.name(),
                phone=fake.phone_number(),
                address=fake.address()
            )
            db.session.add(s)
            suppliers.append(s)
        db.session.commit()
        print(f"生成 {len(suppliers)} 个医药供应商")

        # 6. 生成药品仓库
        warehouses = []
        warehouse_types = ["常温库", "冷藏库", "阴凉库"]
        for i in range(WAREHOUSE_COUNT):
            w = Warehouse(
                name=f"药品仓库{i+1}",
                warehouse_type=random.choice(warehouse_types),
                location=fake.address(),
                manager=fake.name(),
                phone=fake.phone_number(),
                is_active=1
            )
            db.session.add(w)
            warehouses.append(w)
        db.session.commit()
        print(f"生成 {len(warehouses)} 个药品仓库")

        # 7. 生成采购单及明细
        for _ in range(PURCHASE_COUNT):
            # 唯一采购单号：PC+时间戳+随机数
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
            random_num = random.randint(100000, 999999)
            purchase_id = f"PC{timestamp}{random_num}"

            # 随机选择供应商和仓库
            supplier = random.choice(suppliers)
            warehouse = random.choice(warehouses)

            purchase = Purchase(
                purchase_id=purchase_id,
                supplier_id=supplier.id,
                warehouse_id=warehouse.id,
                purchase_date=fake.date_between(start_date='-6m', end_date='now'),
                remark=fake.text()[:50],
                audit_status=random.choice([0, 1, 2])  # 0待审核，1通过，2驳回
            )
            db.session.add(purchase)

            # 每个采购单包含1-4种药品
            for _ in range(random.randint(1, 4)):
                medicine = random.choice(medicines)
                quantity = random.randint(10, 100)  # 采购数量
                unit_price = round(random.uniform(10, 500), 2)  # 单价

                # 生成批次相关信息
                production_date = fake.date_between(start_date='-1y', end_date='now')
                expiry_date = production_date + timedelta(days=random.randint(365, 1095))  # 1-3年有效期

                # 添加采购明细
                detail = PurchaseDetail(
                    purchase_id=purchase_id,
                    medicine_id=medicine.id,
                    production_batch=f"BATCH{random.randint(100000, 999999)}",
                    production_date=production_date,
                    expiry_date=expiry_date,
                    quantity=quantity,
                    unit_price=unit_price,
                    amount=quantity * unit_price
                )
                db.session.add(detail)

                # 已审核的采购单更新库存
                if purchase.audit_status == 1:
                    medicine.stock += quantity
        db.session.commit()
        print(f"生成 {PURCHASE_COUNT} 个采购单（含明细）")

        # 8. 生成销售单及明细
        for _ in range(SALE_COUNT):
            # 唯一销售单号：SL+时间戳+随机数
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
            random_num = random.randint(100000, 999999)
            sale_id = f"SL{timestamp}{random_num}"

            warehouse = random.choice(warehouses)
            sale = Sale(
                sale_id=sale_id,
                warehouse_id=warehouse.id,
                customer_name=fake.name(),  # 客户姓名
                customer_phone=fake.phone_number(),  # 客户电话
                prescription_no=f"RX{random.randint(100000, 999999)}" if random.random() > 0.5 else None,
                sale_date=fake.date_between(start_date='-3m', end_date='now'),
                remark=fake.text()[:50],
                audit_status=random.choice([0, 1, 2])
            )
            db.session.add(sale)

            # 每个销售单包含1-3种药品（确保库存足够）
            for _ in range(random.randint(1, 3)):
                medicine = random.choice(medicines)
                # 销售数量不超过当前库存
                max_quantity = min(30, medicine.stock) if medicine.stock > 0 else 1
                quantity = random.randint(1, max_quantity)
                unit_price = medicine.retail_price  # 使用零售价

                # 添加销售明细
                detail = SaleDetail(
                    sale_id=sale_id,
                    medicine_id=medicine.id,
                    quantity=quantity,
                    unit_price=unit_price,
                    amount=quantity * unit_price
                )
                db.session.add(detail)

                # 已审核的销售单更新库存
                if sale.audit_status == 1 and medicine.stock >= quantity:
                    medicine.stock -= quantity
        db.session.commit()
        print(f"生成 {SALE_COUNT} 个销售单（含明细）")

        # 9. 生成药品盘点单及明细
        for _ in range(STOCK_CHECK_COUNT):
            # 唯一盘点单号：CHECK+时间戳+随机数
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
            random_num = random.randint(100000, 999999)
            check_id = f"CHECK{timestamp}{random_num}"

            check = StockCheck(
                check_id=check_id,
                checker=fake.name(),  # 盘点人
                check_date=fake.date_between(start_date='-1m', end_date='now'),
                remark=fake.text()[:50]
            )
            db.session.add(check)

            # 每个盘点单包含5-10种药品
            checked_medicines = random.sample(medicines, min(10, len(medicines)))
            for med in checked_medicines:
                system_stock = med.stock  # 系统库存
                actual_stock = system_stock + random.randint(-5, 5)  # 实际库存（允许±5误差）
                detail = StockCheckDetail(
                    check_id=check_id,
                    medicine_id=med.id,
                    system_stock=system_stock,
                    actual_stock=actual_stock,
                    diff=actual_stock - system_stock  # 差异
                )
                db.session.add(detail)
        db.session.commit()
        print(f"生成 {STOCK_CHECK_COUNT} 个盘点单（含明细）")

        print("所有药品数据生成完成！采购、销售、盘点单已填充数据。")

if __name__ == '__main__':
    init_data()