from flask import Flask, render_template, redirect, url_for, request,  jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import  datetime
from sqlalchemy import desc
import requests
import json
from sqlalchemy import and_
import goslate


#create application object
app = Flask(__name__)

from scraper import *
# from dbFunctions import *


@app.route("/")
def hello():
    return "Hello, mscan is working"

@app.route('/registeruser', methods = ['GET', 'POST'])
def users_upload():
	 if request.method == 'POST':
	 	user_phone_number = request.json.get('number')
		user=User.query.filter_by(number=user_phone_number).first()
		if user:
			response=jsonify(error='user already registered', message="The provided phone number is already registed in the databse")
			response.status_code=401
			return response
		else:
			d=request.json
			user = User()
			print(d.get('birthdate'))
			user.number=d.get('number')
			user.age =  d.get('age')
			user.contract_current_price =d.get('contract_current_price')
			user.registration_datetime= datetime.datetime.now()
			user.sdk = d.get("sdk")
			user.manufacturer = d.get("manufacturer")
			user.build_device = d.get("build_device")
			user.build_model = d.get("build_model")
			user.device_software_version = d.get("device_software_version")
			user.devide_id = d.get("devide_id")
			user.phone_type = d.get("phone_type")
			user.network_operator_name = d.get("network_operator_name")
			user.network_roaming = d.get("network_roaming")
			user.network_country_iso = d.get("network_country_iso")
			user.network_type = d.get("network_type")
			user.sim_state = d.get("sim_state")
			user.sim_operator = d.get("sim_operator")
			user.sim_operator_name = d.get("sim_operator_name")
			user.sim_serial_number = d.get("sim_serial_number")
			user.subscriber_id = d.get("subscriber_id")
			db.session.add(user)
			db.session.commit()
			user=User.query.filter_by(number=user_phone_number).first()
			message = {'request':'register_user',  'message': 'The user was added successfully', "userID" : user.user_id}
			response = jsonify(message=message)
			response.status_code=200
			return response
#todo: do the same as above for calls, mbdata and sms

@app.route('/viewMD/<userID>')
def viewMD(userID):
	user=User.query.filter_by(user_id=userID).first()
	if user:
		
		mds = MobileData.query.filter(MobileData.md_user_id==userID).order_by(desc(MobileData.md_creation_time)).all()
		return render_template('mds.html', mds = mds)
	else:
		return """<html><body>
		This user is not in the database
		</body></html>""" 



@app.route('/viewCalls/<userID>')
def viewCalls(userID):
	user=User.query.filter_by(user_id=userID).first()
	if user:
		calls = Call.query.filter(Call.user_id==userID).order_by(desc(Call.call_creation_time)).all()
		return render_template('calls.html', calls = calls)
	else:
		return """<html><body>
		This user is not in the database
		</body></html>"""


@app.route('/viewrecentMD/<userID>')
def viewRecentCalls(userID):
	user=User.query.filter_by(user_id=userID).first()
	if user:
		daysback = datetime.timedelta(days=3)
		since = datetime.datetime.now() - daysback
		mds = MobileData.query.filter(and_(MobileData.md_creation_time > since, MobileData.md_user_id==userID) ).all()
	
		return render_template('recent_mds.html', mds = mds)
	else:
		return """<html><body>
		This user is not in the database
		</body></html>"""


@app.route('/viewSMS/<userID>')
def viewSMS(userID):
	user=User.query.filter_by(user_id=userID).first()
	if user:
		sms = SMS.query.filter(SMS.user_id==userID).order_by(desc(SMS.sms_creation_time)).all()
		return render_template('sms.html', sms = sms)
	else:
		return """<html><body>
		This user is not in the database
		</body></html>"""


@app.route('/viewCountryISO/<userID>')
def viewCountryISO(userID):
	user=User.query.filter_by(user_id=userID).first()
	if user:
		countryISOs = CountryISOLog.query.filter(CountryISOLog.cISO_user_id==userID).order_by(desc(CountryISOLog.cISO_creation_time)).all()
		return render_template('countryISO.html', countryISOs = countryISOs)
	else:
		return """<html><body>
		This user is not in the database
		</body></html>"""



