# -*- coding:utf-8 -*- 
import smtplib

#sender name or sender address are not allowed to contain 'receiver'
def send_email(sender, receivers, mail):
	sender_add = sender['address']
	sender_name = sender['name']
	sender_key = sender['key']
	subject = mail['subject']
	content = mail['content']

	msg = "From: " + sender_name + " <" + sender_add + ">\n" \
			+ "To: <receiver>\n" + "Subject: " + subject + "\n\n" \
			+ content
	
	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login(sender_add,sender_key)
	except:
		print "smtp.gmail.com connection failed"
		return

	
	for i in range(0,len(receivers)):
		print "now send mail to " + receivers[i] + ' ' + str(i+1) + '/' + str(len(receivers))
		msg_send = msg.replace('receiver',receivers[i])
		server.sendmail(sender_add,[receivers[i]],msg_send)
	
	server.quit()
