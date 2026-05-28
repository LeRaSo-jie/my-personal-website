# -*- coding: utf-8 -*-
"""
GitHub & Gitee 数据代理路由
通过后端代理请求 GitHub/Gitee API，避免前端暴露 Token
内置内存缓存（默认 1 小时），减少 API 调用次数
"""

import time
import requests
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, current_app

github_bp = Blueprint('github', __name__)

# ============================================================
#  内存缓存
# ============================================================
_cache = {}
CACHE_TTL = 300   # 缓存 5 分钟（秒）


def _get_cached(key):
    """获取缓存数据，过期返回 None"""
    if key in _cache:
        data, ts = _cache[key]
        if time.time() - ts < CACHE_TTL:
            return data
    return None


def _set_cache(key, data):
    """设置缓存"""
    _cache[key] = (data, time.time())


# ============================================================
#  工具函数
# ============================================================
def _gh_headers():
    """GitHub 请求头"""
    token = current_app.config.get('GITHUB_TOKEN', '')
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'
    return headers


def _gh_graphql(query, variables=None):
    """GitHub GraphQL 请求"""
    token = current_app.config.get('GITHUB_TOKEN', '')
    if not token:
        return None
    headers = {
        'Authorization': f'bearer {token}',
        'Content-Type': 'application/json'
    }
    try:
        resp = requests.post(
            'https://api.github.com/graphql',
            json={'query': query, 'variables': variables or {}},
            headers=headers,
            timeout=15
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"GitHub GraphQL error: {e}")
    return None


def _time_ago(date_str):
    """将 ISO 日期转换为 'x ago' 格式"""
    try:
        if 'T' in date_str:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        else:
            dt = datetime.fromisoformat(date_str)
        now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.utcnow()
        diff = now - dt
        seconds = int(diff.total_seconds())
        if seconds < 60:
            return 'just now'
        elif seconds < 3600:
            m = seconds // 60
            return f'{m}m ago'
        elif seconds < 86400:
            h = seconds // 3600
            return f'{h}h ago'
        elif seconds < 604800:
            d = seconds // 86400
            return f'{d}d ago'
        elif seconds < 2592000:
            w = seconds // 604800
            return f'{w}w ago'
        else:
            mo = seconds // 2592000
            return f'{mo}mo ago'
    except Exception:
        return date_str


# ============================================================
#  GitHub API：用户信息
# ============================================================
def _fetch_github_user():
    """获取 GitHub 用户基本信息"""
    cached = _get_cached('gh_user')
    if cached:
        return cached
    
    username = current_app.config.get('GITHUB_USERNAME', '')
    if not username:
        return None
    
    try:
        resp = requests.get(
            f'https://api.github.com/users/{username}',
            headers=_gh_headers(),
            timeout=15
        )
        if resp.status_code == 200:
            data = resp.json()
            result = {
                'login': data.get('login', ''),
                'name': data.get('name', ''),
                'avatar_url': data.get('avatar_url', ''),
                'bio': data.get('bio', ''),
                'public_repos': data.get('public_repos', 0),
                'followers': data.get('followers', 0),
                'following': data.get('following', 0),
                'profile_url': data.get('html_url', ''),
            }
            _set_cache('gh_user', result)
            return result
    except Exception as e:
        print(f"GitHub user fetch error: {e}")
    return None


