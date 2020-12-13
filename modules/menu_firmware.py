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

import os, sys, time
from tkinter import Menu
from os import listdir
from os.path import isfile, join
from intelhex import IntelHex
import serial
import asyncio
import json

PIC_FLASHSIZE = 0xAC00
BOOTLOADER_PLACEMENT = 1
BOOTLOADER_HELLO_STR = 0xC1
PIC_PAGES = 42
PIC_ROWS_IN_PAGE = 8
PIC_WORDS_IN_ROW = 64
PIC_WORD_SIZE = 3
PIC_ROW_SIZE = PIC_WORDS_IN_ROW * PIC_WORD_SIZE
PIC_PAGE_SIZE = PIC_ROWS_IN_PAGE * PIC_ROW_SIZE
PIC_LAST_PAGE = PIC_PAGES - 1
PIC_LAST_PAGE_ROW = PIC_ROWS_IN_PAGE - 1

# BUFFER_SIZE = 
COMMAND_OFFSET = 3
LENGTH_OFFSET = 4
PAYLOAD_OFFSET = 5
HEADER_LENGTH = PAYLOAD_OFFSET




class FirmwareMenu(Menu):

	def __init__(self,root,parent):
		Menu.__init__(self,root,tearoff=0)
		self.parent = parent
		m_bp3 = Menu(self,tearoff=0)
		self.cwd = os.getcwd()
		bp3_fw_dir = join(self.cwd,'modules/fw/3')
		for f in listdir(bp3_fw_dir):
			if not f.endswith('.hex') and not isfile(f):
				continue
			m_bp3.add_command(label=f,command=lambda f=f: self.push_fw(f'3/{f}'))
	
		m_bp4 = Menu(self,tearoff=0)

		self.add_cascade(label='BP 3',menu=m_bp3)
		# self.add_cascade(label='BP 4',menu=m_bp4)


	def push_fw(self,f):
		file_path = join(self.cwd,'modules/fw',f)
		self.parent.create_task(self.fw_read_and_upload(file_path))

	async def fw_read_and_upload(self,file_path):
		
		await asyncio.sleep(.1)
		o_buff = self.read_hex(file_path)
		self.parent.console.send('$')
		await asyncio.sleep(.1)
		self.parent.console.send('y')
		await asyncio.sleep(.01)
		self.parent.console.send('')
		await asyncio.sleep(.5)
		self.parent.console.allow_read = False
		await asyncio.sleep(.5)
		if o_buff is not None:
			await self.write_firmware(o_buff)
		await asyncio.sleep(.1)
		self.parent.console.allow_read = True
		self.parent.console.read_serial()
		self.parent.console.detect_modes()

	def read_hex(self,file_path):
		file_path = file_path.replace('\\','/')
		try:
			fw_hex = IntelHex(file_path)
			self.parent.console.print(f'\nFile: {file_path}\n')
		except:
			self.parent.console.print('\nInvalid file!\n')
			return None
		
		data_map = {}
		u_addr = 0
		for p in range(0,PIC_PAGES):
			if p not in data_map.keys():
				data_map[p] = {}
			for r in range(0,PIC_ROWS_IN_PAGE):
				if r not in data_map[p].keys():
					data_map[p][r] = [0xff] * PIC_WORDS_IN_ROW * PIC_WORD_SIZE
					r_idx = 0
				for w in range(0,PIC_WORDS_IN_ROW):
					data_map[p][r][r_idx] = fw_hex[u_addr+2]
					data_map[p][r][r_idx+1] = fw_hex[u_addr]
					data_map[p][r][r_idx+2] = fw_hex[u_addr+1]
					u_addr += 4
					r_idx += 3
				used = False
				for b in data_map[p][r]:
					if b != 0xff:
						used = True
						break
				if p == PIC_LAST_PAGE and r == PIC_LAST_PAGE_ROW:
					used = True
				if not used:
					del data_map[p][r]
		
		for i in range(6):
			idx = PIC_WORDS_IN_ROW * PIC_WORD_SIZE - 6 + i
			data_map[PIC_LAST_PAGE][PIC_LAST_PAGE_ROW][idx] = data_map[0][0][i]

		i_bl_address = ( PIC_FLASHSIZE - 
			(BOOTLOADER_PLACEMENT * PIC_ROWS_IN_PAGE * PIC_WORDS_IN_ROW * 2))

		data_map[0][0][0] = 0x04
		data_map[0][0][1] = (i_bl_address & 0x0000FE) 
		data_map[0][0][2] = ((i_bl_address & 0x00FF00) >> 8)
		data_map[0][0][3] = 0x00	
		data_map[0][0][4] = ((i_bl_address & 0x7F0000) >> 16)
		data_map[0][0][5] = 0x00

		return data_map

	async def write_firmware(self,data_map):
		self.parent.console.print('\nSending Hello to the Bootloader... ')
		try:
			res = self.parent.console.com.write([0xc1])
			await asyncio.sleep(.02)
		except:
			self.parent.console.print('\nCould not send hello!\n')
		res = self.parent.console.com.read_all()
		if chr(res[3]) != 'K':
			self.parent.console.print('\nDid not receive OK\n')
			return
		self.parent.console.print(f'OK\n')

		failed = False
		try:
			for p in data_map:
				u_addr = p * PIC_WORDS_IN_ROW * 2 * PIC_ROWS_IN_PAGE
				cmd = []
				cmd.append((u_addr & 0x00FF0000) >> 16)
				cmd.append((u_addr & 0x0000FF00) >>  8)
				cmd.append((u_addr & 0x000000FF) >>  0)
				cmd.append(0x01) #erase command
				cmd.append(0x01) #1 byte, CRC
				cmd.append(self.make_crc(cmd))
				self.parent.console.print(f'Erasing page {p:04x} ... ')
				self.parent.console.com.write(cmd)
				await asyncio.sleep(.1)
				res = self.parent.console.com.read_all()
				if chr(res[0]) == 'K':
					self.parent.console.print('OK.')
				else:
					failed = True
					break
				self.parent.console.print(f' Writing page {p:04x}: ')
				for r in data_map[p]:
					r_addr = u_addr + (r * PIC_WORDS_IN_ROW * 2)
					cmd = []
					cmd.append((r_addr & 0x00FF0000) >> 16)
					cmd.append((r_addr & 0x0000FF00) >>  8)
					cmd.append((r_addr & 0x000000FF) >>  0)
					cmd.append(0x02) #write command
					cmd.append(PIC_ROW_SIZE + 0x01) #data length + crc
					for b in data_map[p][r]:
						cmd.append(b)
					cmd.append(self.make_crc(cmd))
					self.parent.console.com.write(cmd)
					await asyncio.sleep(.1)
					res = self.parent.console.com.read_all()
					if len(res) > 0 and chr(res[0]) == 'K':
						self.parent.console.print('.')
					else:
						failed = True
						break
				if failed: 
					break
				self.parent.console.print('OK\n')
		except Exception as ex:
			print(ex)
			failed = True
		if failed:
			self.parent.console.print('\nFirmware upload failed\n')
		else:
			self.parent.console.print('\nFirmware uploaded successfully\n')

	def make_crc(self,data):
		crc = 0
		for i in range(0,len(data)):
			crc -= data[i]
			crc &= 0x00ff			
		return crc
