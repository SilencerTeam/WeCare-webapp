import smtplib
import schedule
import datetime
import pandas as pd
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import os
import json
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import os
from twilio.rest import Client



data = pd.read_csv("file1.csv")
#SMTP server
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login("silencerteam969@gmail.com", "aarr1234?")

#TWILIO server
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
# instantiating the Client
client = Client(account_sid, auth_token)


def message(subject="Python Notification",text="", img=None, attachment=None):
	
	# build message contents
	msg = MIMEMultipart()
	
	# Add Subject
	msg['Subject'] = subject
	
	# Add text contents
	msg.attach(MIMEText(text))

	# Check if we have anything
	# given in the img parameter
	if img is not None:

		# Check whether we have the
		# lists of images or not!
		if type(img) is not list:
			
			# if it isn't a list, make it one
			img = [img]

		# Now iterate through our list
		for one_img in img:
			
			# read the image binary data
			img_data = open(one_img, 'rb').read()
			
			# Attach the image data to MIMEMultipart
			# using MIMEImage,
			# we add the given filename use os.basename
			msg.attach(MIMEImage(img_data,
								name=os.path.basename(one_img)))

	# We do the same for attachments
	# as we did for images
	if attachment is not None:

		# Check whether we have the
		# lists of attachments or not!
		if type(attachment) is not list:
			
			# if it isn't a list, make it one
			attachment = [attachment]

		for one_attachment in attachment:

			with open(one_attachment, 'rb') as f:
				
				# Read in the attachment using MIMEApplication
				file = MIMEApplication(
					f.read(),
					name=os.path.basename(one_attachment)
				)
			file['Content-Disposition'] = f'attachment;\
			filename="{os.path.basename(one_attachment)}"'
			
			# At last, Add the attachment to our message object
			msg.attach(file)
	return msg




SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)



# If modifying these scopes, delete the file token.json.


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1CSsXvnbkM3iNCaw9IRIlM_jAR0E84n4LDdnXzn9b364'


service = build('sheets', 'v4', credentials=creds)


# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="sheet1!A1:E").execute()
values = result.get('values', [])
# print(len(values))
# print(values[0][1],values[0][4])

while(1):
	for i in range(len(values)):
		now = datetime.datetime.now()
		nowtime = now.strftime("%H:%M:%S")
		time = values[i][2]
		# time = time[:len(time)-3]
		# print(nowtime, time)

		if (time == nowtime):
			print(values[i][1], nowtime, values[i][3])
			notific = "Hi " + values[i][0]+ ", it is time for you to take " + values[i][1] + "💊"
			msg = message(subject="WeCare Notification",text= notific)
			server.sendmail("silencerteam969@gmail.com",values[i][3],msg=msg.as_string())
			mob = '+91' + values[i][4]
			message_go = client.messages.create(body= notific, from_='+18484005757', to=mob)
			print(message_go.sid)
            
			
			

		
            

