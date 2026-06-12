# 学生实习求职管理系统数据库

## 📚 文档导航

### 🚀 快速开始
1. **[README_database.md](README_database.md)** - 完整使用指南
   - 安装配置
   - 快速启动
   - 常用查询示例
   - 故障排除

### 📖 设计文档
2. **[normalization_analysis.md](normalization_analysis.md)** - 范式优化分析
   - 原始设计问题
   - 范式优化过程
   - 前后对比分析

3. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - 项目总结
   - 核心成果
   - 技术亮点
   - 应用场景

### 💻 代码文件（推荐使用精简版 ⭐）

4. **[database_schema_simplified.sql](database_schema_simplified.sql)** - 建表脚本（精简版）⭐
   - 13 张表的完整定义
   - 移除了不必要的国家表
   - 外键约束、索引和视图

5. **[insert_data.sql](insert_data.sql)** - 数据导入（INSERT 方式，推荐）⭐⭐
   - 使用 INSERT 语句导入
   - 无需配置，直接可用
   - 1,991 条记录
   - 详见 [INSERT_IMPORT_GUIDE.md](INSERT_IMPORT_GUIDE.md)

6. **[generate_mock_data.py](generate_mock_data.py)** - 数据生成脚本
   - 生成 100 学生、150 简历、50 岗位
   - 生成 CSV 文件到 mock_data/

7. **[csv_to_insert_sql.py](csv_to_insert_sql.py)** - CSV 转 INSERT SQL
   - 将 CSV 转换为 INSERT 语句
   - 批量插入优化

### 📦 其他导入方式（可选）
- **[import_data_simplified.sql](import_data_simplified.sql)** - LOAD DATA 方式（需要配置）
- 说明：需要启用 `local_infile`，适合熟悉 MySQL 的用户

### 📦 原始版本（参考）
- **[database_schema_optimized.sql](database_schema_optimized.sql)** - 14 张表版本（含国家表）
- **[import_data.sql](import_data.sql)** - 原始 LOAD DATA 导入

### 💡 设计说明文档
- **[WHY_REMOVE_COUNTRIES.md](WHY_REMOVE_COUNTRIES.md)** - 为什么移除国家表？⭐
- **[INSERT_IMPORT_GUIDE.md](INSERT_IMPORT_GUIDE.md)** - INSERT 导入完整指南 ⭐

## 🎯 核心特性

### ✅ 实用的范式设计
- 符合第三范式 (3NF)
- 适度规范化，避免过度设计
- 消除数据冗余
- 保证数据一致性

### ✅ 完善的技能体系
- 40+ 技能标准化管理
- 简历-技能多对多关系
- 岗位-技能匹配

### ✅ 智能推荐支持
- 基于技能的岗位推荐
- 技能差距分析
- 供需比统计

### ✅ 真实的模拟数据
- 25 家知名公司
- 15 个专业
- 符合逻辑的业务数据

## 📊 数据库结构（精简版 - 推荐）

```
核心实体表 (7)
├── students        学生
├── resumes         简历
├── positions       岗位
├── applications    申请记录
├── appointments    预约记录
├── companies       公司
└── teachers        教师

字典表 (4)  ← 精简版：移除了国家表
├── majors              专业
├── skills              技能
├── position_categories 岗位类别
└── consultation_types  咨询类型

关联表 (2)
├── resume_skills    简历-技能
└── position_skills  岗位-技能

视图 (3)
├── v_student_profile       学生档案
├── v_position_details      岗位详情
└── v_application_details   申请详情

总计：13 张表 + 3 个视图
```

## 🚀 两步快速启动（推荐 INSERT 方式）⭐

```bash
# 1. 创建数据库和表结构（13 张表）
mysql -u root -p < database_schema_simplified.sql

# 2. 导入数据（使用 INSERT 语句，无需任何配置）
mysql -u root -p internship_system < insert_data.sql
```

### 🔄 如果需要自定义数据

```bash
# 1. 生成 CSV 数据
python3 generate_mock_data.py

# 2. 转换为 INSERT SQL
python3 csv_to_insert_sql.py

# 3. 导入到数据库
mysql -u root -p internship_system < insert_data.sql
```

💡 **为什么使用 INSERT 方式？**
- ✅ 无需配置 `local_infile`
- ✅ 适用于云数据库
- ✅ 跨平台兼容
- ✅ 详见 [INSERT_IMPORT_GUIDE.md](INSERT_IMPORT_GUIDE.md)

