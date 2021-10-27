#!/usr/bin/env python3
# encoding: utf-8

import npyscreen
from datetime import datetime




class ADD_RSS(npyscreen.Form):

	def create(self):
		
		self.url = self.add(npyscreen.TitleText, name = "RSS URL:", value= "www.a_beautiful_rss.com" )
		self.name = self.add(npyscreen.TitleText, name = "NAME:", value= "Name to identify the rss-feed." )
		self.description = self.add(npyscreen.TitleText, name = "DESCRIPTION:", value= "Write a simple description about the origin of the RSS Feed." )
		self.date_added = self.add(npyscreen.TitleDateCombo, name='DATE ADDED', value= datetime.today(),editable=False)
		

	def afterEditing(self):
		self.parentApp.setNextForm('MAIN')