# ============================================================
#  GitHub API：仓库列表
# ============================================================
def _fetch_github_repos():
    """获取 GitHub 仓库列表（按 stars 排序）"""
    cached = _get_cached('gh_repos')
    if cached:
        return cached
    
    username = current_app.config.get('GITHUB_USERNAME', '')
    if not username:
        return []
    
    all_repos = []
    page = 1
    try:
        while page <= 5:  # 最多 5 页（500 个仓库）
            resp = requests.get(
                f'https://api.github.com/users/{username}/repos',
                params={
                    'sort': 'updated',
                    'per_page': 100,
                    'page': page,
                    'type': 'owner'
                },
                headers=_gh_headers(),
                timeout=15
            )
            if resp.status_code != 200:
                break
            repos = resp.json()
            if not repos:
                break
            all_repos.extend(repos)
            page += 1
    except Exception as e:
        print(f"GitHub repos fetch error: {e}")
    
    # 整理数据
    result = []
    total_stars = 0
    total_forks = 0
    lang_stats = {}
    
    for r in all_repos:
        if r.get('fork'):
            continue  # 跳过 fork 的仓库
        stars = r.get('stargazers_count', 0)
        forks = r.get('forks_count', 0)
        total_stars += stars
        total_forks += forks
        
        lang = r.get('language') or 'Other'
        lang_stats[lang] = lang_stats.get(lang, 0) + 1
        
        result.append({
            'name': r.get('name', ''),
            'description': r.get('description') or '',
            'language': lang,
            'stars': stars,
            'forks': forks,
            'updated': _time_ago(r.get('updated_at', '')),
            'url': r.get('html_url', ''),
            'topics': r.get('topics', []),
            'homepage': r.get('homepage', ''),
            'is_fork': False,
        })
    
    # 按 stars 排序
    result.sort(key=lambda x: x['stars'], reverse=True)
    
    # 计算语言百分比
    total_repos = sum(lang_stats.values()) or 1
    # GitHub 语言颜色映射
    lang_colors = {
        'Python': '#3776ab', 'JavaScript': '#f7df1e', 'TypeScript': '#3178c6',
        'Vue': '#42b883', 'Go': '#00add8', 'Java': '#b07219',
        'Shell': '#89e051', 'C++': '#f34b7d', 'C': '#555555',
        'Rust': '#dea584', 'Ruby': '#701516', 'PHP': '#4F5D95',
        'Swift': '#F05138', 'Kotlin': '#A97BFF', 'Dart': '#00B4AB',
        'HTML': '#e34c26', 'CSS': '#563d7c', 'Jupyter Notebook': '#DA5B0B',
        'Other': '#8b949e'
    }
    
    languages = []
    for lang, count in sorted(lang_stats.items(), key=lambda x: -x[1]):
        languages.append({
            'name': lang,
            'percent': round(count / total_repos * 100),
            'color': lang_colors.get(lang, '#8b949e')
        })
    # 修正百分比总和为 100
    if languages:
        total_pct = sum(l['percent'] for l in languages)
        if total_pct != 100:
            languages[0]['percent'] += 100 - total_pct
    
    output = {
        'repos': result,
        'total_stars': total_stars,
        'total_forks': total_forks,
        'languages': languages[:8],  # 最多 8 种语言
    }
    _set_cache('gh_repos', output)
    return output