💡 **为什么使用精简版？** 查看 [WHY_REMOVE_COUNTRIES.md](WHY_REMOVE_COUNTRIES.md)

## 📈 数据规模

| 类型 | 数量 |
|------|------|
| 学生 | 100 |
| 简历 | ~150 |
| 岗位 | 50 |
| 公司 | 25 |
| 申请记录 | 300 |
| 预约记录 | 80 |
| 技能 | 40 |
| 专业 | 15 |

## 🔍 典型查询

### 查询学生档案
```sql
SELECT * FROM v_student_profile WHERE student_id = '20210001';
```

### 岗位推荐
```sql
SELECT p.position_title, COUNT(*) as matched_skills
FROM positions p
JOIN position_skills ps ON p.position_id = ps.position_id
WHERE ps.skill_id IN (
    SELECT skill_id FROM resume_skills WHERE resume_id = ?
)
GROUP BY p.position_id
ORDER BY matched_skills DESC;
```

### 技能统计
```sql
SELECT skill_name, 
       COUNT(DISTINCT resume_id) as student_count,
       COUNT(DISTINCT position_id) as demand_count
FROM skills
LEFT JOIN resume_skills USING (skill_id)
LEFT JOIN position_skills USING (skill_id)
GROUP BY skill_id;
```

## 📋 文件清单

```
lastiara/
├── 数据流图+ER图.png                      # 原始需求图
│
├── database_schema_simplified.sql        # 建表脚本（13张表）⭐
├── insert_data.sql                       # INSERT 导入（推荐）⭐⭐
│
├── generate_mock_data.py                 # 工具：生成 CSV 数据
├── csv_to_insert_sql.py                  # 工具：CSV → INSERT SQL
│
├── INSERT_IMPORT_GUIDE.md                # INSERT 导入完整指南 📖
├── WHY_REMOVE_COUNTRIES.md               # 设计优化说明 💡
├── normalization_analysis.md             # 范式分析
├── README_database.md                    # 使用指南
├── PROJECT_SUMMARY.md                    # 项目总结
├── INDEX.md                              # 本文件
│
├── import_data_simplified.sql            # LOAD DATA 方式（可选）
├── database_schema_optimized.sql         # 14张表版本（参考）
├── import_data.sql                       # LOAD DATA 原始版（参考）
│
└── mock_data/                            # CSV 源文件
    ├── majors.csv          (15 条)
    ├── skills.csv          (40 条)
    ├── students.csv        (100 条)
    ├── resumes.csv         (150 条)
    ├── positions.csv       (50 条)
    ├── applications.csv    (295 条)
    └── ...                 (共 1,991 条)
```

## 💡 建议阅读顺序

### 初学者
1. 📄 README_database.md - 了解如何使用
2. 💻 运行快速启动命令
3. 📊 在 MySQL 中执行示例查询
4. 📖 阅读 normalization_analysis.md 理解设计

### 开发者
1. 📖 normalization_analysis.md - 理解设计思路
2. 💻 database_schema_optimized.sql - 查看表结构
3. 🐍 generate_mock_data.py - 了解数据生成逻辑
4. 📄 README_database.md - 查询示例和 API 集成

### 数据库设计师
1. 📖 normalization_analysis.md - 范式优化案例
2. 📊 PROJECT_SUMMARY.md - 架构亮点
3. 💻 database_schema_optimized.sql - DDL 实现
4. 📈 性能优化和扩展建议

## 🔗 相关资源

- [MySQL 官方文档](https://dev.mysql.com/doc/)
- [数据库范式理论](https://en.wikipedia.org/wiki/Database_normalization)
- [SQL 性能优化](https://use-the-index-luke.com/)

## 📞 问题反馈

如遇到问题或有改进建议，请：
1. 检查 README_database.md 中的常见问题部分
2. 查看各 SQL 脚本中的注释说明
3. 提交 Issue 或 Pull Request

---

**最后更新**: 2024-06-12  
**版本**: v1.2（INSERT 导入版）  
**状态**: ✅ 可投入使用

**更新日志**:
- v1.2: 添加 INSERT 语句导入方式（推荐），无需配置
- v1.1: 移除不必要的国家表，优化为 13 张表
- v1.0: 初始版本，14 张表
