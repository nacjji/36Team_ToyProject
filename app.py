from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi


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
        'quest':quest_receive
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