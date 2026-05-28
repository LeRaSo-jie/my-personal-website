# -*- coding: utf-8 -*-
"""
作品集路由模块
处理作品集相关的 API 请求，包括增删查操作
"""

from flask import Blueprint, request, jsonify
from config import Config
from models import db, Portfolio
from routes.logs import add_log

# 创建作品集蓝图
portfolio_bp = Blueprint('portfolio', __name__)


def check_admin():
    """
    验证管理员权限
    检查请求头中的 X-Admin-Password 是否与配置中的密码匹配
    
    返回：
        bool: 验证成功返回 True，失败返回 False
    """
    password = request.headers.get('X-Admin-Password')
    if not password or password != Config.ADMIN_PASSWORD:
        return False
    return True


@portfolio_bp.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    """
    获取作品列表
    公开接口，返回所有作品，按创建时间倒序排列
    
    返回：
        200: 作品列表 JSON 数组
    """
    try:
        # 查询所有作品，按创建时间倒序
        portfolios = Portfolio.query.order_by(Portfolio.created_at.desc()).all()
        # 转换为字典列表
        return jsonify([p.to_dict() for p in portfolios]), 200
    except Exception as e:
        return jsonify({"error": f"获取作品列表失败: {str(e)}"}), 500


@portfolio_bp.route('/api/portfolio', methods=['POST'])
def add_portfolio():
    """
    添加新作品
    需要管理员权限验证
    
    请求体（JSON）：
        title: 作品标题（必填）
        description: 作品描述（可选）
        tech_stack: 技术标签，逗号分隔（可选）
        image_path: 图片路径（可选）
        github_url: GitHub 链接（可选）
        demo_url: 在线预览链接（可选）
    
    返回：
        201: 创建成功，返回作品对象
        401: 未授权
        400: 请求参数错误
    """
    # 验证管理员权限
    if not check_admin():
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # 获取 JSON 请求体
        data = request.get_json()
        
        # 验证必填字段
        if not data or not data.get('title'):
            return jsonify({"error": "作品标题不能为空"}), 400
        
        # 创建新作品记录
        portfolio = Portfolio(
            title=data['title'],
            description=data.get('description', ''),
            tech_stack=data.get('tech_stack', ''),
            image_path=data.get('image_path', ''),
            github_url=data.get('github_url', ''),
            demo_url=data.get('demo_url', '')
        )
        
        # 保存到数据库
        db.session.add(portfolio)
        db.session.commit()
        
        # 记录日志
        add_log('modify', f'添加新作品：{data["title"]}', target=data['title'],
                detail={'title': data['title'], 'tech_stack': data.get('tech_stack', '')})
        
        return jsonify(portfolio.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"添加作品失败: {str(e)}"}), 500


@portfolio_bp.route('/api/portfolio/<int:id>', methods=['DELETE'])
def delete_portfolio(id):
    """
    删除指定作品
    需要管理员权限验证
    
    参数：
        id: 作品 ID
    
    返回：
        200: 删除成功
        401: 未授权
        404: 作品不存在
    """
    # 验证管理员权限
    if not check_admin():
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # 查询作品
        portfolio = Portfolio.query.get(id)
        if not portfolio:
            return jsonify({"error": "作品不存在"}), 404
        
        # 记录日志（删除前记录标题）
        title = portfolio.title
        
        # 删除记录
        db.session.delete(portfolio)
        db.session.commit()
        
        # 记录日志
        add_log('delete', f'删除作品：{title}', target=title, detail={'id': id, 'title': title})
        
        return jsonify({"message": "deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"删除作品失败: {str(e)}"}), 500