# INSERT 语句导入方式 - 使用指南

## 📋 概述

相比 `LOAD DATA LOCAL INFILE`，使用 INSERT 语句的优势：

✅ **无需配置** - 不需要启用 `local_infile` 选项  
✅ **跨平台兼容** - 适用于所有 MySQL 版本和环境  
✅ **权限友好** - 不需要文件系统访问权限  
✅ **云数据库友好** - 适用于 AWS RDS、阿里云等托管数据库  
✅ **可读性好** - 可以直接查看和修改数据  

## 🚀 使用方法

### 方法 1: 命令行直接导入（推荐）

```bash
# 1. 创建数据库和表结构
mysql -u root -p < database_schema_simplified.sql

# 2. 导入数据（使用 INSERT 语句）
mysql -u root -p internship_system < insert_data.sql
```

### 方法 2: MySQL 客户端导入

```bash
# 登录 MySQL
mysql -u root -p

# 切换数据库
USE internship_system;

# 执行导入脚本
SOURCE /Users/apple/hajime/lastiara/insert_data.sql;
```

### 方法 3: MySQL Workbench 导入

1. 打开 MySQL Workbench
2. 连接到数据库
3. File → Run SQL Script
4. 选择 `insert_data.sql`
5. 点击 Run

## 📊 数据统计

生成的 `insert_data.sql` 包含：

| 表名 | 记录数 | 说明 |
|------|--------|------|
| majors | 15 | 专业 |
| skills | 40 | 技能 |
| position_categories | 20 | 岗位类别 |
| consultation_types | 6 | 咨询类型 |
| companies | 25 | 公司 |
| teachers | 5 | CDO教师 |
| students | 100 | 学生 |
| resumes | 150 | 简历 |
| positions | 50 | 岗位 |
| applications | 295 | 申请记录 |
| appointments | 80 | 预约记录 |
| resume_skills | 846 | 简历-技能关联 |
| position_skills | 359 | 岗位-技能关联 |

**总计**: 1,991 条记录

## 🔄 重新生成数据

如果需要修改数据或重新生成：

```bash
# 1. 生成 CSV 数据
python3 generate_mock_data.py

# 2. 转换为 INSERT SQL
python3 csv_to_insert_sql.py

# 3. 导入到数据库
mysql -u root -p internship_system < insert_data.sql
```

## 🛠️ 文件说明

### 核心文件

1. **database_schema_simplified.sql** - 建表脚本（13 张表）
   ```sql
   -- 创建数据库和所有表结构
   -- 包含外键约束、索引、视图
   ```

2. **insert_data.sql** - 数据导入脚本（INSERT 语句）⭐
   ```sql
   -- 包含所有表的 INSERT 语句
   -- 总计 1,991 条记录
   -- 文件大小: ~174 KB
   ```

### 辅助脚本

3. **generate_mock_data.py** - 生成模拟数据到 CSV
4. **csv_to_insert_sql.py** - 将 CSV 转换为 INSERT SQL

## ⚡ 性能提示

### 大批量数据导入优化

如果数据量更大（数万条以上），可以优化：

```sql
-- 在导入前设置
SET FOREIGN_KEY_CHECKS = 0;
SET UNIQUE_CHECKS = 0;
SET AUTOCOMMIT = 0;

-- 执行 INSERT 语句
SOURCE insert_data.sql;

-- 提交事务
COMMIT;

-- 恢复设置
SET FOREIGN_KEY_CHECKS = 1;
SET UNIQUE_CHECKS = 1;
SET AUTOCOMMIT = 1;
```

### 批量插入

脚本已自动使用批量插入（每批 100 条）：

```sql
INSERT INTO students (...) VALUES
(值1),
(值2),
(值3),
...
(值100);
```

这比单条插入快 10-50 倍。

## 🔍 验证数据

导入完成后自动执行验证查询：

```sql
-- 查看各表记录数
SELECT 'majors' as table_name, COUNT(*) as row_count FROM majors
UNION ALL
SELECT 'skills', COUNT(*) FROM skills
UNION ALL
...

-- 输出示例：
-- +----------------------+-----------+
-- | table_name           | row_count |
-- +----------------------+-----------+
-- | majors               |        15 |
-- | skills               |        40 |
-- | students             |       100 |
-- | applications         |       295 |
-- +----------------------+-----------+
```

## 🐛 常见问题

### Q1: 导入时报错 "Duplicate entry"

