-- ============================================================
-- 学生实习求职管理系统 - 精简优化版
-- 移除不必要的国家表，简化设计
-- ============================================================

CREATE DATABASE IF NOT EXISTS internship_system
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE internship_system;

-- ============================================================
-- 字典表 (Dictionary Tables) - 精简版
-- ============================================================

-- 专业表
DROP TABLE IF EXISTS majors;
CREATE TABLE majors (
    major_id INT AUTO_INCREMENT PRIMARY KEY,
    major_name VARCHAR(100) NOT NULL UNIQUE,
    faculty VARCHAR(100) COMMENT '所属院系',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) COMMENT '专业字典表';

-- 技能表
DROP TABLE IF EXISTS skills;
CREATE TABLE skills (
    skill_id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(50) NOT NULL UNIQUE,
    skill_category VARCHAR(50) COMMENT '技能分类：编程语言/框架/工具/软技能',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (skill_category)
) COMMENT '技能字典表';

-- 岗位类别表
DROP TABLE IF EXISTS position_categories;
CREATE TABLE position_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    parent_category_id INT NULL COMMENT '父类别ID，支持层级分类',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_category_id) REFERENCES position_categories(category_id)
) COMMENT '岗位类别字典表';

-- 咨询类型表
DROP TABLE IF EXISTS consultation_types;
CREATE TABLE consultation_types (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT COMMENT '咨询类型说明',
    duration_minutes INT DEFAULT 30 COMMENT '默认咨询时长（分钟）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) COMMENT '咨询类型字典表';

-- ============================================================
-- 核心实体表 (Core Entity Tables)
-- ============================================================

-- 学生表
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    student_id VARCHAR(20) PRIMARY KEY COMMENT '学号',
    name VARCHAR(50) NOT NULL,
    gender ENUM('M', 'F', 'Other') COMMENT '性别',
    email VARCHAR(100) UNIQUE COMMENT '邮箱',
    phone VARCHAR(20) COMMENT '手机号',
    major_id INT NOT NULL COMMENT '专业ID',
    enrollment_year YEAR NOT NULL COMMENT '入学年份',
    expected_graduation_year YEAR NOT NULL COMMENT '预计毕业年份',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (major_id) REFERENCES majors(major_id),
    INDEX idx_major (major_id),
    INDEX idx_name (name),
    INDEX idx_graduation (expected_graduation_year)
) COMMENT '学生基本信息表';

-- 公司表（精简版 - 移除国家外键）
DROP TABLE IF EXISTS companies;
CREATE TABLE companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(200) NOT NULL UNIQUE,
    industry VARCHAR(100) COMMENT '行业',
    company_size ENUM('startup', 'small', 'medium', 'large', 'enterprise') COMMENT '公司规模',
    country VARCHAR(50) DEFAULT '中国' COMMENT '国家',
    city VARCHAR(100) COMMENT '城市',
    website VARCHAR(255) COMMENT '公司官网',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_company_name (company_name),
    INDEX idx_industry (industry),
    INDEX idx_city (city)
) COMMENT '公司信息表';

-- CDO教师表
DROP TABLE IF EXISTS teachers;
CREATE TABLE teachers (
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    specialization TEXT COMMENT '专长领域',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否在职',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (teacher_name),
    INDEX idx_active (is_active)
) COMMENT 'CDO职业发展老师表';

-- 简历表
DROP TABLE IF EXISTS resumes;
CREATE TABLE resumes (
    resume_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    resume_title VARCHAR(200) COMMENT '简历标题/版本名称',
    upload_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    file_path VARCHAR(255) COMMENT '文件存储路径',
    file_size INT COMMENT '文件大小（字节）',
    is_default BOOLEAN DEFAULT FALSE COMMENT '是否为默认简历',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    INDEX idx_student (student_id),
    INDEX idx_upload_time (upload_time)
) COMMENT '简历信息表';

-- 岗位表
DROP TABLE IF EXISTS positions;
CREATE TABLE positions (
    position_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    position_title VARCHAR(200) NOT NULL COMMENT '岗位名称',
    category_id INT NOT NULL,
    employment_type ENUM('internship', 'full_time', 'part_time', 'contract') DEFAULT 'internship',
    location VARCHAR(200) COMMENT '工作地点',
    salary_range VARCHAR(100) COMMENT '薪资范围',
    description TEXT COMMENT '岗位描述',
    requirements TEXT COMMENT '任职要求',
    application_method VARCHAR(200) COMMENT '投递方式',
    application_deadline DATE COMMENT '截止日期',
    status ENUM('active', 'closed', 'filled') DEFAULT 'active',
    posted_date DATE NOT NULL COMMENT '发布日期',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    FOREIGN KEY (category_id) REFERENCES position_categories(category_id),
    INDEX idx_company (company_id),
    INDEX idx_category (category_id),
    INDEX idx_status (status),
    INDEX idx_deadline (application_deadline)
) COMMENT '岗位信息表';

