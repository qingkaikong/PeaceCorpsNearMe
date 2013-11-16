from twilio.rest import TwilioRestClient
import time
from email.utils import parsedate
from datetime import datetime, timedelta
import sqlite3 as sqlite
from dateutil import parser
from celery.task.schedules import crontab
from celery.decorators import periodic_task

threshold = timedelta(minutes = 1)

account_sid = "AC00298660177c65705d7ba2dd36c16c1b"
auth_token  = "4e40ae55b99c27e51ddc0cd2da622cf9"
client = TwilioRestClient(account_sid, auth_token)

def send_message(phone_num):
	
	message = client.sms.messages.create(body="Please Take Your Pill",
		to=phone_num,    # Replace with your phone number
		from_="+18603576107") # Replace with your Twilio number

def takePill():    
	db = {}
	list = []
	count = 0
	while True:
		messages = client.messages.list()
		if count ==0:
			for message in messages:
				#print message.body
				if message.status == 'received':
					list.append(message.sid)
		else:
			for message in messages:
				if message.status == 'received':
					#print message.sid
					#print list
					#print message.body
					if message.sid not in list:
						print 'We have a new message sent by: ' + message.from_
						print 'The message is: ' + message.body
						print '###################################################'
						list.append(message.sid)
		count += 1
		time.sleep(5)
		
messages = client.messages.list()
takePill()