@app.route('/testFF/<userID>')
def testFF(userID):
	user=User.query.filter_by(user_id=userID).first()
	if user:
		x=20
		stats= {}
		stats["Currenct Contract Price"] = getUserCurrentContractPrice(userID)
		stats["User Operator"] = getUserOperator(userID)
		stats["Number of Calls to Fix in CH"] = callsFixedCH(userID).get('number')
		stats["Seconds of Calls to Fix in CH"] = callsFixedCH(userID).get('duration')
		stats["Number of Calls to Mobile in CH"] = CallsMobileCH(userID).get('number')
		stats["Seconds of Calls to Mobile in CH"] = CallsMobileCH(userID).get('duration')
		stats["Sms to CH"] = SMS_toCH(userID)
		stats["Data in CH"] = dataCH(userID)  + " MBytes"
		stats["Sms to abroad"] = SMS_toABROAD(userID)
		stats["Abroad Country 1"]  = callsToAbroadLandX(userID, 0).get('country')
		stats["Number Calls to Abroad 1"]  = callsToAbroadLandX(userID, 0).get('number')
		stats["Seconds Calls to Abroad 1"]  = callsToAbroadLandX(userID, 0).get('duration')
		return render_template('userStats.html', stats = stats)

	else:
		return """<html><body>
		This user is not in the database
		</body></html>"""


@app.route('/viewUsers')
def viewUsers():
	users=db.session.query(User).all()
	return render_template('view_users.html', users = users)



@app.route('/deleteMDDB')
def deleteMD():
	num_rows_deleted = db.session.query(MobileData).delete()
	print(num_rows_deleted)
	db.session.commit()
	response = jsonify(message="All rows deleted")
	response.status_code=200
	return response

@app.route('/deleteCallsDB')
def deleteCallDb():
	num_rows_deleted = db.session.query(Call).delete()
	db.session.commit()
	print(num_rows_deleted)
	response = jsonify(message="All rows deleted")
	response.status_code=200
	return response
@app.route('/deleteSMSDB')
def deleteSMSDB():
	num_rows_deleted = db.session.query(SMS).delete()
	db.session.commit()
	print(num_rows_deleted)
	response = jsonify(message="All rows deleted")
	response.status_code=200
	return response

@app.route('/deleteUsers')
def deleteUsers():
	num_rows_deleted = db.session.query(User).delete()
	print(num_rows_deleted)
	response = jsonify(message="All rows in users deleted")
	response.status_code=200
	return response

@app.route('/uploadCallsSMS/<user_ID>', methods=["POST"])
def uploadCallsSMS(user_ID):
	if request.method == "POST":
		user=User.query.filter_by(user_id=user_ID).first()
		if user:
			data_entries= request.json
			# mobileData = data_entries[0]
			calls = data_entries[0]
			smss= data_entries[1]
			for call in calls:
				c= Call()

				c.user_id = user.user_id
				c.call_number = call.get('number')
				c.call_creation_time = datetime.datetime.strptime(call.get('creation_time'), '%Y-%m-%d %H:%M:%S')
				isDuplicate = Call.query.filter(and_(Call.call_creation_time==c.call_creation_time , Call.call_number ==c.call_number, Call.user_id == c.user_id)).first()
				if isDuplicate:
					print("Call is duplicate")
					continue
				print("Call is NOT duplicate")

				c.call_type=call.get('type')
				print("number is " + call.get('number'))
				c.duration = call.get('duration')
				c.contact_name = call.get('contact_name')
				c.other_number_location =call.get('location_other_number')
				c.user_location =call.get('location_this_number')
				db.session.add(c)
				db.session.commit()
			for sms in smss:
				s = SMS()
				s.user_id = user.user_id
				s.sms_creation_time =datetime.datetime.strptime(sms.get('creation_time'), '%Y-%m-%d %H:%M:%S')
				s.sms_type = sms.get('type')
				s.sms_number = sms.get('number')
				isDuplicate = SMS.query.filter(and_(SMS.sms_creation_time==s.sms_creation_time , SMS.sms_number ==s.sms_number, SMS.user_id == s.user_id)).first()
				if isDuplicate:
					continue
				db.session.add(s)
				db.session.commit()
			response = jsonify(message="the call and sms data record was added successfully")
			response.status_code=200
			return response
		else:
			reponse=jsonify(error='user not registered', message="The provided phone number is not registed in the databse")
			response.status_code=401
			return response
	else:
		return """<html><body>
		Something went horribly wrong
		</body></html>"""




