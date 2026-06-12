# 数据库设计准备文档

## 项目概述
学生实习求职管理系统 - MySQL 数据库设计

## 核心实体分析

根据数据流图和需求描述，系统包含以下核心实体：

### 1. 学生表 (students)
**业务描述**: 存储学生基本信息

| 字段名 | 中文名 | 数据类型 | 约束 | 说明 |
|--------|--------|----------|------|------|
| student_id | 学号 | VARCHAR(20) | PRIMARY KEY | 学号作为主键 |
| name | 姓名 | VARCHAR(50) | NOT NULL | 学生姓名 |
| major | 专业 | VARCHAR(100) | NOT NULL | 所学专业 |
| contact | 联系方式 | VARCHAR(50) | NOT NULL | 手机号或邮箱 |
| created_at | 创建时间 | DATETIME | DEFAULT CURRENT_TIMESTAMP | 记录创建时间 |
| updated_at | 更新时间 | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 记录更新时间 |

### 2. 简历表 (resumes)
**业务描述**: 存储学生上传的简历信息

| 字段名 | 中文名 | 数据类型 | 约束 | 说明 |
|--------|--------|----------|------|------|
| resume_id | 简历编号 | INT | PRIMARY KEY AUTO_INCREMENT | 简历唯一标识 |
| student_id | 学号 | VARCHAR(20) | FOREIGN KEY | 关联学生表 |
| upload_time | 上传时间 | DATETIME | NOT NULL | 简历上传时间 |
| skill_tags | 技能标签 | TEXT | NULL | JSON 格式存储技能标签数组 |
| file_path | 文件路径 | VARCHAR(255) | NULL | 简历文件存储路径 |
| created_at | 创建时间 | DATETIME | DEFAULT CURRENT_TIMESTAMP | 记录创建时间 |

**关系**: 一个学生可以有多份简历 (1:N)

### 3. 岗位表 (positions)
**业务描述**: 存储企业发布的实习/招聘岗位信息

| 字段名 | 中文名 | 数据类型 | 约束 | 说明 |
|--------|--------|----------|------|------|
| position_id | 岗位编号 | INT | PRIMARY KEY AUTO_INCREMENT | 岗位唯一标识 |
| company_name | 公司名 | VARCHAR(200) | NOT NULL | 发布岗位的公司 |
| position_category | 岗位类别 | VARCHAR(100) | NOT NULL | 如：技术、市场、运营等 |
| skill_requirements | 技能需求 | TEXT | NULL | JSON 格式存储所需技能 |
| application_method | 投递方式 | VARCHAR(200) | NULL | 如：邮箱、网申链接等 |
| status | 状态 | ENUM('active', 'closed') | DEFAULT 'active' | 岗位状态 |
| created_at | 创建时间 | DATETIME | DEFAULT CURRENT_TIMESTAMP | 岗位发布时间 |
| updated_at | 更新时间 | DATETIME | ON UPDATE CURRENT_TIMESTAMP | 记录更新时间 |

### 4. 申请记录表 (applications)
**业务描述**: 记录学生申请岗位的详细信息

| 字段名 | 中文名 | 数据类型 | 约束 | 说明 |
|--------|--------|----------|------|------|
| application_id | 申请记录编号 | INT | PRIMARY KEY AUTO_INCREMENT | 申请记录唯一标识 |
| student_id | 学号 | VARCHAR(20) | FOREIGN KEY | 关联学生表 |
| position_id | 岗位编号 | INT | FOREIGN KEY | 关联岗位表 |
| resume_id | 简历编号 | INT | FOREIGN KEY | 使用的简历 |
| application_status | 申请状态 | ENUM('submitted', 'reviewing', 'interview', 'offered', 'rejected') | DEFAULT 'submitted' | 申请流程状态 |
| update_time | 更新时间 | DATETIME | NOT NULL | 状态最后更新时间 |
| hr_comment | HR评价 | TEXT | NULL | HR 反馈评价 |
| created_at | 创建时间 | DATETIME | DEFAULT CURRENT_TIMESTAMP | 申请提交时间 |

**关系**: 
- 一个学生可以申请多个岗位 (M:N 通过申请记录表实现)
- 一个岗位可以被多个学生申请 (M:N)
- 一份简历可以用于多次申请 (1:N)

### 5. 预约记录表 (appointments)
**业务描述**: 记录学生预约 CDO 咨询的信息

