from mscan import app
from flask.ext.sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///mscan.db'

#create the sqlalchemy object
db =SQLAlchemy(app)




class Contract(db.Model):
	__tablename__= "contracts"

	contract_id=db.Column(db.Integer, primary_key=True)
	contract_name =db.Column(db.String, nullable=False)
	monthly_price =db.Column(db.Integer, nullable=False)
	operator =db.Column(db.String, nullable=False)
	age_limit =db.Column(db.Integer)
	duration= db.Column(db.Integer, nullable=False)

	#calls
	# --national
	limit_same_operator_calls_nat=db.Column(db.Integer, nullable=False) ##in minutes
	limit_other_operator_calls_nat=db.Column(db.Integer, nullable=False) ##in minutes
	limit_fixed_networks_calls_nat=db.Column(db.Integer) 
	limit_national_calls= db.Column(db.Integer)
	# --international
	limit_outgoing_international_calls_fromCH=db.Column(db.Integer, nullable=False)
	limit_calls_at_abroad = db.Column(db.Integer, nullable=False) #TODO does it include incoming calls as well? 
	#standard rates
	rate_call_in_ch = db.Column(db.Float, nullable=False)
	rate_chargable_call_duration = db.Column(db.Integer, nullable=False)
	rate_calls_to_abroad = db.Column(db.Float, nullable=False)
	rate_incoming_call_at_abroad = db.Column(db.Float, nullable=False)
	rate_call_from_abroad_to_abroad = db.Column(db.Float, nullable=False)
	rate_call_from_abroad_to_CH = db.Column(db.Float, nullable=False)
	#--------------------------------------------------------------------------
	#--------------------------------------------------------------------------

	#internet
	#--national
	unlimited_whatsapp = db.Column(db.Boolean, nullable=False)
	limit_3g =db.Column(db.Integer, nullable=False)
	limit_4g =db.Column(db.Integer, nullable=False)
	#internet
	#--international
	limit_roaming =db.Column(db.Integer, nullable=False)
	#starndard rates
	roaming_rate = db.Column(db.Float, nullable=False)
	surfing_daily_cost_unlimited = db.Column(db.Float, nullable=False)
	#--------------------------------------------------------------------------
	#--------------------------------------------------------------------------

	#sms
	#--national
	limit_sms_CH =db.Column(db.Integer, nullable=False)
	#--international
	limit_sms_at_abroad = db.Column(db.Integer, nullable=False)
	#standard rates
	sms_at_abroad_stdRate = db.Column(db.Float, nullable=False)
	sms_CH_stdRate = db.Column(db.Float, nullable=False)

	#def __init__(self, params):
		#todo


class User(db.Model):
	__tablename__= "users"
	user_id=db.Column(db.Integer, primary_key=True)
	number=db.Column(db.String, nullable=False)
	birthdate =  db.Column(db.DateTime, nullable=False)
	contract =db.Column(db.Integer)
	operator =db.Column(db.String, nullable=False)
	contract_start_date = db.Column(db.DateTime, nullable=False)
	contract_end_date = db.Column(db.DateTime, nullable=False)
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
	# from_abroad=db.Column(db.Boolean, nullable=False)
	# to_abroad= db.Column(db.Boolean, nullable=False)
	# to_CH_from_abroad=db.Column(db.Boolean, nullable=False)
	from_country =db.Column(db.String, nullable=False)
	to_country =db.Column(db.String, nullable=False)



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




class SMS(db.Model):
	__tablename__= "sms"
	sms_id=db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	sms_creation_time = db.Column(db.DateTime, nullable=False)
	sms_type = db.Column(db.String, nullable=False)
	sms_number = db.Column(db.String, nullable=False)
	



