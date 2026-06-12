"""
将 CSV 数据转换为 INSERT SQL 语句
适用于精简版 13 张表设计
"""

import csv
from pathlib import Path

INPUT_DIR = Path("mock_data")
OUTPUT_FILE = "insert_data.sql"

def escape_sql_string(value):
    """转义 SQL 字符串中的特殊字符"""
    if value is None or value == '':
        return 'NULL'
    if isinstance(value, (int, float)):
        return str(value)
    # 转义单引号和反斜杠
    value = str(value).replace('\\', '\\\\').replace("'", "''")
    return f"'{value}'"

def csv_to_insert(csv_file, table_name, batch_size=100):
    """将 CSV 文件转换为 INSERT 语句"""
    filepath = INPUT_DIR / csv_file
    if not filepath.exists():
        print(f"⚠️  跳过 {csv_file} (文件不存在)")
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # 读取表头
        rows = list(reader)

    if not rows:
        return []

    inserts = []
    inserts.append(f"\n-- 导入 {table_name} 表 ({len(rows)} 条记录)")

    # 批量插入
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i+batch_size]

        # 构建 INSERT 语句
        columns = ', '.join(headers)
        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES\n"

        values_list = []
        for row in batch:
            # 处理每个字段
            escaped_values = []
            for value in row:
                if value == '' or value == 'None':
                    escaped_values.append('NULL')
                else:
                    escaped_values.append(escape_sql_string(value))

            values_str = '(' + ', '.join(escaped_values) + ')'
            values_list.append(values_str)

        insert_sql += ',\n'.join(values_list) + ';'
        inserts.append(insert_sql)

    print(f"✓ 转换 {csv_file} -> {len(rows)} 条 INSERT 语句")
    return inserts

def main():
    print("=" * 60)
    print("CSV 转 INSERT SQL 脚本")
    print("=" * 60)

    sql_statements = []

    # SQL 文件头部
    sql_statements.append("""-- ============================================================
-- 学生实习求职管理系统 - INSERT 数据导入脚本
-- 精简版 13 张表设计
-- 自动生成，包含完整的模拟数据
-- ============================================================

USE internship_system;

-- 设置选项
SET FOREIGN_KEY_CHECKS = 0;
SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';

-- ============================================================
-- 1. 字典表数据
-- ============================================================
""")

    # 字典表
    print("\n[字典表]")
    sql_statements.extend(csv_to_insert('majors.csv', 'majors'))
    sql_statements.extend(csv_to_insert('skills.csv', 'skills'))
    sql_statements.extend(csv_to_insert('position_categories.csv', 'position_categories'))
    sql_statements.extend(csv_to_insert('consultation_types.csv', 'consultation_types'))
    sql_statements.extend(csv_to_insert('companies.csv', 'companies'))
    sql_statements.extend(csv_to_insert('teachers.csv', 'teachers'))

    sql_statements.append("""
-- ============================================================
-- 2. 核心实体表数据
-- ============================================================
""")

    # 核心实体表
    print("\n[核心实体表]")
    sql_statements.extend(csv_to_insert('students.csv', 'students'))
    sql_statements.extend(csv_to_insert('resumes.csv', 'resumes'))
    sql_statements.extend(csv_to_insert('positions.csv', 'positions'))
    sql_statements.extend(csv_to_insert('applications.csv', 'applications'))
    sql_statements.extend(csv_to_insert('appointments.csv', 'appointments'))

    sql_statements.append("""
-- ============================================================
-- 3. 关联表数据
-- ============================================================
""")

    # 关联表
    print("\n[关联表]")
    sql_statements.extend(csv_to_insert('resume_skills.csv', 'resume_skills'))
    sql_statements.extend(csv_to_insert('position_skills.csv', 'position_skills'))

    sql_statements.append("""
-- ============================================================
-- 4. 恢复设置
-- ============================================================

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- 5. 验证数据
-- ============================================================

SELECT '数据导入验证' as category;

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
SELECT 'teachers', COUNT(*) FROM teachers
UNION ALL
SELECT 'students', COUNT(*) FROM students
UNION ALL
SELECT 'resumes', COUNT(*) FROM resumes
UNION ALL
SELECT 'positions', COUNT(*) FROM positions
UNION ALL
SELECT 'applications', COUNT(*) FROM applications
UNION ALL
SELECT 'appointments', COUNT(*) FROM appointments
UNION ALL
SELECT 'resume_skills', COUNT(*) FROM resume_skills
UNION ALL
SELECT 'position_skills', COUNT(*) FROM position_skills;

SELECT '✓ 数据导入完成！' as status, NOW() as completion_time;
""")

    # 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_statements))

    print("\n" + "=" * 60)
    print(f"✓ SQL 文件已生成: {OUTPUT_FILE}")
    print("=" * 60)

    # 统计信息
    total_lines = len('\n'.join(sql_statements).split('\n'))
    print(f"\n文件统计:")
    print(f"  总行数: {total_lines:,}")
    print(f"  文件大小: {Path(OUTPUT_FILE).stat().st_size / 1024:.1f} KB")
    print(f"\n使用方法:")
    print(f"  mysql -u root -p internship_system < {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
