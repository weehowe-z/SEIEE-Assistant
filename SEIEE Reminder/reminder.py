# -*- coding:utf-8 -*- 
import smtplib
import urllib2
import datetime

#sender name or sender address are not allowed to contain 'receiver'
def send_email(sender, receivers, news):

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

def getInfo():
	url = 'http://xsb.seiee.sjtu.edu.cn/xsb/index.htm'
	url_base = 'http://xsb.seiee.sjtu.edu.cn'
	try:
		page = urllib2.urlopen(url,timeout=2).read()
	except:
		print "cannot access to website"
		return None

	today = datetime.datetime.now().date()
	today_str = today.strftime('%Y-%m-%d')
	
	newslist = []

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
			news = {}
			news['title'] = title
			news['url'] = info_url
			newslist.append(news)
	return newslist

def push(newslist):
	sender = {
		'address': 'your_email@gmail.com',
		'name': 'your_name',
		'key': 'your_key'
	}
	
	receivers = ['weehowe.z@gmail.com','575877982@qq.com']
	
	print "Prepare to send email"
	send_email(sender,receivers,newslist)


if __name__ == '__main__':
	push(getInfo())