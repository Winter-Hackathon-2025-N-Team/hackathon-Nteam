from flask import Flask, request, redirect, render_template, session, flash, url_for
from datetime import timedelta
import hashlib
import uuid
import re
import os
from models import User

# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
YEAR_PATTERN = r"^(19[0-9]{2}|20[0-9]{2})$"
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex) #セッション管理の秘密鍵(環境変数orランダムなUUID)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS) #ログインセッションの有効期限

# 静的ファイルをキャッシュする設定。開発中はコメントアウト推奨。
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 2678400

# ルートページ
@app.route('/', methods=['GET'])
def index():
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    return redirect(url_for('home_view'))

# サインアップページ表示
@app.route('/signup', methods=['GET'])
def signup_view():
    return render_template('signup.html')

# サインアップ処理
@app.route('/signup', methods=['POST'])
def signup_process():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    password_confirmation = request.form.get('passwordConfirmation')
    kindergarten_schoolname = request.form.get('kindergartenName')
    kindergarten_start_year = request.form.get('startYearKindergarten')
    kindergarten_end_year = request.form.get('endYearKindergarten')
    elementary_schoolname = request.form.get('elementarySchoolName')
    elementary_start_year = request.form.get('startYearElementarySchool')
    elementary_end_year = request.form.get('endYearElementarySchool')

    # 入力バリデーション
    if not all([name, email, password, password_confirmation,kindergarten_schoolname ,kindergarten_start_year ,kindergarten_end_year,elementary_schoolname,elementary_start_year,elementary_end_year]):
        flash('空のフォームがあります')
    elif password != password_confirmation:
        flash('パスワードが一致しません')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    elif re.match(YEAR_PATTERN, kindergarten_start_year) is None or re.match(YEAR_PATTERN, kindergarten_end_year) is None or re.match(YEAR_PATTERN, elementary_start_year) is None or re.match(YEAR_PATTERN, elementary_end_year) is None:
        flash('正しい入学年または卒業年の入力ではありません')
    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()#パスワードをハッシュ化
        registered_user = User.find_by_email(email)
    
        if registered_user != None:
            flash('既に登録されているようです')
        else:
         # 新規ユーザー登録
            User.create(uid, name, email, password, kindergarten_schoolname, kindergarten_start_year, kindergarten_end_year, elementary_schoolname, elementary_start_year, elementary_end_year)
            UserId = str(uid)
            session['uid'] = UserId
            return redirect(url_for('home_view'))
    return redirect(url_for('signup_process'))

# ログインページ表示
@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

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
                return redirect(url_for('home_view'))
    return redirect(url_for('login_view'))

# ホームページ表示
@app.route('/home', methods=['GET'])
def home_view():
    return render_template('home.html')

# ログアウト処理
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login_view'))

# エラーハンドラー
@app.errorhandler(500)
def internal_server_error(e):
    return "500 Internal Server Error", 500

@app.errorhandler(404)
def page_not_found(e):
    return "404 Page Not Found", 404

# アプリ起動
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