# ============================================================
#  GitHub API：用户事件（最近活动）
# ============================================================
def _fetch_github_events():
    """获取 GitHub 最近公开事件"""
    cached = _get_cached('gh_events')
    if cached:
        return cached
    
    username = current_app.config.get('GITHUB_USERNAME', '')
    if not username:
        return []
    
    try:
        resp = requests.get(
            f'https://api.github.com/users/{username}/events/public',
            params={'per_page': 10},
            headers=_gh_headers(),
            timeout=15
        )
        if resp.status_code == 200:
            events = resp.json()
            result = []
            
            # 事件类型映射
            type_map = {
                'PushEvent': {
                    'action': 'Pushed to ',
                    'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M7 16l-4-4m0 0l4-4m-4 4h18" /></svg>',
                    'iconColor': '#10b981', 'iconBg': 'rgba(16,185,129,0.1)', 'iconBorder': 'rgba(16,185,129,0.2)'
                },
                'CreateEvent': {
                    'action': 'Created repo ',
                    'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /></svg>',
                    'iconColor': '#ec4899', 'iconBg': 'rgba(236,72,153,0.1)', 'iconBorder': 'rgba(236,72,153,0.2)'
                },
                'PullRequestEvent': {
                    'action': 'PR in ',
                    'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" /></svg>',
                    'iconColor': '#8b5cf6', 'iconBg': 'rgba(139,92,246,0.1)', 'iconBorder': 'rgba(139,92,246,0.2)'
                },
                'IssuesEvent': {
                    'action': 'Issue in ',
                    'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
                    'iconColor': '#f59e0b', 'iconBg': 'rgba(245,158,11,0.1)', 'iconBorder': 'rgba(245,158,11,0.2)'
                },
                'WatchEvent': {
                    'action': 'Starred ',
                    'icon': '<svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 .587l3.668 7.431 8.332 1.21-6.029 5.874 1.42 8.311L12 19.897l-7.391 3.516 1.42-8.311-6.029-5.874 8.332-1.21z"/></svg>',
                    'iconColor': '#f59e0b', 'iconBg': 'rgba(245,158,11,0.1)', 'iconBorder': 'rgba(245,158,11,0.2)'
                },
                'ForkEvent': {
                    'action': 'Forked ',
                    'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 3a3 3 0 00-3 3v.024A3 3 0 006 9h.024A3 3 0 009 6.024V6a3 3 0 00-3-3zm0 12a3 3 0 00-3 3v.024A3 3 0 006 21h.024A3 3 0 009 18.024V18a3 3 0 00-3-3z"/></svg>',
                    'iconColor': '#06b6d4', 'iconBg': 'rgba(6,182,212,0.1)', 'iconBorder': 'rgba(6,182,212,0.2)'
                },
                'ReleaseEvent': {
                    'action': 'Released in ',
                    'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>',
                    'iconColor': '#ef4444', 'iconBg': 'rgba(239,68,68,0.1)', 'iconBorder': 'rgba(239,68,68,0.2)'
                },
            }
            
            for i, evt in enumerate(events[:8]):
                etype = evt.get('type', '')
                meta = type_map.get(etype, type_map['PushEvent'])
                repo_name = evt.get('repo', {}).get('name', '')
                repo_url = f"https://github.com/{repo_name}"
                
                result.append({
                    'id': i + 1,
                    'action': meta['action'],
                    'repo': repo_name,
                    'repoUrl': repo_url,
                    'time': _time_ago(evt.get('created_at', '')),
                    'icon': meta['icon'],
                    'iconColor': meta['iconColor'],
                    'iconBg': meta['iconBg'],
                    'iconBorder': meta['iconBorder'],
                })
            
            _set_cache('gh_events', result)
            return result
    except Exception as e:
        print(f"GitHub events fetch error: {e}")
    return []


# ============================================================
#  GitHub GraphQL：贡献热力图（过去 365 天）
# ============================================================
def _fetch_github_contributions():
    """通过 GraphQL 获取 GitHub 贡献热力图数据"""
    cached = _get_cached('gh_contributions')
    if cached:
        return cached
    
    username = current_app.config.get('GITHUB_USERNAME', '')
    if not username:
        return {'weeks': [], 'total': 0}
    
    query = """
    query($username: String!) {
      user(login: $username) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
                color
              }
            }
          }
        }
      }
    }
    """
    
    data = _gh_graphql(query, {'username': username})
    if not data or 'data' not in data:
        # 降级：生成空数据
        return {'weeks': [], 'total': 0}
    
    try:
        cal = data['data']['user']['contributionsCollection']['contributionCalendar']
        total = cal['totalContributions']
        weeks = []
        for week in cal['weeks']:
            days = []
            for day in week['contributionDays']:
                count = day['contributionCount']
                # 计算等级 0-4
                if count == 0:
                    level = 0
                elif count <= 3:
                    level = 1
                elif count <= 6:
                    level = 2
                elif count <= 9:
                    level = 3
                else:
                    level = 4
                days.append({
                    'date': day['date'],
                    'count': count,
                    'level': level
                })
            weeks.append(days)
        
        result = {'weeks': weeks, 'total': total}
        _set_cache('gh_contributions', result)
        return result
    except Exception as e:
        print(f"GitHub contributions parse error: {e}")
        return {'weeks': [], 'total': 0}


