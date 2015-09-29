# -*- coding:utf-8 -*- 
import smtplib,urllib2
import ConfigParser
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def write_log(logfile,string,need_time = False):
	if need_time == False:
		logfile.write(string+'\n')
	else:
		time = datetime.datetime.now()
		time_str = time.strftime('%Y-%m-%d %H:%M:%S')
		logfile.write(string + '\t' + time_str +'\n')

def send_email(sender, receivers, news):

	if len(news) == 0:
		print "There is no email to send"
		return

	sender_add = sender['address']
	sender_name = sender['name']
	sender_key = sender['key']

	html_template = """
	<html>
	  <head></head>
	  <body>
		<p>
			##information##
		</p>
		<p>
			##url##
		</p>
		<p>
			<br/><br/><br/></br>
		</p>
		<p>
			------------------------------------
		</p>
		<span><strong><small>&copy;<i>2015 SEIEE Reminder<i/></small></strong></span>&nbsp;&nbsp;&nbsp;	
		<span><small><i>Fork me at <a href="https://github.com/weehowe-z/littleProjects">GitHub</a></i></small></span>
	  </body>
	</html>
	"""		
	content_template = "已经在学生办网站发布啦，快去看看吧！"

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

		msg = MIMEMultipart('alternative')
		msg['Subject'] = '【电院提醒】' + title
		msg['From'] = sender_name
		content = '【' + title + '】'+content_template
		html = html_template.replace('##information##',content).replace('##url##',url)
		msg.attach(MIMEText(html, 'html'))

		for j in range(0,len(receivers)):
			del msg['To']
			msg['To'] = receivers[j]
			print "now send mail to " + receivers[j] + ' ' + str(len(receivers)*i+j+1) + '/' + str(len(news)*len(receivers))
			server.sendmail(sender_add,[receivers[j]],msg.as_string())
	
	server.quit()

def has_relationship(title,keyword = None):
	if keyword == None:
		keyword = ['研究生','硕士','博士']
	for i in range(0,len(keyword)):
		if title.find(keyword[i]) != -1 and title.find('本科') == -1:
			return False
	return True

def getInfo(logfile,date):
	url = 'http://xsb.seiee.sjtu.edu.cn/xsb/index.htm'
	url_base = 'http://xsb.seiee.sjtu.edu.cn'
	news = []

	try:
		page = urllib2.urlopen(url,timeout=5).read()
	except:
		write_log(logfile,"[Error]Cannot access to website")
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
			href = page[hrefpos_start+6:hrefpos_end-2]
			title = page[startpos+10:hrefpos_start-2]
			info_url = url_base + href
			newinfo = {}
			newinfo['title'] = title
			newinfo['url'] = info_url
			if has_relationship(title, keyword = None) == True:
				news.append(newinfo)
				write_log(logfile,"[News] Get useful information: [" + newinfo['title'] + "]")
			else:
				write_log(logfile,"[News] Get useless information: [" + newinfo['title'] + "]")

	write_log(logfile,"[News] " + str(len(news)) + ' news to send')

	return news

def configSectionMap(section,config):
	dict = {}
	for key in config.options(section):
		value = config.get(section,key)
		dict[key] = value
	return dict


def push(date = None):

	Config = ConfigParser.ConfigParser()
	Config.read('reminder-setting.conf')
	logfile = open('log.txt','a')

	sender = {
		'address': 'seiee.reminder@gmail.com',
		'name': 'SEIEE REMINDER',
		'key': 'seieereminder'
	}

	sender = configSectionMap('sender',Config)
	receivers_dic = configSectionMap('receivers',Config)
	receivers = receivers_dic['receivers'].split(',')

	write_log(logfile,'--------------------Task begin--------------------')
	write_log(logfile,'[Current Time]',True)
	write_log(logfile,'[Receivers]:')
	for i in range(0,len(receivers)):
		write_log(logfile,receivers[i])

	news = getInfo(logfile,date)
	send_email(sender,receivers,news)

	write_log(logfile,'[Current Time]',True)
	write_log(logfile,'--------------------Task finish--------------------\n')
	logfile.close()

if __name__ == '__main__':
	push()