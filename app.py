import dotenv
dotenv.load_dotenv()
# 取出環境變數
import os
MONGODB_URL = os.getenv('MONGODB_URL')
# 初始化資料庫連線

import pymongo
client = pymongo.MongoClient(MONGODB_URL)
db = client.member_system
print("資料庫連線成功")

from flask import *

app = Flask(
    __name__,
    static_folder='public',
    static_url_path='/'
)


#########################################################

# 處理路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/member')
def member():
    # 如果沒有登入，導向錯誤頁面
    if 'nickname' in session:
        return render_template('member.html')
    else:
        return redirect('/')

# error?msg=錯誤訊息
@app.route('/error')
def error():
    msg = request.args.get('msg', "發生錯誤")
    return render_template('error.html', msg=msg)

#########################################################

# 處理表單
@app.route('/signup', methods=['POST'])
def signup():
    # 從前端接受資料
    nickname = request.form.get('nickname')
    email = request.form.get('email')
    password = request.form.get('password')

    # 根據接收到的資料進行處理
    collection = db.user

    # 檢查 email 是否已經被註冊過
    is_email_used = collection.find_one({
        'email': email
    })
    if is_email_used != None:
        return redirect('/error?msg=此帳號已經被註冊過')
    
    # 將資料存入資料庫，完成註冊
    collection.insert_one({
        'nickname': nickname,
        'email': email,
        'password': password
    })
    return redirect('/')


# 處理登入表單
@app.route('/signin', methods=['POST'])
def signin():
    # 從前端接受資料
    email = request.form.get('email')
    password = request.form.get('password')
    # 檢查 email 和 password 是否正確
    collection = db.user
    is_correct = collection.find_one({
        "$and": [
            {'email': email},
            {'password': password}
        ]
    })
    # 如果不正確，導向錯誤頁面
    # 如果正確，在session中記錄會員資訊，再導向會員頁面
    if is_correct == None:
        return redirect('/error?msg=帳號或密碼輸入錯誤')
    else:
        session['nickname'] = is_correct['nickname']
        return redirect('/member')
    
# 處理登出
@app.route('/logout')
def logout():
    # 清除session
    session.clear()
    return redirect('/')


#########################################################


app.secret_key = '00000000'
app.run(port=3000)
