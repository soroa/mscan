import requests
from bs4 import BeautifulSoup
import urllib
from operator import itemgetter
from DKPostRequestBuilder import* 

def getContractsDict(user_ID): 
	s = requests.Session()

	r= requests.get("http://www.dschungelkompass.ch/mobile/welcomeErweitertesprofil.xhtml")
	# print(r.headers)
	soup = BeautifulSoup(r.content)
	soupH = (r.headers)
	sessionID = soupH["Set-Cookie"]
	sessionID = sessionID.split(';')[0]
	print(sessionID)
	# id="javax.faces.ViewState"
	viewState = soup.find("input", {"id": "javax.faces.ViewState"})
	values = viewState['value'].split(":")
	value1  = values[0]
	value2 = values[1]

	url ="http://www.dschungelkompass.ch/mobile/welcomeSchnellprofil.xhtml"

	url2 ="http://www.dschungelkompass.ch/mobile/welcomeErweitertesprofil.xhtml"

	data = {
	"inputfelderform":"inputfelderform",
	"inputfelderform:inputFelder:anzMinEingabe":totalCallsMinutesCH(user_ID), #Minuten telefonieren CH pro Monat
	"inputfelderform:inputFelder:anzAnrufeEingabe":totalCallsNumberCH(user_ID), # Anzalh Anrufe pro Monat
	"inputfelderform:inputFelder:anteil3NrEingabe":"0", #Anteil auf die gleiche 3 nummer
	"inputfelderform:inputFelder:alterAuswahl":getUserAgeField(user_ID), #Alter: kann 15 (unter 18), 25 (unter 26), 26 (unter 27), 29 (unter 30), 65 (65 oder aelter), 30 (zwischen 30 und 65)
	"inputfelderform:inputFelder:j_idt127":getUserCurrentContractPrice(user_ID),  #wie viel ich jetzt pro Monat bezahle
	"inputfelderform:inputFelder:providerFilterSB":getUserOperator(user_ID), #jetziger Anbieter
	"inputfelderform:inputFelder:j_idt115_collapsed":"false",
	"inputfelderform:inputFelder:j_idt137":"on",
	"inputfelderform:inputFelder:aufFestnetzSwisscom":"0", #Verteilung Fest: Swisscom Festnetz
	"inputfelderform:inputFelder:aufFestnetzUPC":"0",#Verteilung Fest: UPC
	"inputfelderform:inputFelder:j_idt149_collapsed":"false",
	"inputfelderform:inputFelder:aufSwisscom":"40",#Verteilung: Swisscom
	"inputfelderform:inputFelder:aufOrange":"30",#Verteilung: Orange
	"inputfelderform:inputFelder:aufSunrise":"30",#Verteilung: Sunrise
	"inputfelderform:inputFelder:aufMbudget":"0",#Verteilung: Mbdugen
	"inputfelderform:inputFelder:aufCoopMobile":"0",#Verteilung: Coop
	"inputfelderform:inputFelder:j_idt160_collapsed":"false",
	"inputfelderform:inputFelder:aufAldi":"0",#Verteilung: 
	"inputfelderform:inputFelder:aufOk":"0",#Verteilung: 
	"inputfelderform:inputFelder:aufLebara":"0",#Verteilung: 
	"inputfelderform:inputFelder:aufTalkTalk":"0",#Verteilung: 
	"inputfelderform:inputFelder:aufYallo":"0",#Verteilung: 
	"inputfelderform:inputFelder:aufLyca":"0",#Verteilung: 
	"inputfelderform:inputFelder:aufOrtel":"0",#Verteilung: 
	"inputfelderform:inputFelder:aufMobileUPC":"0",#Verteilung: 
	"inputfelderform:inputFelder:aufAndere":"0",#Verteilung: 
	"inputfelderform:inputFelder:j_idt182_collapsed":"true",
	"inputfelderform:inputFelder:anzSMSEingabe":SMS_toCH(user_ID),#Sms pro Monat CH
	"inputfelderform:inputFelder:anzTageSMS":str(getDaysSinceSignUp(user_ID)), #Innerhalb von x Tagen
	"inputfelderform:inputFelder:j_idt227_collapsed":"false",
	"inputfelderform:inputFelder:datenmengeMBEingabe":dataCH(user_ID),#Datenmenge pro Monat
	"inputfelderform:inputFelder:intVerwendungAnzTageEingabe":str(getDaysSinceSignUp(user_ID)), #Innerhalb von x Tagen
	"inputfelderform:inputFelder:speedAuswahl":"1.0", #Geschwindigkeit Minimum
	"inputfelderform:inputFelder:j_idt238_collapsed":"false", #
	"inputfelderform:inputFelder:SmsAusland":SMS_toABROAD(user_ID), #SMS ins Ausland
	"inputfelderform:inputFelder:j_idt270_input":callsToAbroadLandX(user_ID, 0).get('country'), #Anrufe ins Ausland: Land1
	"inputfelderform:inputFelder:Land1FixMin":callsToAbroadLandX(user_ID, 0).get('duration'), #Festnetz minuten anrufe ins ausland
	"inputfelderform:inputFelder:Land1FixAnzAnr":callsToAbroadLandX(user_ID, 0).get('number'), #Festnetz Anzahl Anrufe ins Ausland
	"inputfelderform:inputFelder:Land1MobMin":"12", #Mobilnetx Anzahl Minuten Anrufe
	"inputfelderform:inputFelder:Land1MobAnzAnr":"13", #Mobilnetz Anzah Anrufe
	"inputfelderform:inputFelder:j_idt267_collapsed":"false", 
	"inputfelderform:inputFelder:j_idt294_input":callsToAbroadLandX(user_ID, 1).get('country'), #Anrufe ins Auland: Land2
	"inputfelderform:inputFelder:Land2FixMin":"14", #same as above
	"inputfelderform:inputFelder:Land2FixAnzAnr":"15", 
	"inputfelderform:inputFelder:Land2MobMin":"16",
	"inputfelderform:inputFelder:Land2MobAnzAnr":"17",
	"inputfelderform:inputFelder:j_idt291_collapsed":"false",
	"inputfelderform:inputFelder:j_idt318_input":callsToAbroadLandX(user_ID, 2).get('country'),
	"inputfelderform:inputFelder:Land3FixMin":"18",
	"inputfelderform:inputFelder:Land3FixAnzAnr":"19",
	"inputfelderform:inputFelder:Land3MobMin":"20",
	"inputfelderform:inputFelder:Land3MobAnzAnr":"21",
	"inputfelderform:inputFelder:j_idt315_collapsed":"false",
	"inputfelderform:inputFelder:j_idt342_input":callsToAbroadLandX(user_ID, 3).get('country'),
	"inputfelderform:inputFelder:Land4FixMin":"22",
	"inputfelderform:inputFelder:Land4FixAnzAnr":"23",
	"inputfelderform:inputFelder:Land4MobMin":"24",
	"inputfelderform:inputFelder:Land4MobAnzAnr":"25",
	"inputfelderform:inputFelder:j_idt339_collapsed":"false",
	"inputfelderform:inputFelder:j_idt366_input":callsToAbroadLandX(user_ID, 4).get('country'),
	"inputfelderform:inputFelder:Land5FixMin":"26",
	"inputfelderform:inputFelder:Land5FixAnzAnr":"27",
	"inputfelderform:inputFelder:Land5MobMin":"28",
	"inputfelderform:inputFelder:Land5MobAnzAnr":"29",
	"inputfelderform:inputFelder:j_idt363_collapsed":"false",
	"inputfelderform:inputFelder:j_idt393_input":"Deutschland", #Roaming Land 1
	"inputfelderform:inputFelder:Roaming1AnzTage":"30", #Anzahl Tage romaing
	"inputfelderform:inputFelder:RoamingSMS":"31", #Sms IM Ausland
	"inputfelderform:inputFelder:RoamingDatenMB":"32", #MB Daten im Ausland
	"inputfelderform:inputFelder:RoamingIncomingMin":"33", #eingehnde Anrufe Minuten im Land1
	"inputfelderform:inputFelder:RoamingIncomingAnr":"34", # eingehnde Anrufe Anzahl im Land1
	"inputfelderform:inputFelder:j_idt407_collapsed":"false",
	"inputfelderform:inputFelder:RoamingToCHMin":"35", #Anfrufe MInuten in CH von Land1
	"inputfelderform:inputFelder:RoamingToCHAnr":"36", # Anzhal Anrufe in CH von Land1
	"inputfelderform:inputFelder:j_idt416_collapsed":"false",
	"inputfelderform:inputFelder:RoamingToLocalMin":"37", #Anrufe innerhalb Land1 Minuten
	"inputfelderform:inputFelder:RoamingToLocalAnr":"38", #Anrufe innerhalp Land1 Anzhal
	"inputfelderform:inputFelder:j_idt425_collapsed":"false",
	"inputfelderform:inputFelder:LandlisteDB_R_Land1":"Frankreich", # Land1: Anrufe von Land1 zu Land2 (!=CH)
	"inputfelderform:inputFelder:RoamingToLand1Min":"39",#Anzahl Minuten Anrufe von Land1 zu Land2
	"inputfelderform:inputFelder:RoamingToLand1Anr":"40",#Anzalh Anrufe von L1 zu L2
	"inputfelderform:inputFelder:j_idt434_collapsed":"false",
	"inputfelderform:inputFelder:LandlisteDB_R_Land2":"",
	"inputfelderform:inputFelder:RoamingToLand2Min":"0",
	"inputfelderform:inputFelder:RoamingToLand2Anr":"0",
	"inputfelderform:inputFelder:j_idt447_collapsed":"true",
	"inputfelderform:inputFelder:LandlisteDB_R_Land3":"",
	"inputfelderform:inputFelder:RoamingToLand3Min":"0",
	"inputfelderform:inputFelder:RoamingToLand3Anr":"0",
	"inputfelderform:inputFelder:j_idt460_collapsed":"true",
	"inputfelderform:inputFelder_activeIndex":"4",
	"inputfelderform:j_idt501":"",
	"javax.faces.ViewState":value1 + ":"+value2
	}

	data4 = {
	"inputfelderform":"inputfelderform",
	"inputfelderform:inputFelder:anzMinEingabe":totalCallsMinutesCH(user_ID), #Minuten telefonieren CH pro Monat
	"inputfelderform:inputFelder:anzAnrufeEingabe":totalCallsNumberCH(user_ID), # Anzalh Anrufe pro Monat
	"inputfelderform:inputFelder:anteil3NrEingabe":"3",
	"inputfelderform:inputFelder:alterAuswahl":getUserAgeField(user_ID), #Alter: kann 15 (unter 18), 25 (unter 26), 26 (unter 27), 29 (unter 30), 65 (65 oder aelter), 30 (zwischen 30 und 65)
	"inputfelderform:inputFelder:j_idt132":getUserCurrentContractPrice(user_ID),  #wie viel ich jetzt pro Monat bezahle
	"inputfelderform:inputFelder:providerFilterSB":getUserOperator(user_ID), #jetziger Anbieter
	"inputfelderform:inputFelder:j_idt120_collapsed":"false",
	"inputfelderform:inputFelder:j_idt142":"on",
	"inputfelderform:inputFelder:aufFestnetzSwisscom":"20",
	"inputfelderform:inputFelder:aufFestnetzUPC":"0",
	"inputfelderform:inputFelder:j_idt154_collapsed":"false",
	"inputfelderform:inputFelder:aufSwisscom":"40",#Verteilung: Swisscom
	"inputfelderform:inputFelder:aufOrange":"30",#Verteilung: Orange
	"inputfelderform:inputFelder:aufSunrise":"30",#Verteilung: Sunrise
	"inputfelderform:inputFelder:aufMbudget":"0",
	"inputfelderform:inputFelder:aufCoopMobile":"0",
	"inputfelderform:inputFelder:j_idt165_collapsed":"false",
	"inputfelderform:inputFelder:aufAldi":"0",
	"inputfelderform:inputFelder:aufOk":"0",
	"inputfelderform:inputFelder:aufLebara":"0",
	"inputfelderform:inputFelder:aufTalkTalk":"0",
	"inputfelderform:inputFelder:aufYallo":"0",
	"inputfelderform:inputFelder:aufLyca":"0",
	"inputfelderform:inputFelder:aufOrtel":"0",
	"inputfelderform:inputFelder:aufMobileUPC":"0",
	"inputfelderform:inputFelder:aufAndere":"0",
	"inputfelderform:inputFelder:j_idt187_collapsed":"true",
	"inputfelderform:inputFelder:anzSMSEingabe":SMS_toCH(user_ID),#Sms pro Monat CH
	"inputfelderform:inputFelder:anzTageSMS":str(getDaysSinceSignUp(user_ID)), #Innerhalb von x Tagen
	"inputfelderform:inputFelder:j_idt232_collapsed":"false",
	"inputfelderform:inputFelder:datenmengeMBEingabe":dataCH(user_ID),#Datenmenge pro Monat
	"inputfelderform:inputFelder:intVerwendungAnzTageEingabe":str(getDaysSinceSignUp(user_ID)), #Innerhalb von x Tagen
	"inputfelderform:inputFelder:speedAuswahl":"1.0",
	"inputfelderform:inputFelder:j_idt243_collapsed":"false",
	"inputfelderform:inputFelder:SmsAusland":SMS_toABROAD(user_ID), #SMS ins Ausland
	"inputfelderform:inputFelder:j_idt275_input":callsToAbroadLandX(user_ID, 0).get('country'), #Anrufe ins Ausland: Land1
	"inputfelderform:inputFelder:Land1FixMin":callsToAbroadLandX(user_ID, 0).get('duration'), #Festnetz minuten anrufe ins ausland
	"inputfelderform:inputFelder:Land1FixAnzAnr":callsToAbroadLandX(user_ID, 0).get('number'), #Festnetz Anzahl Anrufe ins Ausland
	"inputfelderform:inputFelder:Land1MobMin":"12",
	"inputfelderform:inputFelder:Land1MobAnzAnr":"12",
	"inputfelderform:inputFelder:j_idt272_collapsed":"false",
	"inputfelderform:inputFelder:j_idt299_input":callsToAbroadLandX(user_ID, 1).get('country'), #Anrufe ins Auland: Land2
	"inputfelderform:inputFelder:Land2FixMin":"12",
	"inputfelderform:inputFelder:Land2FixAnzAnr":"2",
	"inputfelderform:inputFelder:Land2MobMin":"12",
	"inputfelderform:inputFelder:Land2MobAnzAnr":"12",
	"inputfelderform:inputFelder:j_idt296_collapsed":"false",
	"inputfelderform:inputFelder:j_idt323_input":callsToAbroadLandX(user_ID, 2).get('country'),
	"inputfelderform:inputFelder:Land3FixMin":"12",
	"inputfelderform:inputFelder:Land3FixAnzAnr":"2",
	"inputfelderform:inputFelder:Land3MobMin":"12",
	"inputfelderform:inputFelder:Land3MobAnzAnr":"12",
	"inputfelderform:inputFelder:j_idt320_collapsed":"false",
	"inputfelderform:inputFelder:j_idt347_input":callsToAbroadLandX(user_ID, 3).get('country'),
	"inputfelderform:inputFelder:Land4FixMin":"12",
	"inputfelderform:inputFelder:Land4FixAnzAnr":"12",
	"inputfelderform:inputFelder:Land4MobMin":"12",
	"inputfelderform:inputFelder:Land4MobAnzAnr":"12",
	"inputfelderform:inputFelder:j_idt344_collapsed":"false",
	"inputfelderform:inputFelder:j_idt371_input":callsToAbroadLandX(user_ID, 4).get('country'),
	"inputfelderform:inputFelder:Land5FixMin":"12",
	"inputfelderform:inputFelder:Land5FixAnzAnr":"12",
	"inputfelderform:inputFelder:Land5MobMin":"21",
	"inputfelderform:inputFelder:Land5MobAnzAnr":"12",
	"inputfelderform:inputFelder:j_idt368_collapsed":"false",
	"inputfelderform:inputFelder:j_idt398_input":getMostVisitedForeignCountry(user_ID),
	"inputfelderform:inputFelder:Roaming1AnzTage":getDaysInMostVisitedCountry(user_ID),
	"inputfelderform:inputFelder:RoamingSMS":getSMSWhileRoaming(user_ID),
	"inputfelderform:inputFelder:RoamingDatenMB":dataRoaming(user_ID),
	"inputfelderform:inputFelder:RoamingIncomingMin":incomingCallsAbroad(user_ID).get('duration'),
	"inputfelderform:inputFelder:RoamingIncomingAnr":incomingCallsAbroad(user_ID).get('number'),,
	"inputfelderform:inputFelder:j_idt412_collapsed":"false",
	"inputfelderform:inputFelder:RoamingToCHMin":callsToCHfromAbroad(user_ID).get('duration'),
	"inputfelderform:inputFelder:RoamingToCHAnr":callsToCHfromAbroad(user_ID).get('number'),
	"inputfelderform:inputFelder:j_idt421_collapsed":"false",
	"inputfelderform:inputFelder:RoamingToLocalMin":callsWithinVisitedForeignCountry(user_ID).get('duration'),
	"inputfelderform:inputFelder:RoamingToLocalAnr":callsWithinVisitedForeignCountry(user_ID).get('number'),
	"inputfelderform:inputFelder:j_idt430_collapsed":"false",
	"inputfelderform:inputFelder:LandlisteDB_R_Land1":"",
	"inputfelderform:inputFelder:RoamingToLand1Min":"0",
	"inputfelderform:inputFelder:RoamingToLand1Anr":"0",
	"inputfelderform:inputFelder:j_idt439_collapsed":"false",
	"inputfelderform:inputFelder:LandlisteDB_R_Land2":"",
	"inputfelderform:inputFelder:RoamingToLand2Min":"0",
	"inputfelderform:inputFelder:RoamingToLand2Anr":"0",
	"inputfelderform:inputFelder:j_idt452_collapsed":"false",
	"inputfelderform:inputFelder:LandlisteDB_R_Land3":"",
	"inputfelderform:inputFelder:RoamingToLand3Min":"0",
	"inputfelderform:inputFelder:RoamingToLand3Anr":"0",
	"inputfelderform:inputFelder:j_idt465_collapsed":"false",
	"inputfelderform:inputFelder_activeIndex":"4",
	"inputfelderform:j_idt506":"",
	"javax.faces.ViewState":value1 + ":"+value2
	}

	


	data3 = "inputfelderform=inputfelderform&inputfelderform%3AinputFelder%3AanzMinEingabe=12&inputfelderform%3AinputFelder%3AanzAnrufeEingabe=2&inputfelderform%3AinputFelder%3Aanteil3NrEingabe=2&inputfelderform%3AinputFelder%3AalterAuswahl=29&inputfelderform%3AinputFelder%3Aj_idt132=12&inputfelderform%3AinputFelder%3AproviderFilterSB=Sunrise&inputfelderform%3AinputFelder%3Aj_idt120_collapsed=false&inputfelderform%3AinputFelder%3Aj_idt142=on&inputfelderform%3AinputFelder%3AaufFestnetzSwisscom=20&inputfelderform%3AinputFelder%3AaufFestnetzUPC=0&inputfelderform%3AinputFelder%3Aj_idt154_collapsed=false&inputfelderform%3AinputFelder%3AaufSwisscom=40&inputfelderform%3AinputFelder%3AaufOrange=20&inputfelderform%3AinputFelder%3AaufSunrise=20&inputfelderform%3AinputFelder%3AaufMbudget=0&inputfelderform%3AinputFelder%3AaufCoopMobile=0&inputfelderform%3AinputFelder%3Aj_idt165_collapsed=false&inputfelderform%3AinputFelder%3AaufAldi=0&inputfelderform%3AinputFelder%3AaufOk=0&inputfelderform%3AinputFelder%3AaufLebara=0&inputfelderform%3AinputFelder%3AaufTalkTalk=0&inputfelderform%3AinputFelder%3AaufYallo=0&inputfelderform%3AinputFelder%3AaufLyca=0&inputfelderform%3AinputFelder%3AaufOrtel=0&inputfelderform%3AinputFelder%3AaufMobileUPC=0&inputfelderform%3AinputFelder%3AaufAndere=0&inputfelderform%3AinputFelder%3Aj_idt187_collapsed=true&inputfelderform%3AinputFelder%3AanzSMSEingabe=12&inputfelderform%3AinputFelder%3AanzTageSMS=12&inputfelderform%3AinputFelder%3Aj_idt232_collapsed=false&inputfelderform%3AinputFelder%3AdatenmengeMBEingabe=122&inputfelderform%3AinputFelder%3AintVerwendungAnzTageEingabe=12&inputfelderform%3AinputFelder%3AspeedAuswahl=0&inputfelderform%3AinputFelder%3Aj_idt243_collapsed=false&inputfelderform%3AinputFelder%3ASmsAusland=12&inputfelderform%3AinputFelder%3Aj_idt275_input=Deutschland&inputfelderform%3AinputFelder%3ALand1FixMin=12&inputfelderform%3AinputFelder%3ALand1FixAnzAnr=22&inputfelderform%3AinputFelder%3ALand1MobMin=12&inputfelderform%3AinputFelder%3ALand1MobAnzAnr=12&inputfelderform%3AinputFelder%3Aj_idt272_collapsed=false&inputfelderform%3AinputFelder%3Aj_idt299_input=&inputfelderform%3AinputFelder%3ALand2FixMin=0&inputfelderform%3AinputFelder%3ALand2FixAnzAnr=0&inputfelderform%3AinputFelder%3ALand2MobMin=0&inputfelderform%3AinputFelder%3ALand2MobAnzAnr=0&inputfelderform%3AinputFelder%3Aj_idt296_collapsed=true&inputfelderform%3AinputFelder%3Aj_idt323_input=&inputfelderform%3AinputFelder%3ALand3FixMin=0&inputfelderform%3AinputFelder%3ALand3FixAnzAnr=0&inputfelderform%3AinputFelder%3ALand3MobMin=0&inputfelderform%3AinputFelder%3ALand3MobAnzAnr=0&inputfelderform%3AinputFelder%3Aj_idt320_collapsed=true&inputfelderform%3AinputFelder%3Aj_idt347_input=&inputfelderform%3AinputFelder%3ALand4FixMin=0&inputfelderform%3AinputFelder%3ALand4FixAnzAnr=0&inputfelderform%3AinputFelder%3ALand4MobMin=0&inputfelderform%3AinputFelder%3ALand4MobAnzAnr=0&inputfelderform%3AinputFelder%3Aj_idt344_collapsed=true&inputfelderform%3AinputFelder%3Aj_idt371_input=&inputfelderform%3AinputFelder%3ALand5FixMin=0&inputfelderform%3AinputFelder%3ALand5FixAnzAnr=0&inputfelderform%3AinputFelder%3ALand5MobMin=0&inputfelderform%3AinputFelder%3ALand5MobAnzAnr=0&inputfelderform%3AinputFelder%3Aj_idt368_collapsed=true&inputfelderform%3AinputFelder%3Aj_idt398_input=Deutschland&inputfelderform%3AinputFelder%3ARoaming1AnzTage=12&inputfelderform%3AinputFelder%3ARoamingSMS=12&inputfelderform%3AinputFelder%3ARoamingDatenMB=12&inputfelderform%3AinputFelder%3ARoamingIncomingMin=12&inputfelderform%3AinputFelder%3ARoamingIncomingAnr=12&inputfelderform%3AinputFelder%3Aj_idt412_collapsed=false&inputfelderform%3AinputFelder%3ARoamingToCHMin=0&inputfelderform%3AinputFelder%3ARoamingToCHAnr=0&inputfelderform%3AinputFelder%3Aj_idt421_collapsed=true&inputfelderform%3AinputFelder%3ARoamingToLocalMin=0&inputfelderform%3AinputFelder%3ARoamingToLocalAnr=0&inputfelderform%3AinputFelder%3Aj_idt430_collapsed=true&inputfelderform%3AinputFelder%3ALandlisteDB_R_Land1=&inputfelderform%3AinputFelder%3ARoamingToLand1Min=0&inputfelderform%3AinputFelder%3ARoamingToLand1Anr=0&inputfelderform%3AinputFelder%3Aj_idt439_collapsed=true&inputfelderform%3AinputFelder%3ALandlisteDB_R_Land2=&inputfelderform%3AinputFelder%3ARoamingToLand2Min=0&inputfelderform%3AinputFelder%3ARoamingToLand2Anr=0&inputfelderform%3AinputFelder%3Aj_idt452_collapsed=true&inputfelderform%3AinputFelder%3ALandlisteDB_R_Land3=&inputfelderform%3AinputFelder%3ARoamingToLand3Min=0&inputfelderform%3AinputFelder%3ARoamingToLand3Anr=0&inputfelderform%3AinputFelder%3Aj_idt465_collapsed=true&inputfelderform%3AinputFelder_activeIndex=4&inputfelderform%3Aj_idt506=&javax.faces.ViewState="+value1 + "%3A"+value2


	data = urllib.urlencode(data)
	data4 = urllib.urlencode(data4)

	formDataExt2 = "inputfelderform=inputfelderform&inputfelderform%3AinputFelder%3AanzMinEingabe=1&inputfelderform%3AinputFelder%3AanzAnrufeEingabe=2&inputfelderform%3AinputFelder%3Aanteil3NrEingabe=3&inputfelderform%3AinputFelder%3AalterAuswahl=26&inputfelderform%3AinputFelder%3Aj_idt127=4&inputfelderform%3AinputFelder%3AproviderFilterSB=Sunrise&inputfelderform%3AinputFelder%3Aj_idt115_collapsed=false&inputfelderform%3AinputFelder%3Aj_idt137=on&inputfelderform%3AinputFelder%3AaufFestnetzSwisscom=0&inputfelderform%3AinputFelder%3AaufFestnetzUPC=0&inputfelderform%3AinputFelder%3Aj_idt149_collapsed=false&inputfelderform%3AinputFelder%3AaufSwisscom=40&inputfelderform%3AinputFelder%3AaufOrange=30&inputfelderform%3AinputFelder%3AaufSunrise=30&inputfelderform%3AinputFelder%3AaufMbudget=0&inputfelderform%3AinputFelder%3AaufCoopMobile=0&inputfelderform%3AinputFelder%3Aj_idt160_collapsed=false&inputfelderform%3AinputFelder%3AaufAldi=0&inputfelderform%3AinputFelder%3AaufOk=0&inputfelderform%3AinputFelder%3AaufLebara=0&inputfelderform%3AinputFelder%3AaufTalkTalk=0&inputfelderform%3AinputFelder%3AaufYallo=0&inputfelderform%3AinputFelder%3AaufLyca=0&inputfelderform%3AinputFelder%3AaufOrtel=0&inputfelderform%3AinputFelder%3AaufMobileUPC=0&inputfelderform%3AinputFelder%3AaufAndere=0&inputfelderform%3AinputFelder%3Aj_idt182_collapsed=true&inputfelderform%3AinputFelder%3AanzSMSEingabe=5&inputfelderform%3AinputFelder%3AanzTageSMS=6&inputfelderform%3AinputFelder%3Aj_idt227_collapsed=false&inputfelderform%3AinputFelder%3AdatenmengeMBEingabe=7&inputfelderform%3AinputFelder%3AintVerwendungAnzTageEingabe=8&inputfelderform%3AinputFelder%3AspeedAuswahl=1.0&inputfelderform%3AinputFelder%3Aj_idt238_collapsed=false&inputfelderform%3AinputFelder%3ASmsAusland=9&inputfelderform%3AinputFelder%3Aj_idt270_input=Deutschland&inputfelderform%3AinputFelder%3ALand1FixMin=10&inputfelderform%3AinputFelder%3ALand1FixAnzAnr=11&inputfelderform%3AinputFelder%3ALand1MobMin=12&inputfelderform%3AinputFelder%3ALand1MobAnzAnr=13&inputfelderform%3AinputFelder%3Aj_idt267_collapsed=false&inputfelderform%3AinputFelder%3Aj_idt294_input=Frankreich&inputfelderform%3AinputFelder%3ALand2FixMin=14&inputfelderform%3AinputFelder%3ALand2FixAnzAnr=15&inputfelderform%3AinputFelder%3ALand2MobMin=16&inputfelderform%3AinputFelder%3ALand2MobAnzAnr=17&inputfelderform%3AinputFelder%3Aj_idt291_collapsed=false&inputfelderform%3AinputFelder%3Aj_idt318_input=Spanien&inputfelderform%3AinputFelder%3ALand3FixMin=18&inputfelderform%3AinputFelder%3ALand3FixAnzAnr=19&inputfelderform%3AinputFelder%3ALand3MobMin=20&inputfelderform%3AinputFelder%3ALand3MobAnzAnr=21&inputfelderform%3AinputFelder%3Aj_idt315_collapsed=false&inputfelderform%3AinputFelder%3Aj_idt342_input=Italien&inputfelderform%3AinputFelder%3ALand4FixMin=22&inputfelderform%3AinputFelder%3ALand4FixAnzAnr=23&inputfelderform%3AinputFelder%3ALand4MobMin=24&inputfelderform%3AinputFelder%3ALand4MobAnzAnr=25&inputfelderform%3AinputFelder%3Aj_idt339_collapsed=false&inputfelderform%3AinputFelder%3Aj_idt366_input=Russland&inputfelderform%3AinputFelder%3ALand5FixMin=26&inputfelderform%3AinputFelder%3ALand5FixAnzAnr=27&inputfelderform%3AinputFelder%3ALand5MobMin=28&inputfelderform%3AinputFelder%3ALand5MobAnzAnr=29&inputfelderform%3AinputFelder%3Aj_idt363_collapsed=false&inputfelderform%3AinputFelder%3Aj_idt393_input=Deutschland&inputfelderform%3AinputFelder%3ARoaming1AnzTage=30&inputfelderform%3AinputFelder%3ARoamingSMS=31&inputfelderform%3AinputFelder%3ARoamingDatenMB=32&inputfelderform%3AinputFelder%3ARoamingIncomingMin=33&inputfelderform%3AinputFelder%3ARoamingIncomingAnr=34&inputfelderform%3AinputFelder%3Aj_idt407_collapsed=false&inputfelderform%3AinputFelder%3ARoamingToCHMin=35&inputfelderform%3AinputFelder%3ARoamingToCHAnr=36&inputfelderform%3AinputFelder%3Aj_idt416_collapsed=false&inputfelderform%3AinputFelder%3ARoamingToLocalMin=37&inputfelderform%3AinputFelder%3ARoamingToLocalAnr=38&inputfelderform%3AinputFelder%3Aj_idt425_collapsed=false&inputfelderform%3AinputFelder%3ALandlisteDB_R_Land1=Frankreich&inputfelderform%3AinputFelder%3ARoamingToLand1Min=39&inputfelderform%3AinputFelder%3ARoamingToLand1Anr=40&inputfelderform%3AinputFelder%3Aj_idt434_collapsed=false&inputfelderform%3AinputFelder%3ALandlisteDB_R_Land2=&inputfelderform%3AinputFelder%3ARoamingToLand2Min=0&inputfelderform%3AinputFelder%3ARoamingToLand2Anr=0&inputfelderform%3AinputFelder%3Aj_idt447_collapsed=true&inputfelderform%3AinputFelder%3ALandlisteDB_R_Land3=&inputfelderform%3AinputFelder%3ARoamingToLand3Min=0&inputfelderform%3AinputFelder%3ARoamingToLand3Anr=0&inputfelderform%3AinputFelder%3Aj_idt460_collapsed=true&inputfelderform%3AinputFelder_activeIndex=4&inputfelderform%3Aj_idt501=&javax.faces.ViewState="+value1 + "%3A"+value2
	# print(formDataExt)

	headers = { 
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'en-US,en;q=0.8',
	'Connection':'keep-alive',
	'Content-Type':'application/x-www-form-urlencoded',
	'Cookie':sessionID,
	'Host':'www.dschungelkompass.ch',
	'Origin':'http://www.dschungelkompass.ch',
	'Referer':'http://www.dschungelkompass.ch/mobile/welcomeSchnellprofil.xhtm',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
	}
	req = requests.post(url2, data = data4, headers = headers)

	resultsSouped = BeautifulSoup(req.content)

	contracts = resultsSouped.find_all("div", {"class": "ausgabeTabelleRow"})
	


	i = 0;
	contractsParsed =[]


	for c in contracts:
		cParsed = {}
		# print("---------------- ......... -----------------------------")
		providerundAbo = c.find("div",{"class": "ausgabeTabelleProviderUndAbo"})
		providerHTML = providerundAbo.children.next()
		planHTML= providerHTML.next_sibling
		cParsed['Anbieter'] = providerHTML.string
		cParsed['PlanName'] = planHTML.string
		

		priceHTML = c.find("span",{"class": "ausgabeTabelleLabelsKostenTotal"})
		
		cParsed['Price']  = float(priceHTML.string)


		SpeedTypeNetwork = c.find("div",{"class": "ausgabeTabelleSpeed"})
		aboType=""
		for child in SpeedTypeNetwork.children:
			if child.string=="Art: ":
				aboType = child.next_sibling.string
				
		
		cParsed['Abo Type'] = aboType
		details = c.find("div",{"class": "ausgabeTabelleCell3"})
		for d in details.find_all("br"):
			fieldHTML = d.next_sibling
			valueHTML = fieldHTML.next_sibling
			cParsed[fieldHTML.string] = valueHTML.string
		

		bemerkungenSection = c.find("div",{"class": "ausgabeTabelleBemerkungen"})
		minDurationValue = bemerkungenSection.find("span",{"class": "greenText"})
		cParsed["Minium Duration"] = minDurationValue.string + " Months"
		

		contractsParsed.append(cParsed)
			
	contractsParsed = sorted(contractsParsed, key=itemgetter('Price'), reverse=True) 
	# contractsParsedDict  = {}
	# i = 0
	# for c in contractsParsed:
	# 	contractsParsedDict[str(i)]= contractsParsed[i]
		
	return contractsParsed

