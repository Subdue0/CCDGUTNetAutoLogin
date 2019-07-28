#coding=utf-8




# 导入windows模块，用于控制注册表
import win32api
import win32con
# 自定义自动登录模块
import autologin
# 导入kivy的相关模块，用于UI绘制
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
# kivy的数据存储功能，用于保存数据
from kivy.storage.jsonstore import JsonStore
from kivy.core.text import LabelBase
# 导入字体
LabelBase.register(name='Roboto',fn_regular='fonts/Roboto-Regular.ttf', fn_bold='fonts/Houschka Rounded Alt Extra Bold Italic.ttf')





# kivy的UI代码
Builder.load_string('''
#:kivy 1.10.1


<RootWidget>:


	# 属性和控件id捆绑，以便调用
	schoolnumber: schoolnumber
	password1: password1
	phonenumber: phonenumber
	password2: password2
	autorun: autorun
	remember_account: remember_account
	login: login
	log: log
	
	
	canvas:
		Rectangle:
			source: 'images/background.png'
			size: root.size
			pos: root.pos
	BoxLayout:
		orientation: 'vertical'
		padding: 120, 30, 120, 30
		pos: root.pos
		size: root.size
		BoxLayout:
			size_hint_y: .27
			BoxLayout:
				size_hint_x: .4
				Label:
					size_hint_x: .1
				Label:
					size_hint_x: .8
					canvas:
						Rectangle:
							source: 'images/cartoon.png'
							size: self.size
							pos: self.pos
				Label:
					size_hint_x: .1
			GridLayout:
				size_hint_x: .6
				cols: 2
				MyLabel:
					text: 'School Number:'
				MyTextInput:
					id: schoolnumber
					hint_text: '201835012338'
					text: app.schoolnumber
				MyLabel:
					text: 'Password:'
					markup: True
				MyTextInput:
					id: password1
					hint_text: '195233'
					text: app.password1
				MyLabel:
					text: 'Phone Number:'
				MyTextInput:
					id: phonenumber
					hint_text: '17722312656'
					text: app.phonenumber
				MyLabel:
					text: 'Password:'
					markup: True
				MyTextInput:
					id: password2
					hint_text: 'Ab123456'
					text: app.password2
		BoxLayout:
			size_hint_y: .1
			CheckBox:
				id: autorun
				size_hint_x: .1
				color: .3, .43, .93, 1
				active: app.checkbox1_status
				on_active: app.autorun()
			Label:
				size_hint_x: .2
				text: 'Autorun'
				text_size: self.width, None
				color: 0, 0, 0, 1
				halign: 'left'
			CheckBox:
				id: remember_account
				size_hint_x: .1
				color: .3, .43, .93, 1
				active: app.checkbox2_status
				on_active: app.remember_account()
			Label:
				size_hint_x: .3
				text: 'Remember account'
				text_size: self.width, None
				color: 0, 0, 0, 1
				halign: 'left'
			Label:
				size_hint_x: .3
				text: '[ref=change_passwd]Change password?[/ref]'
				text_size: self.width, None
				color: 0, 0, 0, 1
				halign: 'right'
				markup: True
				underline: True
				on_ref_press: app.change_password()
		BoxLayout:
			size_hint_y: .1
			Label:
			Button:
				id: login
				background_normal: 'images/button_normal.png'
				background_down: 'images/button_down.png'
				bold: True
				font_size: '30sp'
				opacity: .9
				text: 'Login'
				on_release: app.login()
			Label:
		BoxLayout:
			size_hint_y: .05
		BoxLayout:
			size_hint_y: .48
			ScrollView:
				canvas.before:
					Color:
						rgba: 1, 1, 1, .5
					RoundedRectangle:
						radius: 30,
						size: self.size
						pos: self.pos
				Label:
					id: log
					text: app.log
					color: 0, 0, 0, 1
					text_size: self.width, None
					halign: 'center'
					valign: 'top'
					size_hint: 1, None
					height: self.texture_size[1]
<MyLabel@Label>:
	color: 0, 0, 0, 1
	font_size: '20sp'
	bold: True
	halign: 'center'
	valign: 'center'
	text_size: self.size
	shorten: True
	shorten_from: 'right'
<MyTextInput@TextInput>:
	canvas.after:
		Color:
			rgba: 0.82, 0.81, 0.78, 1
		SmoothLine:
			overdraw_width: 3.6
			rounded_rectangle: self.x, self.y, self.width, self.height, self.height/2
	background_normal: ''
	background_active: ''
	background_color: 1, 1, 1, 0
	font_size: '20sp'
	multiline: False
	use_bubble: True
	write_tab: False
''')




class RootWidget(Widget):
	def __init__(self, **kwargs):
		super(RootWidget, self).__init__(**kwargs)
		


		
