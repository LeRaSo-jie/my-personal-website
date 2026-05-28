# -*- coding: utf-8 -*-
"""
访问统计路由模块
提供访问统计数据，仅管理员可查看
"""

from flask import Blueprint, request, jsonify
from sqlalchemy import func
from config import Config
from models import db, VisitLog

# 创建统计蓝图
stats_bp = Blueprint('stats', __name__)


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


@stats_bp.route('/api/stats/visits', methods=['GET'])
def get_visit_stats():
    """
    获取访问统计数据
    需要管理员权限验证
    
    返回：
        200: 访问统计数据
            - total_visits: 总访问量
            - by_path: 按页面路径统计的访问量
            - unique_ips: 独立 IP 数量
            - today_visits: 今日访问量
        401: 未授权
    """
    # 验证管理员权限
    if not check_admin():
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # 总访问量
        total_visits = VisitLog.query.count()
        
        # 按页面路径统计访问量
        path_stats = db.session.query(
            VisitLog.path,
            func.count(VisitLog.id).label('count')
        ).group_by(VisitLog.path).all()
        
        by_path = {path: count for path, count in path_stats}
        
        # 独立 IP 数量
        unique_ips = db.session.query(
            func.count(func.distinct(VisitLog.ip))
        ).scalar()
        
        # 今日访问量（使用日期过滤）
        from datetime import datetime, timedelta
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_visits = VisitLog.query.filter(
            VisitLog.visited_at >= today_start
        ).count()
        
        return jsonify({
            "total_visits": total_visits,
            "by_path": by_path,
            "unique_ips": unique_ips,
            "today_visits": today_visits
        }), 200
    except Exception as e:
        return jsonify({"error": f"获取统计数据失败: {str(e)}"}), 500