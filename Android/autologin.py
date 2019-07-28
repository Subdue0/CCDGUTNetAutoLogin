#coding=utf-8




import os
import sys
# 外网登录密码加密模块
import base64
			# 第三方库
# 需用pip安装，pip install requests
import requests
# 需用pip安装，pip install pillow
from PIL import Image




LOG = []
IP = []




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
		# 验证码识别出结果后，删除图片
		os.remove(self.name)
		return code_str

				
	def identification(self):
		photo = self.code_photo_processing()
		number_list = self.each_number_feature()
		code_str = self.code_number_processing(photo, number_list)
		return code_str
	

		
		
class Login():
	def __init__(self, intranet_username, intranet_password, extranet_username, extranet_password):
		# 内网登录用户名及密码
		self.intranet_username = intranet_username
		self.intranet_password = intranet_password
		# 外网登录用户名及密码
		self.extranet_username = extranet_username
		self.extranet_password = extranet_password
		
		
	def connection_check(self):
		try:
			url = 'http://www.iqiyi.com/'
			headers = {
						'Host': 'www.iqiyi.com',
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
					}
			# allow_redirects=False不自动重定向
			response = requests.get(url, headers = headers, allow_redirects=False, timeout=1)
			# 302状态码，说明网络正常，等待认证登录，返回0或者1，0表示未通过内网认证，1表示通过内网认证
			if response.status_code == 302:
				# 获取Location的值
				values = response.headers['Location']
				if values == 'http://192.168.100.1':
					return 0
				else:
					return 1
			# 除了302状态码分状态，其余的状态码都原样返回
			else:
				return response.status_code
		# 服务器不响应异常处理
		except requests.ConnectionError:
			LOG.append('**Connection Error**\n')
			LOG.append('**Please check your WiFi connection, router wiring or IP settings!**\n')
			return -1
		# 设定在1s内收到响应，不然抛出ReadTimeout异常
		except requests.ReadTimeout:
			LOG.append('**Read Timeout**\n')
			return -1
		except:
			LOG.append('**Unknow Error**\n')
			return -1		
			

	def intranet_login(self):
		url = 'http://192.168.100.1/a70.htm'
		data = {'DDDDD':self.intranet_username,'upass':self.intranet_password,'R1':'0','0MKKey':'123456'}
		headers = {
					'Host': '192.168.100.1',
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
				}
		requests.post(url, data=data, headers = headers)

	
	def get_cookie(self, response):
		# 取cookie值
		values = response.headers['Set-Cookie']
		# 分割cookie值
		cookie_list = values.split(';')
		# 保留所需cookie值
		cookie = cookie_list[0]
		return cookie
		
		
	def get_image(self, response):
		with open('code.jpg','wb') as imgfile:
			imgfile.write(response.content)
			
			
	def request_identification_code(self):
		url = 'http://enet.10000.gd.cn:10001/common/image.jsp'
		headers = {
					'Host': 'enet.10000.gd.cn:10001',
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
				}				
		response = requests.get(url, headers = headers)
		cookie_str = self.get_cookie(response)
		# 下载验证码图片到本地
		self.get_image(response)
		c = Code('code.jpg')
		code_str = c.identification()
		return (cookie_str, code_str)
		
	def get_ip(self):
		url = 'http://www.iqiyi.com/'
		headers = {
					'Host': 'www.iqiyi.com',
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
				}
		# allow_redirects=False不自动重定向
		response = requests.get(url, headers = headers, allow_redirects=False)
		# 获取Location的值
		values = response.headers['Location']
		# 切割values值
		IP.append(values.split('=')[1].split('&')[0])
		IP.append(values.split('=')[2])
		return IP[0], IP[1]
		
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
		values = response.headers['Location']
		status = values.split('/')[3].split('.')[0]
		if status == 'success':
			return 1
		else:
			return 0
		
		
		
		
def login(intranet_username, intranet_password, extranet_username, extranet_password):
	l = Login(intranet_username, intranet_password, extranet_username, extranet_password)
	connection_status = l.connection_check()
	'''
########################################################################################
									需要登录
########################################################################################
	'''
	# 多数情况，没有进行内网认证和外网认证，等待内网认证和外网认证
	if connection_status == 0:
		l.intranet_login()
		connection_status = l.connection_check()
		# 内网认证通过，无需外网认证，网络已连通
		if connection_status == 200:
			LOG.append('Intranet login success!\n')
			LOG.append('Network is connected!\n')
			return 2
		 # 通过了内网认证，外网等待认证
		elif connection_status == 1:
			# 通过了内网认证，外网认证，网络已连通
			if l.extranet_login() == 1:
				LOG.append('Intranet login success!\n')
				LOG.append('Extranet login success!\n')
				LOG.append('Network is connected!\n')
				return 1
			# 通过了内网认证，外网认证账号或密码错误
			else:
				LOG.append('**Extranet login failed.**\n')
				LOG.append('**Your phone number or password error, please check!**\n')
				return 3
		# 内网认证失败，学号或者密码不对
		elif connection_status == 0:
			LOG.append('**Intranet login failed.**\n')
			LOG.append("**Your school number or password error, please check!**\n")
			return -1
		# 未知状态码的拦截
		else:
			LOG.append('**Server return unknown status code.**\n')
			return -1
	# 内网认证已经通过，等待外网认证
	elif connection_status == 1:
		if l.extranet_login() == 1:
			LOG.append('Extranet login success!\n')
			LOG.append('Network is connected!\n')
			return 1
		else:
			LOG.append('**Extranet login failed!**\n')
			LOG.append('**Your phone number or password error, please check!**\n')
			return -1
		'''
########################################################################################
									无需登录
########################################################################################
		'''
	# 网络正常
	elif connection_status == 200:
		LOG.append('Network is connected!\n')
		return 0
	# 网络不通，正常情况
	elif connection_status == 502:
		LOG.append('**The agent received an invalid response when it executed the request.**\n')
		return -1
	# 异常退出
	elif connection_status == -1:
		return -1
	# 特殊状态码的拦截
	else:
		LOG.append('**Server return '+str(connection_status)+'.**\n')
		return -1
		

	
		
if __name__=='__main__':
	pass
