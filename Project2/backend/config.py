# -*- coding: utf-8 -*-
"""
????
?????????????????????????
"""

import os
from dotenv import load_dotenv

# ?? .env ??
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))


class Config:
    """?????"""
    
    # ??????? session ? CSRF ??
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # SQLite ???????? charset=utf-8 ???????
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'instance', 'site.db'
    ) + '?charset=utf-8'
    
    # ?? SQLAlchemy ?????????
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ??????
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    
    # ?????? 200MB
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024
    
    # ??????????
    ALLOWED_EXTENSIONS = {'.zip', '.rar', '.7z', '.exe', '.py', '.jar', '.sh'}
    
    # ???????????????????
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'your-admin-password-here')
    
    # GitHub ??
    GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME', '')
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
    
    # Gitee ??
    GITEE_USERNAME = os.environ.get('GITEE_USERNAME', '')
    GITEE_TOKEN = os.environ.get('GITEE_TOKEN', '')
