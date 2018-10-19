#coding:utf-8


# requests需用pip安装，pip install requests
import requests
import shutil
import os
import time
# 数据读取模块
import linecache
# 外网登录密码加密模块
import base64
# PIL需用pip安装，pip install pillow
from PIL import Image
import http.cookiejar, urllib.request
# 导入异常处理模块
from requests.exceptions import ReadTimeout, ConnectionError


class Code():
	def __init__(self, name):
		self.name = name
		
	
	def import_code_photo(self):
		
		img = Image.open(self.name)
		return img

		
	def code_photo_processing(self):
		img = self.import_code_photo()
		# 模式L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
		Img = img.convert('L')

		# 自定义灰度界限（阈值0~255）
		threshold = 180
		table = []
		for i in range(256):
			if i < threshold:
				table.append(0)
			else:
				table.append(1)

		# 图片二值化
		photo = Img.point(table, '1')
		return photo
		

	def each_number_feature(self):
		# 单个验证码数字（0-9）验证码二值化
		number_list = [
						# 数字0，第一个位置，y（3,16）x（7,16）
						[1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,0,1,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0,1,0,0,1,1,1,0,0,1,1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1],
						# 数字1，第一个位置，y（3,16）x（7,16）
						[1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
						# 数字2，第二个位置，y（3,16）x（20,29）
						[1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
						# 数字3，第三个位置，y（3,16）x（33,42）
						[1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,0,1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1],
						# 数字4，第四个位置，y（3,16）x（46,55）
						[1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,1,0,0,1,1,1,1,0,0,1,0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1],
						# 数字5，第三个位置，y（3,16）x（33,42）
						[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,0,1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1],
						# 数字6，第二个位置，y（3,16）x（20,29）
						[1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,1,0,0,1,1,1,1,0,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,1,0,1,1,1,1,1,0,0,1,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1],
						# 数字7，第三个位置，y（3,16）x（33,42）
						[1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1],
						# 数字8，第四个位置，y（3,16）x（46,55）
						[1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0,1,1,0,0,0,1,1,0,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,0,0,1,1,0,0,0,1,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1],
						# 数字9，第一个位置，y（3,16）x（7,16）			
						[1,1,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,1,1,0,0,1,1,1,0,0,1,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1]
					]
		return number_list

				
	def code_number_processing(self, photo, number_list):
		pixel_position_list = [[7,16],[20,29],[33,42],[46,55]]
		code_list = []
		# 四次循环，每一次处理一个验证码数字
		for i in range(4):
			# 四个验证码未知数字
			unknown_number = []
			for y in range(3, 16):
				for x in range(pixel_position_list[i][0], pixel_position_list[i][1]):
					unknown_number.append(photo.getpixel((x,y)))		
			# 从0到9遍历每个数字的特征
			for	row in range(10):
				count = 0
				# 117为每个验证码数字所占最大的面积点
				for col in range(117):
					if unknown_number[col] == number_list[row][col]:
						count += 1
				# 105为相似度，117就是100%相似
				if count > 105:
					code_list.append(str(row))
		# 将列表中的验证码转换成字符串
		code_str = ''.join(code_list)
		if len(code_str) != 4:
			print('**Verification code automatically identifies the error!**')
			print('**Please contact the author by VX:JU1374700812 or e-mail:1374700812@qq.com!**')
			os.system('pause')
			exit(-1)
		# 验证码识别出结果后，删除图片
		os.remove(self.name)
		return code_str

				
	def identification(self):
		photo = self.code_photo_processing()
		number_list = self.each_number_feature()
		code_str = self.code_number_processing(photo, number_list)
		return code_str
	

		
		
class Login():
	def __init__(self, intranet_username, intranet_password, extranet_username, extranet_password, PATH):
		self.PATH = PATH
		# 内网登录用户名及密码
		self.intranet_username = intranet_username
		self.intranet_password = intranet_password
		# 外网登录用户名及密码
		self.extranet_username = extranet_username
		self.extranet_password = extranet_password
		
		
	def intranet_login(self):
		url = 'http://10.20.208.198/a70.htm'
		data = {'DDDDD':self.intranet_username,'upass':self.intranet_password,'R1':'0','0MKKey':'123456'}
		headers = {
					'Host': '10.20.208.198',
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
				}
		requests.post(url, data=data, headers = headers)

		
	def intranet_login_check(self):
		while True:
			try:
				url = 'http://www.qq.com/'
				headers = {
							'Host': 'www.qq.com',
							'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
						}
				# allow_redirects=False不自动重定向
				response = requests.get(url, headers = headers, allow_redirects=False, timeout=3)
				# 重定向302都返回0或者1
				if response.status_code == 302:
					# 获取Location的值
					values = response.headers['Location']
					if values == 'http://10.20.208.198':
						return 0
					else:
						return 1
				# 网络连通200或服务器未响应502或其他异常情况返回0
				else:
					return 0
			# 服务器不响应异常处理
			except ConnectionError:
				print('**Connection Error**')
				print('**Server not responding!**')
				print('\n')
				time.sleep(5)
			# 设置必须在3s内收到响应，不然抛出ReadTimeout异常
			except ReadTimeout:
				print('**Read Timeout**')
				print('\n')
				time.sleep(5)
			except:
				print('**An Unknow Error Happened**')
				print('\n')
				time.sleep(5)
			
	
	def get_cookie(self, response):
		# 取cookie值
		values = response.headers['Set-Cookie']
		# 分割cookie值
		cookie_list = values.split(';')
		# 保留所需cookie值
		cookie = cookie_list[0]
		return cookie

		
	def get_image(self, response):
		with open(PATH+'code.jpg','wb') as imgfile:
			imgfile.write(response.content)
			
			
	def request_identification_code(self):
		url = 'http://enet.10000.gd.cn:10001/common/image.jsp'
		headers = {
					'Host': 'enet.10000.gd.cn:10001',
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
				}				
		response = requests.get(url, headers = headers, timeout=3)
		if response.status_code == 200:
			cookie_str = self.get_cookie(response)
			# 下载验证码图片到本地
			self.get_image(response)
			c = Code(PATH+'code.jpg')
			code_str = c.identification()
			return (cookie_str, code_str)
		else:
			print('**Request code image failed!**')
			os.system('pause')
			exit(-1)
		
		
	def get_ip(self):
		url = 'http://www.qq.com/'
		headers = {
					'Host': 'www.qq.com',
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
				}
		# allow_redirects=False不自动重定向
		response = requests.get(url, headers = headers, allow_redirects=False)
		# 获取Location的值
		values = response.headers['Location']
		# 切割values值
		wlanuserip = values.split('=')[1].split('&')[0]
		wlanacip = values.split('=')[2]
		return (wlanuserip, wlanacip)
		
		
	def extranet_login(self):
		url = 'http://enet.10000.gd.cn:10001/login.do'
		encodestr = base64.b64encode(str(self.extranet_password).encode()).decode()
		cookie, code = self.request_identification_code()
		eduuser, edubas = self.get_ip()
		data = {'userName1':self.extranet_username,'password1':encodestr,'rand':code,'eduuser':eduuser,'edubas':edubas}
		headers = {
					'Host': 'enet.10000.gd.cn:10001',
					'Content-Type': 'application/x-www-form-urlencoded',
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
					'Cookie': cookie
				}
		response = requests.post(url, data=data, headers = headers, allow_redirects=False)
		return response
		
		
	def extranet_login_check(self):
		response = self.extranet_login()
		values = response.headers['Location']
		status = values.split('/')[3].split('.')[0]
		if status == 'success':
			return 1
		else:
			return 0
				
		
	def connectivity_test(self):
		while True:
			try:
				url = 'http://www.qq.com/'
				headers = {
							'Host': 'www.qq.com',
							'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
						}
				
				response = requests.get(url, headers = headers, allow_redirects=False, timeout=3)
				return response.status_code
			# 服务器不响应异常处理
			except ConnectionError:
				print('**Connection Error**')
				print('**Server not responding!**')
				print('\n')
				time.sleep(5)
			# 设置必须在3s内收到响应，不然抛出ReadTimeout异常
			except ReadTimeout:
				print('**Read Timeout**')
				print('\n')
				time.sleep(5)
			except:
				print('**An Unknow Error Happened**')
				print('\n')
				time.sleep(5)
			
		

		
def main(intranet_username, intranet_password, extranet_username, extranet_password, PATH):
	l = Login(intranet_username, intranet_password, extranet_username, extranet_password, PATH)
	'''
	intranet_login_check,返回0表示网络连通或未通过内网认证或服务器未响应或其他异常情况，
	返回1表示直接进行外网认证
	'''
	if l.intranet_login_check() == 0:
		# 网络正常
		if	l.connectivity_test() == 200:
			print('Network is connected!')
			os.system('pause')
		# 网络不通，正常情况
		elif l.connectivity_test() == 302:
			l.intranet_login()
			# 内网认证之后给服务器一点反应时间，不然速度太快，会出现无key值‘Location’的报错
			time.sleep(1)
			# 访问腾讯首页无重定向
			if l.connectivity_test() == 200:
				print('Intranet login success!')
				print('Network is connected!')
				os.system('pause')
			# 访问腾讯首页重定向
			elif l.connectivity_test() == 302:
				# 通过腾讯首页返回的Location值判断内网是否登录成功
				if l.intranet_login_check() == 1:
					print('Intranet login success!')
					if l.extranet_login_check() == 1:
						print('Extranet login success!')
						print('Network is connected!')
						os.system('pause')
					else:
						print('**Extranet login failed!**')
						print('**Your phone number or password error, please check!**')
						os.system('pause')
				else:
					print('**Intranet login failed!**')
					print('**Your school number or password error, please check!**')
					os.system('pause')
			# 出现异常状况的处理
			else:
				print("**Unknown error occurred when visiting Tencent's homepage!**")
				os.system('pause')
		# 服务器出错响应，返回503
		elif l.connectivity_test() == 503:
			print('**Connection Error**')
			print('**Server error response, return 503"!**')
			print('\n')
			time.sleep(5)
			main(intranet_username, intranet_password, extranet_username, extranet_password, PATH)
		# 网络不通，异常情况
		else:
			print('**Intranet login unknown error!**')
			print('\n')
			time.sleep(5)
			main(intranet_username, intranet_password, extranet_username, extranet_password, PATH)
	else:
		if l.extranet_login_check() == 1:
			print('Intranet login success!')
			print('Extranet login success!')
			print('Network is connected!')
			os.system('pause')
		else:
			print('**Extranet login failed!**')
			print('**Your phone number or password error, please check!**')
			os.system('pause')
			

def get_content(PATH):
	if os.path.exists(PATH+'info.txt') == True:
		username1 = "".join(linecache.getline(PATH+'info.txt', 12).split())
		password1 = "".join(linecache.getline(PATH+'info.txt', 14).split())
		username2 = "".join(linecache.getline(PATH+'info.txt', 16).split())
		password2 = "".join(linecache.getline(PATH+'info.txt', 18).split())
		delay = int("".join(linecache.getline(PATH+'info.txt', 27).split()))
		linecache.clearcache()
		if len(username1) != 12 or len(username2) != 11:
			print('**In line 12 or line 16 of the file "info.txt"!**')
			print("**The data's length is not right,please check!**")
			os.system('pause')
			exit(-1)
		return (username1, password1, username2, password2, delay)
	else:
		print('**Can\'t find the file "info.txt" under the current path!**')
		os.system('pause')
		exit(-1)

		
if __name__=='__main__':
	PATH = './'
	username1, password1, username2, password2, delay = get_content(PATH)
	if delay == 0:
		main(username1, password1, username2, password2, PATH)
	else:
		for i in range(delay, -1, -1):
			print('Please wait', i, 'seconds...')
			time.sleep(1)
			null = os.system('cls')
		main(username1, password1, username2, password2, PATH)
