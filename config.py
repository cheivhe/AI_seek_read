import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 飞书应用配置
    FEISHU_APP_ID = os.getenv("FEISHU_APP_ID")
    FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET")
    
    # 多维表格配置
    BASE_ID = os.getenv("BASE_ID")
    TABLE_ID = os.getenv("TABLE_ID")
    
    # Flask配置
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_key_for_blog")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"