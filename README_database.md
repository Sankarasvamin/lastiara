# 学生实习求职管理系统 - 使用指南

## 📁 项目文件说明

```
lastiara/
├── 数据流图+ER图.png                    # 原始需求的数据流图和ER图
├── database_schema_optimized.sql       # 优化后的数据库建表脚本（符合3NF）
├── normalization_analysis.md           # 范式优化分析文档
├── generate_mock_data.py               # Python数据生成脚本
├── import_data.sql                     # MySQL数据导入脚本
├── README_database.md                  # 本文档
└── mock_data/                          # 生成的模拟数据目录（执行脚本后创建）
    ├── countries.csv
    ├── majors.csv
    ├── skills.csv
    ├── students.csv
    ├── resumes.csv
    ├── positions.csv
    └── ... (其他数据文件)
```

## 🚀 快速开始

### 步骤 1: 安装 MySQL

确保已安装 MySQL 8.0 或更高版本：

```bash
mysql --version
```

### 步骤 2: 创建数据库和表结构

```bash
# 登录 MySQL
mysql -u root -p

# 或使用配置文件
mysql -u root -p < database_schema_optimized.sql
```

在 MySQL 命令行中：

```sql
-- 执行建表脚本
SOURCE /path/to/database_schema_optimized.sql;

-- 验证表创建成功
USE internship_system;
SHOW TABLES;

-- 查看表结构
DESCRIBE students;
DESCRIBE positions;
```

### 步骤 3: 生成模拟数据

```bash
# 安装依赖（如果需要）
pip install -r requirements.txt  # 本项目无需额外依赖，仅用标准库

# 执行数据生成脚本
python generate_mock_data.py
```

输出示例：
```
============================================================
学生实习求职管理系统 - 模拟数据生成
============================================================

[字典表]
✓ 生成 countries.csv: 8 条记录
✓ 生成 majors.csv: 15 条记录
✓ 生成 skills.csv: 40 条记录
...

[核心实体表]
✓ 生成 students.csv: 100 条记录
✓ 生成 resumes.csv: 147 条记录
...

✓ 数据生成完成！
```

### 步骤 4: 导入数据到 MySQL

**重要**: MySQL 需要启用 `local_infile` 选项才能导入本地文件。

#### 方法 1: 使用命令行参数

```bash
mysql -u root -p --local-infile=1 internship_system < import_data.sql
```

#### 方法 2: 在 MySQL 会话中设置

```sql
-- 登录 MySQL
mysql -u root -p

-- 启用 local_infile
SET GLOBAL local_infile = 1;

-- 退出并重新登录
exit;

-- 重新登录并导入
mysql -u root -p --local-infile=1 internship_system

-- 执行导入脚本
SOURCE /path/to/lastiara/import_data.sql;
```

#### 方法 3: 修改 MySQL 配置文件（永久启用）

编辑 `my.cnf` 或 `my.ini`：

```ini
[mysqld]
local_infile=1

[mysql]
local_infile=1
```

重启 MySQL 服务后执行导入脚本。

### 步骤 5: 验证数据

```sql
USE internship_system;

-- 查看各表数据量
SELECT 'students' as table_name, COUNT(*) as count FROM students
UNION ALL
SELECT 'resumes', COUNT(*) FROM resumes
UNION ALL
SELECT 'positions', COUNT(*) FROM positions
UNION ALL
SELECT 'applications', COUNT(*) FROM applications
UNION ALL
SELECT 'appointments', COUNT(*) FROM appointments;

-- 查看学生信息
SELECT * FROM v_student_profile LIMIT 10;

-- 查看岗位信息
SELECT * FROM v_position_details LIMIT 10;

-- 查看申请记录
SELECT * FROM v_application_details LIMIT 10;
```

## 📊 数据库设计概览

### 核心实体（7张表）

1. **students** - 学生基本信息
2. **resumes** - 学生简历
3. **positions** - 招聘岗位
4. **applications** - 申请记录
5. **appointments** - 咨询预约
6. **companies** - 公司信息
7. **teachers** - CDO教师信息

### 字典表（5张表）

1. **countries** - 国家地区
2. **majors** - 专业
3. **skills** - 技能
4. **position_categories** - 岗位类别
5. **consultation_types** - 咨询类型

### 关联表（2张表）

1. **resume_skills** - 简历-技能多对多关系
2. **position_skills** - 岗位-技能多对多关系

### 视图（3个）

