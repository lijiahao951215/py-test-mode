from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/user/<username>')
def show_user_profile(username):
    # 显示用户的个人资料
    return f'User {username}'

if __name__ == '__main__':
    app.run(debug=True)
