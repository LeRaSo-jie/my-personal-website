# -*- coding: utf-8 -*-
"""
示例博客种子数据
运行方式: python seed_blog.py

注意：此文件包含示例数据，请根据需要修改为你自己的内容。
"""

from app import create_app
from models import db, BlogPost
from datetime import datetime


def seed():
    """插入示例博客数据"""
    app = create_app()
    
    with app.app_context():
        # 检查是否已有数据
        if BlogPost.query.count() > 0:
            print('博客数据已存在，跳过种子插入。')
            return
        
        posts = [
            {
                'title': 'Hello World - 我的第一篇博客',
                'content': '# Hello World\n\n欢迎来到我的博客！这是使用 **Digital Nexus** 框架创建的第一篇示例文章。\n\n## 关于这个模板\n\n这是一个全栈个人网站模板，包含以下功能：\n\n- 博客系统（支持 Markdown）\n- 在线工具箱\n- 照片墙\n- 作品集展示\n- 简历管理\n- GitHub/Gitee 代码活跃度展示\n\n## 技术栈\n\n- **前端**: Vue 3 + Tailwind CSS + Vite\n- **后端**: Flask + SQLAlchemy + SQLite\n- **风格**: 赛博朋克 / 极客风\n\n---\n\n*Happy Coding!*',
                'summary': '使用 Digital Nexus 框架创建的第一篇示例博客文章',
                'tags': '示例,入门,Digital Nexus',
                'status': 'published',
                'likes': 0,
                'created_at': datetime(2024, 1, 1, 12, 0, 0),
                'updated_at': datetime(2024, 1, 1, 12, 0, 0)
            },
            {
                'title': 'Markdown 写作指南',
                'content': '# Markdown 写作指南\n\n本博客系统支持完整的 Markdown 语法。\n\n## 基本语法\n\n### 标题\n\n```markdown\n# H1 标题\n## H2 标题\n### H3 标题\n```\n\n### 代码块\n\n```python\ndef hello():\n    print("Hello, Digital Nexus!")\n```\n\n### 列表\n\n- 无序列表项 1\n- 无序列表项 2\n\n1. 有序列表项 1\n2. 有序列表项 2\n\n### 引用\n\n> 这是一段引用文字\n\n---\n\n*享受写作的乐趣！*',
                'summary': '介绍如何使用 Markdown 语法撰写博客文章',
                'tags': 'Markdown,教程,写作',
                'status': 'published',
                'likes': 0,
                'created_at': datetime(2024, 1, 2, 12, 0, 0),
                'updated_at': datetime(2024, 1, 2, 12, 0, 0)
            }
        ]
        
        for post_data in posts:
            post = BlogPost(**post_data)
            db.session.add(post)
        
        db.session.commit()
        print(f'成功插入 {len(posts)} 篇示例博客文章。')


if __name__ == '__main__':
    seed()
