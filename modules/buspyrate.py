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

import time, serial
from queue import Queue
from tkinter import Frame
import tkinter.scrolledtext as tkst


class BusPyrate(Frame):

	def __init__(self,root,parent):
		Frame.__init__(self,root,borderwidth=2, relief="sunken")
		self.columnconfigure(0,weight=1)
		self.rowconfigure(0,weight=1)
		self.parent = parent
		self.available_modes = parent.settings('mode_selector')['modes']
		self.console = tkst.ScrolledText(self,state='disabled',tabstyle='wordprocessor')
		self.console.configure(state='disabled')
		self.console.bind('<KeyRelease>',self.key_event)
		self.console.grid(row=0,column=0,sticky='wens')
		self.com = None
		self.cmd_after = None
		self.last_v_index = None
		self.last_line = 1
		self.cmd_stack = Queue()
		
		# self.info = None
		# self.version = None
		# # self.read_info()
		# self.current_mode = None
		# self.pins = None


	def __call__(self):
		return {'settings':None}

	def connect(self,port):
		if self.com is None:
			try:
				self.com = serial.Serial(port,115200)
				self.com.flushInput()
				self.read_serial()
				return True
			except Exception as ex:
				print('BusPyrate.__init__:',ex)
			else:
				self.disconnect()
				return False

	def disconnect(self):
		try:
			self.com.__del__()
			del self.com
			self.com = None
		except:
			pass

	def reset(self):
		self.com.write('\x00'.encode())
		time.sleep(.05)
		self.send('#')
		self.com.flushInput()

	def send(self,cmd,newline = '\n'):
		if self.com is None: return
		self.com.write((cmd+newline).encode())

	def exec(self):
		self.last_line = self.console.index('end').split('.')[0]
		if self.cmd_stack.empty(): return
		try:
			self.after_cancel(self.cmd_after)
		except:
			pass
		self.send(self.cmd_stack.get())
		if self.cmd_stack.empty(): return
		self.cmd_after = self.after(1000,self.exec)

	def read_serial(self):
		if self.com is None: return
		if self.com.inWaiting() > 0:
			in_data = self.com.read(self.com.inWaiting())
			self.print(in_data.decode('ascii'))
		self.after(50,self.read_serial)

	def print(self,text):
		self.console.configure(state='normal')
		for c in text:
			if c == '\b':
				self.console.delete('end-2c','end')
			else:
				self.console.insert('end',c)
		self.console.configure(state='disabled')
		crt_line = self.console.index('end').split('.')[0]
		if(int(crt_line) > int(self.last_line) + 1):
			self.exec()
		self.last_line = crt_line
		self.console.see('end')
		if text.find('1. HiZ') > -1:
			self.after(50,self.parse_modes())
		if text.find('Pinstates:') > -1:
			self.after(50,self.parse_pins())

	def key_event(self,e):
		if self.com is None: return
		self.com.write(e.char.encode())

	def detect_modes(self):
		self.send('m')
		time.sleep(.05)
		self.send('x','')

	def parse_modes(self):
		available_modes = []
		try:
			start = self.console.search('1. HiZ','end',stopindex='end - 20 lines',backwards=True)
			if not start: return
			stop = self.console.search('x. exit','end',backwards=True)
			text = self.console.get(start,stop)
			for mode in text.split('\r\n')[:-1]:
				available_modes.append(mode.split(' ')[1])
			self.available_modes = available_modes
		except Exception as ex:
			print('parse_modes:',ex)
		self.parent.mode_selector(available_modes)

	def parse_pins(self):
		start = self.console.search('Pinstates:','end',stopindex='end - 20 lines',backwards=True)
		if start and start != self.last_v_index:
			try:
				self.parse_voltages(self.console.get(start+'+ 1 lines',start+'+ 5 lines'))
				self.last_v_index = start
			except Exception as ex:
				print('parse_pins:',ex)


	def parse_voltages(self,text):
		lines = text.split('\r\n')
		pins = lines[1].split('\t')
		states = lines[2].split('\t')[:-1]
		voltages = lines[3].split('\t')[:-1]
		pins.reverse()
		states.reverse()
		voltages.reverse()
		data = []
		for i in range(0,9):
			data.append(states[i] + ' ' + voltages[i] if i < 5 else voltages[i])
		self.parent.pinout(pins,data)

	def voltages(self):
		self.send('v')

	def info(self):
		self.send('i')

	def mode(self,mode):	
		self.current_mode = mode
		for i, c in enumerate(mode):
			if i == 0:
				self.send('m' +str(self.available_modes.index(c) + 1))
				time.sleep(.01)
			else:
				self.send(str(c))
				time.sleep(.01)
	
	def power(self,state):
		self.send('w' if state == 'Off' else 'W')

	def aux_pin(self,pin):
		self.send('c' if pin == 'AUX' else 'C')

	def aux(self,mode,state=None):
		if mode == 'Input':
			self.send('@')
		if mode == 'Output':
			self.send('A' if state else 'a')

	def servo(self,position):
		self.send('S{}'.format(position))

	def pwm(self,freq,duty):
		if int(freq) < 1: freq = 1
		if int(freq) > 3999: freq = 3999
		self.send('g{} {}'.format(freq,duty))

	def run_script(self,e=None):
		script = self.parent.editor.editor.get('1.0','end').strip()
		if len(script) == 0: return
		self.after(100,self.exec)
		for cmd in script.split('\n'):
			if cmd.find('#') == 0:
				continue
			cmd = cmd.strip()
			cmd = cmd.split('//')[0].strip()
			for _cmd in cmd.split(','):
				self.cmd_stack.put(_cmd.strip())