**原因**: 数据库中已存在数据

**解决方案**:
```sql
-- 方法1: 清空所有表
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE resume_skills;
TRUNCATE TABLE position_skills;
TRUNCATE TABLE appointments;
TRUNCATE TABLE applications;
TRUNCATE TABLE positions;
TRUNCATE TABLE resumes;
TRUNCATE TABLE students;
TRUNCATE TABLE teachers;
TRUNCATE TABLE companies;
TRUNCATE TABLE consultation_types;
TRUNCATE TABLE position_categories;
TRUNCATE TABLE skills;
TRUNCATE TABLE majors;
SET FOREIGN_KEY_CHECKS = 1;

-- 方法2: 删除数据库重建
DROP DATABASE IF EXISTS internship_system;
CREATE DATABASE internship_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Q2: 外键约束错误

**原因**: 表导入顺序不对

**解决**: 脚本已按正确顺序导入（先父表后子表），如果仍报错：
```sql
SET FOREIGN_KEY_CHECKS = 0;  -- 临时禁用外键检查
SOURCE insert_data.sql;
SET FOREIGN_KEY_CHECKS = 1;  -- 恢复外键检查
```

### Q3: 中文乱码

**解决**:
```bash
# 导入时指定字符集
mysql -u root -p --default-character-set=utf8mb4 internship_system < insert_data.sql
```

或在 MySQL 中设置：
```sql
SET NAMES utf8mb4;
SOURCE insert_data.sql;
```

### Q4: 导入速度慢

**优化**:
```sql
-- 临时禁用日志（仅开发环境）
SET sql_log_bin = 0;
SET FOREIGN_KEY_CHECKS = 0;
SET UNIQUE_CHECKS = 0;

SOURCE insert_data.sql;

-- 恢复设置
SET sql_log_bin = 1;
SET FOREIGN_KEY_CHECKS = 1;
SET UNIQUE_CHECKS = 1;
```

## 📈 与 LOAD DATA 对比

| 方面 | INSERT 语句 | LOAD DATA LOCAL INFILE |
|------|-------------|------------------------|
| **配置要求** | 无需配置 ✅ | 需要启用 local_infile |
| **权限要求** | 普通权限 ✅ | 需要 FILE 权限 |
| **云数据库** | 支持 ✅ | 部分云服务不支持 |
| **跨平台** | 完全兼容 ✅ | 路径问题 |
| **速度** | 较慢（中等数据量够用） | 更快 |
| **可读性** | 可直接查看数据 ✅ | CSV 需单独查看 |
| **调试** | 容易定位问题 ✅ | 错误信息不明确 |
| **文件依赖** | 单个 SQL 文件 ✅ | 需要多个 CSV 文件 |

**建议**:
- **开发/测试环境**: 使用 INSERT 语句 ✅
- **生产环境大批量导入**: 考虑 LOAD DATA（如果支持）
- **云数据库**: 使用 INSERT 语句 ✅

## 🔐 安全提示

1. **生产环境**: 不要直接使用测试数据
2. **敏感信息**: 生成的数据是模拟的，不包含真实信息
3. **权限控制**: 导入数据需要 INSERT 权限

## 📚 相关文件

```
lastiara/
├── database_schema_simplified.sql    # 第1步：建表
├── insert_data.sql                   # 第2步：导入数据 ⭐
├── generate_mock_data.py             # 工具：生成 CSV
├── csv_to_insert_sql.py              # 工具：转换为 INSERT
└── mock_data/                        # CSV 源文件
    ├── students.csv
    ├── resumes.csv
    └── ...
```

## ✅ 快速检查清单

导入后执行以下检查：

```sql
-- 1. 检查表数量
SELECT COUNT(*) as table_count 
FROM information_schema.tables 
WHERE table_schema = 'internship_system';
-- 应该返回 13

-- 2. 检查总记录数
SELECT 
    SUM(table_rows) as total_records
FROM information_schema.tables
WHERE table_schema = 'internship_system';
-- 应该约 1,991

-- 3. 检查外键完整性
SELECT * FROM students WHERE major_id NOT IN (SELECT major_id FROM majors);
-- 应该返回 0 行

-- 4. 测试视图
SELECT * FROM v_student_profile LIMIT 5;
-- 应该正常返回数据
```

---

**最后更新**: 2024-06-12  
**适用版本**: 精简版 13 张表设计
