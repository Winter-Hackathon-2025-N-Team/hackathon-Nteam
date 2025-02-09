from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from datetime import timedelta
import hashlib
import uuid
import re
import os

from models import User, Channel, Message
from util.assets import bundle_css_files

# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

# 静的ファイルをキャッシュする設定。開発中はコメントアウト推奨。
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 2678400
#bundle_css_files(app)


# ルートページのリダイレクト処理
@app.route('/', methods=['GET'])
def index():
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    return redirect(url_for('channels_view'))

# サインアップページ(基本情報)の表示
@app.route('/regist/step1', methods=['GET'])
def signup_view():
    return render_template('auth/signup_basic_info.html')


# サインアップ処理(基本情報)
@app.route('/regist/step1', methods=['POST'])
def signup_process1():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    passwordConfirmation = request.form.get('password-confirmation')
    introduction = request.form.get('introduction')

    if name == '' or email =='' or password == '' or passwordConfirmation == '':
        flash('空のフォームがあるようです')
    elif password != passwordConfirmation:
        flash('二つのパスワードの値が違っています')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        registered_user = User.find_by_email(email)

        if registered_user != None:
            flash('既に登録されているようです')
        else:
            User.create(uid, name, email, password)
            UserId = str(uid)
            session['uid'] = UserId
            return redirect(url_for('signup_process2'))
    return redirect(url_for('signup_process1'))

# サインアップページ(出身履歴)の表示
@app.route('/regist/step2', methods=['GET'])
def signup_view2():
    return render_template('auth/signup_history.html')

# サインアップ処理(出身履歴情報)
@app.route('/regist/step2', methods=['POST'])
def signup_process2():
    """入力した属性をどのように格納する？
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    passwordConfirmation = request.form.get('password-confirmation')
    introduction = request.form.get('introduction')

    if name == '' or email =='' or password == '' or passwordConfirmation == '':
        flash('空のフォームがあるようです')
    elif password != passwordConfirmation:
        flash('二つのパスワードの値が違っています')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        registered_user = User.find_by_email(email)

        if registered_user != None:
            flash('既に登録されているようです')
        else:
            User.create(uid, name, email, password)
            UserId = str(uid)
            session['uid'] = UserId
            return redirect(url_for('signup_process2'))
    """
    return redirect(url_for('signup_process1'))


# ログインページの表示
@app.route('/login', methods=['GET'])
def login_view():
    return render_template('auth/login.html')


# ログイン処理
@app.route('/login', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')

    if email =='' or password == '':
        flash('空のフォームがあるようです')
    else:
        user = User.find_by_email(email)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('パスワードが間違っています！')
            else:
                session['uid'] = user["uid"]
                return redirect(url_for('channels_view'))
    return redirect(url_for('login_view'))


# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_view'))

# チャンネル一覧ページの表示
@app.route('/home', methods=['GET'])
def channels_view():
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    else:
        """""
        channels = Channel.get_all()
        channels.reverse()
        """""
        return render_template('home.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)