# -*- coding: utf-8 -*-
"""
日志路由模块
提供活动日志的查询和管理接口，仅管理员可访问
"""

import json
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from config import Config
from models import db, ActivityLog

# 创建日志蓝图
logs_bp = Blueprint('logs', __name__)


def check_admin():
    """验证管理员权限"""
    password = request.headers.get('X-Admin-Password')
    if not password or password != Config.ADMIN_PASSWORD:
        return False
    return True


def add_log(log_type, action, target=None, detail=None, status='success'):
    """
    添加活动日志的辅助函数
    其他路由模块可导入此函数来记录操作
    
    参数：
        log_type: 日志类型 (visit/modify/download/tool_use/upload/delete/auth)
        action: 操作描述
        target: 操作目标
        detail: 详细信息
        status: 操作状态 (success/fail)
    """
    try:
        log = ActivityLog(
            log_type=log_type,
            action=action,
            target=target,
            detail=json.dumps(detail, ensure_ascii=False) if detail else None,
            ip=request.remote_addr if request else None,
            user_agent=(request.headers.get('User-Agent', '')[:500] if request else None),
            status=status
        )
        db.session.add(log)
        db.session.commit()
        return log
    except Exception as e:
        db.session.rollback()
        print(f"记录日志失败: {e}")
        return None


@logs_bp.route('/api/logs', methods=['GET'])
def get_logs():
    """
    获取活动日志列表（仅管理员）
    
    查询参数：
        page: 页码（默认 1）
        per_page: 每页数量（默认 20）
        log_type: 日志类型筛选
        search: 搜索关键词
        days: 最近几天（默认 30）
    
    返回：
        200: 日志列表
        401: 未授权
    """
    if not check_admin():
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        log_type = request.args.get('log_type', '', type=str)
        search = request.args.get('search', '', type=str)
        days = request.args.get('days', 30, type=int)
        
        # 构建查询
        query = ActivityLog.query
        
        # 时间范围筛选
        if days > 0:
            since = datetime.utcnow() - timedelta(days=days)
            query = query.filter(ActivityLog.created_at >= since)
        
        # 类型筛选
        if log_type:
            query = query.filter(ActivityLog.log_type == log_type)
        
        # 关键词搜索
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                db.or_(
                    ActivityLog.action.like(search_pattern),
                    ActivityLog.target.like(search_pattern),
                    ActivityLog.ip.like(search_pattern)
                )
            )
        
        # 按时间倒序排列
        query = query.order_by(ActivityLog.created_at.desc())
        
        # 分页
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'items': [log.to_dict() for log in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"获取日志失败: {str(e)}"}), 500


@logs_bp.route('/api/logs/stats', methods=['GET'])
def get_log_stats():
    """
    获取日志统计概览（仅管理员）
    
    返回：
        200: 统计数据
        401: 未授权
    """
    if not check_admin():
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # 最近 24 小时
        since_24h = datetime.utcnow() - timedelta(hours=24)
        # 最近 7 天
        since_7d = datetime.utcnow() - timedelta(days=7)
        
        # 各类型日志数量
        type_counts = {}
        for log_type in ['visit', 'modify', 'download', 'tool_use', 'upload', 'delete', 'auth']:
            count = ActivityLog.query.filter(ActivityLog.log_type == log_type).count()
            type_counts[log_type] = count
        
        # 最近 24 小时的总操作数
        recent_24h = ActivityLog.query.filter(ActivityLog.created_at >= since_24h).count()
        
        # 最近 7 天的总操作数
        recent_7d = ActivityLog.query.filter(ActivityLog.created_at >= since_7d).count()
        
        # 总日志数
        total = ActivityLog.query.count()
        
        # 今日各类型统计
        today_counts = {}
        for log_type in ['visit', 'modify', 'download', 'tool_use', 'upload', 'delete', 'auth']:
            count = ActivityLog.query.filter(
                ActivityLog.log_type == log_type,
                ActivityLog.created_at >= since_24h
            ).count()
            today_counts[log_type] = count
        
        return jsonify({
            'total': total,
            'recent_24h': recent_24h,
            'recent_7d': recent_7d,
            'type_counts': type_counts,
            'today_counts': today_counts
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"获取日志统计失败: {str(e)}"}), 500


