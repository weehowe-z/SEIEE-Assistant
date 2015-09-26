# -*- coding:utf-8 -*- 
import smtplib,urllib2,datetime

def send_email(sender, receivers, news):

	if len(news) == 0:
		print "There is no email to send"
		return

	sender_add = sender['address']
	sender_name = sender['name']
	sender_key = sender['key']

	msg = "From: " + sender_name + " <" + sender_add + ">\n" \
			+ "To: <receiver>\n" + "Subject: " + "subject" + "\n\n" \
			+ "content"

	try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login(sender_add,sender_key)
	except:
		print "smtp.gmail.com connection failed"
		return

	for i in range(0,len(news)):
		title = news[i]['title']
		url = news[i]['url']

		subject = '【电院提醒】' + title
		content = '【' + title + "】已经在学生办网站发布了,赶紧去看看吧!\n" \
					 + url + "\n\n\n\n ---------------------\n" \
					 + (u"\u00A9").encode('utf-8') +' 2015 SEIEE Reminder'

		for j in range(0,len(receivers)):
			print "now send mail to " + receivers[j] + ' ' + str(len(receivers)*i+j+1) + '/' + str(len(news)*len(receivers))
			msg_send = msg.replace('receiver',receivers[j]).replace('subject',subject).replace('content',content)
			server.sendmail(sender_add,[receivers[j]],msg_send)

	server.quit()

def has_no_keyword(title,keyword = None):
	if keyword == None:
		keyword = ['研究生','硕士','博士']
	for i in range(0,len(keyword)):
		if title.find(keyword[i]) != -1 and title.find('本科') == -1:
			return False
	return True

def getInfo(date = None):
	url = 'http://xsb.seiee.sjtu.edu.cn/xsb/index.htm'
	url_base = 'http://xsb.seiee.sjtu.edu.cn'
	news = []

	try:
		page = urllib2.urlopen(url,timeout=5).read()
	except:
		print "cannot access to website"
		return None

	if date == None:
		today = datetime.datetime.now().date()
		today_str = today.strftime('%Y-%m-%d')
	else:
		today_str = date
	
	spanpos = 0
	while True:
		startpos = page.find('<a title="',spanpos)
		if startpos == -1:
			break
		spanpos = page.find('<span>',startpos)
		date = page[spanpos+7:spanpos+17]
		if date == today_str:
			hrefpos_start = page.find('href=',startpos)
			hrefpos_end = page.find('target=',startpos)
			href = page[hrefpos_start+6:hrefpos_end]
			title = page[startpos+10:hrefpos_start-2]
			info_url = url_base + href
			newinfo = {}
			newinfo['title'] = title
			newinfo['url'] = info_url
			if has_no_keyword(title, keyword = None) == True:
				news.append(newinfo)
	return news

def push(news):
	sender = {
		'address': 'seiee.reminder@gmail.com',
		'name': 'SEIEE REMINDER',
		'key': 'seieereminder'
	}

	receivers = ['weehowe.z@gmail.com']
	
	print "Prepare to send email"
	send_email(sender,receivers,news)


if __name__ == '__main__':
	push(getInfo())