| 字段名 | 中文名 | 数据类型 | 约束 | 说明 |
|--------|--------|----------|------|------|
| appointment_id | 预约记录编号 | INT | PRIMARY KEY AUTO_INCREMENT | 预约记录唯一标识 |
| student_id | 学号 | VARCHAR(20) | FOREIGN KEY | 关联学生表 |
| appointment_time | 预约时间 | DATETIME | NOT NULL | 咨询预约时间 |
| consultation_type | 咨询类型 | VARCHAR(100) | NOT NULL | 如：简历修改、面试辅导、职业规划 |
| cdo_teacher | CDO老师 | VARCHAR(50) | NOT NULL | 负责咨询的老师姓名 |
| status | 状态 | ENUM('scheduled', 'completed', 'cancelled') | DEFAULT 'scheduled' | 预约状态 |
| notes | 备注 | TEXT | NULL | 咨询备注或记录 |
| created_at | 创建时间 | DATETIME | DEFAULT CURRENT_TIMESTAMP | 预约创建时间 |

**关系**: 一个学生可以有多次预约记录 (1:N)

## 数据关系图 (ERD)

```
students (1) ----< (N) resumes
students (1) ----< (N) applications
students (1) ----< (N) appointments

positions (1) ----< (N) applications

resumes (1) ----< (N) applications

applications 是核心关联表，连接 students, positions, resumes
```

## 索引设计建议

### students 表
- PRIMARY KEY: student_id
- INDEX: name (用于姓名搜索)
- INDEX: major (用于按专业筛选)

### resumes 表
- PRIMARY KEY: resume_id
- FOREIGN KEY INDEX: student_id
- INDEX: upload_time (用于按时间排序)

### positions 表
- PRIMARY KEY: position_id
- INDEX: company_name (用于按公司搜索)
- INDEX: position_category (用于按类别筛选)
- INDEX: status (用于筛选开放岗位)

### applications 表
- PRIMARY KEY: application_id
- FOREIGN KEY INDEX: student_id
- FOREIGN KEY INDEX: position_id
- FOREIGN KEY INDEX: resume_id
- INDEX: application_status (用于按状态筛选)
- COMPOSITE INDEX: (student_id, position_id) 防止重复申请
- INDEX: update_time (用于按时间排序)

### appointments 表
- PRIMARY KEY: appointment_id
- FOREIGN KEY INDEX: student_id
- INDEX: appointment_time (用于按时间查询)
- INDEX: cdo_teacher (用于按老师筛选)
- INDEX: status (用于筛选预约状态)

## 模拟数据准备计划

### 数据规模设计
- 学生: 100 条记录
- 简历: 150 条记录 (部分学生有多份简历)
- 岗位: 50 条记录
- 申请记录: 300 条记录
- 预约记录: 80 条记录

### 数据真实性要求
1. **学生数据**: 
   - 学号格式: 如 "20210001", "20220002"
   - 专业: 计算机科学、软件工程、数据科学、电子工程等
   - 联系方式: 模拟手机号和邮箱

2. **简历数据**:
   - 技能标签: Python, Java, JavaScript, SQL, React, Node.js, 数据分析等
   - 上传时间: 近一年内的随机时间

3. **岗位数据**:
   - 公司: 知名互联网公司、咨询公司、金融机构等
   - 岗位类别: 软件开发、数据分析、产品经理、市场运营等
   - 技能需求: 与岗位类别匹配的技能要求

4. **申请记录**:
   - 状态分布: 已提交 40%, 审核中 25%, 面试 20%, offer 10%, 拒绝 5%
   - 时间跨度: 最近 6 个月

5. **预约记录**:
   - 咨询类型: 简历修改、面试准备、职业规划、行业分析等
   - CDO 老师: 3-5 位不同的老师
   - 预约时间: 工作日上午和下午时段

## 下一步计划

1. ✅ 完成数据库设计文档
2. ⏳ 创建 MySQL 建表 SQL 脚本
3. ⏳ 编写 Python 模拟数据生成脚本
4. ⏳ 执行数据导入
5. ⏳ 验证数据完整性和关系约束

## 技术栈
- 数据库: MySQL 8.0+
- 字符集: utf8mb4
- 排序规则: utf8mb4_unicode_ci
- 数据生成: Python + Faker 库
