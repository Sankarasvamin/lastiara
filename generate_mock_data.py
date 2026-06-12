"""
学生实习求职管理系统 - 数据模拟生成脚本
生成符合第三范式的测试数据
"""

import random
import csv
from datetime import datetime, timedelta
from pathlib import Path

# 设置随机种子，保证可复现
random.seed(42)

# 输出目录
OUTPUT_DIR = Path("mock_data")
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# 字典数据
# ============================================================

# 国家数据（直接存储，不需要独立表）
COUNTRIES = ["中国", "美国", "英国", "日本", "新加坡"]

# 专业数据
MAJORS = [
    (1, "计算机科学与技术", "计算机学院"),
    (2, "软件工程", "软件学院"),
    (3, "数据科学与大数据技术", "数据学院"),
    (4, "人工智能", "人工智能学院"),
    (5, "信息安全", "网络空间安全学院"),
    (6, "电子信息工程", "电子工程学院"),
    (7, "自动化", "自动化学院"),
    (8, "通信工程", "通信学院"),
    (9, "数学与应用数学", "数学学院"),
    (10, "统计学", "统计学院"),
    (11, "金融学", "经济学院"),
    (12, "会计学", "商学院"),
    (13, "市场营销", "商学院"),
    (14, "工商管理", "管理学院"),
    (15, "英语", "外国语学院"),
]

# 技能数据
SKILLS = [
    (1, "Python", "编程语言"),
    (2, "Java", "编程语言"),
    (3, "JavaScript", "编程语言"),
    (4, "C++", "编程语言"),
    (5, "Go", "编程语言"),
    (6, "SQL", "数据库"),
    (7, "MySQL", "数据库"),
    (8, "PostgreSQL", "数据库"),
    (9, "MongoDB", "数据库"),
    (10, "Redis", "数据库"),
    (11, "React", "前端框架"),
    (12, "Vue.js", "前端框架"),
    (13, "Angular", "前端框架"),
    (14, "Node.js", "后端框架"),
    (15, "Django", "后端框架"),
    (16, "Spring Boot", "后端框架"),
    (17, "Flask", "后端框架"),
    (18, "Docker", "DevOps工具"),
    (19, "Kubernetes", "DevOps工具"),
    (20, "Git", "版本控制"),
    (21, "Linux", "操作系统"),
    (22, "AWS", "云计算"),
    (23, "Azure", "云计算"),
    (24, "机器学习", "人工智能"),
    (25, "深度学习", "人工智能"),
    (26, "TensorFlow", "AI框架"),
    (27, "PyTorch", "AI框架"),
    (28, "数据分析", "数据科学"),
    (29, "数据可视化", "数据科学"),
    (30, "Pandas", "数据处理"),
    (31, "NumPy", "数据处理"),
    (32, "Spark", "大数据"),
    (33, "Hadoop", "大数据"),
    (34, "Excel", "办公软件"),
    (35, "PowerPoint", "办公软件"),
    (36, "数据分析能力", "软技能"),
    (37, "沟通能力", "软技能"),
    (38, "团队协作", "软技能"),
    (39, "项目管理", "软技能"),
    (40, "问题解决", "软技能"),
]

# 岗位类别数据
POSITION_CATEGORIES = [
    (1, "技术开发", None),
    (2, "后端开发", 1),
    (3, "前端开发", 1),
    (4, "全栈开发", 1),
    (5, "移动开发", 1),
    (6, "测试工程", 1),
    (7, "数据相关", None),
    (8, "数据分析", 7),
    (9, "数据工程", 7),
    (10, "数据科学", 7),
    (11, "算法研究", None),
    (12, "机器学习", 11),
    (13, "计算机视觉", 11),
    (14, "自然语言处理", 11),
    (15, "产品运营", None),
    (16, "产品经理", 15),
    (17, "运营专员", 15),
    (18, "市场营销", None),
    (19, "设计相关", None),
    (20, "UI/UX设计", 19),
]

# 咨询类型数据
CONSULTATION_TYPES = [
    (1, "简历修改", "简历内容、格式、措辞优化指导", 45),
    (2, "面试准备", "面试技巧、常见问题、模拟面试", 60),
    (3, "职业规划", "职业发展路径、行业选择建议", 60),
    (4, "行业分析", "特定行业现状、趋势、要求分析", 45),
    (5, "求职策略", "求职渠道、申请技巧、时间规划", 45),
    (6, "技能提升", "技能差距分析、学习建议", 30),
]

