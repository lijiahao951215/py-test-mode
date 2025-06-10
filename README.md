
# 注释
有些可能需要使用  python3 进行替换 python

# 本地运行

## 下载和安装Python
https://www.python.org/

## 验证安装
python --version

## Flask 框架安装
pip install flask
### 其他安装（产品关联性计算）
pip install sentence-transformers

### 生成依赖
pip freeze > requirements.txt

### 追加测试环境
python -m venv .venv

## 示例 demo
demo.py
.venv\Scripts\activate
flask --app demo run

## 运行项目
flask --app hello run --host=0.0.0.0 --port=5000

### 运行激活  
.venv\Scripts\activate

### 启动项目
flask --app hello run
flask --app demo run
flask app run

# Linux

## 首次运行项目
python -m venv .venv
pip install -r requirements.txt

## 运行项目
cd /www/wwwroot/py-test-mode/
source .venv/bin/activate
flask --app demo run --host=0.0.0.0
flask --app demo run
flask --app hello run

## Gunicorn运行Flask应用
cd /www/wwwroot/py-test-mode/
source .venv/bin/activate
pip install gunicorn
gunicorn --workers 3 --bind unix:demo.sock -m 007 demo:app

### supervisor
[program:flask_app]
directory=/www/wwwroot/py-test-mode/
command=/www/wwwroot/py-test-mode/.venv/bin/gunicorn --workers 3 --bind unix:demo.sock -m 007 demo:app
autostart=true
autorestart=true
stderr_logfile=/var/log/flask_app/flask_app.err.log
stdout_logfile=/var/log/flask_app/flask_app.out.log
user=ubuntu

### 创建日志文件目录
sudo mkdir -p /var/log/flask_app

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start flask_app

### 配置Nginx作为反向代理

server {
    listen 80;
    server_name your_domain_or_IP;

    location / {
        proxy_pass http://unix:/www/wwwroot/py-test-mode/demo.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
创建符号链接以启用此配置：
sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled

最后，测试Nginx配置是否有语法错误：
sudo nginx -t

sudo systemctl restart nginx