-- 申请记录表
DROP TABLE IF EXISTS applications;
CREATE TABLE applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    position_id INT NOT NULL,
    resume_id INT NOT NULL,
    application_status ENUM('submitted', 'screening', 'interview', 'assessment', 'offered', 'accepted', 'rejected', 'withdrawn') DEFAULT 'submitted',
    submit_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    hr_comment TEXT COMMENT 'HR评价反馈',
    student_notes TEXT COMMENT '学生备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (position_id) REFERENCES positions(position_id),
    FOREIGN KEY (resume_id) REFERENCES resumes(resume_id),
    UNIQUE KEY unique_application (student_id, position_id) COMMENT '防止重复申请',
    INDEX idx_student (student_id),
    INDEX idx_position (position_id),
    INDEX idx_status (application_status),
    INDEX idx_update_time (update_time)
) COMMENT '申请记录表';

-- 预约记录表
DROP TABLE IF EXISTS appointments;
CREATE TABLE appointments (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    teacher_id INT NOT NULL,
    type_id INT NOT NULL,
    appointment_time DATETIME NOT NULL,
    duration_minutes INT DEFAULT 30 COMMENT '咨询时长',
    status ENUM('scheduled', 'completed', 'cancelled', 'no_show') DEFAULT 'scheduled',
    location VARCHAR(200) COMMENT '咨询地点/会议室',
    notes TEXT COMMENT '预约说明',
    feedback TEXT COMMENT '咨询反馈记录',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
    FOREIGN KEY (type_id) REFERENCES consultation_types(type_id),
    INDEX idx_student (student_id),
    INDEX idx_teacher (teacher_id),
    INDEX idx_appointment_time (appointment_time),
    INDEX idx_status (status)
) COMMENT '咨询预约记录表';

-- ============================================================
-- 关联表 (Many-to-Many Relationship Tables)
-- ============================================================

-- 简历-技能关联表
DROP TABLE IF EXISTS resume_skills;
CREATE TABLE resume_skills (
    resume_id INT NOT NULL,
    skill_id INT NOT NULL,
    proficiency_level ENUM('beginner', 'intermediate', 'advanced', 'expert') COMMENT '熟练程度',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (resume_id, skill_id),
    FOREIGN KEY (resume_id) REFERENCES resumes(resume_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id),
    INDEX idx_skill (skill_id)
) COMMENT '简历技能关联表';

-- 岗位-技能关联表
DROP TABLE IF EXISTS position_skills;
CREATE TABLE position_skills (
    position_id INT NOT NULL,
    skill_id INT NOT NULL,
    is_required BOOLEAN DEFAULT TRUE COMMENT '是否必需',
    priority INT DEFAULT 0 COMMENT '优先级：数字越大越重要',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (position_id, skill_id),
    FOREIGN KEY (position_id) REFERENCES positions(position_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id),
    INDEX idx_skill (skill_id),
    INDEX idx_required (is_required)
) COMMENT '岗位技能需求关联表';

-- ============================================================
-- 视图 (Views for Common Queries)
-- ============================================================

-- 学生完整信息视图
CREATE OR REPLACE VIEW v_student_profile AS
SELECT
    s.student_id,
    s.name,
    s.gender,
    s.email,
    s.phone,
    m.major_name,
    m.faculty,
    s.enrollment_year,
    s.expected_graduation_year,
    COUNT(DISTINCT r.resume_id) as resume_count,
    COUNT(DISTINCT a.application_id) as application_count,
    COUNT(DISTINCT ap.appointment_id) as appointment_count
FROM students s
LEFT JOIN majors m ON s.major_id = m.major_id
LEFT JOIN resumes r ON s.student_id = r.student_id
LEFT JOIN applications a ON s.student_id = a.student_id
LEFT JOIN appointments ap ON s.student_id = ap.student_id
GROUP BY s.student_id;

-- 岗位完整信息视图
CREATE OR REPLACE VIEW v_position_details AS
SELECT
    p.position_id,
    p.position_title,
    c.company_name,
    c.industry,
    c.country,
    c.city,
    pc.category_name as position_category,
    p.employment_type,
    p.location,
    p.salary_range,
    p.status,
    p.posted_date,
    p.application_deadline,
    COUNT(DISTINCT a.application_id) as application_count,
    GROUP_CONCAT(DISTINCT s.skill_name ORDER BY ps.priority DESC SEPARATOR ', ') as required_skills
FROM positions p
JOIN companies c ON p.company_id = c.company_id
JOIN position_categories pc ON p.category_id = pc.category_id
LEFT JOIN applications a ON p.position_id = a.position_id
LEFT JOIN position_skills ps ON p.position_id = ps.position_id
LEFT JOIN skills s ON ps.skill_id = s.skill_id
GROUP BY p.position_id;

-- 申请记录详情视图
CREATE OR REPLACE VIEW v_application_details AS
SELECT
    a.application_id,
    a.student_id,
    s.name as student_name,
    m.major_name,
    p.position_id,
    p.position_title,
    c.company_name,
    a.application_status,
    a.submit_time,
    a.update_time,
    a.hr_comment
FROM applications a
JOIN students s ON a.student_id = s.student_id
JOIN majors m ON s.major_id = m.major_id
JOIN positions p ON a.position_id = p.position_id
JOIN companies c ON p.company_id = c.company_id;

-- ============================================================
-- 设计说明
-- ============================================================
-- 1. 移除了不必要的 countries 表，简化设计
-- 2. companies.country 改为 VARCHAR 直接存储
-- 3. 保留了核心的范式设计优势
-- 4. 减少了不必要的 JOIN 操作
-- 5. 更适合校内求职系统的实际场景
-- ============================================================