# 公司数据（精简版 - 直接存储国家）
COMPANIES = [
    (1, "腾讯", "互联网", "large", "中国", "深圳", "https://www.tencent.com"),
    (2, "阿里巴巴", "互联网", "enterprise", "中国", "杭州", "https://www.alibaba.com"),
    (3, "字节跳动", "互联网", "large", "中国", "北京", "https://www.bytedance.com"),
    (4, "华为", "通信", "enterprise", "中国", "深圳", "https://www.huawei.com"),
    (5, "百度", "互联网", "large", "中国", "北京", "https://www.baidu.com"),
    (6, "美团", "互联网", "large", "中国", "北京", "https://www.meituan.com"),
    (7, "京东", "电商", "large", "中国", "北京", "https://www.jd.com"),
    (8, "网易", "互联网", "large", "中国", "杭州", "https://www.163.com"),
    (9, "小米", "电子", "large", "中国", "北京", "https://www.mi.com"),
    (10, "拼多多", "电商", "large", "中国", "上海", "https://www.pinduoduo.com"),
    (11, "滴滴出行", "互联网", "large", "中国", "北京", "https://www.didiglobal.com"),
    (12, "携程", "在线旅游", "medium", "中国", "上海", "https://www.ctrip.com"),
    (13, "哔哩哔哩", "视频", "medium", "中国", "上海", "https://www.bilibili.com"),
    (14, "快手", "短视频", "large", "中国", "北京", "https://www.kuaishou.com"),
    (15, "商汤科技", "人工智能", "medium", "中国", "上海", "https://www.sensetime.com"),
    (16, "微软中国", "科技", "enterprise", "中国", "北京", "https://www.microsoft.com"),
    (17, "谷歌中国", "科技", "enterprise", "中国", "北京", "https://www.google.com"),
    (18, "亚马逊中国", "电商", "enterprise", "中国", "北京", "https://www.amazon.com"),
    (19, "苹果中国", "电子", "enterprise", "中国", "上海", "https://www.apple.com"),
    (20, "IBM中国", "科技", "enterprise", "中国", "上海", "https://www.ibm.com"),
    (21, "毕马威", "咨询", "large", "中国", "上海", "https://home.kpmg"),
    (22, "德勤", "咨询", "large", "中国", "上海", "https://www2.deloitte.com"),
    (23, "普华永道", "咨询", "large", "中国", "上海", "https://www.pwc.com"),
    (24, "麦肯锡", "咨询", "large", "中国", "上海", "https://www.mckinsey.com"),
    (25, "中国银行", "金融", "enterprise", "中国", "北京", "https://www.boc.cn"),
]

# CDO教师数据
TEACHERS = [
    (1, "张老师", "zhang@university.edu.cn", "13800138001", "技术类岗位、互联网行业", True),
    (2, "李老师", "li@university.edu.cn", "13800138002", "金融行业、咨询行业", True),
    (3, "王老师", "wang@university.edu.cn", "13800138003", "简历优化、面试技巧", True),
    (4, "刘老师", "liu@university.edu.cn", "13800138004", "职业规划、行业分析", True),
    (5, "陈老师", "chen@university.edu.cn", "13800138005", "数据分析、AI岗位", True),
]

# ============================================================
# 辅助函数
# ============================================================

def random_date(start_date, end_date):
    """生成随机日期"""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def random_datetime(start_date, end_date):
    """生成随机日期时间"""
    date = random_date(start_date, end_date)
    hour = random.choice([9, 10, 11, 14, 15, 16])
    minute = random.choice([0, 30])
    return date.replace(hour=hour, minute=minute, second=0, microsecond=0)

def generate_student_id(year, index):
    """生成学号：年份 + 4位序号"""
    return f"{year}{index:04d}"

def save_to_csv(filename, headers, data):
    """保存数据到CSV"""
    filepath = OUTPUT_DIR / filename
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"✓ 生成 {filename}: {len(data)} 条记录")

# ============================================================
# 生成核心实体数据
# ============================================================