1. **v_student_profile** - 学生完整档案视图
2. **v_position_details** - 岗位详细信息视图
3. **v_application_details** - 申请记录详情视图

## 🔍 常用查询示例

### 1. 查询学生完整档案

```sql
SELECT * FROM v_student_profile
WHERE student_id = '20210001';
```

### 2. 查找掌握特定技能的学生

```sql
SELECT DISTINCT s.student_id, s.name, sk.skill_name, rs.proficiency_level
FROM students s
JOIN resumes r ON s.student_id = r.student_id
JOIN resume_skills rs ON r.resume_id = rs.resume_id
JOIN skills sk ON rs.skill_id = sk.skill_id
WHERE sk.skill_name IN ('Python', 'Java', 'Machine Learning')
ORDER BY s.student_id, sk.skill_name;
```

### 3. 统计各公司的申请数量

```sql
SELECT c.company_name,
       COUNT(DISTINCT p.position_id) as position_count,
       COUNT(a.application_id) as application_count,
       ROUND(COUNT(a.application_id) * 1.0 / COUNT(DISTINCT p.position_id), 2) as avg_applications_per_position
FROM companies c
JOIN positions p ON c.company_id = p.company_id
LEFT JOIN applications a ON p.position_id = a.position_id
GROUP BY c.company_id, c.company_name
ORDER BY application_count DESC;
```

### 4. 查询某学生的申请状态

```sql
SELECT a.application_id,
       p.position_title,
       c.company_name,
       a.application_status,
       a.submit_time,
       a.update_time,
       a.hr_comment
FROM applications a
JOIN positions p ON a.position_id = p.position_id
JOIN companies c ON p.company_id = c.company_id
WHERE a.student_id = '20210001'
ORDER BY a.submit_time DESC;
```

### 5. 技能匹配度分析

```sql
-- 查找与某个岗位技能最匹配的学生
SET @target_position_id = 1;

SELECT s.student_id,
       s.name,
       COUNT(*) as matched_skills,
       SUM(CASE WHEN ps.is_required THEN 1 ELSE 0 END) as matched_required_skills,
       GROUP_CONCAT(sk.skill_name ORDER BY ps.priority DESC SEPARATOR ', ') as skills
FROM students s
JOIN resumes r ON s.student_id = r.student_id AND r.is_default = 1
JOIN resume_skills rs ON r.resume_id = rs.resume_id
JOIN skills sk ON rs.skill_id = sk.skill_id
JOIN position_skills ps ON sk.skill_id = ps.skill_id
WHERE ps.position_id = @target_position_id
GROUP BY s.student_id, s.name
HAVING matched_skills > 0
ORDER BY matched_required_skills DESC, matched_skills DESC
LIMIT 10;
```

### 6. 热门技能统计

```sql
SELECT s.skill_name,
       s.skill_category,
       COUNT(DISTINCT rs.resume_id) as student_count,
       COUNT(DISTINCT ps.position_id) as position_demand,
       ROUND(COUNT(DISTINCT ps.position_id) * 1.0 / COUNT(DISTINCT rs.resume_id), 2) as demand_supply_ratio
FROM skills s
LEFT JOIN resume_skills rs ON s.skill_id = rs.skill_id
LEFT JOIN position_skills ps ON s.skill_id = ps.skill_id
GROUP BY s.skill_id, s.skill_name, s.skill_category
HAVING student_count > 0 OR position_demand > 0
ORDER BY demand_supply_ratio DESC, position_demand DESC
LIMIT 20;
```

### 7. CDO教师工作量统计

```sql
SELECT t.teacher_name,
       COUNT(a.appointment_id) as total_appointments,
       SUM(CASE WHEN a.status = 'completed' THEN 1 ELSE 0 END) as completed,
       SUM(CASE WHEN a.status = 'scheduled' THEN 1 ELSE 0 END) as scheduled,
       SUM(CASE WHEN a.status = 'cancelled' THEN 1 ELSE 0 END) as cancelled,
       ROUND(AVG(a.duration_minutes), 0) as avg_duration
FROM teachers t
LEFT JOIN appointments a ON t.teacher_id = a.teacher_id
GROUP BY t.teacher_id, t.teacher_name
ORDER BY total_appointments DESC;
```

### 8. 申请漏斗分析

```sql
SELECT application_status,
       COUNT(*) as count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM applications), 2) as percentage
FROM applications
GROUP BY application_status
ORDER BY FIELD(application_status,
               'submitted', 'screening', 'interview', 'assessment',
               'offered', 'accepted', 'rejected', 'withdrawn');
```

