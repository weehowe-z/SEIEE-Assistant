# -*- coding:utf-8 -*- 
import smtplib,urllib,urllib2,ConfigParser,datetime,requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

url_base = 'http://xsb.seiee.sjtu.edu.cn'
intern_url_base = 'http://xsb.seiee.sjtu.edu.cn/xsb/list/2496-1-20.htm'
fulltime_url_base = 'http://xsb.seiee.sjtu.edu.cn/xsb/list/2495-1-20.htm'
page_url_template = 'http://xsb.seiee.sjtu.edu.cn/xsb/detail/id.htm?nocache=1'

data_url = 'https://leancloud.cn/1.1/classes/fulltimes'
data_headers = {'Content-Type': 'application/json',
				'X-LC-Id': 'BH1ggDkDzqXkdREQpWjoGjOp',
				'X-LC-Key': 'h0vTbVQmrAN7pWV7XTqckLcP'
				}


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
		</p>
			##content##
		<p>
			<br/>
		</p>
		<p>
			------------------------------------
		</p>
		<span><strong><small>&copy;<i>2015 SEIEE Reminder<i/></small></strong></span>&nbsp;&nbsp;&nbsp;	
		<span><small><i><a href="http://blog.delvin.xyz">Contact me</a></i></small></span>
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
		msg['Subject'] = '【全职招聘】' + title
		msg['From'] = sender_name

		html = html_template.replace('##content##',content)
		msg.attach(MIMEText(html, 'html', 'utf-8'))

		for j in range(0,len(receivers)):
			del msg['To']
			msg['To'] = receivers[j]
			print "now send mail to " + receivers[j] + ' ' + str(len(receivers)*i+j+1) + '/' + str(len(news)*len(receivers))
			server.sendmail(sender_add,[receivers[j]],msg.as_string())
	
	server.quit()

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
def getAllInfo():
	url = fulltime_url_base
	infos = []
	try:
		page = urllib2.urlopen(url,timeout=5).read()
	except:
		print "[Error]Cannot access to website"
		return None
	currentPos = 0
	while True:
		startpos = page.find('<li><span>',currentPos)
		if startpos == -1:#not find
			break
		#get unique id
		idStartPos = page.find('/detail',startpos)
		idEndPos = page.find('.htm',idStartPos)
		id = page[idStartPos + len('/detail') + 1:idEndPos]
		
		#check id valid
		query = "{\"specid\": \""+ id +"\"}"
		para =  {'where': query } 
		x = requests.get(url= data_url, headers = data_headers, params = para, timeout = 10)

		if len(x.json()['results']) != 0:
			currentPos = idEndPos
			continue
		
		titleStartPos = page.find('title',idEndPos)
		titleEndPos = page.find('target',titleStartPos)
		title = page[titleStartPos + len('title') + 2:titleEndPos-2]


		page_url = page_url_template.replace("id",id)
		
		content_page = urllib2.urlopen(page_url,timeout=5).read()
		content_start = content_page.find('<p>',0)
		content_end = content_page.find('<p style',content_start)
		content = content_page[content_start:content_end-1]

		content = attachImages(content)
		content = attachFiles(content)

		newinfo = {}
		newinfo['title'] = title
		newinfo['content'] = content
		newinfo['url'] = page_url
		newinfo['specid'] = id
		infos.append(newinfo)
		
		#save news
		requests.post(url= data_url, json = newinfo, headers = data_headers, timeout = 10)

		currentPos = idEndPos
		
	return infos

# map conf sections into library
def configSectionMap(section,config_path):
	Config = ConfigParser.ConfigParser()
	Config.read(config_path)
	dict = {}
	for key in Config.options(section):
		value = Config.get(section,key)
		dict[key] = value
	return dict

def push():


	sender = configSectionMap('sender','setting.conf')
	receivers_dic = configSectionMap('receivers','setting.conf')
	receivers = receivers_dic['receivers'].split(',')

	infos = getAllInfo()
	send_email(sender,receivers,infos)


if __name__ == '__main__':
	push()