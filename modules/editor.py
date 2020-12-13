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

import os
from tkinter import ttk, Frame, messagebox, filedialog
import tkinter.scrolledtext as tkst

class Editor(Frame):

	def __init__(self,root,parent):
		Frame.__init__(self,root,borderwidth=2, relief="sunken")
		self.root = root
		self.parent = parent
		self.opened_file = None
		self.editor = tkst.ScrolledText(self,tabstyle='wordprocessor')
		self.editor.grid(row=0,column=0,columnspan=2,sticky='wens')
		self.columnconfigure(0,weight=1)	

	def open(self,file_path=None):
		reply = self.close()
		if reply is None: return
		if file_path is None:
			file_path = self.select_file()
		if file_path is None: return
		self.editor.delete('1.0','end')
		try:
			with open(file_path,'r') as input_file:
				text = input_file.read()
				self.editor.insert('1.0',text)
			self.editor.edit_modified(False)
			self.opened_file = file_path
			self.update_recent(file_path)
		except Exception as ex:
			print(file_path,ex)
			messagebox.showerror('File open','Could not open file!')

	def close(self):
		reply = False
		if self.editor.edit_modified():
			reply = messagebox.askyesnocancel('Editor content is modified!','\nWould you like to save the changes?')
		if reply is None: return None
		elif reply is True:
			return self.save()
		return reply

	def select_file(self,title='Open'):
		last_dir = self.parent.settings('last_dir')
		file = filedialog.askopenfilename(initialdir=last_dir, title=title)
		if not file: return None
		self.parent.settings('last_dir',os.path.dirname(file))
		self.update_recent(file)
		return file

	def save(self):
		if self.opened_file is None:
			return self.save_as()
		try:
			with open(self.opened_file,'w') as output_file:
				output_file.write(self.editor.get('1.0','end'))
			self.editor.edit_modified(False)
			self.update_recent(self.opened_file)
		except Exception as ex:
			print(ex)
			messagebox.showerror('File save','Could not save file!')
		return True

	def save_as(self):
		last_dir = self.parent.settings('last_dir')
		file = filedialog.asksaveasfilename(initialdir=last_dir)
		if not file: return None
		self.opened_file = file
		self.save()
		self.update_recent(file)
		return True

	def update_recent(self,file):
		recent = self.parent.settings('recent')
		try:
			recent.remove(file)
		except:
			pass
		self.parent.settings('recent',[file] + recent[:9])