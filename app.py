from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.vpw4dwu.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

# 메인 페이지 로드
@app.route('/')
def home():
    return render_template('index.html')

# 자유게시판
@app.route('/free_board')
def free_board():
    comment_receive = request.form['free_board_give']
    return render_template('/free_board.html')

# 자유게시판 포스트
@app.route('/templates/free_board_review', methods=['POST'])
def free_board_post():
    comment_receive = request.form['comment_give']
    doc = {
        'comment':comment_receive
    }

    db.freeboard.insert_one(doc)

    return jsonify({'msg':'저장 완료!'})

# 자유게시판 보여주기
@app.route('/36Team_ToyProject',methods=["GET"])
def free_board_get():
    code_list = list(db.develco_code.find({}, {'_id': False}))

    return jsonify({'codes':code_list})


# 코드리뷰 페이지로 이동
@app.route('/code_review')
def code_review():
    return render_template('/code_review.html')


# 코드 포스트
@app.route('/templates/code_review', methods=['POST'])
def code_review_post():
    code_receive = request.form['code_give']
    doc = {
        'code': code_receive
    }
    db.develco_code.insert_one(doc)

    return jsonify({'msg':'업로드 완료!'})

# 코드 보여주기
@app.route('/36Team_ToyProject',methods=["GET"])
def code_get():
    code_list = list(db.develco_code.find({}, {'_id': False}))

    return jsonify({'codes':code_list})




# @app.route("/36Team_ToyProject", methods=["GET"])
# def homework_get():
#
#     return jsonify({'msg':'GET 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)