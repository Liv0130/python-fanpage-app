from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

import os
from dotenv import load_dotenv

load_dotenv()
ca = certifi.where()

DB_URL = os.environ.get("DB_URL")
client = MongoClient(DB_URL, tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/homework", methods=["POST"])
def homework_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    doc = {
        'name': name_receive,
        'comment': comment_receive
    }
    db.fanpage.insert_one(doc)
    return jsonify({'msg':'응원 완료!'})

@app.route("/homework", methods=["GET"])
def homework_get():
    all_cheers = list(db.fanpage.find({}, {'_id': False}))
    return jsonify({'cheers': all_cheers})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)