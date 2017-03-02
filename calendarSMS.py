"""
This program retrieves all MS Outlook 2013 calendar events, 
finds any that are occurring the next work day, 
and texts them to a specified phone number.

Credentials stored in calendar_sms.txt:
Twilio Account SID
Twilio Authorization Token
Twilio phone number (inc. +countrycode)
My Twilio-validated personal phone number (inc. +countrycode)

Adapted from Automate the Boring Stuff with Python
https://automatetheboringstuff.com/chapter16/
"""

import win32com.client
import datetime
from twilio.rest import TwilioRestClient

if datetime.date.today().weekday() == 4:
	tomorrow = datetime.date.today() + datetime.timedelta(days=3)
else: 
	tomorrow = datetime.date.today() + datetime.timedelta(days=1)
outlook = win32com.client.Dispatch("Outlook.Application")
namespace = outlook.GetNamespace("MAPI")
appointments = namespace.GetDefaultFolder(9).Items 
# ^ https://msdn.microsoft.com/en-us/library/office/ff861868.aspx
appointments.Sort("[Start]")
appointments.IncludeRecurrences = "True"

reminders = "-\n\nEvents for {d}\n\n".format(d=tomorrow.strftime("%A %d %B %Y"))
for x in range(1, len(appointments)+1): 
	# https://msdn.microsoft.com/en-us/library/office/ff862177.aspx#Anchor_4
	appointmentDate = datetime.date(
		appointments(x).Start.year,
		appointments(x).Start.month,
		appointments(x).Start.day)
	if appointmentDate == tomorrow:
		reminders += "Subject: " + str(appointments(x).Subject) + "\n"
		reminders += "Start Time: " + str(appointments(x).Start.strftime("%I:%M %p")) + "\n"
		reminders += "Location: " + str(appointments(x).Location) + "\n\n"
	if appointmentDate > tomorrow:
		break

with open('calendar_sms.txt') as f:
	data = [str(x.strip()) for x in f.readlines()]
accountSID = data[0]
authToken = data[1]
twilioCli = TwilioRestClient(accountSID, authToken)
myTwilioNumber = data[2]
myCellPhone = data[3]
message = twilioCli.messages.create(
	to = myCellPhone,
	from_ = myTwilioNumber,
	body = reminders)

