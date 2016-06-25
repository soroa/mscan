# -*- coding: utf-8 -*-

import re
import operator
import resources
import  datetime
from sqlalchemy import and_
from models import *
import goslate

def getUserAgeField(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		age = int(user.age)
		print("age is  " +str(age))
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


def getDaysSinceSignUp(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		registration = user.registration_datetime
		now = datetime.datetime.now()
		timeSinceSignup = int((now - registration).days)
		if timeSinceSignup<30:
			return timeSinceSignup
		else:
			return 30


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
def callsFixedCH(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter=0; 
		duration = 0;  
		calls = getLastXDaysCalls(user_ID, getDaysSinceSignUp(user_ID))
		for c in calls: 
			print ("Number is: "+ c.call_number)
			if isSwissFixedNumber(c.call_number) and c.user_location=="Schweiz" and int(c.duration)>0 and c.call_type=="outgoing":
				
				counter +=1
				print("*********************************************")
				print ("Number is fix swiss: "+ c.call_number)
				print ("Duration of call is "+ str(c.duration))
				print ("Total Duration  is "+ str(duration))
				
				duration +=int(c.duration); 
				
				print ("Total Duration after sum  is "+ str(duration))
				print("*********************************************")
				
		return {'number': counter, 'duration': str(int(duration/60))}


#tested: ok 
def CallsMobileCH(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter=0; 
		duration = 0; 
		calls = getLastXDaysCalls(user_ID, getDaysSinceSignUp(user_ID))
		for c in calls: 
			if isSwissMobileNumber(c.call_number) and c.user_location=="Schweiz" and int(c.duration)>0 and c.call_type=="outgoing":
				counter +=1
				# print("*********************************************")
				# print ("Number is mob swiss: "+ c.call_number)
				# print ("Duration of call is "+ str(c.duration))
				# print ("Total Duration  is "+ str(duration))
				duration +=int(c.duration); 
				# print ("Total Duration after sum  is "+ str(duration))
				# print("*********************************************")
		return {'number': counter, 'duration': str(int(duration/60))}

def totalCallsMinutesCH(user_ID):
	return str(CallsMobileCH(user_ID).get("duration") + callsFixedCH(user_ID).get("duration"))


def totalCallsNumberCH(user_ID):
	return str(CallsMobileCH(user_ID).get("number") + callsFixedCH(user_ID).get("number"))

# TODO 3 most frequent numbers

def get3MostFrequentlyCalledNumbers(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter=0; 
		duration = 0; 
		calls = getLastXDaysCalls(user_ID, getDaysSinceSignUp(user_ID))
		frequent_numbers = {}
		for c in calls: 
			if c.call_type=="outgoing":
				if c.call_number not in frequent_numbers:
					frequent_numbers[c.call_number] = 1
				else:
					frequent_numbers[c.call_number] = frequent_numbers.get(c.call_number) + 1
		
		top3 = ["", "", ""]
		for i in range(0, 3): 
			if len(frequent_numbers)==0:
				break
			current_first = max(frequent_numbers, key=frequent_numbers.get)		
			top3[i] = current_first
			frequent_numbers.pop(current_first, None)

		return {'number1': top3[0], 'number2': top3[1], 'number3':top3[2]}


def getTrafficPercentageTop3Numbers(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter=0; 
		calls = getLastXDaysCalls(user_ID, getDaysSinceSignUp(user_ID))
		n1 = get3MostFrequentlyCalledNumbers(user_ID).get('number1')
		n2 = get3MostFrequentlyCalledNumbers(user_ID).get('number2')
		n3 = get3MostFrequentlyCalledNumbers(user_ID).get('number3')
		out_calls  = []
		for c in calls: 
			if c.call_type=="outgoing":
				out_calls.append(c)
				if c.call_number==n1 or c.call_number==n2 or c.call_number==n3:
					counter +=1
		if len(out_calls)>0:
			p = int((float(counter) / float(len(out_calls)))*100)
		else:
			return 0
		return p


def SMS_toCH(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter =0; 
		sms =getLastXDaysSMS(user_ID,getDaysSinceSignUp(user_ID))
		for s in sms: 
			if isSwissMobileNumber(s.sms_number) and  s.sms_type =="SENT":
				counter +=1
		return str(counter)

def dataCH(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter =0; 
		# daysback = datetime.timedelta(days=getDaysSinceSignUp(user_ID))
		daysback = datetime.timedelta(days=30)
		since = datetime.datetime.now() - daysback
		mds = MobileData.query.filter(and_(MobileData.md_creation_time > since, MobileData.md_user_id==user_ID, MobileData.md_roaming==False ) ).all()

		for m in mds: 
			counter +=int(m.totalMB)

		return str(long(counter/1000000))


# .......................................
## from Switzerland to abroad
# .......................................


def SMS_toABROAD(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter =0; 
		sms =getLastXDaysSMS(user_ID,getDaysSinceSignUp(user_ID))
		for s in sms: 
			if isForeignNumber(s.sms_number) and s.sms_type =="SENT":
				print("Number is " + s.sms_number)
				counter +=1
		return str(counter)


#tested, OK!
def callsToAbroadLandX(user_ID, x):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter=0
		duration = 0
		calls = getLastXDaysCalls(user_ID, getDaysSinceSignUp(user_ID))
		callsToAbroad = []
		for c in calls: 
			if isForeignNumber(c.call_number) and c.user_location=="Schweiz" and c.call_type=="outgoing"and c.duration>0:
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
	return {'number': str(int(counter/2)), 'duration': str(int(duration/120)), 'country': xMostfrequentCountry}



def callsToAbroadFromAbroadLandX(user_ID, x):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter=0
		duration = 0
		calls = getLastXDaysCalls(user_ID, getDaysSinceSignUp(user_ID))
		callsToAbroad = []
		for c in calls: 
			if isForeignNumber(c.call_number) and  (not isNumberFromCountry(c.call_number, getMostVisitedForeignCountry(user_ID))) and c.call_type=="outgoing"and c.duration>0:
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
	return {'number': str(int(counter)), 'duration': str(int(duration/60)), 'country': xMostfrequentCountry}

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
		daysback = datetime.timedelta(days=getDaysSinceSignUp(user_ID))
		since = datetime.datetime.now() - daysback
		mds = MobileData.query.filter(and_(MobileData.md_creation_time > since, MobileData.md_user_id==user_ID, MobileData.md_roaming==True ) ).all()
		for m in mds: 
			counter +=int(m.totalMB)
		return str(int(counter/1000000))



def getMostVisitedForeignCountry(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		calls = getLastXDaysCalls(user_ID, getDaysSinceSignUp(user_ID))
		countries = []
		for c in calls:
			if(c.user_location!="Schweiz"):
				countries.append(c.user_location)
		if len(countries)>0:
			most_frequent_country = max(set(countries), key=countries.count)
			return most_frequent_country
		else:
			return ""


		
def incomingCallsAbroad(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter=0; 
		duration = 0; 
		calls = getLastXDaysCalls(user_ID, getDaysSinceSignUp(user_ID))
		for c in calls: 
			if c.user_location==getMostVisitedForeignCountry(user_ID) and int(c.duration)>0 and c.call_type=="incoming":
				counter +=1
				duration +=int(c.duration); 
		return {'number': str(counter), 'duration': str(int(duration/60))}

def getDaysInMostVisitedCountry(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		calls = getLastXDaysCalls(user_ID, getDaysSinceSignUp(user_ID))
		days= []
		for c in calls:
			if c.user_location==getMostVisitedForeignCountry(user_ID):
				if c.call_creation_time.date() not in days:
					days.append(c.call_creation_time.date())
		return len(days)


def callsToCHfromAbroad(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter=0; 
		duration = 0; 
		calls = getLastXDaysCalls(user_ID, getDaysSinceSignUp(user_ID))
		for c in calls: 
			if (isSwissMobileNumber(c.call_number) or isSwissFixedNumber(c.call_number)) and c.user_location==getMostVisitedForeignCountry(user_ID) and int(c.duration)>0 and c.call_type=="outgoing":
				counter +=1
				duration +=int(c.duration); 
		return {'number': str(counter), 'duration': str(int(duration/60))}

def callsWithinVisitedForeignCountry(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter=0; 
		duration = 0; 
		calls = getLastXDaysCalls(user_ID, getDaysSinceSignUp(user_ID))
		for c in calls: 
			if isNumberFromCountry(c.call_number,getMostVisitedForeignCountry) and c.user_location==getMostVisitedForeignCountry(user_ID) and int(c.duration)>0 and c.call_type=="outgoing":
				counter +=1
				duration +=int(c.duration); 
		return {'number': str(counter), 'duration': str(int(duration/60))}

def isNumberFromCountry(number,country):
	prefix_3digits = number[:4]
	prefix_2digits = number[:3]
	prefix_1digits = number[:2]
	countryName = resources.country_prefixes.get(prefix_3digits,  None)
	if(not countryName):
		countryName = resources.country_prefixes.get(prefix_2digits,  None)
		if(not countryName):
			countryName = resources.country_prefixes.get(prefix_1digits,  None)
			if(not countryName):
				return False
	if countryName == country:
		return True

def getSMSWhileRoaming(user_ID):
	user=User.query.filter_by(user_id=user_ID).first()
	if user:
		counter =0; 
		sms =getLastXDaysSMS(user_ID,getDaysSinceSignUp(user_ID))
		for s in sms: 
			a = s.sms_creation_time-  datetime.timedelta(hours=1)
			b = s.sms_creation_time+  datetime.timedelta(hours=1)
			hour = s.sms_creation_time.hour
			countriesISOLog = CountryISOLog.query.filter(and_(CountryISOLog.cISO_creation_time > a,CountryISOLog.cISO_creation_time < b, CountryISOLog.cISO_user_id==user_ID) ).all()
			for c in countriesISOLog:
				if c.cISO_creation_time.hour==hour and c.cISO_countryISO==getMostVisitedForeignCountry(user_ID):
					counter+=1
		return str(counter)



# Helper Functions


def isSwissMobileNumber(number):
	if (number[:3]=="075" ) or  (number[:3]=="076" ) or  (number[:3]=="077" ) or (number[:3]=="078" ) or (number[:3]=="079" ) or (number[:5]=="+4175") or (number[:5]=="+4176") or (number[:5]=="+4177") or (number[:5]=="+4178") or (number[:5]=="+4179"):
		
		return True
	else: 
		return False
	

def isForeignNumber(number): 
	if (number[:1]=="+"):
		if(number[:3]!="+41"):
			return True
		else:
			return False
	else:
		return False

def isSwissFixedNumber(number):
	return (not isForeignNumber(number)) and (not isSwissMobileNumber(number))





def locationIsCH(location):
	return location=="Schweiz" or location=="Switzerland" or location=="Suisse" or location=="Svizzera" or location=="Suíça" or location=="Suiza"


def getLastXDaysSMS(user_ID,x):
	daysback = datetime.timedelta(days=30)
	since = datetime.datetime.now() - daysback
	print("type of return value is "+ str(type(SMS.query.filter(and_(SMS.sms_creation_time > since, SMS.user_id==user_ID) ).all())))
	return SMS.query.filter(and_(SMS.sms_creation_time > since, SMS.user_id==user_ID) ).all()

def getLastXDaysCalls(user_ID, x):
	daysback = datetime.timedelta(days=30)
	since = datetime.datetime.now() - daysback
	return Call.query.filter(and_(Call.call_creation_time > since, Call.user_id==user_ID) ).all()





