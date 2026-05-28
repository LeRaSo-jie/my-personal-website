# -*- coding: utf-8 -*-
"""
示例照片种子数据
运行方式: python seed_photos.py

注意：此文件包含示例数据，请根据需要修改为你自己的内容。
      需要先在 backend/uploads/images/ 目录下放入对应的图片文件。
"""

from app import create_app
from models import db, Photo
from datetime import datetime


def seed():
    """插入示例照片数据"""
    app = create_app()
    
    with app.app_context():
        # 检查是否已有数据
        if Photo.query.count() > 0:
            print('照片数据已存在，跳过种子插入。')
            return
        
        photos = [
            {
                'title': '示例照片 1',
                'description': '这是一张示例照片，请替换为你自己的图片',
                'filename': 'example1.jpg',
                'category': '风景',
                'position': 0,
                'created_at': datetime(2024, 1, 1, 12, 0, 0)
            },
            {
                'title': '示例照片 2',
                'description': '另一张示例照片',
                'filename': 'example2.jpg',
                'category': '生活',
                'position': 1,
                'created_at': datetime(2024, 1, 2, 12, 0, 0)
            }
        ]
        
        for photo_data in photos:
            photo = Photo(**photo_data)
            db.session.add(photo)
        
        db.session.commit()
        print(f'成功插入 {len(photos)} 条示例照片记录。')
        print('注意：请确保 backend/uploads/images/ 目录下有对应的图片文件！')


if __name__ == '__main__':
    seed()
