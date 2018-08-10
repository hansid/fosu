import requests
from lxml import etree
from urllib import request
from http import cookiejar
import re
from bs4 import BeautifulSoup
import os
import base64
end = os.path.exists("C:/dont_delete.txt")#获取txt文件中的帐号密码，如果没有，要求输入
if end == True:
	f = open('C:/dont_delete.txt',encoding='utf-8')
	secret = f.read()
	f.close()
else:
	print('第一次登录需要验证')
	number = input('学号：')
	key = input('密码（密码和学号将会保存在C盘的dont_delete.txt中）：')
	str_encrypt=number+key
	base64_encrypt = base64.b64encode(str_encrypt.encode('utf-8'))
	f = open(r'C:/dont_delete.txt','w',encoding='utf-8')  #文件路径、操作模式、编码  # r''
	f.write(str(base64_encrypt, encoding = "utf-8"))
	f.close()


headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
url = 'http://123.207.32.179/jsxsd/xk/LoginToXk'
req = requests.get(url,headers=headers)
req.encoding = 'gbk'
item = input('请输入学期(举例：大二第一个学期为3，所有学期请输入0）')#选择学期
if item == 0:
	t= ''
elif item =='1':
	t= '2016-2017-1'
elif item =='2':
	t= '2016-2017-2'
elif item =='3':
	t= '2017-2018-1'
elif item =='4':
	t= '2017-2018-2'
elif item =='5':
	t= '2018-2019-1'
elif item =='6':
	t= '2018-2019-2'
elif item =='7':
	t= '2019-2020-1'
elif item =='8':
	t= '2019-2020-2'
else:
	t = ''
params = {
'kksj':t,
'kcxz':'',
'kcmc':'',
'xsfs':'all'
}
html =requests.post(url,params)
def getcookie():#获取cookies，为下步做准备
	data={'encoded':'MjAxNjA3MTA0MzU=%%%MzQ5Mzc0OTBneWg='}
	session=requests.session()
	loginurl="http://123.207.32.179/jsxsd/xk/LoginToXk"
	#具体要接口登录后才可以获得cookies
	result=session.post(loginurl,data=data)
	#print(result.text)
	cookies=requests.utils.dict_from_cookiejar(session.cookies)
	cookies1=str(cookies)
	a = cookies1.strip('}')
	b = a.strip('{')
	c = re.sub(':','=',b)
	d = re.sub("'",'',c)
	e = re.sub(' ','',d)
	return e
def headers():
	headers1 = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.9',
	'Cache-Control':'max-age=0',
	'Connection':'keep-alive',
	'Content-Length':'26',
	'Content-Type':'application/x-www-form-urlencoded',
	'Cookie':getcookie(),
	'Host':'123.207.32.179',
	'Origin':'http://123.207.32.179',
	'Referer':'http://123.207.32.179/jsxsd/kscj/cjcx_query',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36' 
	}
	return headers1

def getnames():#获取课程名称
	url1 = 'http://123.207.32.179/jsxsd/kscj/cjcx_list'
	html1 = requests.post(url1,params,headers = headers())
	names = re.findall('<td align="left">(.*?)</td>',html1.text,re.S)
	return names

def getscores():#获取课程成绩
	url2 = 'http://123.207.32.179/jsxsd/kscj/cjcx_list'
	html2 = requests.post(url2,params,headers = headers())
	scores = re.findall('(\d+)</a>',html2.text,re.S)
	return scores

def getlinks():#获取详细成绩的链接
	url3 = 'http://123.207.32.179/jsxsd/kscj/cjcx_list'
	html1 = requests.post(url3,params,headers = headers())
	links =re.findall('<a href="javascript:openWindow(''(.*?)'',700,500)',html1.text,re.S)
	for link in links :
		a = re.findall("'/(.*?)',",str(link),re.S)
		b = a[0].strip(']')
		c = 'http://123.207.32.179/'+b
	return links


def getmorescore(url):#获取详细成绩的详情
	url4 = url
	html4 = requests.post(url4,params,headers = headers())
	morescore = re.findall('<td>(.*?)</td>',html4.text,re.S)
	return morescore	

def deallink(linkx):#构建详细成绩的链接
	xlink = re.findall("'/(.*?)',",str(linkx),re.S)
	aa = xlink[0].strip(']')
	url2 = 'http://123.207.32.179/'+aa
	return url2
def dealmorescore(score):#整理好详细成绩，输出算式
	num = len(score)
	turescores = []
	for x in range(num):
		b = score[x].strip(']')
		turescores.append(b)
	if num == 2:
		equal = turescores[1]+'*100%='+turescores[1]
	else:
		equal = turescores[1]+'*'+turescores[2]+'+'+turescores[3]+'*'+turescores[4]+'+'+turescores[5]+'*'+turescores[6]+'='+turescores[7]
	return(equal)



if __name__ == '__main__':
	#print(getnames())
	#print(getscores())
	#print(getlinks())
	#print(deallink(getlinks()[0]))
	#print(getmorescore(deallink(getlinks()[0])))
	#dealmorescore(getmorescore(deallink(getlinks()[0])))



	try:
		m = len(getscores())
		names = getnames()
		scores = getscores()
		lists = []
		for x in range(m):
			a = m-x-1
			lists.append(a)
		for x in lists:
			print(names[x*2+1],'      ',scores[x],'     ',dealmorescore(getmorescore(deallink(getlinks()[x]))))
	except : ConnectionResetError#我测试时经常会网络有问题
	pass 
    # 处理异常

os.system('pause')





#JSESSIONID=48F757A5FB3349431539CAFAB4766F5F
#<a href="javascript:openWindow('/jsxsd/kscj/pscj_list.do?xs0101id=20160710435&amp;jx0404id=201720182002554&amp;zcj=77',700,500)">77</a>