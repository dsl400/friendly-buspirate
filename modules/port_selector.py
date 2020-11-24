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

from tkinter import ttk, Frame, Label, BooleanVar, StringVar, Button, Checkbutton
import tkinter.scrolledtext as tkst
import sys, serial
import serial.tools.list_ports  as list_ports

class PortSelector(Frame):

	def __init__(self,root,parent):
		settings = parent.settings('port_selector')
		Frame.__init__(self,root,borderwidth=2, relief="groove",height=10)
		self.parent = parent
		self.autoconnect = BooleanVar()
		self.autoconnect.set(settings['autoconnect'])
		self.debug = BooleanVar()
		self.debug.set(settings['debug'])

		self.selected_port = StringVar(name='selected_port')

		port_select_label = Label(self,text="Port:",anchor="e",width=10)
		port_select_label.grid(row=0,column=0)
		self.port_select = ttk.Combobox(self, state="readonly",
			textvariable=self.selected_port,postcommand=self.update_portlist)
		self.update_portlist(settings['port'])
		self.port_select.bind('<<ComboboxSelected>>',self.port_changed)
		self.port_select.grid(row=0,column=1)

		self.port_connect = Button(self,text="Connect",command=self.connect,width=12)
		self.port_connect.grid(row=0,column=2)

		self.port_autoconnect = Checkbutton(self, variable=self.autoconnect, command=self.port_changed,text="Autoconnect")
		self.port_autoconnect.grid(row=1,column=1,columnspan=3,sticky="W")

		# self.port_debug = Checkbutton(self, variable=self.debug, command=self.port_changed,text="Debug")
		# self.port_debug.grid(row=1,column=2,columnspan=3,sticky="W")

		# self.port_descriptor_label = Label(self,text=" Desc:",anchor="e",width=10)
		# self.port_descriptor_label.grid(row=2,column=0)

		# self.port_descriptor = Label(self, text="-",justify="left")
		# self.port_descriptor.grid(row=2,column=1,columnspan=3,sticky="W")	

		# linfo = Label(self,text='Info:',anchor="e",width=10)
		# linfo.grid(row=3,column=0,sticky="N")
		# self.info = Label(self,text='-',anchor="w",justify='left')
		# self.info.grid(row=3,column=1,columnspan=3,sticky="W")

		self.grid_columnconfigure(0,minsize=10)
		self.grid_columnconfigure(1,weight=1)
		self.grid_columnconfigure(2,pad=10)
		self.grid_rowconfigure(0,pad=10)

	def __call__(self):
		return {
			'port':self.port_select.get(),
			'autoconnect':self.autoconnect.get(),
			'debug': self.debug.get()
		}


	def update_portlist(self,port=None):
		self.ports = []
		ports = []
		if sys.platform.startswith('win'):
			for p in list_ports.comports():				
				self.ports.append(p)
				ports.append(p.device)
		self.port_select['values'] = ports
		if port is None: return
		if port in ports:			
			self.port_select.set(port)

	def port_changed(self,e=None):
		self.parent.settings('port_selector',self())
	
	def connect(self):
		if self.parent.console.connect(self.port_select.get()):
			self.connected()
		else:
			self.parent.console.disconnect()
			self.disconnected()

	def connected(self):
		self.port_connect['text'] = 'Disconnect'
		self.port_select['state'] = 'disabled'
	
	def disconnected(self):
		self.port_connect['text'] = 'Connect'
		self.port_select['state'] = 'readonly'