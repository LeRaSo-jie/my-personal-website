# -*- coding: utf-8 -*-
"""
简历数据路由模块
处理简历数据的读取和更新
使用 JSON 文件存储简历数据
"""

import json
import os
from flask import Blueprint, request, jsonify
from config import Config

# 创建简历蓝图
resume_bp = Blueprint('resume', __name__)

# 简历数据文件路径
RESUME_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resume.json')


def check_admin():
    """
    验证管理员权限
    
    返回：
        bool: 验证成功返回 True，失败返回 False
    """
    password = request.headers.get('X-Admin-Password')
    if not password or password != Config.ADMIN_PASSWORD:
        return False
    return True


@resume_bp.route('/api/resume', methods=['GET'])
def get_resume():
    """
    获取简历数据
    公开接口
    
    返回：
        200: 简历数据 JSON
    """
    try:
        if os.path.exists(RESUME_FILE):
            with open(RESUME_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(data), 200
        # 如果文件不存在，返回空对象
        return jsonify({}), 200
    except Exception as e:
        return jsonify({"error": f"获取简历数据失败: {str(e)}"}), 500


@resume_bp.route('/api/resume', methods=['PUT'])
def update_resume():
    """
    更新简历数据
    需要管理员权限
    
    请求体：简历数据 JSON
    
    返回：
        200: 更新成功
        401: 未授权
    """
    # 验证管理员权限
    if not check_admin():
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        
        # 写入 JSON 文件
        with open(RESUME_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return jsonify({"success": True, "message": "简历数据已更新"}), 200
    except Exception as e:
        return jsonify({"error": f"更新简历数据失败: {str(e)}"}), 500