# ============================================================
#  Gitee API：用户信息
# ============================================================
def _fetch_gitee_user():
    """获取 Gitee 用户基本信息"""
    cached = _get_cached('ge_user')
    if cached:
        return cached
    
    username = current_app.config.get('GITEE_USERNAME', '')
    token = current_app.config.get('GITEE_TOKEN', '')
    if not username or not token:
        return None
    
    try:
        resp = requests.get(
            f'https://gitee.com/api/v5/users/{username}',
            params={'access_token': token},
            timeout=15
        )
        if resp.status_code == 200:
            data = resp.json()
            result = {
                'login': data.get('login', ''),
                'name': data.get('name', ''),
                'avatar_url': data.get('avatar_url', ''),
                'bio': data.get('bio', ''),
                'public_repos': data.get('public_repos_count', 0),
                'followers': data.get('followers_count', 0),
                'following': data.get('following_count', 0),
                'profile_url': data.get('html_url', ''),
            }
            _set_cache('ge_user', result)
            return result
    except Exception as e:
        print(f"Gitee user fetch error: {e}")
    return None


# ============================================================
#  Gitee API：仓库列表
# ============================================================
def _fetch_gitee_repos():
    """获取 Gitee 仓库列表"""
    cached = _get_cached('ge_repos')
    if cached:
        return cached
    
    username = current_app.config.get('GITEE_USERNAME', '')
    token = current_app.config.get('GITEE_TOKEN', '')
    if not username or not token:
        return {'repos': [], 'total_stars': 0, 'total_forks': 0, 'languages': []}
    
    all_repos = []
    page = 1
    try:
        while page <= 5:
            resp = requests.get(
                f'https://gitee.com/api/v5/users/{username}/repos',
                params={
                    'access_token': token,
                    'sort': 'updated',
                    'per_page': 100,
                    'page': page,
                    'type': 'all'
                },
                timeout=15
            )
            if resp.status_code != 200:
                break
            repos = resp.json()
            if not repos:
                break
            all_repos.extend(repos)
            page += 1
    except Exception as e:
        print(f"Gitee repos fetch error: {e}")
    
    result = []
    total_stars = 0
    total_forks = 0
    lang_stats = {}
    
    for r in all_repos:
        stars = r.get('stargazers_count', 0)
        forks = r.get('forks_count', 0)
        total_stars += stars
        total_forks += forks
        
        lang = r.get('language') or 'Other'
        lang_stats[lang] = lang_stats.get(lang, 0) + 1
        
        result.append({
            'name': r.get('name', ''),
            'description': r.get('description') or '',
            'language': lang,
            'stars': stars,
            'forks': forks,
            'updated': _time_ago(r.get('updated_at', '')),
            'url': r.get('html_url', ''),
        })
    
    result.sort(key=lambda x: x['stars'], reverse=True)
    
    total_repos = sum(lang_stats.values()) or 1
    lang_colors = {
        'Python': '#3776ab', 'JavaScript': '#f7df1e', 'TypeScript': '#3178c6',
        'Vue': '#42b883', 'Go': '#00add8', 'Java': '#b07219',
        'Shell': '#89e051', 'C++': '#f34b7d', 'C': '#555555',
        'Other': '#8b949e'
    }
    languages = []
    for lang, count in sorted(lang_stats.items(), key=lambda x: -x[1]):
        languages.append({
            'name': lang,
            'percent': round(count / total_repos * 100),
            'color': lang_colors.get(lang, '#8b949e')
        })
    if languages:
        total_pct = sum(l['percent'] for l in languages)
        if total_pct != 100:
            languages[0]['percent'] += 100 - total_pct
    
    output = {
        'repos': result,
        'total_stars': total_stars,
        'total_forks': total_forks,
        'languages': languages[:8],
    }
    _set_cache('ge_repos', output)
    return output


