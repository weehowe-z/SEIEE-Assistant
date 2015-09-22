# -*- coding:utf-8 -*- 

import urllib2
def getInfo(student_id):
	url_base = 'http://z.seiee.com/index.php/Score/search?sid='
	url = url_base + '5130309'+str(student_id)
	page = urllib2.urlopen(url).read()

	name_start = page.find('<td width="70%">',0)
	if name_start == -1:
		return None
	name_end = page.find('</td>',name_start)
	id_start = page.find('<td width="70%">',name_end)
	id_end = page.find('</td>',id_start)
	mark_start = page.find('<span class="badge badge-info">',id_end)
	mark_end = page.find('</span>',mark_start)
	rank_start = page.find('<span class="badge badge-info">',mark_end)
	rank_end = page.find('</span>',rank_start)

	name = page[name_start+16:name_end]
	name = name.decode('utf-8')
	id = page[id_start+16:id_end]
	mark = page[mark_start+31:mark_end]
	rank = page[rank_start+31:rank_end]

	return name,id,mark,rank

#print data
if __name__ == '__main__':
	for i in range(100,730):
		if i != 172 and i != 493: 
			print getInfo(i)
#	print getInfo(172)