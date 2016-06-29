
from mscan  import db
from mscan  import User, Call, SMS, MobileData,CountryISOLog,Phone, PhoneInformation, Measurement, MLSCellRecord


# !!!!!!!
# N.B. Before when starting the server for the first time you gotta execute this pythong
# file form the console


#create the databse and the db tables

db.create_all()

#commit the changes
db.session.commit()
