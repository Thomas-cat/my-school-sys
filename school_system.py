import requests
import re
import time
from PIL import Image
from threading import Thread
import pytesseract
import os
from bs4 import BeautifulSoup
from PrintTable import printtable
ua_agent = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
req = requests.Session()

login_url = 'http://211.68.152.100/loginAction.do'
logout_url = 'http://211.68.152.100/logout.do'
code_url = 'http://211.68.152.100/validateCodeAction.do'
xk_url = 'http://211.68.152.100/xkAction.do'
tk_url = 'http://211.68.152.100/xkAction.do?actionType=7'
xk_result_url = 'http://211.68.152.100/xkAction.do?actionType=6'
exam_day_url = 'http://211.68.152.100/ksApCxAction.do?oper=getKsapXx'
now_term_score_url = 'http://211.68.152.100/bxqcjcxAction.do'
oper_img_url = 'http://211.68.152.100/xjInfoAction.do?oper=img'
check_exam_url = 'http://211.68.152.100/ksApCxAction.do?oper=getKsapXx'
total_class = []
def select_class():
	num = input('请输入要选课序号:\n')
	for item in total_class:
		if num == item[0]:
			kcid = item[-1]
	if kcid == None:
		print ('序号有误')
	url = 'http://211.68.152.100/xkAction.do'
	data = {'kcId':kcid,'preActionType':'2','actionType':'9'}
	req.post(url,headers = ua_agent,data = data)
	print ('选课成功\n\n')
def check_class():
	url = 'http://211.68.152.100/xkAction.do?actionType=7'
	respon = req.get(url,headers = ua_agent)
	content = respon.content.decode('GBK')

	soup = BeautifulSoup(content,'lxml')
	a = soup.find('table',{'class':'titleTop2'})
	b = a.find_all('tr')
	
	v = b[1].find_all('th') or b[1].find_all('td')
	tmp = ['序号',v[2].string,v[3].string or v[3].find('a').string or v[3].find('a').get_text(),v[8].string,]
	table = printtable(tmp)
	class_table = []

	j = 1 
	for i in range(2,len(b)):
		v = b[i].find_all('th') or b[i].find_all('td')
		try:
			tmp = [str(j),v[2].string,v[3].string or v[3].find('a').string or v[3].find('a').get_text(),v[8].string,]
		except:
			continue	
		tmp = remove_sign(tmp)
		class_table.append(tmp)
		table.add_row(tmp)
		j +=1
	print (table)
	return class_table
def remove_class(class_table):
	num = input('请选择想要退选的课序号:\n')
	for item in class_table:
		if item[0] == num:
			kcid = item[1]
			break
	flag = input('是否真的删除该课?(y/n)\n')
	if flag == 'y' or flag == 'Y':
		url = 'http://211.68.152.100/xkAction.do?actionType=10&kcId=%s'%kcid
		req.get(url,headers = ua_agent)
		print ('退课成功\n\n')
def remove_sign(raw_list):
	tmp = []
	for text in raw_list:
		text = text.replace('\r','').replace('\t','').replace('\n','').strip()
		if len(text)>10:
			text = text[0:10]
		tmp.append(text)
	return tmp
def get_class():
	url = 'http://211.68.152.100/xkAction.do?actionType=-1&fajhh=13406'
	respon = req.get(url,headers = ua_agent)

	mode = input('1.方案课程\n2.校任选课\n')
	if mode == '1':
		url = 'http://211.68.152.100/xkAction.do?actionType=2&pageNumber=%d&oper1=ori'%1
	if mode == '2':
		url = 'http://211.68.152.100/xkAction.do?actionType=3&pageNumber=1'
	respon = req.get(url,headers = ua_agent)
	content = respon.content.decode('GBK')

	reg = re.compile(r'共(\d)页',re.S)
	count = int(reg.findall(content)[0])
	soup = BeautifulSoup(content,'lxml')
	a = soup.find('table',{'class':'titleTop2'})
	b = a.find_all('tr')
	
	v = b[1].find_all('th') or b[1].find_all('td')
	tmp = ['序号',v[2].string,v[3].string or v[3].find('a').string or v[3].find('a').get_text(),v[4].string,v[6].string,v[8].string,v[9].string]
	table = printtable(tmp)

	j = 1 

	for num in range(1,count+1):
		reg = re.compile(r'pageNumber=\d',re.S)
		url = reg.sub('pageNumber=%d'%num,url)
		respon = req.get(url,headers = ua_agent)
		content = respon.content.decode('GBK')

		soup = BeautifulSoup(content,'lxml')
		a = soup.find('table',{'class':'titleTop2'})
		b = a.find_all('tr')
		for i in range(2,len(b)):
			v = b[i].find_all('th') or b[i].find_all('td')
			try:
				if mode == '1':
					if v[0].find('input') == None:
						continue
				tmp = [str(j),v[2].string,v[3].string or v[3].find('a').string or v[3].find('a').get_text(),v[4].string,v[6].string,v[8].string,v[9].string]
			except:
				continue	
			tmp.append(tmp[1]+'_'+tmp[3])
			tmp = remove_sign(tmp)
			total_class.append(tmp)
			table.add_row(tmp[0:-1])
			j +=1
	print (table)
	auto_class(int(mode)+1)
	return table 
		
