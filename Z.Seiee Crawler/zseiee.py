# -*- coding:utf-8 -*- 
import xlwt #deal with excel
import urllib2

def getInfo(student_id):
	url_base = 'http://z.seiee.com/index.php/Score/search?sid='
	student_id_str = str(student_id) 
	if len(student_id_str) == 1:
		student_id_str = '00'+student_id_str
	elif len(student_id_str) == 2:
		student_id_str = '0' + student_id_str
	url = url_base + '5130309'+ student_id_str
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

	return [name,id,mark,rank]

def createXls():
	book = xlwt.Workbook(encoding='utf-8',style_compression=0)
	sheet = book.add_sheet('test',cell_overwrite_ok=True)
	sheet.write(0,0,'name')
	sheet.write(0,1,'id')
	sheet.write(0,2,'mark')
	sheet.write(0,3,'rank')
	xpos = 0
	for i in range(0,800):
		if i != 172 and i !=271 and i != 493:
			info = getInfo(i)
			if info != None:
				print 'deal ' + str(i)
				xpos = xpos +1
				sheet.write(xpos,0,info[0])
				sheet.write(xpos,1,info[1])
				sheet.write(xpos,2,info[2])
				sheet.write(xpos,3,info[3])
	book.save('studentInfo.xls')



if __name__ == '__main__':
	createXls()