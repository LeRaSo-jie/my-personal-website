# -*- coding: utf-8 -*-
"""
博客路由模块
提供博客文章的 CRUD API，支持管理员认证保护
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, BlogPost
from routes.logs import add_log

# 创建博客蓝图
blog_bp = Blueprint('blog', __name__)


def check_admin():
    """检查管理员权限"""
    from flask import current_app
    password = request.headers.get('X-Admin-Password')
    if not password:
        return False
    return password == current_app.config.get('ADMIN_PASSWORD', 'your-admin-password-here')


@blog_bp.route('/api/blog', methods=['GET'])
def get_posts():
    """
    获取博客文章列表
    支持分页、标签筛选、搜索
    查询参数:
      - page: 页码（默认1）
      - per_page: 每页数量（默认12）
      - tag: 标签筛选
      - search: 搜索关键词（匹配标题和摘要）
      - status: 文章状态（默认 published）
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        tag = request.args.get('tag', '', type=str)
        search = request.args.get('search', '', type=str)
        status = request.args.get('status', 'published', type=str)
        sort = request.args.get('sort', 'desc', type=str)  # desc=最新在前, asc=最早在前

        query = BlogPost.query

        # 状态筛选
        if status:
            query = query.filter(BlogPost.status == status)

        # 标签筛选
        if tag:
            query = query.filter(BlogPost.tags.like(f'%{tag}%'))

        # 搜索
        if search:
            query = query.filter(
                db.or_(
                    BlogPost.title.like(f'%{search}%'),
                    BlogPost.summary.like(f'%{search}%')
                )
            )

        # 按发布时间排序
        if sort == 'asc':
            query = query.order_by(BlogPost.published_at.asc())
        else:
            query = query.order_by(BlogPost.published_at.desc())

        # 分页
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'items': [post.to_dict() for post in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
            'per_page': per_page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@blog_bp.route('/api/blog/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """获取单篇文章详情"""
    try:
        post = BlogPost.query.get_or_404(post_id)
        # 增加阅读量
        post.views += 1
        db.session.commit()
        return jsonify(post.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@blog_bp.route('/api/blog', methods=['POST'])
def create_post():
    """
    创建博客文章（需管理员权限）
    """
    if not check_admin():
        return jsonify({'error': '需要管理员权限'}), 403

    try:
        data = request.get_json()
        if not data or not data.get('title'):
            return jsonify({'error': '标题不能为空'}), 400

        post = BlogPost(
            title=data['title'],
            summary=data.get('summary', ''),
            content=data.get('content', ''),
            tags=data.get('tags', ''),
            cover_gradient=data.get('cover_gradient', ''),
            icon=data.get('icon', '📝'),
            read_time=data.get('read_time', 5),
            status=data.get('status', 'published'),
            published_at=datetime.utcnow()
        )
        db.session.add(post)
        db.session.commit()

        add_log('upload', f'创建博客文章: {post.title}', target=post.title)
        return jsonify(post.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@blog_bp.route('/api/blog/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    更新博客文章（需管理员权限）
    """
    if not check_admin():
        return jsonify({'error': '需要管理员权限'}), 403

    try:
        post = BlogPost.query.get_or_404(post_id)
        data = request.get_json()

        if 'title' in data:
            post.title = data['title']
        if 'summary' in data:
            post.summary = data['summary']
        if 'content' in data:
            post.content = data['content']
        if 'tags' in data:
            post.tags = data['tags']
        if 'cover_gradient' in data:
            post.cover_gradient = data['cover_gradient']
        if 'icon' in data:
            post.icon = data['icon']
        if 'read_time' in data:
            post.read_time = data['read_time']
        if 'status' in data:
            post.status = data['status']

        post.updated_at = datetime.utcnow()
        db.session.commit()

        add_log('modify', f'更新博客文章: {post.title}', target=post.title)
        return jsonify(post.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@blog_bp.route('/api/blog/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    删除博客文章（需管理员权限）
    """
    if not check_admin():
        return jsonify({'error': '需要管理员权限'}), 403

    try:
        post = BlogPost.query.get_or_404(post_id)
        title = post.title
        db.session.delete(post)
        db.session.commit()

        add_log('delete', f'删除博客文章: {title}', target=title)
        return jsonify({'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@blog_bp.route('/api/blog/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    """点赞文章（无需管理员权限）"""
    try:
        post = BlogPost.query.get_or_404(post_id)
        post.likes += 1
        db.session.commit()
        return jsonify({'likes': post.likes})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@blog_bp.route('/api/blog/tags', methods=['GET'])
def get_tags():
    """获取所有文章标签"""
    try:
        posts = BlogPost.query.filter(BlogPost.status == 'published').all()
        tags = set()
        for post in posts:
            if post.tags:
                for tag in post.tags.split(','):
                    tag = tag.strip()
                    if tag:
                        tags.add(tag)
        return jsonify(sorted(tags))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
