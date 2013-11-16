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
 
#set up the database
conn = sqlite.connect('./reminder.db')
c = conn.cursor()

#create table REMINDER
conn.execute('''CREATE TABLE IF NOT EXISTS REMINDER
   (user 			  	  TEXT    NOT NULL,
   last_taken             timestamp    NOT NULL,
   schedule       	      TEXT    NOT NULL,
   duration				  INT		   NOT NULL,
   no_to			      TEXT    NOT NULL,    
   PRIMARY KEY (user));''')
 
 
def send_message(phone_num):
	'''
	function to send a sms given the number
	'''
	message = client.sms.messages.create(body="Please Take Your Pill",
		to=phone_num,    # Replace with your phone number
		from_="+18603576107") # Replace with your Twilio number
		
def takePill():
	'''
	Test function, we save the data fields send by the phone into dict, not
	database, so that we can easily test. 
	'''    
	#messages = client.messages.list()
	#print map(lambda x: (x.body, x.from_), messages)
	db = {}
	
	while True:
		for message in messages:
			if message.status == 'received':	
				if message.body.lower() == 'yes':
					phone = message.from_
					date = parsedate(message.date_sent)
					t = datetime.fromtimestamp(time.mktime(date))
					db[phone] = t
		for phone in db.keys():
			#hard coded change the timezone, may not right when use the summer time
			time_lapse = datetime.now() -db[phone] + timedelta(hours=8)
			print time_lapse
			#if time_lapse > threshold:
				#send_message(phone)
		time.sleep(30)

def parser_message():
	'''
	Main function to parser the message sent by the phone. We check the message field 
	'''
	while True:
		for message in messages:
			body = message.body
			first_line = body.split('\n')[0].lower()
			if message.status == 'received':	
				if first_line == 'yes':
					phone = message.from_
					date = parsedate(message.date_sent)
					t = datetime.fromtimestamp(time.mktime(date)) - timedelta(hours=8)
					#print t
					cursor = conn.execute("SELECT user FROM REMINDER WHERE user = ?", (phone,))
					data = cursor.fetchall()
					#print phone
					if len(data) == 0:
						#print 'no user exist'
						conn.execute('insert into REMINDER values(?,?,?,?,?)', (phone,datetime.now(),'0',0,'0'))
						conn.commit()
					else:
						conn.execute("UPDATE REMINDER SET last_taken = ? WHERE user=?", (t, phone))
						conn.commit()
								
			if first_line == 'set up':
				''' if this is set up, then we should run the register '''
				#print body.split('\n')[1]
				register(message)
		cursor = conn.execute("SELECT user, last_taken FROM REMINDER")
		for phone, last_taken in cursor.fetchall():
			#hard coded change the timezone, may not right when use the summer time
			time_lapse = datetime.now() -db[phone] + timedelta(hours=8)
			if time_lapse > threshold:
				send_message('+18609878666')
		    	
		time.sleep(30)

def register(message):
		'''
		This function is when the user actually set up there alert from sms, the format:
		'set up               #set up 
		 12:00:00             #schedule time (every day at 12)
		 3                    #duration, 3 days
		 5100000000'          #which number send to 
		'''
		phone = message.from_
		schedule = message.body.split('\n')[1]
		#schedule = parser.parse('9:12:12')
		duration = message.body.split('\n')[2]
		
		date = parsedate(message.date_sent)
		t0 = datetime.fromtimestamp(time.mktime(date)) - timedelta(hours=8)
		
		#print d.seconds
		no_to = message.body.split('\n')[3]
		cursor = conn.execute("SELECT user FROM REMINDER WHERE user = ?", (phone,))
		data = cursor.fetchall()
		#print phone
		if len(data) == 0:
			#print 'no user exist'
			conn.execute('insert into REMINDER values(?,?,?,?,?)', (phone,t0,schedule,duration,no_to))
			conn.commit()
		else:
			#print 'user exist'
			conn.execute("UPDATE REMINDER SET last_taken = ?, schedule = ?, no_to = ?, duration = ? WHERE user=?", (t0,schedule,no_to,duration, phone))
			conn.commit()

'''
#we can start the reminder based on the period time the user specified

#@periodic_task(run_every=crontab(hour=7, minute=30, day_of_week="mon"))
@periodic_task(run_every=crontab())
def every_day():
	print 'this is run every monday'
'''

messages = client.messages.list()
messages.reverse()
parser_message()
#takePill()
#register()

