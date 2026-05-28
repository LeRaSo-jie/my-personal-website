# -*- coding: utf-8 -*-
"""
Flask 主应用入口
初始化应用、数据库、CORS，并注册所有蓝图路由
添加访问日志中间件记录每次请求
"""

import sys
import io
import os

# 设置标准输出编码为 UTF-8，确保中文正常显示
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import event
from sqlalchemy.engine import Engine
from config import Config
from models import db, VisitLog
from routes import portfolio_bp, tools_bp, auth_bp, stats_bp, resume_bp, logs_bp, blog_bp, photos_bp, github_bp


# 设置 SQLite 连接编码为 UTF-8
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """确保 SQLite 连接使用 UTF-8 编码"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA encoding = 'UTF-8'")
    cursor.close()


def create_app():
    """
    应用工厂函数
    创建并配置 Flask 应用实例
    """
    # 创建 Flask 应用
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(Config)
    
    # 确保 JSON 响应支持中文（不转义非 ASCII 字符）
    app.config['JSON_AS_ASCII'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    # 初始化数据库
    db.init_app(app)
    
    # 配置 CORS，允许前端跨域访问
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-Admin-Password"]
        }
    })
    
    # 注册蓝图
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(tools_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(photos_bp)
    app.register_blueprint(github_bp)
    
    # 创建必要的目录
    create_directories(app)
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    # 添加响应头，确保中文正确显示
    @app.after_request
    def after_request(response):
        """设置响应头，确保 UTF-8 编码"""
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    
    # 添加请求日志中间件
    @app.before_request
    def log_visit():
        """
        记录每次访问请求
        排除健康检查和静态文件请求
        """
        # 排除健康检查和静态文件
        skip_paths = ['/api/health', '/favicon.ico']
        if any(request.path.startswith(path) for path in skip_paths):
            return
        
        try:
            # 创建访问日志记录
            log = VisitLog(
                ip=request.remote_addr,
                path=request.path,
                user_agent=request.headers.get('User-Agent', '')[:500]  # 限制长度
            )
            db.session.add(log)
            db.session.commit()
        except Exception as e:
            # 日志记录失败不应影响正常请求
            db.session.rollback()
            print(f"记录访问日志失败: {e}")
    
    # 健康检查路由
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """健康检查接口，用于验证服务是否正常运行"""
        return jsonify({"status": "ok"}), 200
    
    return app


def create_directories(app):
    """
    创建应用所需的目录结构
    确保上传目录和数据库目录存在
    """
    try:
        # 创建上传目录
        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        # 创建图片上传子目录
        images_folder = os.path.join(upload_folder, 'images')
        os.makedirs(images_folder, exist_ok=True)
        
        # 创建数据库实例目录
        instance_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
        os.makedirs(instance_folder, exist_ok=True)
        
    except OSError as e:
        print(f"创建目录时出错: {e}")


# 创建应用实例
app = create_app()


if __name__ == '__main__':
    # 开发模式下运行，监听所有网络接口的 5000 端口
    app.run(host='0.0.0.0', port=5000, debug=True)