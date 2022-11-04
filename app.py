from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi


app = Flask(__name__)
ca = certifi.where()
client = MongoClient('mongodb+srv://test:123@cluster0.vpw4dwu.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/36Team_ToyProject", methods=["POST"])
def homework_post():
    sample_receive = request.form['sample_give']
    return jsonify({'msg':'POST 완료!'})


@app.route("/36Team_ToyProject", methods=["GET"])
def homework_get():

    return jsonify({'msg':'GET 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)