@logs_bp.route('/api/logs/seed', methods=['POST'])
def seed_logs():
    """
    生成测试日志数据（仅管理员）
    
    返回：
        200: 生成成功
        401: 未授权
    """
    if not check_admin():
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # 测试日志数据
        test_logs = [
            # 访问日志
            ActivityLog(log_type='visit', action='访问首页', target='/', ip='192.168.1.100', 
                       user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0', status='success',
                       created_at=datetime.utcnow() - timedelta(minutes=5)),
            ActivityLog(log_type='visit', action='访问作品集页面', target='/portfolio', ip='192.168.1.101',
                       user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X) Safari/17.0', status='success',
                       created_at=datetime.utcnow() - timedelta(minutes=15)),
            ActivityLog(log_type='visit', action='访问工具箱页面', target='/tools', ip='10.0.0.55',
                       user_agent='Mozilla/5.0 (X11; Linux x86_64) Firefox/121.0', status='success',
                       created_at=datetime.utcnow() - timedelta(minutes=30)),
            ActivityLog(log_type='visit', action='访问简历页面', target='/resume', ip='172.16.0.22',
                       user_agent='Mozilla/5.0 (Windows NT 10.0) Edge/120.0', status='success',
                       created_at=datetime.utcnow() - timedelta(hours=1)),
            ActivityLog(log_type='visit', action='访问下载页面', target='/downloads', ip='192.168.1.100',
                       user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0', status='success',
                       created_at=datetime.utcnow() - timedelta(hours=2)),
            
            # 修改日志
            ActivityLog(log_type='modify', action='更新作品信息', target='Vue 个人网站项目',
                       detail='{"field": "description", "old": "旧描述", "new": "使用 Vue 3 + Flask 构建的个人网站"}',
                       ip='192.168.1.100', status='success',
                       created_at=datetime.utcnow() - timedelta(hours=3)),
            ActivityLog(log_type='modify', action='更新简历数据', target='个人简历',
                       detail='{"section": "skills", "skills": ["Python", "JavaScript", "Vue.js", "Flask"]}',
                       ip='192.168.1.100', status='success',
                       created_at=datetime.utcnow() - timedelta(hours=5)),
            ActivityLog(log_type='modify', action='添加新作品', target='自动化测试框架',
                       detail='{"title": "自动化测试框架", "tech_stack": ["Python", "Selenium", "pytest"]}',
                       ip='192.168.1.100', status='success',
                       created_at=datetime.utcnow() - timedelta(hours=8)),
            
            # 下载日志
            ActivityLog(log_type='download', action='下载工具文件', target='JSON格式化工具.zip',
                       detail='{"file_size": 2048576, "file_type": ".zip"}',
                       ip='10.0.0.55', status='success',
                       created_at=datetime.utcnow() - timedelta(hours=1)),
            ActivityLog(log_type='download', action='下载工具文件', target='正则表达式测试器.py',
                       detail='{"file_size": 15360, "file_type": ".py"}',
                       ip='172.16.0.22', status='success',
                       created_at=datetime.utcnow() - timedelta(hours=4)),
            ActivityLog(log_type='download', action='下载工具文件', target='数据备份脚本.sh',
                       detail='{"file_size": 8192, "file_type": ".sh"}',
                       ip='192.168.1.101', status='success',
                       created_at=datetime.utcnow() - timedelta(hours=6)),
            
            # 上传日志
            ActivityLog(log_type='upload', action='上传新工具', target='代码生成器.py',
                       detail='{"file_size": 32768, "file_type": ".py"}',
                       ip='192.168.1.100', status='success',
                       created_at=datetime.utcnow() - timedelta(hours=12)),
            ActivityLog(log_type='upload', action='上传新工具', target='API测试工具.zip',
                       detail='{"file_size": 5242880, "file_type": ".zip"}',
                       ip='192.168.1.100', status='success',
                       created_at=datetime.utcnow() - timedelta(days=1)),
            
            # 删除日志
            ActivityLog(log_type='delete', action='删除作品', target='旧项目Demo',
                       detail='{"id": 5, "title": "旧项目Demo"}',
                       ip='192.168.1.100', status='success',
                       created_at=datetime.utcnow() - timedelta(days=1, hours=2)),
            ActivityLog(log_type='delete', action='删除工具文件', target='test_old.zip',
                       detail='{"id": 3, "filename": "test_old.zip"}',
                       ip='192.168.1.100', status='success',
                       created_at=datetime.utcnow() - timedelta(days=2)),
            
            # 认证日志
            ActivityLog(log_type='auth', action='管理员登录成功', target='管理员',
                       ip='192.168.1.100', status='success',
                       created_at=datetime.utcnow() - timedelta(hours=3)),
            ActivityLog(log_type='auth', action='管理员登录失败（密码错误）', target='未知用户',
                       ip='10.0.0.99', status='fail',
                       created_at=datetime.utcnow() - timedelta(hours=7)),
            ActivityLog(log_type='auth', action='管理员登录成功', target='管理员',
                       ip='192.168.1.100', status='success',
                       created_at=datetime.utcnow() - timedelta(days=1, hours=6)),
            
            # 工具使用日志
            ActivityLog(log_type='tool_use', action='使用 JSON 格式化工具', target='JSON 格式化',
                       detail='{"input_length": 1024}',
                       ip='192.168.1.101', status='success',
                       created_at=datetime.utcnow() - timedelta(minutes=45)),
            ActivityLog(log_type='tool_use', action='使用 Base64 编解码工具', target='Base64 编解码',
                       detail='{"mode": "encode", "input_length": 256}',
                       ip='10.0.0.55', status='success',
                       created_at=datetime.utcnow() - timedelta(hours=2)),
            ActivityLog(log_type='tool_use', action='使用时间戳转换工具', target='时间戳转换',
                       detail='{"timestamp": 1706112000}',
                       ip='172.16.0.22', status='success',
                       created_at=datetime.utcnow() - timedelta(hours=4)),
        ]
        
        # 批量添加
        db.session.add_all(test_logs)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": f"已生成 {len(test_logs)} 条测试日志"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"生成测试日志失败: {str(e)}"}), 500
