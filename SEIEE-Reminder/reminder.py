# -*- coding:utf-8 -*- 
import smtplib,urllib2
import ConfigParser
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender, receivers, news):
	if len(news) == 0:
		return

	sender_add = sender['address']
	sender_name = sender['name']
	sender_key = sender['key']

	html_template = """
	<html>
	  <head></head>
	  <body>
		<p>
			<strong>##title##</strong> 已经在学生办网站发布了!
		</p>
		<p>
			原文链接 ---> ##url##
		</p>
		<p>
			------------------------------------
		</p>
			##content##
		<p>
			<br/>
		</p>
		<p>
			------------------------------------
		</p>
		<span><strong><small>&copy;<i>2015 SEIEE Reminder<i/></small></strong></span>&nbsp;&nbsp;&nbsp;	
		<span><small><i>Fork me on <a href="https://github.com/weehowe-z/littleProjects">GitHub</a></i></small></span>
	  </body>
	</html>
	"""

	#connect gmail server
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
		content = news[i]['content']

		msg = MIMEMultipart('alternative')
		msg['Subject'] = '【电院提醒】' + title
		msg['From'] = sender_name

		html = html_template.replace('##title##',title).replace('##url##',url).replace('##content##',content)
		msg.attach(MIMEText(html, 'html', 'utf-8'))

		for j in range(0,len(receivers)):
			del msg['To']
			msg['To'] = receivers[j]
			print "now send mail to " + receivers[j] + ' ' + str(len(receivers)*i+j+1) + '/' + str(len(news)*len(receivers))
			server.sendmail(sender_add,[receivers[j]],msg.as_string())
	
	server.quit()

# !!require further upgrade
def checkRelativity(title):
	keyword = ['研究生','硕士','博士']
	for i in range(0,len(keyword)):
		if title.find(keyword[i]) != -1 and title.find('本科') == -1:
			return False
	return True

def attachImages(content):
	url_base = 'http://xsb.seiee.sjtu.edu.cn'
	image_start = 0
	while True:
		image_start = content.find('<p><img id="showImage\"',image_start+1)
		if image_start == -1:
			break
		else:
			src_start = content.find('src',image_start)
			src_end = content.find('\"',src_start + 5)
			origin_image_url = content[src_start+5:src_end]
			image_url = url_base + origin_image_url.replace(';','&')
			content = content.replace(origin_image_url,image_url)
	return content

def attachFiles(content):
	url_base = 'http://xsb.seiee.sjtu.edu.cn'
	file_start = 0
	while True:
		file_start = content.find('<a href="/content/',file_start+1)
		if file_start == -1:
			break
		else:
			file_end = content.find('\"',file_start+9)
			origin_file_url = content[file_start+9:file_end]
			file_url = url_base + origin_file_url.replace(';','&')
			content = content.replace(origin_file_url,file_url)
	return content

# get news title, content, and url
def getNews(logfile,date = None):
	url = 'http://xsb.seiee.sjtu.edu.cn/xsb/index.htm'
	url_base = 'http://xsb.seiee.sjtu.edu.cn'
	news = []

	try:
		page = urllib2.urlopen(url,timeout=5).read()
	except:
		write_log(logfile,"[Error]Cannot access to website")
		print "[Error]Cannot access to website"
		return None

	#default date is current time
	if date == None:
		today = datetime.datetime.now().date()
		today_str = today.strftime('%Y-%m-%d')
	else:
		today_str = date
	
	spanpos = 0
	while True:
		startpos = page.find('<a title="',spanpos)
		if startpos == -1:#not find
			break
		spanpos = page.find('<span>',startpos)
		date = page[spanpos+7:spanpos+17]
		if date == today_str:
			hrefpos_start = page.find('href=',startpos)
			hrefpos_end = page.find('target=',startpos)
			href = page[hrefpos_start+6:hrefpos_end-2]
			title = page[startpos+10:hrefpos_start-2]
			info_url = url_base + href

			content_page = urllib2.urlopen(info_url,timeout=5).read()
			content_start = content_page.find('<p>',0)
			content_end = content_page.find('<script>',content_start)
			content = content_page[content_start:content_end-1]
			content = attachImages(content)
			content = attachFiles(content)

			newinfo = {}
			newinfo['title'] = title
			newinfo['url'] = info_url
			newinfo['content'] = content

			if checkRelativity(title) == True:
				news.append(newinfo)
				write_log(logfile,"[News] Get useful information: [" + newinfo['title'] + "]")
			else:
				write_log(logfile,"[News] Get useless information: [" + newinfo['title'] + "]")
	return news

# map conf sections into library
def configSectionMap(section,config_path):
	Config = ConfigParser.ConfigParser()
	Config.read(config_path)
	dict = {}
	for key in Config.options(section):
		value = Config.get(section,key)
		dict[key] = value
	return dict

def write_log(logfile,string,need_time = False):
	if need_time == False:
		logfile.write(string+'\n')
	else:
		time = datetime.datetime.now()
		time_str = time.strftime('%Y-%m-%d %H:%M:%S')
		logfile.write(string + '\t' + time_str +'\n')

def push(date = None):

	logfile = open('log.txt','a')

	sender = configSectionMap('sender','setting.conf')
	receivers_dic = configSectionMap('receivers','setting.conf')
	receivers = receivers_dic['receivers'].split(',')

	write_log(logfile,'--------------------Task begin--------------------')
	write_log(logfile,'[Current Time]',True)
	write_log(logfile,'[Receivers]:')
	for i in range(0,len(receivers)):
		write_log(logfile,receivers[i])

	news = getNews(logfile,date)
	send_email(sender,receivers,news)

	write_log(logfile,'[Current Time]',True)
	write_log(logfile,'--------------------Task finish--------------------\n')
	logfile.close()

if __name__ == '__main__':
	push()