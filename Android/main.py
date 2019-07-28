#coding=utf-8



# 登录模块
import autologin
# kivy模块
from kivy.app import App
from kivy.uix.widget import Widget
# 数据存储
from kivy.storage.jsonstore import JsonStore
# 注册中文
from kivy.core.text import LabelBase
LabelBase.register(name='Roboto',fn_regular='fonts/droid.ttf')
# 虚拟键盘始终低于目标控件
from kivy.core.window import WindowBase
WindowBase.softinput_mode='below_target'
# 使用平台的检测
from kivy.utils import platform
if platform == 'android':
	# python调用JAVA类的安卓API
	from jnius import autoclass, cast



# 根控件类
class RootWidget(Widget):
	def __init__(self, **kwargs):
		# RootWidget继承Widget
		super(RootWidget, self).__init__(**kwargs)
		


# CCDGUTApp继承APP
class CCDGUTApp(App):
	# 创建并返回根控件
	def build(self):
		self.store = JsonStore('info.json')
		self.read_info()
		return RootWidget()

	# 判断当前用户的输入是否和之前存储的数据相同
	def is_same(self):
		if self.schoolnumber == self.root.schoolnumber.text:
			if self.password1 == self.root.password1.text:
				if self.phonenumber == self.root.phonenumber.text:
					if self.password2 == self.root.password2.text:
						return True
		return False
	
	# 从配置文件中读取信息
	def read_info(self):
		# 通过检测存储数据查看之前是否保存过密码
		try:
			self.schoolnumber = self.store.get('Intranet')['SchoolNumber']
			self.password1 = self.store.get('Intranet')['Password']
			self.phonenumber = self.store.get('Extranet')['PhoneNumber']
			self.password2 = self.store.get('Extranet')['Password']
		except:
			self.schoolnumber = ''
			self.password1 = ''
			self.phonenumber = ''
			self.password2 = ''
		# 启动APP时，发包检测网络状态，初始化显示
		l = autologin.Login(self.schoolnumber, self.password1, self.phonenumber, self.password2)
		status = l.connection_check()
		if status == 200:
			self.light = 'images/connected.png'
			self.network_status = '网络连通'
		else:
			self.light = 'images/disconnected.png'
			self.network_status = '网络断开'
		# 通过检测存储数据查看是否可以更改密码
		try:
			self.wlanuserip = self.store.get('IP')['IP1']
			self.wlanacip = self.store.get('IP')['IP2']
			self.change_password_status = False
			self.strikethrough = False
		except:
			self.change_password_status = True
			self.strikethrough = True
	
	# 存储账号密码
	def store_info(self):
		self.store.put('Intranet', SchoolNumber=self.root.schoolnumber.text, Password=self.root.password1.text)
		self.store.put('Extranet', PhoneNumber=self.root.phonenumber.text, Password=self.root.password2.text)
		
	# 登录按钮的方法实现
	def login(self):
		# 按下按钮的微震动
		if self.root.login.state == 'down':
			if platform == 'android':
				Context = autoclass('android.content.Context')
				PythonActivity = autoclass('org.kivy.android.PythonActivity')
				vibrator = PythonActivity.mActivity.getSystemService(Context.VIBRATOR_SERVICE)
				vibrator.vibrate(100)
			
		if self.root.login.state == 'normal':
			# 查看当前输入框内容和之前是否相同
			if self.is_same() != True:
				self.store_info()
			l = autologin.login(self.root.schoolnumber.text, self.root.password1.text, self.root.phonenumber.text, self.root.password2.text)
			# 改变连接状态
			if l == 0 or l == 1 or l == 2:
				self.root.mylabel.light = 'images/connected.png'
				self.root.mylabel.network_status = '网络连通'
			else:
				self.root.mylabel.light = 'images/disconnected.png'
				self.root.mylabel.network_status = '网络断开'
				
			# 返回1, 2表示登录成功，(调用安卓振动器)震动
			if l == 1 or l == 2:
				if platform == 'android':
					Context = autoclass('android.content.Context')
					PythonActivity = autoclass('org.kivy.android.PythonActivity')
					vibrator = PythonActivity.mActivity.getSystemService(Context.VIBRATOR_SERVICE)
					vibrator.vibrate(1000)
					
			# 返回1, 3表示可以改密码
			if l == 1 or l == 3:
				self.store.put('IP', IP1 = autologin.IP[0], IP2 = autologin.IP[1])
				self.wlanuserip = self.store.get('IP')['IP1']
				self.wlanacip = self.store.get('IP')['IP2']
				self.root.mylabel.change_password_status = False
				self.root.mylabel.strikethrough = False
		
	# 修改密码方法的实现
	def change_password(self):
		if platform == 'android':
			PythonActivity = autoclass('org.kivy.android.PythonActivity')
			Uri = autoclass('android.net.Uri')
			Intent = autoclass('android.content.Intent')
			currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
			uri = Uri.parse('http://enet.10000.gd.cn:10001/?wlanuserip={wlanuserip}&wlanacip={wlanacip}'.format(wlanuserip=self.wlanuserip, wlanacip=self.wlanacip))
			intent  = Intent(Intent.ACTION_VIEW, uri)
			currentActivity.startActivity(intent)




if __name__ == '__main__':
	CCDGUTApp().run()