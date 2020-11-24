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
from tkinter import Menu

class AppMenu(Menu):

	def __init__(self,root):
		self.root = root
		Menu.__init__(self,root,postcommand=self.update_menu)
		m_file = Menu(self,tearoff=0)
		self.add_cascade(label='File',menu=m_file)
		m_file.add_command(label='Open',command=root.editor.open)
		m_file.add_command(label='Save',command=root.editor.save)
		m_file.add_command(label='Save as',command=root.editor.save_as)
		m_file.add_separator()
		self.m_recent = Menu(m_file,tearoff=0) 
		m_file.add_cascade(label='Recent',menu=self.m_recent)
		m_file.add_separator()
		m_file.add_command(label='Exit',command=root.close)
		self.add_cascade(label='Run Script (F5)',command=self.root.console.run_script)
		self.add_command(label='About',command=self.root.about)

	def clear_recent(self):
		self.root.settings('recent',[])

	def update_menu(self):
		self.m_recent.delete(0,20)
		for file in self.root.settings('recent'):
			self.m_recent.add_command(label=file,command=lambda file=file: self.root.editor.open(file))
		self.m_recent.add_separator()
		self.m_recent.add_command(label='Clear',command=self.clear_recent)