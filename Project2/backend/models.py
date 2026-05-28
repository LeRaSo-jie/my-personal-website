# -*- coding: utf-8 -*-
"""
数据库模型定义
定义所有数据库表结构，包括作品集、工具和访问日志
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# 创建 SQLAlchemy 实例
db = SQLAlchemy()


class Portfolio(db.Model):
    """
    作品集模型
    存储个人项目/作品信息
    """
    __tablename__ = 'portfolio'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    
    # 作品标题（最长100字符）
    title = db.Column(db.String(100), nullable=False)
    
    # 作品描述（长文本）
    description = db.Column(db.Text, nullable=True)
    
    # 技术标签，多个标签用逗号分隔
    tech_stack = db.Column(db.String(200), nullable=True)
    
    # 作品封面图片路径（可为空）
    image_path = db.Column(db.String(200), nullable=True)
    
    # GitHub 仓库链接（可为空）
    github_url = db.Column(db.String(200), nullable=True)
    
    # 在线预览链接（可为空）
    demo_url = db.Column(db.String(200), nullable=True)
    
    # 创建时间，默认为当前时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """将模型转换为字典格式，便于 JSON 序列化"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'tech_stack': self.tech_stack.split(',') if self.tech_stack else [],
            'image_path': self.image_path,
            'github_url': self.github_url,
            'demo_url': self.demo_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Tool(db.Model):
    """
    工具模型
    存储可下载的工具/脚本信息
    """
    __tablename__ = 'tool'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    
    # 工具名称
    name = db.Column(db.String(100), nullable=False)
    
    # 工具描述
    description = db.Column(db.Text, nullable=True)
    
    # 原始文件名
    filename = db.Column(db.String(200), nullable=False)
    
    # 文件存储路径
    file_path = db.Column(db.String(200), nullable=False)
    
    # 文件大小（字节）
    file_size = db.Column(db.Integer, nullable=False)
    
    # 文件扩展名
    file_type = db.Column(db.String(20), nullable=False)
    
    # 下载次数，默认为0
    download_count = db.Column(db.Integer, default=0)
    
    # 上传时间，默认为当前时间
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """将模型转换为字典格式，便于 JSON 序列化"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'filename': self.filename,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'download_count': self.download_count,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }


class BlogPost(db.Model):
    """
    博客文章模型
    存储博客文章信息，支持标签、点赞、阅读量等
    """
    __tablename__ = 'blog_post'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    
    # 文章标题
    title = db.Column(db.String(200), nullable=False)
    
    # 文章摘要
    summary = db.Column(db.Text, nullable=True)
    
    # 文章正文（HTML 格式）
    content = db.Column(db.Text, nullable=True)
    
    # 标签，多个标签用逗号分隔
    tags = db.Column(db.String(300), nullable=True)
    
    # 封面渐变色
    cover_gradient = db.Column(db.String(200), nullable=True)
    
    # 文章图标（emoji）
    icon = db.Column(db.String(10), default='📝')
    
    # 预计阅读时间（分钟）
    read_time = db.Column(db.Integer, default=5)
    
    # 阅读量
    views = db.Column(db.Integer, default=0)
    
    # 点赞数
    likes = db.Column(db.Integer, default=0)
    
    # 文章状态：draft(草稿), published(已发布)
    status = db.Column(db.String(20), default='published', index=True)
    
    # 发布时间
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 更新时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """将模型转换为字典格式，便于 JSON 序列化"""
        return {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'content': self.content,
            'tags': [t.strip() for t in self.tags.split(',')] if self.tags else [],
            'cover_gradient': self.cover_gradient,
            'icon': self.icon,
            'read_time': self.read_time,
            'views': self.views,
            'likes': self.likes,
            'status': self.status,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class VisitLog(db.Model):
    """
    访问日志模型
    记录网站访问信息，仅管理员可见
    """
    __tablename__ = 'visit_log'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    
    # 访客 IP 地址
    ip = db.Column(db.String(50), nullable=True)
    
    # 访问的页面路径
    path = db.Column(db.String(200), nullable=True)
    
    # 用户代理（浏览器信息）
    user_agent = db.Column(db.String(500), nullable=True)
    
    # 访问时间，默认为当前时间
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """将模型转换为字典格式，便于 JSON 序列化"""
        return {
            'id': self.id,
            'ip': self.ip,
            'path': self.path,
            'user_agent': self.user_agent,
            'visited_at': self.visited_at.isoformat() if self.visited_at else None
        }


class ActivityLog(db.Model):
    """
    活动日志模型
    记录网站所有重要操作，包括访问、修改、下载、工具使用等
    仅管理员可见
    """
    __tablename__ = 'activity_log'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    
    # 日志类型：visit(访问), modify(修改), download(下载), tool_use(工具使用), upload(上传), delete(删除), auth(认证)
    log_type = db.Column(db.String(20), nullable=False, index=True)
    
    # 操作描述
    action = db.Column(db.String(200), nullable=False)
    
    # 详细信息（JSON 格式存储）
    detail = db.Column(db.Text, nullable=True)
    
    # 操作目标（如作品标题、工具名称等）
    target = db.Column(db.String(200), nullable=True)
    
    # IP 地址
    ip = db.Column(db.String(50), nullable=True)
    
    # 用户代理
    user_agent = db.Column(db.String(500), nullable=True)
    
    # 操作状态：success(成功), fail(失败)
    status = db.Column(db.String(20), default='success')
    
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """将模型转换为字典格式，便于 JSON 序列化"""
        return {
            'id': self.id,
            'log_type': self.log_type,
            'action': self.action,
            'detail': self.detail,
            'target': self.target,
            'ip': self.ip,
            'user_agent': self.user_agent,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Photo(db.Model):
    """
    照片墙模型
    存储照片墙的照片信息
    """
    __tablename__ = 'photo'

    # 主键
    id = db.Column(db.Integer, primary_key=True)

    # 图片 URL 或路径
    url = db.Column(db.String(500), nullable=False)

    # 照片描述/标题
    caption = db.Column(db.String(200), nullable=True)

    # 标签分类
    tag = db.Column(db.String(50), nullable=True)

    # 尺寸：sm / md / tall / lg
    size = db.Column(db.String(10), default='md')

    # 旋转角度（度）
    rotate = db.Column(db.Float, default=0)

    # 图片位置偏移（百分比 0-100，用于 object-position）
    position_x = db.Column(db.Float, default=50)
    position_y = db.Column(db.Float, default=50)

    # 排序顺序（越小越靠前）
    sort_order = db.Column(db.Integer, default=0)

    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """将模型转换为字典格式，便于 JSON 序列化"""
        return {
            'id': self.id,
            'url': self.url,
            'caption': self.caption,
            'tag': self.tag,
            'size': self.size,
            'rotate': self.rotate,
            'position_x': self.position_x,
            'position_y': self.position_y,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }