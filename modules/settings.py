# This file is part of Friendly BusPirate.

# Friendly BusPirate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.

# Friendly BusPirate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Friendly BusPirate.  If not, see <http://www.gnu.org/licenses/>.

#developed by Valentin Sasek <dsl400@gmail.com>

import json

_SETTINGS_FILE_NAME = 'pyrateLab.settings.json'
_DEFAULT_SETTINGS = {
	'aux_mode':{
		'power':'Off',
		'mode':'Input',
		'aux_state':0,
		'aux_pin': 'AUX',
		'servo':90,
		'pwm_freq':1,
		'pwm_duty':50
	},
	
	'console':False,
	'mode_selector':{
		'modes':['HiZ'],
		'mode':'HiZ',
		'uart': [8,0,0,0,0],
		'spi': [2,0,0,0,0,0],
		'i2c': [0],
		'2wire': [2,1],
		'3wire': [2,0,1]
		
	},
	'port_selector':{
		'port':'COM4',
		'autoconnect': True,
		'debug': True
	},
	'data': {
		'puulup': {'None': 1,'Internal3V3': 2,'Internal5V': 3},
		'output_format': {'Hex': 1,'Dec': 2,'Bin': 3,'Raw': 4},
		'spi_speed': {'30KHz': 1,'125KHz': 2,'250KHz': 3,'1MHz': 4},
		'spi_clock_polarity': {'Low': 1,'High': 2},
		'spi_clock_edge': {'Idle': 1,'Active': 2},
		'spi_input_phase': {'Middle': 1,'End': 2},
		'cs_polarity': {'Positive': 1,'Negative': 2},
		'output': {'OpenDrain': 1,'Normal': 2},
		'uart_speed': {'300': 1,'1200': 2,'2400': 3,'4800': 4,'9600': 5,'19200': 6,'38400': 7,'57600': 8,'115200': 9},
		'uart_protocol': {'Data_8_None': 1,'Data_8_Even': 2,'Data_8_Odd': 3,'Data_9_None': 4},
		'uart_stop': {'1': 1,'2': 2},
		'uart_polarity': {'Idle_1': 1,'Idle_0': 2},
		'i2c_speed': {'I2C_5KHz': 1,'I2C_50KHz': 2,'I2C_100KHz': 3,'I2C_400KHz': 4},
		'wire_speed': {'5KHz': 1,'50KHz': 2,'100KHz': 3,'400KHz': 4},
		'aux_state':{'Output':0,'Servo':0,'PWM':0,'pwm_freq':1000}
	},
	'recent':[],
	'last_dir':''
}

class Settings():

	def __init__(self):
		self.load_settings()		

	def __call__(self,name,value=None):
		if value is None:
			return self.settings[name]
		else:
			self.settings[name] = value
		self.save_settings()

	def load_settings(self):
		try:
			with open(_SETTINGS_FILE_NAME,'r') as settings_file:
				self.settings = json.load(settings_file)
		except:
			self.settings = _DEFAULT_SETTINGS
			self.save_settings()

	def save_settings(self):
		try:
			with open(_SETTINGS_FILE_NAME,'w') as settings_file:
				json.dump(self.settings,settings_file)
		except Exception as ex:
			print('save_settings',ex)
