from sayhello import app, db
from sayhello.forms import HelloForm,ReplyForm
from sayhello.models import Message,Reply
from flask import flash, render_template, request, redirect, session,url_for
import functools

users = [
    {'username': 'gjb', 'password': '123456'},
    {'username': 'shaungyi', 'password': '666666'},
    # ...
]


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 验证用户名和密码
        for user in users:
            if user['username'] == username and user['password'] == password:
                # 将用户信息存储在会话中
                session['username'] = username
                return redirect('/')

        # 用户名或密码不正确时的处理
        return render_template('login.html', error='用户名或密码无效')
    # GET 请求时渲染登录页面
    return render_template('login.html')

# 装饰器函数，用于检查用户是否已登录

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'username' not in session:
            return redirect('/login')
        return view(*args, **kwargs)
    return wrapped_view

# 需要登录才能访问的页面
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(body=body, name=name)  # 实例化模型类，创建记录
        db.session.add(message)  # 添加记录到数据库回会话
        db.session.commit()  # 提交会话
        flash('Your message have been sent to the world!')
        return redirect(url_for('index'))  # 重定向到index视图
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('index.html', form=form, messages=messages)
@app.route('/logout')

def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/delete/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    message = Message.query.get(message_id)
    if message:
        db.session.delete(message)
        db.session.commit()
        flash('Message deleted successfully!')
    return redirect('/')
from faker import Faker

@app.route('/generate_messages', methods=['GET'])
def generate_messages():
    fake = Faker('zh-CN')
    for _ in range(10):  # 生成 10 条测试留言
        name = fake.name()
        body = fake.text(max_nb_chars=200)
        message = Message(name=name, body=body)
        db.session.add(message)
    db.session.commit()
    flash('Generated test messages!')
    return redirect('/')

@app.route('/reply', methods=['POST'])
def reply_message():
    form = ReplyForm()
    if form.validate_on_submit():
        parent_id = request.form.get('parent_id')
        body = form.reply_body.data

        # 创建回复对象
        reply = Reply(body=body, message_id=parent_id)
        db.session.add(reply)
        db.session.commit()

        flash('Your reply has been posted.')
        return redirect(url_for('index'))

    return redirect(url_for('index'))
