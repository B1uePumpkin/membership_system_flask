# 初始化資料庫連嫌

import pymongo
client = pymongo.MongoClient("mongodb+srv://root:Password@mycluster.b0llbe5.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster")
db = client.member_system
print("資料庫連線成功")

from flask import *

app = Flask(
    __name__,
    static_folder='public',
    static_url_path='/'
)

# 處理路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/member')
def member():
    return render_template('member.html')

# error?msg=錯誤訊息
@app.route('/error')
def error():
    msg = request.args.get('msg', "發生錯誤")
    return render_template('error.html', msg=msg)



app.secret_key = '00000000'
app.run(port=3000)
