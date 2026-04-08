#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
闪卡索引页面生成器 - 简化版
自动扫描当前目录下的flashcards_xxxx.html文件并生成索引页面
只显示日期和开始学习按钮
"""

import os
import re
import glob
from datetime import datetime

def extract_date_from_filename(filename):
    """
    从文件名中提取日期信息
    支持格式: flashcards_YYYYMMDD.html
    """
    match = re.search(r'flashcards_(\d{8})\.html$', filename)
    if match:
        return match.group(1)
    return None

def format_date_string(date_str):
    """
    格式化日期字符串为 YYYY年MM月DD日 格式
    """
    try:
        # 确保日期字符串是8位数字
        if len(date_str) == 8 and date_str.isdigit():
            year = date_str[:4]
            month = date_str[4:6]
            day = date_str[6:8]
            return f"{year}年{int(month)}月{int(day)}日"
        else:
            # 处理其他格式的日期字符串
            parts = re.findall(r'\d+', date_str)
            if len(parts) >= 3:
                year = parts[0]
                month = parts[1]
                day = parts[2]
                return f"{year}年{int(month)}月{int(day)}日"
            else:
                return date_str  # 无法解析，返回原始字符串
    except:
        return date_str  # 出错时返回原始字符串

def generate_index_html(flashcard_files, output_file="index.html"):
    """
    生成索引HTML文件
    """
    # 按日期排序文件（从新到旧）
    flashcard_files.sort(key=lambda x: x['date'], reverse=True)
    
    # HTML模板
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>英语学习闪卡 - 主菜单</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }
        
        body {
            font-family: 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #6dd5ed 0%, #2193b0 100%);
            min-height: 100vh;
            color: #333;
            line-height: 1.6;
        }
        
        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
        }
        
        .header h1 {
            font-size: 2.2rem;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .compact-list {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .section-title {
            font-size: 1.4rem;
            margin-bottom: 20px;
            color: #2c3e50;
            padding-bottom: 10px;
            border-bottom: 2px solid #07C160;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .course-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
            transition: background 0.2s;
        }
        
        .course-item:last-child {
            border-bottom: none;
        }
        
        .course-item:hover {
            background: #f9f9f9;
        }
        
        .course-date {
            font-weight: bold;
            color: #2193b0;
            font-size: 1.1rem;
        }
        
        .course-action {
            text-align: right;
        }
        
        .btn-compact {
            display: inline-block;
            padding: 8px 15px;
            background: #07C160;
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-size: 0.9rem;
            transition: background 0.3s ease;
        }
        
        .btn-compact:hover {
            background: #05a75a;
        }
        
        .sort-controls {
            display: flex;
            gap: 10px;
        }
        
        .sort-btn {
            padding: 6px 12px;
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #ddd;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.9rem;
        }
        
        .sort-btn.active {
            background: #07C160;
            color: white;
            border-color: #07C160;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            color: white;
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        @media (max-width: 600px) {
            .course-item {
                flex-direction: column;
                align-items: center;
                padding: 15px;
                text-align: center;
            }
            
            .course-date {
                margin-bottom: 10px;
            }
            
            .section-title {
                flex-direction: column;
                align-items: center;
                gap: 10px;
            }
            
            .sort-controls {
                width: 100%;
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>英语学习闪卡</h1>
            <p>八年级上学期 - 主菜单</p>
        </div>
        
        <div class="compact-list">
            <div class="section-title">
                <span>所有课程 (TOTAL_COUNT)</span>
                <div class="sort-controls">
                    <button class="sort-btn active" id="sort-newest">最新优先</button>
                    <button class="sort-btn" id="sort-oldest">最旧优先</button>
                </div>
            </div>
            
            <div id="courses-list">
                COURSES_LIST
            </div>
        </div>
        
        <div class="footer">
            <p>© 2025 英语学习闪卡 - 六年级上学期</p>
            <p>点击日期开始学习</p>
        </div>
    </div>

    <script>
        // 课程数据
        const courses = [
            COURSES_DATA
        ];

        // 渲染课程列表
        function renderCourses(sortOrder = 'newest') {
            const coursesList = document.getElementById('courses-list');
            coursesList.innerHTML = '';
            
            // 排序课程
            const sortedCourses = [...courses];
            if (sortOrder === 'newest') {
                sortedCourses.sort((a, b) => new Date(b.date) - new Date(a.date));
            } else {
                sortedCourses.sort((a, b) => new Date(a.date) - new Date(b.date));
            }
            
            // 生成课程列表
            sortedCourses.forEach(course => {
                const courseItem = document.createElement('div');
                courseItem.className = 'course-item';
                
                courseItem.innerHTML = `
                    <div class="course-date">${course.formattedDate}</div>
                    <div class="course-action">
                        <a href="${course.filename}" class="btn-compact">开始学习</a>
                    </div>
                `;
                
                coursesList.appendChild(courseItem);
            });
        }
        
        // 初始化页面
        document.addEventListener('DOMContentLoaded', function() {
            // 初始渲染
            renderCourses('newest');
            
            // 排序按钮事件
            document.getElementById('sort-newest').addEventListener('click', function() {
                this.classList.add('active');
                document.getElementById('sort-oldest').classList.remove('active');
                renderCourses('newest');
            });
            
            document.getElementById('sort-oldest').addEventListener('click', function() {
                this.classList.add('active');
                document.getElementById('sort-newest').classList.remove('active');
                renderCourses('oldest');
            });
        });
    </script>
</body>
</html>"""
    
    # 生成课程列表HTML
    courses_list_html = ""
    for file_info in flashcard_files:
        formatted_date = format_date_string(file_info['date'])
        
        courses_list_html += f"""
            <div class="course-item">
                <div class="course-date">{formatted_date}</div>
                <div class="course-action">
                    <a href="{file_info['filename']}" class="btn-compact">开始学习</a>
                </div>
            </div>
        """
    
    # 生成课程数据JS
    courses_data_js = ""
    for i, file_info in enumerate(flashcard_files):
        if i > 0:
            courses_data_js += ",\n            "
        
        # 格式化日期为 YYYY-MM-DD 格式，以便 JavaScript 可以正确解析
        date_str = file_info['date']
        if len(date_str) == 8 and date_str.isdigit():
            js_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        else:
            # 如果日期格式不正确，使用当前日期
            js_date = datetime.now().strftime("%Y-%m-%d")
        
        formatted_date = format_date_string(date_str)
        
        courses_data_js += f"""{{date: '{js_date}', formattedDate: '{formatted_date}', filename: '{file_info['filename']}'}}"""
    
    # 替换模板中的占位符
    html_content = html_template.replace("TOTAL_COUNT", str(len(flashcard_files)))
    html_content = html_content.replace("COURSES_LIST", courses_list_html)
    html_content = html_content.replace("COURSES_DATA", courses_data_js)
    
    # 写入HTML文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"成功生成索引页面: {output_file}")
        print(f"共找到 {len(flashcard_files)} 个闪卡文件")
        return True
    except Exception as e:
        print(f"生成索引页面时出错: {e}")
        return False

def main():
    """主函数"""
    print("闪卡索引页面生成器 - 简化版")
    print("=" * 40)
    
    # 查找所有flashcards_xxxx.html文件
    flashcard_files = []
    for filepath in glob.glob("flashcards_*.html"):
        date_str = extract_date_from_filename(filepath)
        if date_str:
            flashcard_files.append({
                'filename': os.path.basename(filepath),
                'date': date_str
            })
    
    if not flashcard_files:
        print("未找到任何flashcards_xxxx.html文件")
        return
    
    # 生成索引页面
    if generate_index_html(flashcard_files):
        print("索引页面生成完成！")
        print("请打开 index.html 文件查看所有闪卡课程")
    else:
        print("索引页面生成失败")

if __name__ == "__main__":
    main()