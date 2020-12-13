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

import sys, asyncio
import tkinter as tk
from tkinter import ttk, PanedWindow, messagebox
from modules.settings import Settings
from modules.buspyrate import BusPyrate
from modules.editor import Editor
from modules.mode_selector import ModeSelector
from modules.port_selector import PortSelector
from modules.aux_mode import AuxMode
from modules.pinout import Pinout
from modules.menu import AppMenu


_WINDOW_TITLE = 'Friendly BusPirate (v0.1) - UI automation over BusPirate'


class App(tk.Tk):

	def __init__(self, loop, interval=1/100):
		super().__init__()
		super().title(_WINDOW_TITLE)
		super().geometry('%dx%d+%d+%d' % (950, 650, 400, 0))
		self.loop = loop
		self.protocol('WM_DELETE_WINDOW', self.close)
		self.settings = Settings()
		self.tasks = []
		self.create_task(self.updater(interval))
		self.port = None
		self.initUi()
		self.columnconfigure(0,weight=1)
		self.rowconfigure(0,weight=1)

	def create_task(self,task):
		self.tasks.append(loop.create_task(task))

	def initUi(self):
		root = PanedWindow(self, orient='horizontal')
		root.grid(row=0,column=0,sticky='wens') 
		
		left_pane = PanedWindow(root, orient='vertical')
		root.add(left_pane,width=100,height=100)
		left_pane.grid(row=0,column=0,sticky='wens')

		self.port_selector = PortSelector(left_pane,self)
		left_pane.add(self.port_selector, width=300,height=125)

		self.mode_selector = ModeSelector(left_pane,self)
		left_pane.add(self.mode_selector,height=220)

		self.aux_mode = AuxMode(left_pane,self)
		left_pane.add(self.aux_mode,height=145)
		
		self.pinout  = Pinout(left_pane,self)
		left_pane.add(self.pinout,height=80)
		
		self.right_pane = PanedWindow(root, orient='vertical')
		root.add(self.right_pane)
		self.right_pane.grid(row=0,column=1,sticky='wens')

		root.columnconfigure(1, weight=1)
		root.rowconfigure(0, weight=1) 

		self.editor = Editor(self.right_pane,self)
		self.right_pane.add(self.editor,height=200)

		self.console = BusPyrate(self.right_pane,self)
		self.right_pane.add(self.console)

		menu = AppMenu(self)
		self.config(menu=menu)

		self.bind('<F5>',self.console.run_script)

		if self.port_selector()['autoconnect']:
			self.port_selector.connect()

		self.mode_selector.btn_get_modes.configure(command=self.console.detect_modes)
		
		self.mode_selector.select_mode()
		try:
			self.editor.open(self.settings('recent')[0])
		except:
			pass

	async def updater(self, interval):
		while True:
			self.tasks = [x for x in self.tasks if x is not None]
			self.update()
			await asyncio.sleep(interval)

	def close(self):
		if self.editor.close() is None: 
			return
		for task in self.tasks:
			task.cancel()
		try:
			self.after_cancel(self.voltages_timer)
		except:
			pass
		self.loop.stop()
		self.destroy()

	def about(self):
		messagebox.showinfo('Friendly BusPirate - About',
'''GUI interface for BusPirate
http://dangerousprototypes.com/docs/Bus_Pirate
developed by Valentin Sasek <dsl400@gmail.com>''')

loop = asyncio.get_event_loop()
app = App(loop)

loop.run_forever()
loop.close()