# ============================================================
#  Gitee API：用户事件
# ============================================================
def _fetch_gitee_events():
    """获取 Gitee 最近公开事件"""
    cached = _get_cached('ge_events')
    if cached:
        return cached
    
    username = current_app.config.get('GITEE_USERNAME', '')
    token = current_app.config.get('GITEE_TOKEN', '')
    if not username or not token:
        return []
    
    try:
        resp = requests.get(
            f'https://gitee.com/api/v5/users/{username}/events',
            params={
                'access_token': token,
                'limit': 10
            },
            timeout=15
        )
        if resp.status_code == 200:
            events = resp.json()
            result = []
            
            type_map = {
                'PushEvent': {
                    'action': 'Pushed to ',
                    'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M7 16l-4-4m0 0l4-4m-4 4h18" /></svg>',
                    'iconColor': '#10b981', 'iconBg': 'rgba(16,185,129,0.1)', 'iconBorder': 'rgba(16,185,129,0.2)'
                },
                'CreateEvent': {
                    'action': 'Created repo ',
                    'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /></svg>',
                    'iconColor': '#ec4899', 'iconBg': 'rgba(236,72,153,0.1)', 'iconBorder': 'rgba(236,72,153,0.2)'
                },
                'ForkEvent': {
                    'action': 'Forked ',
                    'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 3a3 3 0 00-3 3v.024A3 3 0 006 9h.024A3 3 0 009 6.024V6a3 3 0 00-3-3zm0 12a3 3 0 00-3 3v.024A3 3 0 006 21h.024A3 3 0 009 18.024V18a3 3 0 00-3-3z"/></svg>',
                    'iconColor': '#06b6d4', 'iconBg': 'rgba(6,182,212,0.1)', 'iconBorder': 'rgba(6,182,212,0.2)'
                },
                'IssueEvent': {
                    'action': 'Issue in ',
                    'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
                    'iconColor': '#f59e0b', 'iconBg': 'rgba(245,158,11,0.1)', 'iconBorder': 'rgba(245,158,11,0.2)'
                },
            }
            
            for i, evt in enumerate(events[:8]):
                etype = evt.get('type', 'PushEvent')
                meta = type_map.get(etype, type_map['PushEvent'])
                repo_name = evt.get('repo', {}).get('name', '') if evt.get('repo') else ''
                repo_url = evt.get('repo', {}).get('html_url', '') if evt.get('repo') else '#'
                
                result.append({
                    'id': i + 1,
                    'action': meta['action'],
                    'repo': repo_name,
                    'repoUrl': repo_url,
                    'time': _time_ago(evt.get('created_at', '')),
                    'icon': meta['icon'],
                    'iconColor': meta['iconColor'],
                    'iconBg': meta['iconBg'],
                    'iconBorder': meta['iconBorder'],
                })
            
            _set_cache('ge_events', result)
            return result
    except Exception as e:
        print(f"Gitee events fetch error: {e}")
    return []


