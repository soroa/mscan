from mscan import app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///mscan.db'


#create the sqlalchemy object
db =SQLAlchemy(app)






class User(db.Model):
	__tablename__= "users"
	user_id=db.Column(db.Integer, primary_key=True)
	number=db.Column(db.String, nullable=False)
	registration_datetime = db.Column(db.DateTime, nullable=False)
	age =  db.Column(db.String, nullable=False)
	contract_current_price = db.Column(db.String, nullable=False)
	sdk = db.Column(db.Integer)
	manufacturer = db.Column(db.String)
	build_device = db.Column(db.String)
	build_model = db.Column(db.String)
	device_software_version = db.Column(db.Integer)
	devide_id = db.Column(db.String)
	phone_type = db.Column(db.Integer)
	network_operator_name = db.Column(db.String)
	network_roaming = db.Column(db.String)
	network_country_iso = db.Column(db.String)
	network_type = db.Column(db.Integer)
	sim_state = db.Column(db.Integer)
	sim_operator = db.Column(db.String)
	sim_operator_name = db.Column(db.String)
	sim_serial_number = db.Column(db.String)
	subscriber_id = db.Column(db.String)
	calls_log = db.relationship('Call', backref='c_user_id',
                                lazy='dynamic')
	mobile_data_log = db.relationship('Call', backref='md_user_id',
                                lazy='dynamic')
	sms = db.relationship('Call', backref='sms_user_id',
                                lazy='dynamic')
	#todo anything missing?


class Call(db.Model):
	__tablename__= "calls"
	call_id=db.Column(db.Integer, primary_key=True)
	call_creation_time = db.Column(db.DateTime, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	call_number = db.Column(db.String, nullable=False)
	duration = db.Column(db.Integer, nullable=False)
	contact_name = db.Column(db.String)
	call_type=db.Column(db.String, nullable=False)
	other_number_location =db.Column(db.String, nullable=False)#other number
	user_location =db.Column(db.String, nullable=False)#user location



class MobileData(db.Model):
	__tablename__= "mobiledata"
	md_id=db.Column(db.Integer, primary_key=True)
	md_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	md_creation_time = db.Column(db.DateTime, nullable=False)
	whatsappBytes =db.Column(db.Integer, nullable=False)
	totalMB=db.Column(db.Integer, nullable=False)
	no_whatsappBytes=db.Column(db.Integer, nullable=False)
	latitude=db.Column(db.Float)
	longitude=db.Column(db.Float)
	md_country=db.Column(db.String)
	md_roaming=db.Column(db.Boolean)




class SMS(db.Model):
	__tablename__= "sms"
	sms_id=db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	sms_creation_time = db.Column(db.DateTime, nullable=False)
	sms_type = db.Column(db.String, nullable=False)
	sms_number = db.Column(db.String, nullable=False)


class CountryISOLog(db.Model):
	__tablename__= "countryISOLog"
	cISO_id=db.Column(db.Integer, primary_key=True)
	cISO_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	cISO_creation_time = db.Column(db.DateTime, nullable=False)
	cISO_countryISO = db.Column(db.String)
	





