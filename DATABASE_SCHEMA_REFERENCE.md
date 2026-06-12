# 学生实习求职管理系统 - 数据库结构精简参考

## 数据库概览

**数据库名**: `internship_system`  
**字符集**: `utf8mb4`  
**排序规则**: `utf8mb4_unicode_ci`  
**总表数**: 13 张（4 字典表 + 7 实体表 + 2 关联表）  
**视图数**: 3 个

---

## 1. 字典表 (Dictionary Tables)

### 1.1 majors - 专业表
```
表名: majors
主键: major_id (INT, AUTO_INCREMENT)
字段:
  - major_id: 专业ID
  - major_name: 专业名称 (VARCHAR(100), NOT NULL, UNIQUE)
  - faculty: 所属院系 (VARCHAR(100))
  - created_at: 创建时间 (TIMESTAMP)

示例数据:
  (1, '计算机科学与技术', '计算机学院')
  (2, '软件工程', '软件学院')
  (3, '数据科学与大数据技术', '数据学院')
```

### 1.2 skills - 技能表
```
表名: skills
主键: skill_id (INT, AUTO_INCREMENT)
字段:
  - skill_id: 技能ID
  - skill_name: 技能名称 (VARCHAR(50), NOT NULL, UNIQUE)
  - skill_category: 技能分类 (VARCHAR(50))
  - created_at: 创建时间 (TIMESTAMP)

索引: idx_category (skill_category)

示例数据:
  (1, 'Python', '编程语言')
  (2, 'Java', '编程语言')
  (6, 'SQL', '数据库')
  (24, '机器学习', '人工智能')
```

### 1.3 position_categories - 岗位类别表
```
表名: position_categories
主键: category_id (INT, AUTO_INCREMENT)
字段:
  - category_id: 类别ID
  - category_name: 类别名称 (VARCHAR(100), NOT NULL, UNIQUE)
  - parent_category_id: 父类别ID (INT, NULL) → 自引用
  - created_at: 创建时间 (TIMESTAMP)

外键:
  - parent_category_id → position_categories(category_id)

示例数据:
  (1, '技术开发', NULL)
  (2, '后端开发', 1)  ← 父类别是"技术开发"
  (3, '前端开发', 1)
```

### 1.4 consultation_types - 咨询类型表
```
表名: consultation_types
主键: type_id (INT, AUTO_INCREMENT)
字段:
  - type_id: 咨询类型ID
  - type_name: 类型名称 (VARCHAR(100), NOT NULL, UNIQUE)
  - description: 类型说明 (TEXT)
  - duration_minutes: 默认时长 (INT, DEFAULT 30)
  - created_at: 创建时间 (TIMESTAMP)

示例数据:
  (1, '简历修改', '简历内容优化指导', 45)
  (2, '面试准备', '面试技巧培训', 60)
```

---

## 2. 核心实体表 (Core Entity Tables)

### 2.1 students - 学生表
```
表名: students
主键: student_id (VARCHAR(20))
字段:
  - student_id: 学号 (主键)
  - name: 姓名 (VARCHAR(50), NOT NULL)
  - gender: 性别 (ENUM('M', 'F', 'Other'))
  - email: 邮箱 (VARCHAR(100), UNIQUE)
  - phone: 手机号 (VARCHAR(20))
  - major_id: 专业ID (INT, NOT NULL)
  - enrollment_year: 入学年份 (YEAR, NOT NULL)
  - expected_graduation_year: 预计毕业年份 (YEAR, NOT NULL)
  - created_at, updated_at: 时间戳

外键:
  - major_id → majors(major_id)

索引:
  - idx_major (major_id)
  - idx_name (name)
  - idx_graduation (expected_graduation_year)

示例数据:
  ('20210001', '张三', 'M', 'student001@university.edu.cn', '13800138001', 1, 2021, 2025)
```

