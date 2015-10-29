  #!/usr/bin/python
  #coding:utf-8
import requests, json

url="http://sendcloud.sohu.com/webapi/mail.send.json"
html = """
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
   
  # 不同于登录SendCloud站点的帐号，您需要登录后台创建发信子帐号，使用子帐号和密码才可以进行邮件的发送。
params = {"api_user": "DelvinZhuAtSendCloud", \
    "api_key" : "sHLR8fEMR1M5cPs2",\
    "from" : "reminder@mail.delvin.xyz", \
    "fromname" : "Reminder", \
    "to" : "575877982@qq.com", \
    "subject" : "ceshi！", \
    "html": html, \
    "resp_email_id": "true"
}
  
r = requests.post(url, files={}, data=params)
print r.text