class CCDGUTApp(App):


						# 初始化UI并返回根控件

	
	def build(self):
		# 先确定jpg和json的存储路径
		autologin.handle_path()
		# 创建json对象
		self.store = JsonStore(autologin.PATH+'\\'+'info.json')
		self.judge_checkbox()
		self.read_info()
		self.autologin()
		return RootWidget()
		
		
						# 初始化UI方法
						
	
	def judge_checkbox(self):
		try:
			self.checkbox1_status = self.store.get('Checkbox1')['Checkbox1_status']
		except:
			self.checkbox1_status = False
		try:
			self.checkbox2_status = self.store.get('Checkbox2')['Checkbox2_status']
		except:
			self.checkbox2_status = False
	
	
	def read_info(self):
		if self.checkbox2_status == True:
			try:
				self.schoolnumber = self.store.get('Intranet')['SchoolNumber']
				self.password1 = self.store.get('Intranet')['Password']
				self.phonenumber = self.store.get('Extranet')['PhoneNumber']
				self.password2 = self.store.get('Extranet')['Password']
				self.log = ''
			except:
				self.log = ''
		else:
			self.schoolnumber = ''
			self.password1 = ''
			self.phonenumber = ''
			self.password2 = ''
			self.log = ''
			
			
				
	def autologin(self):
		if self.checkbox1_status == True:
			is_change_password = autologin.login(self.schoolnumber, self.password1, self.phonenumber, self.password2)
			# 返回1表示可以改密码
			if is_change_password == 1:
				self.store.put('IP', IP1 = autologin.IP[0], IP2 = autologin.IP[1])
			self.list_to_str()
			autologin.LOG = []
			
			

							# 选择框及超链接标签方法

	
	def autorun(self):
		checkbox1_status = self.root.autorun.active
		subKey = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
		key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,  subKey, 0,  win32con.KEY_ALL_ACCESS)
		if checkbox1_status == True:
			try:
				valueName = 'CCDGUT'
				value = autologin.PATH+'\\'+'CCDGUT.exe'
				win32api.RegSetValueEx(key, valueName, 0, win32con.REG_SZ, value)
				win32api.RegCloseKey(key)
				self.store.put('Checkbox1', Checkbox1_status = checkbox1_status)
				self.root.log.text += 'Automatic login when the computer is turned on.\n'
			except:
				self.root.log.text += '**AutoRun, failed to join.**\n'
		else:
			try:
				win32api.RegDeleteValue(key, 'CCDGUT')
				win32api.RegCloseKey(key)
				self.store.delete('Checkbox1')
				self.root.log.text += 'Manual login.\n'
			except:
				self.root.log.text += '**AutoRun, failed to delete.**\n'
	
			
	def remember_account(self):
		checkbox2_status = self.root.remember_account.active
		if checkbox2_status == True:
			self.store.put('Checkbox2', Checkbox2_status = checkbox2_status)
			self.store.put('Intranet', SchoolNumber=self.root.schoolnumber.text, Password=self.root.password1.text)
			self.store.put('Extranet', PhoneNumber=self.root.phonenumber.text, Password=self.root.password2.text)
			self.root.log.text += 'Remember the account password.\n'
		else:
			self.store.delete('Intranet')
			self.store.delete('Extranet')
			self.store.delete('Checkbox2')
			self.root.log.text += "Don't remember the account password\n"
			
			
	def change_password(self):
		try:
			import webbrowser
			wlanuserip = self.store.get('IP')['IP1']
			wlanacip = self.store.get('IP')['IP2']
			webbrowser.open('http://enet.10000.gd.cn:10001/?wlanuserip={wlanuserip}&wlanacip={wlanacip}'.format(wlanuserip=wlanuserip, wlanacip=wlanacip))
		except:
			self.root.log.text += '**You should change your password after logining.**\n'
			
				
							# 登录按钮方法


	def is_same(self):
		if self.schoolnumber == self.root.schoolnumber.text:
			if self.password1 == self.root.password1.text:
				if self.phonenumber == self.root.phonenumber.text:
					if self.password2 == self.root.password2.text:
						return True
		return False
	
		
	def login(self):
		if self.root.remember_account.active == True:
			if self.is_same() == False:
				self.store.put('Intranet', SchoolNumber=self.root.schoolnumber.text, Password=self.root.password1.text)
				self.store.put('Extranet', PhoneNumber=self.root.phonenumber.text, Password=self.root.password2.text)
		is_change_password = autologin.login(self.root.schoolnumber.text, self.root.password1.text, self.root.phonenumber.text, self.root.password2.text)
		# 返回1表示可以改密码
		if is_change_password == 1:
			self.store.put('IP', IP1 = autologin.IP[0], IP2 = autologin.IP[1])
		self.list_to_str()
		autologin.LOG = []
		self.root.log.text += self.log
		
		
	def list_to_str(self):
		self.log = ''.join(autologin.LOG)
	

	
			
if __name__ == '__main__':
	CCDGUTApp().run()