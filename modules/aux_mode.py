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

from tkinter import ttk, Frame, Label, Scale, Radiobutton, IntVar, Entry
import tkinter.scrolledtext as tkst

class AuxMode(Frame):

	def __init__(self,root,parent):
		Frame.__init__(self,root,borderwidth=2, relief='groove',height=10)
		settings = parent.settings('aux_mode')
		self.parent = parent
		
		
		lbl_power = Label(self,text='Power:')
		lbl_power.grid(row=0,column=0,pady=2)
		self.cmb_power = ttk.Combobox(self,value=['Off','On'])
		self.cmb_power.grid(row=0,column=1,pady=2)
		self.cmb_power.set(settings['power'])
		self.cmb_power['state'] = 'readonly'
		self.cmb_power.bind('<<ComboboxSelected>>',self.set_power)

		lbl_aux_pin = Label(self,text='AUX pin:')
		lbl_aux_pin.grid(row=1,column=0,pady=2)
		self.cmb_aux_pin = ttk.Combobox(self, values=['AUX','CS'])
		self.cmb_aux_pin.grid(row=1,column=1,pady=2)
		self.cmb_aux_pin['state'] = 'readonly'
		self.cmb_aux_pin.set(settings['aux_pin'])
		self.cmb_aux_pin.bind('<<ComboboxSelected>>',self.select_aux_pin)

		lbl_aux = Label(self,text='AUX mode:')
		lbl_aux.grid(row=2,column=0,pady=2)
		self.cmb_aux_mode = ttk.Combobox(self, values=['Input','Output','Servo','PWM'])
		self.cmb_aux_mode.grid(row=2,column=1,pady=2)
		self.cmb_aux_mode['state'] = 'readonly'
		self.cmb_aux_mode.set(settings['mode'])
		self.cmb_aux_mode.bind('<<ComboboxSelected>>',self.select_aux_mode)
		
		self.aux_servo = Scale(self,from_=0,to=180,orient='horizontal')
		self.aux_servo.set(settings['servo'])
		self.aux_servo.bind('<ButtonRelease-1>',self.select_aux_mode)

		self.aux_pin_state = IntVar()
		self.aux_pin_state.set(settings['aux_state'])
		self.aux_pin_state.trace_add('write',self.select_aux_mode)

		self.aux_high = Radiobutton(self,text='HIGH',value=1,variable=self.aux_pin_state)
		self.aux_low = Radiobutton(self,text='LOW',value=0,variable=self.aux_pin_state)

		self.aux_pwm_lbl = Label(self,text='Frequency (KHz):')
		self.aux_pwm_freq = Entry(self)
		self.aux_pwm_freq.insert(0,settings['pwm_freq'])
		self.aux_pwm_freq.bind('<KeyRelease>',self.select_aux_mode)

		self.aux_pwm_duty_lbl = Label(self,text='Duty cycle (%):')
		self.aux_pwm_duty = Scale(self,from_=0,to=99,orient='horizontal')
		self.aux_pwm_duty.set(settings['pwm_duty'])
		self.aux_pwm_duty.bind('<ButtonRelease-1>',self.select_aux_mode)

	def __call__(self):
		return{
			'power': self.cmb_power.get(),
			'mode': self.cmb_aux_mode.get(),
			'aux_state': self.aux_pin_state.get(),
			'aux_pin': self.cmb_aux_pin.get(),
			'servo': self.aux_servo.get(),
			'pwm_freq': self.aux_pwm_freq.get(),
			'pwm_duty': self.aux_pwm_duty.get()
		}

	def select_aux_mode(self,e=None,a=None,b=None):
		
		for i, widget in enumerate(self.winfo_children()):
			if i > 5:
				widget.grid_forget()
		mode = self.cmb_aux_mode.get()

		# if self.parent.console.mode == 'HiZ': return
		if mode == 'Input':
			self.parent.console.aux('Input')

		if mode == 'Output':
			self.aux_high.grid(row=3,column=1)
			self.aux_low.grid(row=4,column=1)
			self.parent.console.aux('Output',self.aux_pin_state.get())

		if mode == 'Servo':
			self.aux_servo.grid(row=3,column=1)
			self.parent.console.servo(self.aux_servo.get())

		if mode == 'PWM':
			self.aux_pwm_lbl.grid(row=3,column=0)
			self.aux_pwm_freq.grid(row=3,column=1)
			self.aux_pwm_duty_lbl.grid(row=4,column=0)
			self.aux_pwm_duty.grid(row=4,column=1)
			self.parent.console.pwm(self.aux_pwm_freq.get(),self.aux_pwm_duty.get())
		
		if mode == 'CS':
			self.parent.console.cs()
			
		self.parent.settings('aux_mode',self())
	
	def select_aux_pin(self,e=None):
		self.parent.console.aux_pin(self.cmb_aux_pin.get())

	def set_power(self,e=None):
		self.parent.console.power(self.cmb_power.get())
		self.parent.settings('aux_mode',self())

	def disable(self):
		self.cmb_power['state'] = 'disabled'
		self.cmb_aux_mode['state'] = 'disabled'
		self.aux_high['state'] = 'disabled'
		self.aux_low['state'] = 'disabled'
		self.aux_servo['state'] = 'disabled'
		self.aux_pwm_freq['state'] = 'disabled'
		self.aux_pwm_duty['state'] = 'disabled'

	def enable(self):
		self.cmb_power['state'] = 'readonly'
		self.cmb_aux_mode['state'] = 'readonly'
		self.aux_high['state'] = 'normal'
		self.aux_low['state'] = 'normal'
		self.aux_servo['state'] = 'normal'
		self.aux_pwm_freq['state'] = 'normal'
		self.aux_pwm_duty['state'] = 'normal'