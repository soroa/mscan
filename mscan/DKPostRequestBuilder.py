from dbFunctions import *

def buildRequest(user_ID, days):
	
	data = {
	"inputfelderform":"inputfelderform",
	"inputfelderform:inputFelder:anzMinEingabe":totalCallsMinutesCH(user_ID,days) #Minuten telefonieren CH pro Monat
	"inputfelderform:inputFelder:anzAnrufeEingabe":totalCallsNumberCH(user_ID,days), # Anzalh Anrufe pro Monat
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
	"inputfelderform:inputFelder:anzSMSEingabe":SMS_toCH(user_ID,days),#Sms pro Monat CH
	"inputfelderform:inputFelder:anzTageSMS":str(days), #Innerhalb von x Tagen
	"inputfelderform:inputFelder:j_idt227_collapsed":"false",
	"inputfelderform:inputFelder:datenmengeMBEingabe":dataCH(user_ID, days),#Datenmenge pro Monat
	"inputfelderform:inputFelder:intVerwendungAnzTageEingabe":str(days), #Innerhalb von x Tagen
	"inputfelderform:inputFelder:speedAuswahl":"1.0", #Geschwindigkeit Minimum
	"inputfelderform:inputFelder:j_idt238_collapsed":"false", #
	"inputfelderform:inputFelder:SmsAusland":SMS_toABROAD(user_ID, days), #SMS ins Ausland
	"inputfelderform:inputFelder:j_idt270_input":"Deutschland", #Anrufe ins Ausland: Land1
	"inputfelderform:inputFelder:Land1FixMin":"10", #Festnetz minuten anrufe ins ausland
	"inputfelderform:inputFelder:Land1FixAnzAnr":"11", #Festnetz Anzahl Anrufe ins Ausland
	"inputfelderform:inputFelder:Land1MobMin":"12", #Mobilnetx Anzahl Minuten Anrufe
	"inputfelderform:inputFelder:Land1MobAnzAnr":"13", #Mobilnetz Anzah Anrufe
	"inputfelderform:inputFelder:j_idt267_collapsed":"false", 
	"inputfelderform:inputFelder:j_idt294_input":"Frankreich", #Anrufe ins Auland: Land2
	"inputfelderform:inputFelder:Land2FixMin":"14", #same as above
	"inputfelderform:inputFelder:Land2FixAnzAnr":"15", 
	"inputfelderform:inputFelder:Land2MobMin":"16",
	"inputfelderform:inputFelder:Land2MobAnzAnr":"17",
	"inputfelderform:inputFelder:j_idt291_collapsed":"false",
	"inputfelderform:inputFelder:j_idt318_input":"Spanien",
	"inputfelderform:inputFelder:Land3FixMin":"18",
	"inputfelderform:inputFelder:Land3FixAnzAnr":"19",
	"inputfelderform:inputFelder:Land3MobMin":"20",
	"inputfelderform:inputFelder:Land3MobAnzAnr":"21",
	"inputfelderform:inputFelder:j_idt315_collapsed":"false",
	"inputfelderform:inputFelder:j_idt342_input":"Italien",
	"inputfelderform:inputFelder:Land4FixMin":"22",
	"inputfelderform:inputFelder:Land4FixAnzAnr":"23",
	"inputfelderform:inputFelder:Land4MobMin":"24",
	"inputfelderform:inputFelder:Land4MobAnzAnr":"25",
	"inputfelderform:inputFelder:j_idt339_collapsed":"false",
	"inputfelderform:inputFelder:j_idt366_input":"Russland",
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
	return data