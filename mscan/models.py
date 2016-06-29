from mscan import app
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry, Geography
from geoalchemy2.shape import to_shape
from sqlalchemy import func, cast
from utils import distance

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
	


##=====================================================
##========= Marc's stuff =======================


class MLSCellRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    radio = db.Column(db.String(length=4))
    mcc = db.Column(db.SmallInteger)
    net = db.Column(db.SmallInteger)
    area = db.Column(db.Integer)
    cell = db.Column(db.BigInteger)
    unit = db.Column(db.SmallInteger)
    position = db.Column(Geometry(geometry_type='POINT', srid=4326, spatial_index=True))
    range = db.Column(db.Integer)
    samples = db.Column(db.Integer)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __init__(self, data=None):
        def lame_int(obj):
            try:
                return int(obj)
            except (ValueError, TypeError):
                return None

        def lame_float(obj):
            try:
                return float(obj)
            except (ValueError, TypeError):
                return None

        if data:
            self.radio = lame_int(data.get('radio'))
            self.mcc = lame_int(data.get('mcc'))
            self.net = lame_int(data.get('net'))
            self.area = lame_int(data.get('area'))
            self.cell = lame_int(data.get('cell'))
            self.unit = lame_int(data.get('unit'))
            self.position = func.ST_SetSRID(
                func.ST_Point(lame_float(data.get('lon')), lame_float(data.get('lat'))), 4326
            )
            self.range = lame_int(data.get('range'))
            self.samples = lame_int(data.get('samples'))
            self.created = datetime.fromtimestamp(int(data.get('created', 0)))
            self.updated = datetime.fromtimestamp(int(data.get('updated', 0)))

    def to_json(self):
        return {
            'id': self.id,
            'radio': self.radio,
            'mcc': self.mcc,
            'net': self.net,
            'area': self.area,
            'cell': self.cell,
            'unit': self.unit,
            'position': {'lng': to_shape(self.position).x, 'lat': to_shape(self.position).y},
            'range': self.range,
            'samples': self.samples,
            'created': self.created,
            'updated': self.updated
        }
	
class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(length=36), unique=True, index=True)

    def __init__(self, uuid):
        self.uuid = uuid

    def to_json(self):
        last_information = self.phone_information.order_by(PhoneInformation.creation_time.desc()).first()
        last_measurement = self.measurements.order_by(Measurement.creation_time.desc()).first()
        return {
            'uuid': self.uuid,
            'total_information': self.phone_information.count(),
            'last_information': last_information.to_json() if last_information else None,
            'total_measurements': self.measurements.count(),
            'last_measurement': last_measurement.to_json() if last_measurement else None,
        }


class PhoneInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_id = db.Column(db.Integer, db.ForeignKey(Phone.id))
    phone = db.relationship(Phone, backref=db.backref('phone_information', lazy='dynamic'))
    creation_time = db.Column(db.DateTime, default=datetime.now)
    android_version = db.Column(db.Integer)
    build_manufacturer = db.Column(db.String(length=20))
    build_device = db.Column(db.String(length=20))
    build_model = db.Column(db.String(length=20))
    device_software_version = db.Column(db.String(length=20))
    device_id = db.Column(db.String(length=20))
    phone_type = db.Column(db.Integer)
    network_operator = db.Column(db.Integer)
    network_operator_name = db.Column(db.String(length=20))
    network_roaming = db.Column(db.Boolean)
    network_country_iso = db.Column(db.String(length=2))
    network_type = db.Column(db.Integer)
    sim_state = db.Column(db.Integer)
    sim_operator = db.Column(db.Integer)
    sim_operator_name = db.Column(db.String(length=20))
    sim_country_iso = db.Column(db.String(length=2))
    sim_serial_number = db.Column(db.String(length=20))
    subscriber_id = db.Column(db.String(length=20))

    def __init__(self):
        pass

    def to_json(self, include_phone=False):
        j = {
            'creation_time': self.creation_time,
            'android_version': self.android_version,
            'build_manufacturer': self.build_manufacturer,
            'build_device': self.build_device,
            'build_model': self.build_model,
            'device_software_version': self.device_software_version,
            'device_id': self.device_id,
            'phone_type': self.phone_type,
            'network_operator': self.network_operator,
            'network_operator_name': self.network_operator_name,
            'network_roaming': self.network_roaming,
            'network_country_iso': self.network_country_iso,
            'network_type': self.network_type,
            'sim_state': self.sim_state,
            'sim_operator': self.sim_operator,
            'sim_operator_name': self.sim_operator_name,
            'sim_country_iso': self.sim_country_iso,
            'sim_serial_number': self.sim_serial_number,
            'subscriber_id': self.subscriber_id,
        }
        if include_phone:
            j['phone'] = self.phone.to_json() if self.phone else None
        return j


class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_id = db.Column(db.Integer, db.ForeignKey(Phone.id))
    phone = db.relationship(Phone, backref=db.backref('measurements', lazy='dynamic'))
    creation_time = db.Column(db.DateTime, default=datetime.now)
    cid = db.Column(db.Integer)
    lac = db.Column(db.Integer)
    psc = db.Column(db.Integer)
    base_station_id = db.Column(db.Integer)
    base_station_lat = db.Column(db.Integer)
    base_station_longitude = db.Column(db.Integer)
    system_id = db.Column(db.Integer)
    network_id = db.Column(db.Integer)
    gsm = db.Column(db.SmallInteger)
    lte = db.Column(db.SmallInteger)
    latitude = db.Column(db.Float, index=True)
    longitude = db.Column(db.Float, index=True)
    accuracy = db.Column(db.Float)
    altitude = db.Column(db.Float)
    speed = db.Column(db.Float)

    def __init__(self, device):
        self.phone = device

    def to_json(self, include_phone=False):
        j = {
            'creation_time': self.creation_time,
            'cid': self.cid,
            'lac': self.lac,
            'psc': self.psc,
            'base_station_id': self.base_station_id,
            'base_station_lat': self.base_station_lat,
            'base_station_lon': self.base_station_longitude,
            'system_id': self.system_id,
            'network_id': self.network_id,
            'gsm': self.gsm,
            'lte': self.lte,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'accuracy': self.accuracy,
            'altitude': self.altitude,
            'speed': self.speed,
        }
        if include_phone:
            j['phone'] = self.phone.to_json() if self.phone else None,
        return j







