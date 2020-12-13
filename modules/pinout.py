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

from tkinter import ttk
from tkinter import Frame, Label
import tkinter.scrolledtext as tkst

class Pinout(Frame):
	def __init__(self,root,parent):
		Frame.__init__(self,root,borderwidth=2, relief="groove",height=10)
		self.parent = parent
		
		self.lbl_voltages = Label(self,text='Update interval (ms):',width=15)
		self.cmb_interval = ttk.Combobox(self,value=['Off','200','300','400','500','1000','2000','3000'],width=14)
		self.cmb_interval['state'] = 'readonly'
		self.cmb_interval.bind('<<ComboboxSelected>>',self.update_voltages)
		self.cmb_interval.set('Off')

		self.lbl_voltages.grid(row=0,column=2,columnspan=2)
		self.cmb_interval.grid(row=0,column=4,columnspan=2)

		self.pin_9  = Label(self,text='GND',borderwidth=2, relief="groove",width=8,bg='black',fg='white')
		self.pin_8  = Label(self,text='3.3v',borderwidth=2, relief="groove",width=8,bg='white')
		self.pin_8v = Label(self,text='-',borderwidth=2, relief="groove",width=8)
		self.pin_7  = Label(self,text='5.0v',borderwidth=2, relief="groove",width=8,bg='gray')
		self.pin_7v = Label(self,text='-',borderwidth=2, relief="groove",width=8)
		self.pin_6  = Label(self,text='ADC',borderwidth=2, relief="groove",width=8,bg='magenta')
		self.pin_6v = Label(self,text='-',borderwidth=2, relief="groove",width=8)
		self.pin_5  = Label(self,text='VPU',borderwidth=2, relief="groove",width=8,bg='blue',fg='white')
		self.pin_5v = Label(self,text='-',borderwidth=2, relief="groove",width=8)
		self.pin_4  = Label(self,text='AUX',borderwidth=2, relief="groove",width=8,bg='green')
		self.pin_4v = Label(self,text='-',borderwidth=2, relief="groove",width=8)
		self.pin_3  = Label(self,text='-',borderwidth=2, relief="groove",width=8,bg='yellow')
		self.pin_3v = Label(self,text='-',borderwidth=2, relief="groove",width=8)
		self.pin_2  = Label(self,text='-',borderwidth=2, relief="groove",width=8,bg='orange')
		self.pin_2v = Label(self,text='-',borderwidth=2, relief="groove",width=8)
		self.pin_1  = Label(self,text='-',borderwidth=2, relief="groove",width=8,bg='red')
		self.pin_1v = Label(self,text='-',borderwidth=2, relief="groove",width=8)
		self.pin_0  = Label(self,text='-',borderwidth=2, relief="groove",width=8,bg='brown')
		self.pin_0v = Label(self,text='-',borderwidth=2, relief="groove",width=8)

		self.pin_9.grid(row=1,column=3)
		self.pin_8.grid(row=1,column=4)
		self.pin_8v.grid(row=1,column=5)
		self.pin_7v.grid(row=2,column=2)
		self.pin_7.grid(row=2,column=3)
		self.pin_6.grid(row=2,column=4)
		self.pin_6v.grid(row=2,column=5)
		self.pin_5v.grid(row=3,column=2)
		self.pin_5.grid(row=3,column=3)
		self.pin_4.grid(row=3,column=4)
		self.pin_4v.grid(row=3,column=5)
		self.pin_3v.grid(row=4,column=2)
		self.pin_3.grid(row=4,column=3)
		self.pin_2.grid(row=4,column=4)
		self.pin_2v.grid(row=4,column=5)
		self.pin_1v.grid(row=5,column=2)
		self.pin_1.grid(row=5,column=3)
		self.pin_0.grid(row=5,column=4)
		self.pin_0v.grid(row=5,column=5)

		self.columnconfigure([0,7],weight=1)

	def update_voltages(self,e=None):
		self.parent.console.voltages()
		interval =  self.cmb_interval.get()
		if interval == 'Off':
			return
		self.after(int(interval),self.update_voltages)

	def __call__(self,pins,states):
		for i in range(0,9):
			getattr(self,'pin_{}v'.format(i))['text'] = states[i]
		for i in range(0,4):
			pin = getattr(self,'pin_'+str(i))
			pin['text'] = pins[i]