## 🛠️ 数据维护操作

### 添加新学生

```sql
INSERT INTO students (student_id, name, gender, email, phone, major_id,
                      enrollment_year, expected_graduation_year)
VALUES ('20240001', '张三', 'M', 'zhangsan@university.edu.cn', '13800138000',
        1, 2024, 2028);
```

### 添加新简历

```sql
INSERT INTO resumes (student_id, resume_title, upload_time, is_default)
VALUES ('20240001', '技术岗位简历', NOW(), 1);

-- 获取刚插入的简历ID
SET @resume_id = LAST_INSERT_ID();

-- 添加简历技能
INSERT INTO resume_skills (resume_id, skill_id, proficiency_level)
VALUES
    (@resume_id, 1, 'advanced'),    -- Python
    (@resume_id, 2, 'intermediate'), -- Java
    (@resume_id, 6, 'advanced');     -- SQL
```

### 提交申请

```sql
-- 检查是否已申请
SELECT * FROM applications
WHERE student_id = '20240001' AND position_id = 1;

-- 如果未申请，提交新申请
INSERT INTO applications (student_id, position_id, resume_id, application_status, submit_time, update_time)
VALUES ('20240001', 1, @resume_id, 'submitted', NOW(), NOW());
```

### 更新申请状态

```sql
UPDATE applications
SET application_status = 'interview',
    update_time = NOW(),
    hr_comment = '简历通过初筛，邀请参加面试'
WHERE application_id = 1;
```

### 预约咨询

```sql
INSERT INTO appointments (student_id, teacher_id, type_id, appointment_time, status)
VALUES ('20240001', 1, 1, '2024-06-15 14:00:00', 'scheduled');
```

## 📈 性能优化建议

### 1. 索引使用检查

```sql
-- 查看慢查询
EXPLAIN SELECT * FROM applications
WHERE student_id = '20210001'
AND application_status = 'interview';

-- 检查索引使用情况
SHOW INDEX FROM applications;
```

### 2. 定期维护

```sql
-- 优化表
OPTIMIZE TABLE applications;
OPTIMIZE TABLE resumes;
OPTIMIZE TABLE positions;

-- 分析表
ANALYZE TABLE applications;
```

### 3. 查询缓存

对于频繁查询的统计数据，考虑创建物化视图或定时任务更新汇总表。

## 🔒 安全建议

1. **权限管理**: 为不同用户角色创建不同的数据库用户

```sql
-- 创建只读用户（供查询使用）
CREATE USER 'reader'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT ON internship_system.* TO 'reader'@'localhost';

-- 创建应用用户（供应用程序使用）
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT, INSERT, UPDATE ON internship_system.* TO 'app_user'@'localhost';
```

2. **数据备份**

```bash
# 备份整个数据库
mysqldump -u root -p internship_system > backup_$(date +%Y%m%d).sql

# 恢复数据库
mysql -u root -p internship_system < backup_20240612.sql
```

3. **敏感信息处理**
   - 学生手机号、邮箱等敏感信息应考虑加密存储
   - 简历文件应存储在安全的文件系统中，数据库仅保存路径引用

## ❓ 常见问题

### Q1: LOAD DATA LOCAL INFILE 报错

**错误**: `The used command is not allowed with this MySQL version`

**解决**: 启用 `local_infile` 选项
```sql
SET GLOBAL local_infile = 1;
```

### Q2: 外键约束失败

**错误**: `Cannot add or update a child row: a foreign key constraint fails`

**解决**: 检查数据导入顺序，确保先导入父表（字典表），再导入子表（实体表和关联表）

### Q3: 中文乱码

**解决**: 确保数据库、表、连接都使用 utf8mb4 字符集
```sql
ALTER DATABASE internship_system CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
```

### Q4: 模拟数据不符合实际需求

**解决**: 修改 `generate_mock_data.py` 中的数据生成逻辑，调整数据量、分布等参数

## 📚 延伸阅读

- [MySQL 官方文档](https://dev.mysql.com/doc/)
- [数据库范式详解](https://en.wikipedia.org/wiki/Database_normalization)
- [SQL 性能优化最佳实践](https://use-the-index-luke.com/)

## 🤝 贡献

如发现问题或有改进建议，请提交 Issue 或 Pull Request。

---

**最后更新**: 2024-06-12