def generate_students(count=100):
    """生成学生数据"""
    students = []
    surnames = ["王", "李", "张", "刘", "陈", "杨", "黄", "赵", "吴", "周", "徐", "孙", "马", "朱", "胡", "郭", "何", "高", "林", "罗"]
    given_names = ["伟", "芳", "娜", "秀英", "敏", "静", "丽", "强", "磊", "军", "洋", "勇", "艳", "杰", "涛", "明", "超", "秀兰", "霞", "平"]

    for i in range(count):
        year = random.choice([2020, 2021, 2022, 2023])
        student_id = generate_student_id(year, i + 1)
        name = random.choice(surnames) + random.choice(given_names)
        gender = random.choice(['M', 'F'])
        major_id = random.choice([m[0] for m in MAJORS])
        email = f"student{i+1:04d}@university.edu.cn"
        phone = f"138{random.randint(10000000, 99999999)}"
        graduation_year = year + 4

        students.append([
            student_id, name, gender, email, phone, major_id,
            year, graduation_year,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

    return students

def generate_resumes(students, avg_per_student=1.5):
    """生成简历数据"""
    resumes = []
    resume_id = 1

    for student in students:
        student_id = student[0]
        num_resumes = random.choices([1, 2, 3], weights=[50, 40, 10])[0]

        for i in range(num_resumes):
            titles = ["通用简历", "技术岗位简历", "实习简历", "秋招简历", "春招简历"]
            upload_time = random_datetime(
                datetime(2023, 1, 1),
                datetime.now()
            )

            resumes.append([
                resume_id,
                student_id,
                random.choice(titles),
                upload_time.strftime("%Y-%m-%d %H:%M:%S"),
                f"/resumes/{student_id}_{resume_id}.pdf",
                random.randint(100000, 500000),
                1 if i == 0 else 0,  # 第一份简历设为默认
                upload_time.strftime("%Y-%m-%d %H:%M:%S"),
                upload_time.strftime("%Y-%m-%d %H:%M:%S")
            ])
            resume_id += 1

    return resumes

def generate_positions(count=50):
    """生成岗位数据"""
    positions = []
    job_titles = {
        2: ["Java开发工程师", "Python开发工程师", "Go开发工程师", "后端开发实习生"],
        3: ["前端开发工程师", "React开发工程师", "Vue.js开发工程师", "前端实习生"],
        4: ["全栈开发工程师", "全栈实习生"],
        5: ["iOS开发工程师", "Android开发工程师", "移动端开发实习生"],
        8: ["数据分析师", "数据分析实习生", "商业分析师"],
        9: ["数据工程师", "数据开发工程师"],
        10: ["数据科学家", "算法工程师"],
        12: ["机器学习工程师", "深度学习工程师"],
        16: ["产品经理", "产品经理实习生"],
        17: ["运营专员", "用户运营", "内容运营"],
    }

    cities = ["北京", "上海", "杭州", "深圳", "广州", "成都", "南京", "武汉"]
    employment_types = ["internship", "full_time"]

    for i in range(count):
        company_id = random.choice([c[0] for c in COMPANIES])
        category_id = random.choice(list(job_titles.keys()))
        position_title = random.choice(job_titles[category_id])
        employment_type = random.choice(employment_types)

        salary_ranges = {
            "internship": ["150-200元/天", "200-300元/天", "300-400元/天"],
            "full_time": ["10-15K", "15-20K", "20-30K", "30-40K"]
        }

        posted_date = random_date(datetime(2024, 1, 1).date(), datetime.now().date())
        deadline = posted_date + timedelta(days=random.randint(30, 90))
        status = random.choices(
            ["active", "closed", "filled"],
            weights=[70, 20, 10]
        )[0]

        positions.append([
            i + 1,
            company_id,
            position_title,
            category_id,
            employment_type,
            random.choice(cities),
            random.choice(salary_ranges[employment_type]),
            f"{position_title}岗位描述...",
            "本科及以上学历，相关专业...",
            random.choice(["邮箱投递", "官网申请", "内推"]),
            deadline.strftime("%Y-%m-%d"),
            status,
            posted_date.strftime("%Y-%m-%d"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

    return positions

def generate_applications(students, resumes, positions, count=300):
    """生成申请记录"""
    applications = []
    application_id = 1
    used_combinations = set()

    # 构建学生-简历映射
    student_resumes = {}
    for resume in resumes:
        student_id = resume[1]
        if student_id not in student_resumes:
            student_resumes[student_id] = []
        student_resumes[student_id].append(resume[0])  # resume_id

    statuses = ["submitted", "screening", "interview", "assessment", "offered", "accepted", "rejected", "withdrawn"]
    weights = [25, 20, 15, 10, 8, 5, 15, 2]

    for _ in range(count):
        student = random.choice(students)
        student_id = student[0]
        position = random.choice(positions)
        position_id = position[0]

        # 防止重复申请
        combination = (student_id, position_id)
        if combination in used_combinations:
            continue
        used_combinations.add(combination)

        # 选择简历
        resume_id = random.choice(student_resumes[student_id])

        status = random.choices(statuses, weights=weights)[0]
        submit_time = random_datetime(datetime(2024, 1, 1), datetime.now())
        update_time = submit_time + timedelta(days=random.randint(0, 30))

        hr_comments = {
            "rejected": "简历不匹配岗位要求",
            "offered": "表现优秀，发放offer",
            "interview": "简历通过，邀请面试",
            "screening": "简历审核中"
        }
        hr_comment = hr_comments.get(status, None)

        applications.append([
            application_id,
            student_id,
            position_id,
            resume_id,
            status,
            submit_time.strftime("%Y-%m-%d %H:%M:%S"),
            update_time.strftime("%Y-%m-%d %H:%M:%S"),
            hr_comment,
            None,  # student_notes
            submit_time.strftime("%Y-%m-%d %H:%M:%S")
        ])
        application_id += 1

    return applications

def generate_appointments(students, count=80):
    """生成预约记录"""
    appointments = []
    statuses = ["scheduled", "completed", "cancelled", "no_show"]
    weights = [40, 50, 8, 2]
    locations = ["A栋201", "B栋305", "CDO办公室", "线上咨询", "图书馆会议室"]

    for i in range(count):
        student = random.choice(students)
        teacher_id = random.choice([t[0] for t in TEACHERS])
        type_id = random.choice([t[0] for t in CONSULTATION_TYPES])

        appointment_time = random_datetime(
            datetime(2024, 1, 1),
            datetime.now() + timedelta(days=30)
        )

        status = random.choices(statuses, weights=weights)[0]

        feedback = None
        if status == "completed":
            feedback = "咨询效果良好，学生收获颇丰"

        appointments.append([
            i + 1,
            student[0],
            teacher_id,
            type_id,
            appointment_time.strftime("%Y-%m-%d %H:%M:%S"),
            random.choice([30, 45, 60]),
            status,
            random.choice(locations),
            "学生预约备注",
            feedback,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

    return appointments

# ============================================================
# 生成关联表数据
# ============================================================

def generate_resume_skills(resumes):
    """生成简历-技能关联"""
    resume_skills = []
    proficiency_levels = ["beginner", "intermediate", "advanced", "expert"]

    for resume in resumes:
        resume_id = resume[0]
        # 每份简历随机3-8个技能
        num_skills = random.randint(3, 8)
        selected_skills = random.sample(SKILLS, num_skills)

        for skill in selected_skills:
            skill_id = skill[0]
            level = random.choice(proficiency_levels)
            resume_skills.append([
                resume_id,
                skill_id,
                level,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])

    return resume_skills

def generate_position_skills(positions):
    """生成岗位-技能关联"""
    position_skills = []

    # 定义不同岗位类别对应的技能组合
    category_skills = {
        2: [2, 6, 7, 16, 18, 20],  # 后端开发
        3: [3, 11, 12, 20],  # 前端开发
        4: [1, 2, 3, 14, 20],  # 全栈开发
        8: [1, 6, 28, 29, 30, 34],  # 数据分析
        10: [1, 24, 25, 26, 27, 28],  # 数据科学
        12: [1, 24, 25, 26, 27],  # 机器学习
    }

    for position in positions:
        position_id = position[0]
        category_id = position[3]

        # 获取该类别的技能
        if category_id in category_skills:
            base_skills = category_skills[category_id]
        else:
            base_skills = random.sample([s[0] for s in SKILLS], 5)

        # 添加一些通用技能
        common_skills = [20, 37, 38, 40]  # Git, 沟通, 团队协作, 问题解决
        all_skills = base_skills + random.sample(common_skills, 2)

        for i, skill_id in enumerate(all_skills):
            is_required = i < len(base_skills) // 2  # 前半部分为必需技能
            priority = len(all_skills) - i  # 优先级递减

            position_skills.append([
                position_id,
                skill_id,
                1 if is_required else 0,
                priority,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])

    return position_skills

# ============================================================
# 主函数
# ============================================================

def main():
    print("=" * 60)
    print("学生实习求职管理系统 - 模拟数据生成")
    print("=" * 60)

    # 生成字典表数据
    print("\n[字典表]")

    # 注意：精简版设计中移除了 countries 表

    save_to_csv("majors.csv", ["major_id", "major_name", "faculty", "created_at"],
                [[*m, datetime.now().strftime("%Y-%m-%d %H:%M:%S")] for m in MAJORS])

    save_to_csv("skills.csv", ["skill_id", "skill_name", "skill_category", "created_at"],
                [[*s, datetime.now().strftime("%Y-%m-%d %H:%M:%S")] for s in SKILLS])

    save_to_csv("position_categories.csv", ["category_id", "category_name", "parent_category_id", "created_at"],
                [[*pc, datetime.now().strftime("%Y-%m-%d %H:%M:%S")] for pc in POSITION_CATEGORIES])

    save_to_csv("consultation_types.csv", ["type_id", "type_name", "description", "duration_minutes", "created_at"],
                [[*ct, datetime.now().strftime("%Y-%m-%d %H:%M:%S")] for ct in CONSULTATION_TYPES])

    save_to_csv("companies.csv",
                ["company_id", "company_name", "industry", "company_size", "country", "city", "website", "created_at", "updated_at"],
                [[*c, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")] for c in COMPANIES])

    save_to_csv("teachers.csv",
                ["teacher_id", "teacher_name", "email", "phone", "specialization", "is_active", "created_at", "updated_at"],
                [[*t, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")] for t in TEACHERS])

    # 生成核心实体数据
    print("\n[核心实体表]")
    students = generate_students(100)
    save_to_csv("students.csv",
                ["student_id", "name", "gender", "email", "phone", "major_id", "enrollment_year", "expected_graduation_year", "created_at", "updated_at"],
                students)

    resumes = generate_resumes(students)
    save_to_csv("resumes.csv",
                ["resume_id", "student_id", "resume_title", "upload_time", "file_path", "file_size", "is_default", "created_at", "updated_at"],
                resumes)

    positions = generate_positions(50)
    save_to_csv("positions.csv",
                ["position_id", "company_id", "position_title", "category_id", "employment_type", "location", "salary_range", "description", "requirements", "application_method", "application_deadline", "status", "posted_date", "created_at", "updated_at"],
                positions)

    applications = generate_applications(students, resumes, positions, 300)
    save_to_csv("applications.csv",
                ["application_id", "student_id", "position_id", "resume_id", "application_status", "submit_time", "update_time", "hr_comment", "student_notes", "created_at"],
                applications)

    appointments = generate_appointments(students, 80)
    save_to_csv("appointments.csv",
                ["appointment_id", "student_id", "teacher_id", "type_id", "appointment_time", "duration_minutes", "status", "location", "notes", "feedback", "created_at", "updated_at"],
                appointments)

    # 生成关联表数据
    print("\n[关联表]")
    resume_skills = generate_resume_skills(resumes)
    save_to_csv("resume_skills.csv",
                ["resume_id", "skill_id", "proficiency_level", "created_at"],
                resume_skills)

    position_skills = generate_position_skills(positions)
    save_to_csv("position_skills.csv",
                ["position_id", "skill_id", "is_required", "priority", "created_at"],
                position_skills)

    print("\n" + "=" * 60)
    print("✓ 数据生成完成！")
    print(f"输出目录: {OUTPUT_DIR.absolute()}")
    print("=" * 60)

    # 统计信息
    print("\n[数据统计]")
    print(f"学生: {len(students)} 人")
    print(f"简历: {len(resumes)} 份")
    print(f"岗位: {len(positions)} 个")
    print(f"申请: {len(applications)} 条")
    print(f"预约: {len(appointments)} 条")
    print(f"简历技能: {len(resume_skills)} 条")
    print(f"岗位技能: {len(position_skills)} 条")

if __name__ == "__main__":
    main()
