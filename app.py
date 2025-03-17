# 确保以下导入和初始化代码位于文件顶部
from flask import Flask, render_template, request, redirect, url_for, abort
import requests
import json
from config import Config
import time
from functools import wraps
import markdown
import logging
import traceback
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
app.config.from_object(Config)
app.logger.setLevel(logging.INFO)

# 缓存机制
cache = {
    'token': None,
    'token_expires': 0,
    'articles': None,
    'articles_expires': 0
}

# 确保所有函数定义在被调用之前
def get_tenant_access_token():
    """获取飞书tenant_access_token"""
    now = time.time()
    
    # 如果缓存中有有效的token，直接返回
    if cache['token'] and cache['token_expires'] > now:
        return cache['token']
    
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "app_id": app.config['FEISHU_APP_ID'],
        "app_secret": app.config['FEISHU_APP_SECRET']
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()
        
        if result.get("code") == 0:
            # 缓存token，设置过期时间（提前5分钟过期）
            cache['token'] = result.get("tenant_access_token")
            cache['token_expires'] = now + result.get("expire") - 300
            return cache['token']
        else:
            app.logger.error(f"获取飞书token失败: {result}")
            return None
    except Exception as e:
        app.logger.error(f"获取飞书token异常: {str(e)}")
        app.logger.error(traceback.format_exc())
        return None

def get_articles():
    """从飞书多维表格获取文章数据"""
    now = time.time()
    
    # 如果缓存中有有效的文章数据，直接返回
    if cache['articles'] and cache['articles_expires'] > now:
        return cache['articles']
    
    token = get_tenant_access_token()
    if not token:
        app.logger.error("无法获取飞书访问令牌")
        return []
    
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app.config['BASE_ID']}/tables/{app.config['TABLE_ID']}/records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        result = response.json()
        
        if result.get("code") == 0:
            items = result.get("data", {}).get("items", [])
            articles = []
            
            for item in items:
                fields = item.get("fields", {})
                content = fields.get("概要内容输出", "")
                
                # 将Markdown内容转换为HTML
                html_content = markdown.markdown(content)
                
                article = {
                    "id": item.get("record_id"),
                    "title": fields.get("标题", ""),
                    "quote": fields.get("金句输出", ""),
                    "comment": fields.get("老何点评", ""),
                    "content": content,
                    "html_content": html_content,
                    "preview": content[:100] + "..." if len(content) > 100 else content
                }
                articles.append(article)
            
            # 缓存文章数据，设置过期时间（5分钟）
            cache['articles'] = articles
            cache['articles_expires'] = now + 300
            return articles
        else:
            app.logger.error(f"获取飞书数据失败: {result}")
            return []
    except Exception as e:
        app.logger.error(f"获取飞书数据异常: {str(e)}")
        app.logger.error(traceback.format_exc())
        return []

def get_article_by_id(article_id):
    """根据ID获取文章详情"""
    articles = get_articles()
    for article in articles:
        if article["id"] == article_id:
            return article
    return None

def clear_cache():
    """清除缓存"""
    cache['articles'] = None
    cache['articles_expires'] = 0
    return True

@app.route('/')
def index():
    """首页"""
    try:
        app.logger.info("开始加载首页")
        articles = get_articles()
        app.logger.info(f"成功获取文章列表，共{len(articles)}篇")
        return render_template('index.html', articles=articles)
    except Exception as e:
        app.logger.error(f"首页渲染异常: {str(e)}")
        app.logger.error(traceback.format_exc())
        return render_template('500.html', error_message=str(e)), 500

@app.route('/article/<article_id>')
def article_detail(article_id):
    """文章详情页"""
    try:
        article = get_article_by_id(article_id)
        if not article:
            abort(404)
        return render_template('detail.html', article=article)
    except Exception as e:
        app.logger.error(f"文章详情页渲染异常: {str(e)}")
        app.logger.error(traceback.format_exc())
        return render_template('500.html', error_message=str(e)), 500

@app.route('/refresh', methods=['GET'])
def refresh():
    """刷新缓存"""
    try:
        if clear_cache():
            # 重新获取文章数据
            get_articles()
            return redirect(url_for('index'))
        else:
            abort(500)
    except Exception as e:
        app.logger.error(f"刷新缓存异常: {str(e)}")
        app.logger.error(traceback.format_exc())
        return render_template('500.html', error_message=str(e)), 500

# 添加测试路由
@app.route('/test')
def test():
    """测试路由，检查应用是否正常运行"""
    return {
        "status": "ok",
        "message": "应用正常运行",
        "config": {
            "app_id_set": bool(app.config.get('FEISHU_APP_ID')),
            "app_secret_set": bool(app.config.get('FEISHU_APP_SECRET')),
            "base_id_set": bool(app.config.get('BASE_ID')),
            "table_id_set": bool(app.config.get('TABLE_ID'))
        }
    }

# 错误处理器
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html', error_message=str(e)), 500

# 添加当前年份变量
@app.context_processor
def inject_year():
    """向所有模板注入当前年份变量"""
    import datetime
    return {'current_year': datetime.datetime.now().year}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)