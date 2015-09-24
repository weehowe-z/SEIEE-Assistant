# -*- coding:utf-8 -*- 
import xlwt #deal with excel
import xlrd
import urllib2

def getInfo(student_id):
	url_base = 'http://z.seiee.com/index.php/Score/search?sid='
	student_id_str = str(student_id)
	url = url_base + student_id_str
	try:
		page = urllib2.urlopen(url,timeout=1).read()
	except:
		return None


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

def dealXls():
	book = xlrd.open_workbook('content.xls')
	savebook = xlwt.Workbook(encoding = 'utf-8',style_compression=0)
	for i in range (0,10):
		sheet = book.sheet_by_index(i)
		print "now deal with major " + sheet.name
		savesheet =savebook.add_sheet(sheet.name,cell_overwrite_ok=True)
		savesheet.write(0,0,'序号'.decode('utf-8'))
		savesheet.write(0,1,'学号'.decode('utf-8'))
		savesheet.write(0,2,'专业'.decode('utf-8'))
		savesheet.write(0,3,'第一学期综合测评成绩'.decode('utf-8'))
		savesheet.write(0,4,'第二学期综合测评成绩'.decode('utf-8'))
		savesheet.write(0,5,'2014-15学年综合测评成绩'.decode('utf-8'))
		savesheet.write(0,6,'姓名'.decode('utf-8'))
		rows = sheet.nrows
		for i in range(1,rows):
			print "now deal with people " + str(i)
			savesheet.write(i,0,i)
			savesheet.write(i,1,sheet.cell_value(i,1))
			savesheet.write(i,2,sheet.cell_value(i,2))
			savesheet.write(i,3,sheet.cell_value(i,3))
			savesheet.write(i,4,sheet.cell_value(i,4))
			savesheet.write(i,5,sheet.cell_value(i,5))			
			info = getInfo(int(sheet.cell_value(i,1)))
			if info == None:
				savesheet.write(i,6,'unknown')
			else:
				savesheet.write(i,6,info[0])
	savebook.save('content(new).xls')
	return 0
	#book = xlwt.Workbook(encoding='utf-8',style_compression=0)
	sheet = book.add_sheet('test',cell_overwrite_ok=True)
	sheet.write(0,0,'姓名'.decode('utf-8'))
	sheet.write(0,1,'学号'.decode('utf-8'))
	sheet.write(0,2,'素拓'.decode('utf-8'))
	sheet.write(0,3,'排名'.decode('utf-8'))
	xpos = 0
	for i in range(0,800):
		print i
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
	dealXls()
