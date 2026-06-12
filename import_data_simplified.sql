-- ============================================================
-- 学生实习求职管理系统 - 数据导入脚本（精简版）
-- 使用 LOAD DATA LOCAL INFILE 批量导入 CSV 数据
-- 移除了国家表，简化设计
-- ============================================================

USE internship_system;

-- 设置导入选项
SET FOREIGN_KEY_CHECKS = 0;  -- 临时禁用外键检查
SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';

-- ============================================================
-- 1. 导入字典表
-- ============================================================

-- 导入专业表
LOAD DATA LOCAL INFILE 'mock_data/majors.csv'
INTO TABLE majors
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(major_id, major_name, faculty, created_at);

-- 导入技能表
LOAD DATA LOCAL INFILE 'mock_data/skills.csv'
INTO TABLE skills
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(skill_id, skill_name, skill_category, created_at);

-- 导入岗位类别表
LOAD DATA LOCAL INFILE 'mock_data/position_categories.csv'
INTO TABLE position_categories
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(category_id, category_name, @parent_category_id, created_at)
SET parent_category_id = NULLIF(@parent_category_id, '');

-- 导入咨询类型表
LOAD DATA LOCAL INFILE 'mock_data/consultation_types.csv'
INTO TABLE consultation_types
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(type_id, type_name, description, duration_minutes, created_at);

-- 导入公司表（精简版 - country 直接存储）
LOAD DATA LOCAL INFILE 'mock_data/companies.csv'
INTO TABLE companies
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(company_id, company_name, industry, company_size, country, city, website, created_at, updated_at);

-- 导入教师表
LOAD DATA LOCAL INFILE 'mock_data/teachers.csv'
INTO TABLE teachers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(teacher_id, teacher_name, @email, @phone, @specialization, is_active, created_at, updated_at)
SET
    email = NULLIF(@email, ''),
    phone = NULLIF(@phone, ''),
    specialization = NULLIF(@specialization, '');

-- ============================================================
-- 2. 导入核心实体表
-- ============================================================

-- 导入学生表
LOAD DATA LOCAL INFILE 'mock_data/students.csv'
INTO TABLE students
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(student_id, name, @gender, @email, @phone, major_id, enrollment_year, expected_graduation_year, created_at, updated_at)
SET
    gender = NULLIF(@gender, ''),
    email = NULLIF(@email, ''),
    phone = NULLIF(@phone, '');

-- 导入简历表
LOAD DATA LOCAL INFILE 'mock_data/resumes.csv'
INTO TABLE resumes
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(resume_id, student_id, @resume_title, upload_time, @file_path, @file_size, is_default, created_at, updated_at)
SET
    resume_title = NULLIF(@resume_title, ''),
    file_path = NULLIF(@file_path, ''),
    file_size = NULLIF(@file_size, '');

-- 导入岗位表
LOAD DATA LOCAL INFILE 'mock_data/positions.csv'
INTO TABLE positions
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(position_id, company_id, position_title, category_id, employment_type,
 @location, @salary_range, @description, @requirements, @application_method,
 @application_deadline, status, posted_date, created_at, updated_at)
SET
    location = NULLIF(@location, ''),
    salary_range = NULLIF(@salary_range, ''),
    description = NULLIF(@description, ''),
    requirements = NULLIF(@requirements, ''),
    application_method = NULLIF(@application_method, ''),
    application_deadline = NULLIF(@application_deadline, '');

-- 导入申请记录表
LOAD DATA LOCAL INFILE 'mock_data/applications.csv'
INTO TABLE applications
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(application_id, student_id, position_id, resume_id, application_status,
 submit_time, update_time, @hr_comment, @student_notes, created_at)
SET
    hr_comment = NULLIF(@hr_comment, ''),
    student_notes = NULLIF(@student_notes, '');

-- 导入预约记录表
LOAD DATA LOCAL INFILE 'mock_data/appointments.csv'
INTO TABLE appointments
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(appointment_id, student_id, teacher_id, type_id, appointment_time,
 duration_minutes, status, @location, @notes, @feedback, created_at, updated_at)