### 2.2 companies - 公司表
```
表名: companies
主键: company_id (INT, AUTO_INCREMENT)
字段:
  - company_id: 公司ID
  - company_name: 公司名称 (VARCHAR(200), NOT NULL, UNIQUE)
  - industry: 行业 (VARCHAR(100))
  - company_size: 规模 (ENUM('startup', 'small', 'medium', 'large', 'enterprise'))
  - country: 国家 (VARCHAR(50), DEFAULT '中国')
  - city: 城市 (VARCHAR(100))
  - website: 官网 (VARCHAR(255))
  - created_at, updated_at: 时间戳

索引:
  - idx_company_name (company_name)
  - idx_industry (industry)
  - idx_city (city)

示例数据:
  (1, '腾讯', '互联网', 'large', '中国', '深圳', 'https://www.tencent.com')
```

### 2.3 teachers - CDO教师表
```
表名: teachers
主键: teacher_id (INT, AUTO_INCREMENT)
字段:
  - teacher_id: 教师ID
  - teacher_name: 教师姓名 (VARCHAR(50), NOT NULL)
  - email: 邮箱 (VARCHAR(100), UNIQUE)
  - phone: 手机号 (VARCHAR(20))
  - specialization: 专长领域 (TEXT)
  - is_active: 是否在职 (BOOLEAN, DEFAULT TRUE)
  - created_at, updated_at: 时间戳

索引:
  - idx_name (teacher_name)
  - idx_active (is_active)

示例数据:
  (1, '张老师', 'zhang@university.edu.cn', '13800138001', '技术类岗位、互联网行业', TRUE)
```

### 2.4 resumes - 简历表
```
表名: resumes
主键: resume_id (INT, AUTO_INCREMENT)
字段:
  - resume_id: 简历ID
  - student_id: 学号 (VARCHAR(20), NOT NULL)
  - resume_title: 简历标题 (VARCHAR(200))
  - upload_time: 上传时间 (TIMESTAMP, NOT NULL)
  - file_path: 文件路径 (VARCHAR(255))
  - file_size: 文件大小 (INT, 单位:字节)
  - is_default: 是否默认简历 (BOOLEAN, DEFAULT FALSE)
  - created_at, updated_at: 时间戳

外键:
  - student_id → students(student_id) ON DELETE CASCADE

索引:
  - idx_student (student_id)
  - idx_upload_time (upload_time)

示例数据:
  (1, '20210001', '技术岗位简历', '2024-01-15 10:30:00', '/resumes/20210001_1.pdf', 256000, TRUE)
```

### 2.5 positions - 岗位表
```
表名: positions
主键: position_id (INT, AUTO_INCREMENT)
字段:
  - position_id: 岗位ID
  - company_id: 公司ID (INT, NOT NULL)
  - position_title: 岗位名称 (VARCHAR(200), NOT NULL)
  - category_id: 岗位类别ID (INT, NOT NULL)
  - employment_type: 雇佣类型 (ENUM('internship', 'full_time', 'part_time', 'contract'))
  - location: 工作地点 (VARCHAR(200))
  - salary_range: 薪资范围 (VARCHAR(100))
  - description: 岗位描述 (TEXT)
  - requirements: 任职要求 (TEXT)
  - application_method: 投递方式 (VARCHAR(200))
  - application_deadline: 截止日期 (DATE)
  - status: 状态 (ENUM('active', 'closed', 'filled'), DEFAULT 'active')
  - posted_date: 发布日期 (DATE, NOT NULL)
  - created_at, updated_at: 时间戳

外键:
  - company_id → companies(company_id)
  - category_id → position_categories(category_id)

索引:
  - idx_company (company_id)
  - idx_category (category_id)
  - idx_status (status)
  - idx_deadline (application_deadline)

示例数据:
  (1, 1, 'Java后端开发工程师', 2, 'internship', '深圳', '200-300元/天', '负责后端开发...', '本科及以上...', '官网申请', '2024-12-31', 'active', '2024-01-01')
```

