# -*- coding: utf-8 -*-
"""
工具管理路由模块
处理工具上传、下载和管理相关的 API 请求
"""

import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from config import Config
from models import db, Tool
from routes.logs import add_log

# 创建工具管理蓝图
tools_bp = Blueprint('tools', __name__)


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


def allowed_file(filename):
    """
    检查文件扩展名是否在允许列表中
    
    参数：
        filename: 文件名
    
    返回：
        bool: 允许返回 True，不允许返回 False
    """
    # 获取文件扩展名（小写）
    ext = os.path.splitext(filename)[1].lower()
    return ext in Config.ALLOWED_EXTENSIONS


def generate_unique_filename(filename):
    """
    生成唯一的文件名，防止文件名冲突
    格式：时间戳_UUID_原始文件名
    
    参数：
        filename: 原始文件名
    
    返回：
        str: 唯一的文件名
    """
    # 安全处理文件名
    safe_name = secure_filename(filename)
    # 生成时间戳
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 生成 UUID 前8位
    unique_id = uuid.uuid4().hex[:8]
    # 组合文件名
    return f"{timestamp}_{unique_id}_{safe_name}"


@tools_bp.route('/api/tools', methods=['GET'])
def get_tools():
    """
    获取工具列表
    支持分页和搜索功能
    
    查询参数：
        page: 页码，默认 1
        per_page: 每页数量，默认 12
        search: 搜索关键词（按名称模糊匹配）
    
    返回：
        200: 包含分页信息的工具列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        search = request.args.get('search', '', type=str)
        
        # 构建查询
        query = Tool.query
        
        # 如果有搜索关键词，按名称模糊匹配
        if search:
            query = query.filter(Tool.name.like(f'%{search}%'))
        
        # 按上传时间倒序排列，分页
        pagination = query.order_by(Tool.uploaded_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # 构建返回数据
        result = {
            "items": [tool.to_dict() for tool in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": pagination.pages
        }
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"获取工具列表失败: {str(e)}"}), 500


@tools_bp.route('/api/tools/upload', methods=['POST'])
def upload_tool():
    """
    上传工具文件
    需要管理员权限验证
    
    请求：multipart/form-data
        file: 工具文件（必填）
        name: 工具名称（可选，默认使用文件名）
        description: 工具描述（可选）
    
    返回：
        201: 上传成功，返回工具对象
        401: 未授权
        400: 请求参数错误
    """
    # 验证管理员权限
    if not check_admin():
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({"error": "没有上传文件"}), 400
        
        file = request.files['file']
        
        # 检查文件名是否为空
        if file.filename == '':
            return jsonify({"error": "文件名为空"}), 400
        
        # 检查文件扩展名是否允许
        if not allowed_file(file.filename):
            return jsonify({"error": "不允许的文件类型"}), 400
        
        # 生成唯一文件名
        unique_filename = generate_unique_filename(file.filename)
        
        # 确保上传目录存在
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        # 文件保存路径
        file_path = os.path.join(upload_folder, unique_filename)
        
        # 保存文件
        file.save(file_path)
        
        # 获取文件大小
        file_size = os.path.getsize(file_path)
        
        # 获取文件扩展名
        file_type = os.path.splitext(file.filename)[1].lower()
        
        # 获取工具名称和描述
        name = request.form.get('name', os.path.splitext(file.filename)[0])
        description = request.form.get('description', '')
        
        # 创建数据库记录
        tool = Tool(
            name=name,
            description=description,
            filename=file.filename,
            file_path=unique_filename,
            file_size=file_size,
            file_type=file_type
        )
        
        db.session.add(tool)
        db.session.commit()
        
        # 记录上传日志
        add_log('upload', f'上传新工具：{name}', target=name,
                detail={'file_size': file_size, 'file_type': file_type, 'filename': file.filename})
        
        return jsonify(tool.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"上传文件失败: {str(e)}"}), 500


@tools_bp.route('/api/tools/download/<int:id>', methods=['GET'])
def download_tool(id):
    """
    下载工具文件
    公开接口，会自动增加下载计数
    
    参数：
        id: 工具 ID
    
    返回：
        200: 文件流
        404: 工具或文件不存在
    """
    try:
        # 查询工具记录
        tool = Tool.query.get(id)
        if not tool:
            return jsonify({"error": "工具不存在"}), 404
        
        # 构建文件完整路径
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, tool.file_path)
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return jsonify({"error": "文件不存在"}), 404
        
        # 增加下载计数
        tool.download_count += 1
        db.session.commit()
        
        # 记录下载日志
        add_log('download', f'下载工具文件：{tool.name}', target=tool.name,
                detail={'file_size': tool.file_size, 'file_type': tool.file_type})
        
        # 返回文件
        return send_from_directory(
            upload_folder,
            tool.file_path,
            as_attachment=True,
            download_name=tool.filename
        )
    except Exception as e:
        return jsonify({"error": f"下载文件失败: {str(e)}"}), 500


@tools_bp.route('/api/tools/<int:id>', methods=['DELETE'])
def delete_tool(id):
    """
    删除工具文件
    需要管理员权限验证
    同时删除磁盘文件和数据库记录
    
    参数：
        id: 工具 ID
    
    返回：
        200: 删除成功
        401: 未授权
        404: 工具不存在
    """
    # 验证管理员权限
    if not check_admin():
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        # 查询工具记录
        tool = Tool.query.get(id)
        if not tool:
            return jsonify({"error": "工具不存在"}), 404
        
        # 删除磁盘文件（如果存在）
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, tool.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # 记录删除日志（删除前记录信息）
        tool_name = tool.name
        
        # 删除数据库记录
        db.session.delete(tool)
        db.session.commit()
        
        # 记录删除日志
        add_log('delete', f'删除工具文件：{tool_name}', target=tool_name,
                detail={'id': id, 'filename': tool_name})
        
        return jsonify({"message": "deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"删除工具失败: {str(e)}"}), 500