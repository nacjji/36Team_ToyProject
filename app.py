from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
from bson.json_util import dumps


app = Flask(__name__)
ca = certifi.where()
client = MongoClient('mongodb+srv://test:123@cluster0.vpw4dwu.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

# 메인 페이지 로드
@app.route('/')
def home():
    return render_template('index.html')


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
    code_receive = request.form['code_give']
    quest_receive = request.form['quest_give']

    doc = {
        'code': code_receive,
        'quest': quest_receive,
    }
    db.develco_code.insert_one(doc)

    return jsonify({'msg': '업로드 완료!'})


# 중고거래 페이지로 이동
@app.route('/trading')
def trading():
    return render_template('/trading.html')

# 중고거래 포스트
@app.route('/templates/trading', methods=['POST'])
def trading_post():
    post_receive = request.form['post_give']
    trading_list = list(db.develco_trading_post.find({}, {'_id': False}))
    count = len(trading_list) + 1

    doc_post = {
        'num':count,
        'post':post_receive
    }

    db.develco_trading_post.insert_one(doc_post)

    doc_comment = {
        'post_id':list(db.develco_trading_post.find({'num':count},{'_id':True}))[0],
        'comment': []
    }
    db.develco_trading_comment.insert_one(doc_comment)

    return jsonify({'msg':'거래글 작성 완료!'})

# 댓글 포스트
# @app.route('/templates/trading_comment', methods=['POST'])
# def comment_post():
#     comment_receive = request.form['comment_give']
#     num_receive = request.form['num_give']
#
#     posts = list(db.develco_trading_post.find({},{'_id':True}))
#
#     for post in posts:
#         print(post)
#
#     doc = {
#         'num': num_receive,
#         'comment':comment_receive
#     }
#     db.develco_trading_comment.insert_one(doc)
#
#     db.develco_trading_comment.update_one(
#         {'num': num_receive},
#         {'$push': {'comment': comment_receive}}
#     )
#
#     return jsonify({'msg':'댓글 완료'})

# 중고거래 보여주기
@app.route('/templates/trading',methods=["GET"])
def trading_get():
    trading_list = list(db.develco_trading_post.find({}))
    return dumps({'trading_posts':trading_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)