@app.route('/uploadMD/<user_ID>', methods=["POST"])
def uploadMD(user_ID):
	if request.method == "POST":
		user=User.query.filter_by(user_id=user_ID).first()
		if user:
			data_entries= request.json
			for data_entry in data_entries:
				print(data_entry)			
				md = MobileData()	
				md.md_user_id = user.user_id
				md.md_creation_time = datetime.datetime.strptime(data_entry.get('creation_time'), '%Y-%m-%d %H:%M:%S')
				md.whatsappBytes =data_entry.get('whatsappBytes')
				md.totalMB=data_entry.get('totalMB')
				md.no_whatsappBytes=data_entry.get('no_whatsappBytes')
				md.latitude=data_entry.get('latitude')
				md.longitude=data_entry.get('longitude')
				md.md_country = data_entry.get('country')
				md.md_roaming = data_entry.get('roaming')
				db.session.add(md)
				db.session.commit()
			response = jsonify(message="the mobile data record was added successfully")
			response.status_code=200
			return response
		else:
			response=jsonify(error='user not registered', message="The provided phone number is not registed in the databse")
			response.status_code=401
			return response
	else:
		return """<html><body>
		Something went horribly wrong
		</body></html>"""


@app.route('/getContracts/<user_ID>', methods=['GET', 'POST'])
def getContracts(user_ID):
	if request.method == "POST":
		user=User.query.filter_by(user_id=user_ID).first()
		if user:
			
			contractsDictArray = getContractsDict(user_ID)

			contractsJSON =json.dumps(contractsDictArray)
			print(contractsJSON)
			return jsonify(message="contracts", contracts =  contractsJSON)
	if request.method == "GET":
		contractsDictArray = getContractsDict("1")	
		contractsJSON =json.dumps(contractsDictArray)
		print(contractsJSON)
		return jsonify(message="contracts", contracts =  contractsJSON)


@app.route('/getUsage/<user_ID>', methods=['POST'])
def getUsage(user_ID):
	if request.method == "POST":
		user=User.query.filter_by(user_id=user_ID).first()
		if user:
			
			usage= {}
			usage["Number of outgoing calls to swiss landlines"] = callsFixedCH(user_ID).get('number')
			usage["Calling time of outgoing calls to swiss landlines"] = callsFixedCH(user_ID).get('duration')
			usage["Number of outgoing calls to swiss cellphones"] = CallsMobileCH(user_ID).get('number')
			usage["Calling time of outgoing calls to swiss cellphones"] = CallsMobileCH(user_ID).get('duration')
			usage["SMS sent within Switzerland"] = SMS_toCH(user_ID)
			usage["Internet data in Switzerland"] = dataCH(user_ID)  + " MBytes"
			usage["SMS to abroad"] = SMS_toABROAD(user_ID)
			usage["#1 foreign country called"]  = callsToAbroadLandX(user_ID, 0).get('country')
			usage["Number of outgoing calls to foreign country #1"]  = callsToAbroadLandX(user_ID, 0).get('number')
			usage["Calling time of outgoing calls to foreign country #1"]  = callsToAbroadLandX(user_ID, 0).get('duration')
			usage["#2 foreign country called"]  = callsToAbroadLandX(user_ID, 1).get('country')
			usage["Number of outgoing calls to foreign country #2"]  = callsToAbroadLandX(user_ID, 1).get('number')
			usage["Calling time of outgoing calls to foreign country #2"]  = callsToAbroadLandX(user_ID, 1).get('duration')
			usage["#2 foreign country called"]  = callsToAbroadLandX(user_ID, 2).get('country')
			usage["Number of outgoing calls to foreign country #3"]  = callsToAbroadLandX(user_ID, 2).get('number')
			usage["Calling time of outgoing calls to foreign country #3"]  = callsToAbroadLandX(user_ID, 2).get('duration')

			usageJSON =json.dumps(usage)
			return jsonify(message="usage", usage = usageJSON)

@app.route('/uploadCountryISOLog/<user_ID>', methods=['POST'])
def uploadCountryISOLog(user_ID):
	if request.method == "POST":
		user=User.query.filter_by(user_id=user_ID).first()
		if user:
			data_entries= request.json
			for data_entry in data_entries:
				print(data_entry)			
				cISO = CountryISOLog()	
				cISO.cISO_user_id = user.user_id
				cISO.cISO_creation_time = datetime.datetime.strptime(data_entry.get('iso_entry_creation_time'), '%Y-%m-%d %H:%M:%S')
				gs = goslate.Goslate()
				cISO.cISO_countryISO =gs.translate(data_entry.get('countryISO'), 'de')
				db.session.add(cISO)
				db.session.commit()
			response = jsonify(message="the countryISOLog was added successfully")
			response.status_code=200
			return response
			
		else:
			response=jsonify(error='user not registered', message="The provided phone number is not registed in the databse")
			response.status_code=401
			return response
	else:
		return """<html><body>
		Something went horribly wrong
		</body></html>"""
	


if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)