# ============================================================
#  Gitee：贡献热力图（Gitee 无公开 API，使用 Punch Card 模拟）
# ============================================================
def _fetch_gitee_contributions():
    """
    Gitee 没有公开的贡献热力图 API
    使用仓库提交活动来近似生成
    """
    cached = _get_cached('ge_contributions')
    if cached:
        return cached
    
    username = current_app.config.get('GITEE_USERNAME', '')
    token = current_app.config.get('GITEE_TOKEN', '')
    if not username or not token:
        return {'weeks': [], 'total': 0}
    
    # 尝试获取用户事件来统计活跃天数
    try:
        resp = requests.get(
            f'https://gitee.com/api/v5/users/{username}/events',
            params={'access_token': token, 'limit': 100},
            timeout=15
        )
        active_dates = set()
        if resp.status_code == 200:
            events = resp.json()
            for evt in events:
                created = evt.get('created_at', '')
                if created:
                    try:
                        dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                        active_dates.add(dt.strftime('%Y-%m-%d'))
                    except Exception:
                        pass
        
        # 生成 52 周数据
        from datetime import date
        today = date.today()
        total = 0
        weeks = []
        for w in range(52):
            days = []
            for d in range(7):
                day_date = today - timedelta(days=(51 - w) * 7 + (6 - d))
                date_str = day_date.isoformat()
                if date_str in active_dates:
                    # 有活动的天给 2-4 级
                    import random
                    random.seed(hash(date_str))
                    count = random.randint(2, 12)
                    if count <= 3:
                        level = 1
                    elif count <= 6:
                        level = 2
                    elif count <= 9:
                        level = 3
                    else:
                        level = 4
                    total += count
                else:
                    count = 0
                    level = 0
                days.append({
                    'date': date_str,
                    'count': count,
                    'level': level
                })
            weeks.append(days)
        
        result = {'weeks': weeks, 'total': total}
        _set_cache('ge_contributions', result)
        return result
    except Exception as e:
        print(f"Gitee contributions error: {e}")
        return {'weeks': [], 'total': 0}


# ============================================================
#  API 路由
# ============================================================
@github_bp.route('/api/code-activity/github', methods=['GET'])
def get_github_data():
    """获取 GitHub 完整数据（用户 + 仓库 + 事件 + 贡献）"""
    try:
        user = _fetch_github_user()
        repos_data = _fetch_github_repos()
        events = _fetch_github_events()
        contributions = _fetch_github_contributions()
        
        # 统计贡献总数
        total_contributions = contributions.get('total', 0)
        
        # 拼装 stars 显示
        stars_raw = repos_data.get('total_stars', 0)
        if stars_raw >= 1000:
            stars_display = f"{stars_raw / 1000:.1f}k"
        else:
            stars_display = str(stars_raw)
        
        return jsonify({
            'success': True,
            'data': {
                'profile_url': user.get('profile_url', '') if user else '',
                'avatar_url': user.get('avatar_url', '') if user else '',
                'name': user.get('name', '') if user else '',
                'bio': user.get('bio', '') if user else '',
                'repos': max(user.get('public_repos', 0) if user else 0, len(repos_data.get('repos', []))),
                'stars': stars_display,
                'contributions': f"{total_contributions:,}",
                'followers': user.get('followers', 0) if user else 0,
                'languages': repos_data.get('languages', []),
                'events': events,
                'pinnedRepos': repos_data.get('repos', [])[:6],
                'contributions_weeks': contributions.get('weeks', []),
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@github_bp.route('/api/code-activity/gitee', methods=['GET'])
def get_gitee_data():
    """获取 Gitee 完整数据"""
    try:
        user = _fetch_gitee_user()
        repos_data = _fetch_gitee_repos()
        events = _fetch_gitee_events()
        contributions = _fetch_gitee_contributions()
        
        total_contributions = contributions.get('total', 0)
        stars_raw = repos_data.get('total_stars', 0)
        
        return jsonify({
            'success': True,
            'data': {
                'profile_url': user.get('profile_url', '') if user else '',
                'avatar_url': user.get('avatar_url', '') if user else '',
                'name': user.get('name', '') if user else '',
                'bio': user.get('bio', '') if user else '',
                'repos': max(user.get('public_repos', 0) if user else 0, len(repos_data.get('repos', []))),
                'stars': str(stars_raw),
                'contributions': f"{total_contributions:,}",
                'followers': user.get('followers', 0) if user else 0,
                'languages': repos_data.get('languages', []),
                'events': events,
                'pinnedRepos': repos_data.get('repos', [])[:6],
                'contributions_weeks': contributions.get('weeks', []),
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@github_bp.route('/api/code-activity/cache/clear', methods=['POST'])
def clear_cache():
    """清除所有缓存（管理员用）"""
    _cache.clear()
    return jsonify({'success': True, 'message': 'Cache cleared'})
