from app import db
from models import Contract


''' Sunrise''' 


contractName = Contract()
contractName.contract_name =""
contractName.monthly_price =0#setvalues
contractName.operator =""
contractName.age_limit =0
contractName.duration= 0#setvalues

#calls
# --national
contractName.limit_same_operator_calls_nat=0#setvalues ##in minutes
contractName.limit_other_operator_calls_nat=0#setvalues ##in minutes
contractName.limit_fixed_networks_calls_nat=0 
contractName.limit_national_calls= 0
# --international
contractName.limit_outgoing_international_calls_fromCH=0#setvalues
contractName.limit_calls_at_abroad = 0#setvalues #TODO does it include incoming calls as well? 
#standard rates
contractName.rate_call_in_ch = 0.0
contractName.rate_chargable_call_duration = 0#setvalues
contractName.rate_calls_to_abroad = 0.0
contractName.rate_incoming_call_at_abroad = 0.0
contractName.rate_call_from_abroad_to_abroad = 0.0
contractName.rate_call_from_abroad_to_CH = 0.0
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------

#internet
#--national
contractName.unlimited_whatsapp = true 
contractName.limit_3g =0#setvalues
contractName.limit_4g =0#setvalues
#internet
#--international
contractName.limit_roaming =0#setvalues
#starndard rates
contractName.roaming_rate = 0.0
contractName.surfing_daily_cost_unlimited = 0.0
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------

#sms
#--national
contractName.limit_sms_CH =0#setvalues
#--international
contractName.limit_sms_at_abroad = 0#setvalues
#standard rates
contractName.sms_at_abroad_stdRate = 0.0
	sms_CH_stdRate = 0.0
db.session.add(contractName)
db.session.commit()