def auto_class(mode):
	tmp = []
	while True:
		a = input('请输入要添加自动抢课的课程序号(退出请输入-1):\n')
		if a =='-1':
			break 
		tmp.append(a)
		
	real_tmp = []
	try:
		for item in total_class:
			for num in tmp:
				if item[0] == num:
					print ('%s\t添加进抢课任务\n'%item[2])
					real_tmp.append([item[1]+'_'+item[3],item[2]])
					tmp.remove(num)
					continue
	except:
		pass
	while True:	
		if real_tmp == []:
			break
		for kcid in real_tmp:
			url = 'http://211.68.152.100/xkAction.do'
			data = {'kcId':kcid[0],'preActionType':str(mode),'actionType':'9'}
			respon = req.post(url,headers = ua_agent,data = data)
			content = respon.content.decode('GBK')
			soup = BeautifulSoup(content,'lxml')
			a = soup.find('strong').get_text()
			if a.find('没有课余量')!=-1:
				print (a)
			elif a.find('选择')!=-1:
				print (kcid[1]+': 该课不能选\n')
				real_tmp.remove(kcid)
			else:
				print (kcid[1]+': 已选上课\n')
				real_tmp.remove(kcid)
			time.sleep(3)	
		

def get_exam():
	respon = req.get(exam_day_url)
	html = respon.content.decode('GBK')
	soup = BeautifulSoup(html,'lxml')
	a = soup.find_all('table',{'id':'user'})[1]
	b = a.find_all('tr')
	for i in b:
		c = i.find_all('th')
		if c != []:
			c = ['{blue}'+item.string for item in c[0:-2]]
			table = printtable(c)
		else:
			c = i.find_all('td')
			c = [item.string for item in c[0:-2]]
			table.add_row(c)
	print (table)	

def convert_code():
	a = os.listdir('./code')
	for item in a:
		Image.open('./code/'+item).convert('L').save('./code/'+item)
def get_code():
	respon = req.get(url = code_url, headers = ua_agent)
	with open('check_code.jpg','wb') as f:
		f.write(respon.content)
	code = pytesseract.image_to_string(Image.open('check_code.jpg').convert('L'),lang = '001')
	return code 

def auto_login():
	code = get_code()
	while len(code) != 4:
		code = get_code()
	data = { 'zjh1':'',
		 'tips':'',
		 'lx':'',
		 'evalue':'',
		 'eflag':'',
		 'fs':'',
		 'dzslh':'',
		 'zjh':'201514570219',
		 'mm':'kangta123',
		 'v_yzm':code}
	try:
		respon = req.post(url = login_url, headers = ua_agent, data = data)
		text = respon.content.decode('GBK')
	except:
		return -1

	if text.find('学分制综合教务')!=-1:
		print ('登录成功')
		return 0
	elif text.find('URP 综合教务系统 - 登录')!=-1:
		print ('验证码或密码错误')
		return -1
	else:
		print ('登录失败,正在重新登录')
		return -1
def select_func():
	num = input('请选择功能序号:\n1.查看考试信息\n2.选课\n3.退课\n4.查询已选课表\n')
	if num == '1':
		get_exam()
	if num == '2':
		get_class()
	if num == '3':
		class_table = check_class()
		remove_class(class_table)
	if num == '4':
		check_class()

def main():
	flag = auto_login()
	while flag == -1:
		flag = auto_login()
	while True:
		select_func()
		print ('\n\n')
if __name__ == '__main__':
	main()



