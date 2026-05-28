# -*- coding: utf-8 -*-
"""
管理员认证路由模块
处理管理员密码验证相关的 API 请求
"""

from flask import Blueprint, request, jsonify
from config import Config
from routes.logs import add_log

# 创建认证蓝图
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/auth/verify', methods=['POST'])
def verify_password():
    """
    验证管理员密码
    公开接口，用于前端验证密码是否正确
    
    请求体（JSON）：
        password: 管理员密码
    
    返回：
        200: 验证结果（success: true/false）
        400: 请求参数错误
    """
    try:
        # 获取请求体
        data = request.get_json()
        
        # 验证参数
        if not data or not data.get('password'):
            return jsonify({
                "success": False,
                "message": "请输入密码"
            }), 400
        
        # 验证密码
        if data['password'] == Config.ADMIN_PASSWORD:
            # 记录登录成功日志
            add_log('auth', '管理员登录成功', target='管理员', status='success')
            return jsonify({
                "success": True,
                "message": "验证成功"
            }), 200
        else:
            # 记录登录失败日志
            add_log('auth', '管理员登录失败（密码错误）', target='未知用户', status='fail')
            return jsonify({
                "success": False,
                "message": "密码错误"
            }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"验证失败: {str(e)}"
        }), 500