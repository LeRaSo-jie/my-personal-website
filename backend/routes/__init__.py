# -*- coding: utf-8 -*-
"""
路由模块初始化
导出所有蓝图对象，供主应用注册使用
"""

from .portfolio import portfolio_bp
from .tools import tools_bp
from .auth import auth_bp
from .stats import stats_bp
from .resume import resume_bp
from .logs import logs_bp, add_log
from .blog import blog_bp
from .photos import photos_bp
from .github import github_bp

__all__ = ['portfolio_bp', 'tools_bp', 'auth_bp', 'stats_bp', 'resume_bp', 'logs_bp', 'blog_bp', 'photos_bp', 'github_bp', 'add_log']