### 2.6 applications - 申请记录表
```
表名: applications
主键: application_id (INT, AUTO_INCREMENT)
字段:
  - application_id: 申请ID
  - student_id: 学号 (VARCHAR(20), NOT NULL)
  - position_id: 岗位ID (INT, NOT NULL)
  - resume_id: 简历ID (INT, NOT NULL)
  - application_status: 申请状态 (ENUM)
      值: 'submitted', 'screening', 'interview', 'assessment', 'offered', 'accepted', 'rejected', 'withdrawn'
      默认: 'submitted'
  - submit_time: 提交时间 (TIMESTAMP, NOT NULL)
  - update_time: 更新时间 (TIMESTAMP, NOT NULL)
  - hr_comment: HR评价 (TEXT)
  - student_notes: 学生备注 (TEXT)
  - created_at: 创建时间 (TIMESTAMP)

外键:
  - student_id → students(student_id) ON DELETE CASCADE
  - position_id → positions(position_id)
  - resume_id → resumes(resume_id)

唯一约束:
  - UNIQUE KEY unique_application (student_id, position_id)  ← 防止重复申请

索引:
  - idx_student (student_id)
  - idx_position (position_id)
  - idx_status (application_status)
  - idx_update_time (update_time)

示例数据:
  (1, '20210001', 1, 1, 'interview', '2024-02-01 09:00:00', '2024-02-15 14:30:00', '表现优秀，进入面试', NULL)
```

### 2.7 appointments - 预约记录表
```
表名: appointments
主键: appointment_id (INT, AUTO_INCREMENT)
字段:
  - appointment_id: 预约ID
  - student_id: 学号 (VARCHAR(20), NOT NULL)
  - teacher_id: 教师ID (INT, NOT NULL)
  - type_id: 咨询类型ID (INT, NOT NULL)
  - appointment_time: 预约时间 (DATETIME, NOT NULL)
  - duration_minutes: 咨询时长 (INT, DEFAULT 30)
  - status: 状态 (ENUM('scheduled', 'completed', 'cancelled', 'no_show'), DEFAULT 'scheduled')
  - location: 咨询地点 (VARCHAR(200))
  - notes: 预约说明 (TEXT)
  - feedback: 咨询反馈 (TEXT)
  - created_at, updated_at: 时间戳

外键:
  - student_id → students(student_id) ON DELETE CASCADE
  - teacher_id → teachers(teacher_id)
  - type_id → consultation_types(type_id)

索引:
  - idx_student (student_id)
  - idx_teacher (teacher_id)
  - idx_appointment_time (appointment_time)
  - idx_status (status)

示例数据:
  (1, '20210001', 1, 1, '2024-03-15 14:00:00', 45, 'completed', 'CDO办公室', '希望优化简历', '已完成简历修改指导')
```

---

## 3. 关联表 (Many-to-Many Relationship Tables)

### 3.1 resume_skills - 简历-技能关联表
```
表名: resume_skills
主键: (resume_id, skill_id) 复合主键
字段:
  - resume_id: 简历ID (INT, NOT NULL)
  - skill_id: 技能ID (INT, NOT NULL)
  - proficiency_level: 熟练程度 (ENUM('beginner', 'intermediate', 'advanced', 'expert'))
  - created_at: 创建时间 (TIMESTAMP)

外键:
  - resume_id → resumes(resume_id) ON DELETE CASCADE
  - skill_id → skills(skill_id)

索引:
  - idx_skill (skill_id)

示例数据:
  (1, 1, 'advanced')    ← 简历1 掌握 Python (高级)
  (1, 2, 'intermediate') ← 简历1 掌握 Java (中级)
```

