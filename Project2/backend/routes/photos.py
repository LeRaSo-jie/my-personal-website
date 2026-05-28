# -*- coding: utf-8 -*-
"""
照片墙路由
提供照片的增删改查 API，支持图片上传
"""

import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from config import Config
from models import db, Photo
from .logs import add_log

photos_bp = Blueprint('photos', __name__)


def check_admin():
    """验证管理员权限"""
    password = request.headers.get('X-Admin-Password')
    if not password or password != Config.ADMIN_PASSWORD:
        return False
    return True


def allowed_image(filename):
    """检查是否为允许的图片类型"""
    ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg'}
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


@photos_bp.route('/api/photos', methods=['GET'])
def get_photos():
    """
    获取照片列表
    按 sort_order 排序
    """
    try:
        photos = Photo.query.order_by(Photo.sort_order.asc(), Photo.id.asc()).all()
        return jsonify([p.to_dict() for p in photos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@photos_bp.route('/api/photos', methods=['POST'])
def create_photo():
    """
    创建照片（管理员权限）
    支持两种方式：
    1. JSON：直接传 url
    2. multipart/form-data：上传图片文件
    """
    if not check_admin():
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        # 判断是文件上传还是 JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            # 文件上传模式
            file = request.files.get('file')
            url = request.form.get('url', '')
            
            if file and file.filename:
                if not allowed_image(file.filename):
                    return jsonify({'error': '不支持的图片格式'}), 400
                
                ext = os.path.splitext(file.filename)[1].lower()
                unique_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{ext}"
                upload_folder = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'uploads'), 'images')
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, unique_name)
                file.save(file_path)
                url = f'/api/photos/image/{unique_name}'
            
            caption = request.form.get('caption', '')
            tag = request.form.get('tag', '')
            size = request.form.get('size', 'md')
            rotate = float(request.form.get('rotate', 0))
            position_x = float(request.form.get('position_x', 50))
            position_y = float(request.form.get('position_y', 50))
            sort_order = int(request.form.get('sort_order', 0))
        else:
            # JSON 模式
            data = request.get_json()
            if not data:
                return jsonify({'error': '请求数据为空'}), 400
            url = data.get('url', '')
            caption = data.get('caption', '')
            tag = data.get('tag', '')
            size = data.get('size', 'md')
            rotate = float(data.get('rotate', 0))
            position_x = float(data.get('position_x', 50))
            position_y = float(data.get('position_y', 50))
            sort_order = int(data.get('sort_order', 0))

        if not url:
            return jsonify({'error': '图片 URL 不能为空'}), 400

        photo = Photo(
            url=url,
            caption=caption,
            tag=tag,
            size=size,
            rotate=rotate,
            position_x=position_x,
            position_y=position_y,
            sort_order=sort_order
        )
        db.session.add(photo)
        db.session.commit()

        add_log('modify', f'添加照片：{caption or url}', target=caption or 'photo')

        return jsonify(photo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'添加照片失败: {str(e)}'}), 500


@photos_bp.route('/api/photos/image/<filename>', methods=['GET'])
def serve_image(filename):
    """提供上传图片的访问"""
    upload_folder = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'uploads'), 'images')
    from flask import send_from_directory
    return send_from_directory(upload_folder, filename)


@photos_bp.route('/api/photos/<int:photo_id>', methods=['PUT'])
def update_photo(photo_id):
    """
    更新照片信息（管理员权限）
    """
    if not check_admin():
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        photo = Photo.query.get(photo_id)
        if not photo:
            return jsonify({'error': '照片不存在'}), 404

        # 判断是文件上传还是 JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            file = request.files.get('file')
            if file and file.filename:
                if not allowed_image(file.filename):
                    return jsonify({'error': '不支持的图片格式'}), 400
                ext = os.path.splitext(file.filename)[1].lower()
                unique_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{ext}"
                upload_folder = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'uploads'), 'images')
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, unique_name)
                file.save(file_path)
                photo.url = f'/api/photos/image/{unique_name}'

            if request.form.get('caption') is not None:
                photo.caption = request.form.get('caption')
            if request.form.get('tag') is not None:
                photo.tag = request.form.get('tag')
            if request.form.get('size') is not None:
                photo.size = request.form.get('size')
            if request.form.get('rotate') is not None:
                photo.rotate = float(request.form.get('rotate'))
            if request.form.get('position_x') is not None:
                photo.position_x = float(request.form.get('position_x'))
            if request.form.get('position_y') is not None:
                photo.position_y = float(request.form.get('position_y'))
            if request.form.get('sort_order') is not None:
                photo.sort_order = int(request.form.get('sort_order'))
        else:
            data = request.get_json()
            if not data:
                return jsonify({'error': '请求数据为空'}), 400
            if 'url' in data:
                photo.url = data['url']
            if 'caption' in data:
                photo.caption = data['caption']
            if 'tag' in data:
                photo.tag = data['tag']
            if 'size' in data:
                photo.size = data['size']
            if 'rotate' in data:
                photo.rotate = float(data['rotate'])
            if 'position_x' in data:
                photo.position_x = float(data['position_x'])
            if 'position_y' in data:
                photo.position_y = float(data['position_y'])
            if 'sort_order' in data:
                photo.sort_order = int(data['sort_order'])

        db.session.commit()
        add_log('modify', f'更新照片：{photo.caption or photo.url}', target=photo.caption or 'photo')

        return jsonify(photo.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新照片失败: {str(e)}'}), 500


@photos_bp.route('/api/photos/<int:photo_id>', methods=['DELETE'])
def delete_photo(photo_id):
    """
    删除照片（管理员权限）
    """
    if not check_admin():
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        photo = Photo.query.get(photo_id)
        if not photo:
            return jsonify({'error': '照片不存在'}), 404

        caption = photo.caption or photo.url

        # 如果是本地上传的图片，删除文件
        if photo.url and photo.url.startswith('/api/photos/image/'):
            filename = photo.url.split('/')[-1]
            file_path = os.path.join(
                current_app.config.get('UPLOAD_FOLDER', 'uploads'), 'images', filename
            )
            if os.path.exists(file_path):
                os.remove(file_path)

        db.session.delete(photo)
        db.session.commit()

        add_log('modify', f'删除照片：{caption}', target=caption)

        return jsonify({'message': '照片已删除'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'删除照片失败: {str(e)}'}), 500
