# 个人博客网站（飞书多维表格驱动）

这是一个基于 Flask 的个人博客网站，数据来源于飞书多维表格。采用苹果设计风格，融入中国红主题色，提供简洁优雅的阅读体验。

## Zeabur一键部署

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/XXXXX)

## 部署说明

1. 在Zeabur上部署时，需要设置以下环境变量：
   - `FEISHU_APP_ID`: 飞书应用的App ID
   - `FEISHU_APP_SECRET`: 飞书应用的App Secret
   - `BASE_ID`: 飞书多维表格的Base ID
   - `TABLE_ID`: 飞书多维表格的Table ID
   - `SECRET_KEY`: Flask应用的密钥（可以是任意复杂字符串）
   - `DEBUG`: 是否开启调试模式（生产环境设为False）

2. 确保飞书应用已开启多维表格权限：`bitable:record:read`

## 本地开发

1. 克隆项目
2. 创建并配置`.env`文件
3. 安装依赖：`pip install -r requirements.txt`
4. 运行应用：`python app.py`
5. 访问：http://localhost:5000