### 3.2 position_skills - 岗位-技能关联表
```
表名: position_skills
主键: (position_id, skill_id) 复合主键
字段:
  - position_id: 岗位ID (INT, NOT NULL)
  - skill_id: 技能ID (INT, NOT NULL)
  - is_required: 是否必需 (BOOLEAN, DEFAULT TRUE)
  - priority: 优先级 (INT, DEFAULT 0)  ← 数字越大越重要
  - created_at: 创建时间 (TIMESTAMP)

外键:
  - position_id → positions(position_id) ON DELETE CASCADE
  - skill_id → skills(skill_id)

索引:
  - idx_skill (skill_id)
  - idx_required (is_required)

示例数据:
  (1, 2, TRUE, 10)   ← 岗位1 必须要求 Java，优先级10
  (1, 6, TRUE, 8)    ← 岗位1 必须要求 SQL，优先级8
  (1, 20, FALSE, 3)  ← 岗位1 优先掌握 Git，优先级3
```

---

## 4. 视图 (Views)

### 4.1 v_student_profile - 学生档案视图
```
视图名: v_student_profile
用途: 学生完整档案，包含统计信息
字段:
  - student_id: 学号
  - name: 姓名
  - gender: 性别
  - email: 邮箱
  - phone: 手机号
  - major_name: 专业名称
  - faculty: 所属院系
  - enrollment_year: 入学年份
  - expected_graduation_year: 预计毕业年份
  - resume_count: 简历数量 (COUNT)
  - application_count: 申请数量 (COUNT)
  - appointment_count: 预约次数 (COUNT)

关联表:
  students ← majors ← resumes ← applications ← appointments

示例查询:
  SELECT * FROM v_student_profile WHERE student_id = '20210001';
```

### 4.2 v_position_details - 岗位详情视图
```
视图名: v_position_details
用途: 岗位完整信息，包含公司和技能
字段:
  - position_id: 岗位ID
  - position_title: 岗位名称
  - company_name: 公司名称
  - industry: 行业
  - country: 国家
  - city: 城市
  - position_category: 岗位类别名称
  - employment_type: 雇佣类型
  - location: 工作地点
  - salary_range: 薪资范围
  - status: 状态
  - posted_date: 发布日期
  - application_deadline: 截止日期
  - application_count: 申请人数 (COUNT)
  - required_skills: 所需技能列表 (GROUP_CONCAT)

关联表:
  positions ← companies ← position_categories ← applications ← position_skills ← skills

示例查询:
  SELECT * FROM v_position_details WHERE status = 'active';
```

### 4.3 v_application_details - 申请详情视图
```
视图名: v_application_details
用途: 申请记录完整信息
字段:
  - application_id: 申请ID
  - student_id: 学号
  - student_name: 学生姓名
  - major_name: 专业名称
  - position_id: 岗位ID
  - position_title: 岗位名称
  - company_name: 公司名称
  - application_status: 申请状态
  - submit_time: 提交时间
  - update_time: 更新时间
  - hr_comment: HR评价

关联表:
  applications ← students ← majors ← positions ← companies

示例查询:
  SELECT * FROM v_application_details 
  WHERE application_status = 'interview' 
  ORDER BY update_time DESC;
```

---

## 5. 关系图 (Entity Relationships)

```
字典表:
  majors (专业)
  skills (技能)
  position_categories (岗位类别，支持自引用层级)
  consultation_types (咨询类型)

核心流程:
  students (学生)
    ↓ 1:N
  resumes (简历)
    ↓ 1:N
  applications (申请) ← N:1 → positions (岗位) ← N:1 → companies (公司)
    
  students (学生)
    ↓ 1:N
  appointments (预约) ← N:1 → teachers (教师)
                       ↓ N:1
                consultation_types (咨询类型)

技能匹配:
  resumes ←→ resume_skills ←→ skills
  positions ←→ position_skills ←→ skills

外键关系:
  students.major_id → majors.major_id
  resumes.student_id → students.student_id [CASCADE]
  positions.company_id → companies.company_id
  positions.category_id → position_categories.category_id
  applications.student_id → students.student_id [CASCADE]
  applications.position_id → positions.position_id
  applications.resume_id → resumes.resume_id
  appointments.student_id → students.student_id [CASCADE]
  appointments.teacher_id → teachers.teacher_id
  appointments.type_id → consultation_types.type_id
  resume_skills.resume_id → resumes.resume_id [CASCADE]
  resume_skills.skill_id → skills.skill_id
  position_skills.position_id → positions.position_id [CASCADE]
  position_skills.skill_id → skills.skill_id
```

