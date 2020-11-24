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

from tkinter import ttk, Frame, Label, Button
import tkinter.scrolledtext as tkst

class ModeSelector(Frame):

	def __init__(self,root,parent):
		Frame.__init__(self,root, relief='sunken')
		self.modes_tabs = ttk.Notebook(self,width=100)
		self.modes_tabs.pack(fill='both',expand=1)
		self.settings = parent.settings('mode_selector')
		self.data = parent.settings('data')
		self.parent = parent

		self.fmode_HiZ = Frame(self.modes_tabs,width=100,height=100,borderwidth=2,relief='groove')
		self.btn_get_modes = Button(self.fmode_HiZ, text='Get Modes')
		self.btn_get_modes.place(relx=0.5, rely=0.5, anchor='center')



		self.fmode_UART = Frame(self.modes_tabs,width=100,height=100,borderwidth=2,relief='groove')
		lbl_baud = Label(self.fmode_UART,text='Speed (bps):')
		lbl_baud.grid(row=0,column=0,pady=2)
		baud_rates = list(self.data['uart_speed'].keys())
		baud_rates = [x.rjust(8,' ') for x in baud_rates]
		self.cmb_baud = ttk.Combobox(self.fmode_UART,value=baud_rates)
		self.cmb_baud.grid(row=0,column=1,pady=2)
		self.cmb_baud['state'] = 'readonly'
		self.cmb_baud.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_baud.current(self.settings['uart'][0])

		lbl_data = Label(self.fmode_UART,text='Data bits & parity:')
		lbl_data.grid(row=1,column=0,pady=2)
		uart_protocol = list(self.data['uart_protocol'].keys())
		uart_protocol = [x for x in uart_protocol]
		self.cmb_data = ttk.Combobox(self.fmode_UART,value=uart_protocol)
		self.cmb_data.grid(row=1,column=1,pady=2)
		self.cmb_data['state'] = 'readonly'
		self.cmb_data.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_data.current(self.settings['uart'][1])

		lbl_stop = Label(self.fmode_UART,text='Stop bit:')
		lbl_stop.grid(row=2,column=0,pady=2)
		uart_stop = list(self.data['uart_stop'].keys())
		uart_stop = [x for x in uart_stop]
		self.cmb_stop = ttk.Combobox(self.fmode_UART,value=uart_stop)
		self.cmb_stop.grid(row=2,column=1,pady=2)
		self.cmb_stop['state'] = 'readonly'
		self.cmb_stop.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_stop.current(self.settings['uart'][2])

		lbl_polarity = Label(self.fmode_UART,text='Polarity:')
		lbl_polarity.grid(row=3,column=0,pady=2)
		uart_polarity = list(self.data['uart_polarity'].keys())
		uart_polarity = [x for x in uart_polarity]
		self.cmb_uart_polarity = ttk.Combobox(self.fmode_UART,value=uart_polarity)
		self.cmb_uart_polarity.grid(row=3,column=1,pady=2)
		self.cmb_uart_polarity['state'] = 'readonly'
		self.cmb_uart_polarity.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_uart_polarity.current(self.settings['uart'][3])

		lbl_otype = Label(self.fmode_UART,text='Output type:')
		lbl_otype.grid(row=4,column=0,pady=2)
		output_format = list(self.data['output'].keys())
		output_format = [x for x in output_format]
		self.cmb_uart_output = ttk.Combobox(self.fmode_UART,value=output_format)
		self.cmb_uart_output.grid(row=4,column=1,pady=2)
		self.cmb_uart_output['state'] = 'readonly'
		self.cmb_uart_output.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_uart_output.current(self.settings['uart'][4])

		self.fmode_SPI = Frame(self.modes_tabs,width=100,height=100,borderwidth=2,relief='groove')

		lbl_spi_speed = Label(self.fmode_SPI,text='Speed:')
		lbl_spi_speed.grid(row=0,column=0,pady=2)
		spi_speed = list(self.data['spi_speed'].keys())
		spi_speed = [x for x in spi_speed]
		self.cmb_spi_speed = ttk.Combobox(self.fmode_SPI,value=spi_speed)
		self.cmb_spi_speed.grid(row=0,column=1,pady=2)
		self.cmb_spi_speed['state'] = 'readonly'
		self.cmb_spi_speed.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_spi_speed.current(self.settings['spi'][0])

		lbl_polarity = Label(self.fmode_SPI,text='Polarity:')
		lbl_polarity.grid(row=1,column=0,pady=2)
		spi_clock_polarity = list(self.data['spi_clock_polarity'].keys())
		spi_clock_polarity = [x for x in spi_clock_polarity]
		self.cmb_spi_polarity = ttk.Combobox(self.fmode_SPI,value=spi_clock_polarity)
		self.cmb_spi_polarity.grid(row=1,column=1,pady=2)
		self.cmb_spi_polarity['state'] = 'readonly'
		self.cmb_spi_polarity.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_spi_polarity.current(self.settings['spi'][1])

		lbl_phase = Label(self.fmode_SPI,text='Input sample phase:')
		lbl_phase.grid(row=2,column=0,pady=2)
		spi_input_phase = list(self.data['spi_input_phase'].keys())
		spi_input_phase = [x for x in spi_input_phase]
		self.cmb_phase = ttk.Combobox(self.fmode_SPI,value=spi_input_phase)
		self.cmb_phase.grid(row=2,column=1,pady=2)
		self.cmb_phase['state'] = 'readonly'
		self.cmb_phase.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_phase.current(self.settings['spi'][2])

		lbl_clock_edge = Label(self.fmode_SPI,text='Output clock edge:')
		lbl_clock_edge.grid(row=3,column=0,pady=2)
		spi_clock_edge = list(self.data['spi_clock_edge'].keys())
		spi_clock_edge = [x for x in spi_clock_edge]
		self.cmb_clock_edge = ttk.Combobox(self.fmode_SPI,value=spi_clock_edge)
		self.cmb_clock_edge.grid(row=3,column=1,pady=2)
		self.cmb_clock_edge['state'] = 'readonly'
		self.cmb_clock_edge.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_clock_edge.current(self.settings['spi'][3])
		
		lbl_cs_polarity = Label(self.fmode_SPI,text='CS polarity:')
		lbl_cs_polarity.grid(row=4,column=0,pady=2)
		cs_polarity = list(self.data['cs_polarity'].keys())
		cs_polarity = [x for x in cs_polarity]
		self.cmb_spi_cs_polarity = ttk.Combobox(self.fmode_SPI,value=cs_polarity)
		self.cmb_spi_cs_polarity.grid(row=4,column=1,pady=2)
		self.cmb_spi_cs_polarity['state'] = 'readonly'
		self.cmb_spi_cs_polarity.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_spi_cs_polarity.current(self.settings['spi'][4])

		lbl_output = Label(self.fmode_SPI,text='Output type:')
		lbl_output.grid(row=5,column=0,pady=2)
		output = list(self.data['output'].keys())
		output = [x for x in output]
		self.cmb_spi_output = ttk.Combobox(self.fmode_SPI,value=output)
		self.cmb_spi_output.grid(row=5,column=1,pady=2)
		self.cmb_spi_output['state'] = 'readonly'
		self.cmb_spi_output.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_spi_output.current(self.settings['spi'][5])

		self.fmode_I2C = Frame(self.modes_tabs,width=100,height=100,borderwidth=2,relief='groove')

		lbl_i2c_speed = Label(self.fmode_I2C,text='Speed:')
		lbl_i2c_speed.grid(row=0,column=0,pady=2)
		i2c_speed = list(self.data['i2c_speed'].keys())
		i2c_speed = [x.replace('I2C_','') for x in i2c_speed]
		self.cmb_i2c_speed = ttk.Combobox(self.fmode_I2C,value=i2c_speed)
		self.cmb_i2c_speed.grid(row=0,column=1,pady=2)
		self.cmb_i2c_speed['state'] = 'readonly'
		self.cmb_i2c_speed.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_i2c_speed.current(self.settings['i2c'][0])

		self.fmode_2WIRE = Frame(self.modes_tabs,width=100,height=100,borderwidth=2,relief='groove')
		
		lbl_wire_speed = Label(self.fmode_2WIRE,text='Speed:')
		lbl_wire_speed.grid(row=0,column=0,pady=2)
		wire_speed = list(self.data['wire_speed'].keys())
		wire_speed = [x for x in wire_speed]
		self.cmb_2w_speed = ttk.Combobox(self.fmode_2WIRE,value=wire_speed)
		self.cmb_2w_speed.grid(row=0,column=1,pady=2)
		self.cmb_2w_speed['state'] = 'readonly'
		self.cmb_2w_speed.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_2w_speed.current(self.settings['2wire'][0])

		lbl_output = Label(self.fmode_2WIRE,text='Output type:')
		lbl_output.grid(row=1,column=0,pady=2)
		output = list(self.data['output'].keys())
		output = [x for x in output]
		self.cmb_2w_output = ttk.Combobox(self.fmode_2WIRE,value=output)
		self.cmb_2w_output.grid(row=1,column=1,pady=2)
		self.cmb_2w_output['state'] = 'readonly'
		self.cmb_2w_output.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_2w_output.current(self.settings['2wire'][1])

		self.fmode_3WIRE = Frame(self.modes_tabs,width=100,height=100,borderwidth=2,relief='groove')

		lbl_wire_speed = Label(self.fmode_3WIRE,text='Speed:')
		lbl_wire_speed.grid(row=0,column=0,pady=2)
		wire_speed = list(self.data['wire_speed'].keys())
		wire_speed = [x for x in wire_speed]
		self.cmb_3w_speed = ttk.Combobox(self.fmode_3WIRE,value=wire_speed)
		self.cmb_3w_speed.grid(row=0,column=1,pady=2)
		self.cmb_3w_speed['state'] = 'readonly'
		self.cmb_3w_speed.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_3w_speed.current(self.settings['3wire'][0])

		lbl_output = Label(self.fmode_3WIRE,text='Output type:')
		lbl_output.grid(row=1,column=0,pady=2)
		output = list(self.data['output'].keys())
		output = [x for x in output]
		self.cmb_3w_output = ttk.Combobox(self.fmode_3WIRE,value=output)
		self.cmb_3w_output.grid(row=1,column=1,pady=2)
		self.cmb_3w_output['state'] = 'readonly'
		self.cmb_3w_output.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_3w_output.current(self.settings['3wire'][1])

		lbl_cs_polarity = Label(self.fmode_3WIRE,text='CS polarity:')
		lbl_cs_polarity.grid(row=2,column=0,pady=2)
		cs_polarity = list(self.data['cs_polarity'].keys())
		cs_polarity = [x for x in cs_polarity]
		self.cmb_3w_cs_polarity = ttk.Combobox(self.fmode_3WIRE,value=cs_polarity)
		self.cmb_3w_cs_polarity.grid(row=2,column=1,pady=2)
		self.cmb_3w_cs_polarity['state'] = 'readonly'
		self.cmb_3w_cs_polarity.bind('<<ComboboxSelected>>',self.select_mode)
		self.cmb_3w_cs_polarity.current(self.settings['3wire'][2])
	
		self.fmode_1WIRE = Frame(self.modes_tabs,width=100,height=100,borderwidth=2,relief='groove')
		self.fmode_LCD = Frame(self.modes_tabs,width=100,height=100,borderwidth=2,relief='groove')
		self.fmode_DIO = Frame(self.modes_tabs,width=100,height=100,borderwidth=2,relief='groove')
		self.fmode_JTAG = Frame(self.modes_tabs,width=100,height=100,borderwidth=2,relief='groove')

		self.show_modes()
		
		
		self.after(1,self.bind_tab_change)

	def bind_tab_change(self):
		self.modes_tabs.bind('<<NotebookTabChanged>>',self.select_mode)

	def __call__(self,modes=None,mode=None):
		if modes is not None:
			self.settings['modes'] = modes
			self.parent.settings('mode_selector',self())
			self.modes_tabs.unbind('<<NotebookTabChanged>>')
			self.show_modes()
			self.after(1,self.bind_tab_change)
		if mode is not None:
			self.select_mode(mode=mode)

		if mode is None and modes is None:
			return self.settings
		
	def show_modes(self):
		for tab in self.modes_tabs.winfo_children():
			try:
				self.modes_tabs.forget(tab)
			except:
				pass
		for mode in self.settings['modes']:
			if mode == 'HiZ':
				self.modes_tabs.add(self.fmode_HiZ,text='HiZ')

			if mode == 'UART':
				self.modes_tabs.add(self.fmode_UART,text='UART')

			if mode == 'SPI':
				self.modes_tabs.add(self.fmode_SPI,text='SPI')

			if mode == 'I2C':
				self.modes_tabs.add(self.fmode_I2C,text='I2C')

			if mode == '1-WIRE':
				self.modes_tabs.add(self.fmode_1WIRE,text='1-WIRE')

			if mode == '2WIRE':
				self.modes_tabs.add(self.fmode_2WIRE,text='2WIRE')

			if mode == '3WIRE':
				self.modes_tabs.add(self.fmode_3WIRE,text='3WIRE')

			if mode == 'LCD':
				self.modes_tabs.add(self.fmode_LCD,text='LCD')

			if mode == 'DIO':
				self.modes_tabs.add(self.fmode_DIO,text='DIO')

			if mode == 'JTAG':
				self.modes_tabs.add(self.fmode_JTAG,text='JTAG')

		active_mode = self.settings['modes'].index(self.settings['mode'])
		if active_mode < 0:
			active_mode = 0
		self.modes_tabs.select(active_mode)

	def uart(self):
		return (self.cmb_baud.current(),
				self.cmb_data.current(),
				self.cmb_stop.current(),
				self.cmb_uart_polarity.current(),
				self.cmb_uart_output.current())

	def spi(self):
		return (self.cmb_spi_speed.current(),
				self.cmb_spi_polarity.current(),
				self.cmb_clock_edge.current(),
				self.cmb_phase.current(),
				self.cmb_spi_cs_polarity.current(),
				self.cmb_spi_output.current())
	
	def i2c(self):
		return (self.cmb_i2c_speed.current(),)
	
	def two_wire(self):
		return (self.cmb_2w_speed.current(),
				self.cmb_2w_output.current())

	def three_wire(self):
		return  (self.cmb_3w_speed.current(),
				self.cmb_3w_cs_polarity.current(),
				self.cmb_3w_output.current())

	def select_mode(self,e=None,mode=None):
		mode = self.modes_tabs.tab(self.modes_tabs.select(),'text')
		self.settings['mode'] = mode

		if mode == 'HiZ':
			self.parent.aux_mode.disable()
		else:
			self.parent.aux_mode.enable()

		data = tuple()
		if mode == 'UART':
			data = self.uart()
			self.settings['uart'] = data
		elif mode == 'SPI':
			data = self.spi()
			self.settings['spi'] = data
		elif mode == 'I2C':
			data = self.i2c()
			self.settings['i2c'] = data
		elif mode == '2WIRE':
			data = self.two_wire()
			self.settings['2wire'] = data
		elif mode == '3WIRE':
			data = self.three_wire()
			self.settings['3wire'] = data
		
		self.parent.console.mode((mode,) +tuple(i+1 for i in data))
		self.parent.settings('mode_selector',self())