SET
    location = NULLIF(@location, ''),
    notes = NULLIF(@notes, ''),
    feedback = NULLIF(@feedback, '');

-- ============================================================
-- 3. 导入关联表
-- ============================================================

-- 导入简历-技能关联表
LOAD DATA LOCAL INFILE 'mock_data/resume_skills.csv'
INTO TABLE resume_skills
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(resume_id, skill_id, @proficiency_level, created_at)
SET proficiency_level = NULLIF(@proficiency_level, '');

-- 导入岗位-技能关联表
LOAD DATA LOCAL INFILE 'mock_data/position_skills.csv'
INTO TABLE position_skills
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(position_id, skill_id, is_required, priority, created_at);

-- ============================================================
-- 4. 恢复设置
-- ============================================================

SET FOREIGN_KEY_CHECKS = 1;  -- 恢复外键检查

-- ============================================================
-- 5. 验证导入结果
-- ============================================================

SELECT '字典表导入结果' as category;
SELECT 'majors' as table_name, COUNT(*) as row_count FROM majors
UNION ALL
SELECT 'skills', COUNT(*) FROM skills
UNION ALL
SELECT 'position_categories', COUNT(*) FROM position_categories
UNION ALL
SELECT 'consultation_types', COUNT(*) FROM consultation_types
UNION ALL
SELECT 'companies', COUNT(*) FROM companies
UNION ALL
SELECT 'teachers', COUNT(*) FROM teachers;

SELECT '核心实体表导入结果' as category;
SELECT 'students' as table_name, COUNT(*) as row_count FROM students
UNION ALL
SELECT 'resumes', COUNT(*) FROM resumes
UNION ALL
SELECT 'positions', COUNT(*) FROM positions
UNION ALL
SELECT 'applications', COUNT(*) FROM applications
UNION ALL
SELECT 'appointments', COUNT(*) FROM appointments;

SELECT '关联表导入结果' as category;
SELECT 'resume_skills' as table_name, COUNT(*) as row_count FROM resume_skills
UNION ALL
SELECT 'position_skills', COUNT(*) FROM position_skills;

-- ============================================================
-- 6. 数据完整性检查
-- ============================================================

-- 检查外键引用完整性
SELECT 'students -> majors 外键检查' as check_name,
       COUNT(*) as invalid_count
FROM students s
LEFT JOIN majors m ON s.major_id = m.major_id
WHERE m.major_id IS NULL;

SELECT 'applications -> students 外键检查' as check_name,
       COUNT(*) as invalid_count
FROM applications a
LEFT JOIN students s ON a.student_id = s.student_id
WHERE s.student_id IS NULL;

SELECT 'applications -> positions 外键检查' as check_name,
       COUNT(*) as invalid_count
FROM applications a
LEFT JOIN positions p ON a.position_id = p.position_id
WHERE p.position_id IS NULL;

SELECT 'applications -> resumes 外键检查' as check_name,
       COUNT(*) as invalid_count
FROM applications a
LEFT JOIN resumes r ON a.resume_id = r.resume_id
WHERE r.resume_id IS NULL;

-- 检查唯一性约束
SELECT '重复申请检查' as check_name,
       COUNT(*) as duplicate_count
FROM (
    SELECT student_id, position_id, COUNT(*) as cnt
    FROM applications
    GROUP BY student_id, position_id
    HAVING cnt > 1
) duplicates;

-- ============================================================
-- 7. 数据统计分析
-- ============================================================

-- 公司分布统计
SELECT '公司地区分布' as analysis_type;
SELECT country, city, COUNT(*) as company_count
FROM companies
GROUP BY country, city
ORDER BY country, company_count DESC;

-- ============================================================
-- 导入完成提示
-- ============================================================

SELECT '数据导入完成！（精简版 - 无国家表）' as status,
       NOW() as completion_time;
