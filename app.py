from flask import Flask, jsonify, request
from pymongo import MongoClient
from config import db
from config import gcmKey
from gcm import GCM
import json
import imaplib


app = Flask(__name__)

@app.route('/register', methods=['POST'])
def add_user():
	if request.method == "POST":
                data=request.json
                pno = data['pno']
                reg_id = data['regno']
                nick = data['nick']
                print request.json
                db.users.insert({
				"pno": pno,
				"registration_id": reg_id,
                                "nick":nick
				})
                
		return jsonify( ( { "Signed Up" : 1 } ) )

# Route is for backing up attendance
@app.route('/newAlarm',methods=['POST'])
def newAlarm():
    if request.method == 'POST':
        datas=request.json
        to = datas['to']

        print "1"
        print '2\n\n--------------------------------'
        gcm = GCM(gcmKey)
        users = db.users.find({"pno" : to})
        print users
        reg_ids = []
        for i in users:
            reg_ids.append(i['registration_id'])
        print len(reg_ids)
        print"--------------------------"
        print '-------------------------------------------'
        response = gcm.json_request(registration_ids=reg_ids, data=datas,collapse_key='chat')
        return  response

if __name__ =="__main__":
  app.run(debug=True)

