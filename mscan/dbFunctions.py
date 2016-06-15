# -*- coding: utf-8 -*-

import re
import operator
import resources
import  datetime
from models import *

def getUserAgeField(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		age = user.age
		if age<18:
			return 15
		elif age<26:
			return 25
		elif age<27:
			return 26
		elif age<30:
			return 29
		elif  age>=30 and age<65:
			return 30
		elif age>=65:
			return 65


def getUserCurrentContractPrice(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		return user.contract_current_price

def getUserOperator(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		return (user.sim_operator_name).title()#title() makes the first letter of every word uppercase 

# .......................................
##Everthing within Switzerland
# .......................................
#tested: OK 
def callsFixedCH(user_ID,x):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter=0; 
		duration = 0;  
		calls = getLastXDaysCalls(user_ID, x)
		for c in calls: 
			if isSwissFixedNumber(c.call_number) and c.user_location=="CH" and int(c.duration)>0 and c.call_type=="outgoing":
				counter +=1
				duration +=int(c.duration); 
		return {'number': counter, 'duration': duration}


#tested: ok 
def CallsMobileCH(user_ID,x):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter=0; 
		duration = 0; 
		calls = getLastXDaysCalls(user_ID, x)
		for c in calls: 
			if isSwissMobileNumber(c.call_number) and c.user_location=="CH" and int(c.duration)>0 and c.call_type=="outgoing":
				counter +=1
				duration +=int(c.duration); 
		return {'number': counter, 'duration': duration}

def totalCallsMinutesCH(user_ID):
	return str(nationalCallsMobile(user_ID).get("duration") + nationalCallsFixed(user_ID).get("duration"))


def totalCallsNumberCH(user_ID):
	return str(nationalCallsMobile(user_ID).get("number") + nationalCallsFixed(user_ID).get("number"))

# TODO 3 most frequent numbers


def SMS_toCH(user_ID,x):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter =0; 
		sms =getLastXDaysSMS(user_ID,x)
		for s in sms: 
			if isSwissMobileNumber(s.sms_number):
				counter +=1
		return str(counter)

def dataCH(user_ID, x):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter =0; 
		daysback = datetime.timedelta(days=x)
		since = datetime.datetime.now() - daysback
		mds = MobileData.query.filter(and_(MobileData.md_creation_time > since, MobileData.md_user_id==user_ID, MobileData.md_roaming==False ) ).all()

		for m in mds: 
			counter +=int(m.totalMB)

		return str(int(counter/1000000))





# .......................................
## from Switzerland to abroad
# .......................................


def SMS_toABROAD(user_ID, x):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter =0; 
		sms =getLastXDaysSMS(user_ID,x)
		for s in sms: 
			if isForeignNumber(s.sms_number):
				counter +=1
		return str(counter)


#tested, OK!
def callsToAbroadLandX(user_ID, x,daysBack):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter=0
		duration = 0
		calls = getLastXDaysCalls(user_ID, daysBack)
		callsToAbroad = []
		for c in calls: 
			if isForeignNumber(c.call_number) and c.user_location=="CH" and c.call_type=="outgoing"and c.duration>0:
				callsToAbroad.append(c)
		if len(callsToAbroad)>0:
			xMostfrequentCountry  = getXMostFrequentForeignCountryCalled(x, callsToAbroad)
		else:	
			xMostfrequentCountry = ""
		if xMostfrequentCountry =="":
			return {'number': "0", 'duration': "0", 'country': xMostfrequentCountry}
		prefix = None
		for pref in resources.country_prefixes:
			if resources.country_prefixes.get(pref) == xMostfrequentCountry: 
				prefix = pref 
				continue
		for c in callsToAbroad: 
			if c.call_number[:len(prefix)] == prefix:
				counter+= 1
				duration += int(c.duration)
	return {'number': str(counter), 'duration': str(duration), 'country': xMostfrequentCountry}


#TODO return empty strings in case there's less than 5 countires

def getXMostFrequentForeignCountryCalled(x, callstoAbroad):
	frequency_chart = {}
	for c in callstoAbroad:
		prefix_3digits = c.call_number[:4]
		prefix_2digits = c.call_number[:3]
		prefix_1digits = c.call_number[:2]
		countryName = resources.country_prefixes.get(prefix_3digits,  None)
		if(not countryName):
			countryName = resources.country_prefixes.get(prefix_2digits,  None)
			if(not countryName):
				countryName = resources.country_prefixes.get(prefix_1digits,  None)
				if(not countryName):
					continue
		if(frequency_chart.get(countryName, None)):
			frequency_chart[countryName] = frequency_chart.get(countryName, None) + 1
		else:
			frequency_chart[countryName] = 1
	frequent_countries_top5 = []
	for i in range(0, 5):
		if len(frequency_chart)==0:
			frequent_countries_top5.append("")
			break
		current_first = max(frequency_chart, key=frequency_chart.get)		
		frequent_countries_top5.append(current_first)
		frequency_chart.pop(current_first, None) #always erase the first one because fi there's two with the same count, the library will only take one of them and ignore the other, this it will take the second one in the next round
	return frequent_countries_top5[x]
	

#ROAMING
#TODO test 
def dataRoaming(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter =0; 
		daysback = datetime.timedelta(days=30)
		since = datetime.datetime.now() - daysback
		mds = MobileData.query.filter(and_(MobileData.md_creation_time > since, MobileData.md_user_id==user_ID, MobileData.md_roaming==True ) ).all()
		countries = []
		for m in mds: 
			countries.append(md_country)
		country_with_most_roaming = max(set(countries), key=countries.count)
		for m in mds: 
			counter +=int(m.totalMB)

		return str(int(counter/1000000))




def SMS_fromABROADtoCH(user_ID):
	return

def SMS_fromABROAD(user_ID):
	return

# Helper Functions


def isSwissMobileNumber(number):
	if (number[:3]=="075" ) or  (number[:3]=="076" ) or  (number[:3]=="077" ) or (number[:3]=="078" ) or (number[:3]=="079" ) or (number[:5]=="+4175") or (number[:5]=="+4176") or (number[:5]=="+4177") or (number[:5]=="+4178") or (number[:5]=="+4179"):
		return True
	else: 
		return False
	return True

def isForeignNumber(number): 
	if (number[:1]=="+"):
		if(number[:3]!="+41"):
			return True
		else:
			return False
	else:
		return False

def isSwissFixedNumber(number):
	return not isForeignNumber(number) and not isSwissMobileNumber(number)


def locationIsCH(location):
	return location=="Schweiz" or location=="Switzerland" or location=="Suisse" or location=="Svizzera" or location=="Suíça" or location=="Suiza"


def getLastXDaysSMS(user_ID,x):
	daysback = datetime.timedelta(days=x)
	since = datetime.datetime.now() - daysback
	return SMS.query.filter(and_(SMS.sms_creation_time > since, SMS.user_id==user_ID) ).all

def getLastXDaysCalls(user_ID, x):
	daysback = datetime.timedelta(days=x)
	since = datetime.datetime.now() - daysback
	return Call.query.filter(and_(Call.call_creation_time > since, Call.user_id==user_ID) ).all()