---

## 6. 常用查询场景

### 6.1 学生相关
```sql
-- 查询某专业学生数
SELECT m.major_name, COUNT(*) as count
FROM students s JOIN majors m ON s.major_id = m.major_id
WHERE m.major_name = '计算机科学与技术';

-- 查询学生完整档案（使用视图）
SELECT * FROM v_student_profile WHERE student_id = '20210001';
```

### 6.2 岗位相关
```sql
-- 查询开放岗位（使用视图）
SELECT * FROM v_position_details WHERE status = 'active';

-- 查询岗位所需技能
SELECT p.position_title, GROUP_CONCAT(s.skill_name) as skills
FROM positions p
JOIN position_skills ps ON p.position_id = ps.position_id
JOIN skills s ON ps.skill_id = s.skill_id
WHERE ps.is_required = TRUE
GROUP BY p.position_id;
```

### 6.3 申请状态
```sql
-- 查询某状态的申请数
SELECT COUNT(*) FROM applications WHERE application_status = 'interview';

-- 申请漏斗分析
SELECT application_status, COUNT(*) as count
FROM applications
GROUP BY application_status;
```

### 6.4 技能匹配
```sql
-- 查询掌握Python的学生
SELECT DISTINCT s.student_id, s.name
FROM students s
JOIN resumes r ON s.student_id = r.student_id
JOIN resume_skills rs ON r.resume_id = rs.resume_id
JOIN skills sk ON rs.skill_id = sk.skill_id
WHERE sk.skill_name = 'Python';
```

---

## 7. 数据规模参考

```
字典表:
  majors: 15 条
  skills: 40 条
  position_categories: 20 条
  consultation_types: 6 条

实体表:
  students: 100 条
  companies: 25 条
  teachers: 5 条
  resumes: 150 条
  positions: 50 条
  applications: 295 条
  appointments: 80 条

关联表:
  resume_skills: 846 条
  position_skills: 359 条

总计: 1,991 条记录
```

---

## 8. 重要约束

### 主键
- 所有表都有主键
- 关联表使用复合主键

### 外键
- 级联删除: students 删除时，相关 resumes、applications、appointments 自动删除
- 引用完整性: 所有外键都有对应的父表记录

### 唯一约束
- students.email (唯一)
- companies.company_name (唯一)
- majors.major_name (唯一)
- skills.skill_name (唯一)
- applications (student_id, position_id) 复合唯一 ← 防止重复申请

### 枚举约束
- students.gender: 'M', 'F', 'Other'
- companies.company_size: 'startup', 'small', 'medium', 'large', 'enterprise'
- positions.employment_type: 'internship', 'full_time', 'part_time', 'contract'
- positions.status: 'active', 'closed', 'filled'
- applications.application_status: 'submitted', 'screening', 'interview', 'assessment', 'offered', 'accepted', 'rejected', 'withdrawn'
- appointments.status: 'scheduled', 'completed', 'cancelled', 'no_show'
- resume_skills.proficiency_level: 'beginner', 'intermediate', 'advanced', 'expert'

---

## 9. 快速查询清单

**查询专业**: `SELECT * FROM majors;`  
**查询技能**: `SELECT * FROM skills;`  
**查询学生**: `SELECT * FROM v_student_profile;`  
**查询岗位**: `SELECT * FROM v_position_details WHERE status = 'active';`  
**查询申请**: `SELECT * FROM v_application_details;`  
**查询预约**: `SELECT * FROM appointments;`  
**查询公司**: `SELECT * FROM companies;`  
**查询教师**: `SELECT * FROM teachers WHERE is_active = TRUE;`

---

**版本**: v1.0  
**适用于**: 精简版 13 张表设计  
**完整SQL**: `database_schema_simplified.sql`  
**最后更新**: 2024-06-12
