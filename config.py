import os
from dotenv import load_dotenv

# 加载环境变量（本地开发时使用）
load_dotenv()

class Config:
    # 飞书应用配置
    FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "cli_a75d2ca26b93900d")
    FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "Z9IvHXxPVYpgJKPR8DsV0e1QfnUld0R7")
    
    # 多维表格配置
    BASE_ID = os.environ.get("BASE_ID", "CFo2b6qHtah7aYsQxtzcDD1bnpb")
    TABLE_ID = os.environ.get("TABLE_ID", "tbldNNryflOEeaMN")
    
    # Flask配置
    SECRET_KEY = os.environ.get("SECRET_KEY", "G908HJIIHFFJKMNouin012")
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"