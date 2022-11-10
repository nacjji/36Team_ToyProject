import jwt as jwt
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
from bson.json_util import dumps
import bcrypt
import jwt

app = Flask(__name__)
ca = certifi.where()
client = MongoClient('mongodb+srv://test:123@cluster0.vpw4dwu.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

# 메인 페이지 로드
@app.route('/')
def home():
    return render_template('index.html')
# 로그인 창으로 이동
# @app.route('/login')
# def devel_login():
#     return render_template('/login.html')
#
#
# @bp.route('/login', methods=['POST'])
# def login():
#     credential = request.json
#     email = credential['email']  # 요청한 이메일
#     password = credential['password']  # 요청한 비밀번호
#
#     row = user.get_user_from_email(email)  # 이메일을 이용하여 실제 유저 정보를 가져옴
#
#     # 요청한 이메일의 유저 정보가 있는 경우, 비밀번호를 대조하여 확인
#     if row and bcrypt.checkpw(password.encode('UTF-8'), row['hashed_password'].encode('UTF-8')):
#         user_id = row['id']
#         payload = {
#             'user_id': user_id,  # user id
#             'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 만료 시간(24시간 후 )
#         }
#         # 비밀번호가 일치하는 경우 JWT 생성
#         token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], 'HS256')
#
#         return jsonify({
#             'access_token': token.decode('UTF-8')
#         })
#     else:
#         # 유저 정보가 없거나 비밀번호가 일치하지 않는 경우 401 코드 반환
#         return '', 401








# 자유게시판
@app.route('/free_board')
def free_board():
    return render_template('/free_board.html')

# 자유게시판 포스트
@app.route('/templates/free_board', methods=['POST'])
def free_board_post():
    comment_receive = request.form['comment_give']
    doc = {
        'comment':comment_receive
    }

    db.freeboard.insert_one(doc)

    return jsonify({'msg':'저장 완료!'})

# 자유게시판 보여주기
@app.route('/templates/free_board',methods=["GET"])
def free_board_get():
    free_list = list(db.freeboard.find({}, {'_id': False}))

    return jsonify({'comments': free_list})

# 코드리뷰 게시판 보여주기
@app.route('/templates/code_review',methods=["GET"])
def code_get():

    code_list = list(db.develco_code.find({}, {'_id': False}))

    return jsonify({'codes': code_list})



# 코드리뷰 페이지로 이동
@app.route('/code_review')
def code_review():
    return render_template('/code_review.html')


# 코드 포스트
@app.route('/templates/code_review', methods=['POST'])
def code_review_post():

    code_list = list(db.develco_code.find({}, {'_id': False}))

    code_receive = request.form['code_give']
    quest_receive = request.form['quest_give']
    count = len(code_list)+1

    doc = {
        'num': count,
        'code': code_receive,
        'quest': quest_receive,

    }
    db.develco_code.insert_one(doc)
    return jsonify({'msg': '업로드 완료!'})


# 댓글 작성 num 값 받아와서 작성하기
@app.route('/code_review/code_post', methods=['POST'])
def code_com_post():
    code_list = list(db.code_comment.find({}, {'_id': False}))
    comment_receive = request.form['code_com_give']
    count = len(code_list)+1

    doc = {
        'num': count,
        'com_code': comment_receive
    }
    db.code_comment.insert_one(doc)
    return jsonify({'msg': '댓글작성 완료!'})



# 코드리뷰 작성 댓글 보여주기
@app.route('/code_review/show_code',methods=["GET"])
def code_com_get():
    codCom_list = list(db.code_comment.find({}, {'_id': False}))

    return jsonify({'com_code': codCom_list})

# 댓글 수정
@app.route("/code_review/update", methods=["POST"])
def update_code():
    num_receive = request.form['num_give']
    update_receive = request.form['update_give']
    # mongoDB에서의 데이터는 숫자로 저장되는데 보내지는 데이터는 문자열로 보내지기 때문에 캐스팅을 해서 보냄
    db.code_comment.update_one({'num': update_receive}, {'$set': {'com_code': update_receive}})
    return jsonify({'msg': '댓글 수정 완료!!'})

# 중고거래 페이지로 이동
@app.route('/trading')
def trading():
    return render_template('/trading.html')

# 중고거래 포스트
@app.route('/templates/trading', methods=['POST'])
def trading_post():
    post_receive = request.form['post_give']

    doc = {
        'post':post_receive
    }
    db.develco_trading_post.insert_one(doc)
    return jsonify({'msg':'거래글 작성 완료!'})

# 중고거래 보여주기
@app.route('/templates/trading',methods=["GET"])
def trading_get():
    trading_list = list(db.develco_trading_post.find({},{'_id':False}))
    return jsonify({'trading_posts':trading_list})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)