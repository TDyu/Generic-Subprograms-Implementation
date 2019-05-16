#!/usr/bin/python3
# -*- coding: utf-8 -*-

class ExceptionModuleNotImport(Exception):
	"""If the module not imported when user want to add to use."""
	def __init__(self, module_name):
		super(ExceptionModuleNotImport, self).__init__()
		self.message = ('[ExceptionModuleNotImport]\n The module named "' 
						+ module_name + '" has not be imported in "processor.py".\n')
		self.short_message = ('The module named "'+ module_name
						+ '" has not be imported in "processor.py".')

	def __str__(self):
		return self.short_message

class ExceptionFilenameExtensionNotFound(Exception):
	"""If the filename extension cannot be found in absolute path."""
	def __init__(self, path):
		super(ExceptionFilenameExtensionNotFound, self).__init__()
		self.message = ('[ExceptionFilenameExtensionNotFound]\n	'
						+ 'The file path "' + path 
						+ '" lost filename extension or does not exist.\n')
		self.short_message = 'The file path lost filename extension or does not exist.'

	def __str__(self):
		return self.short_message

class ExceptionNoSignMatch(Exception):
	"""If the file sign(filename extension) cannot be matched with any sign in custom class."""
	def __init__(self, sign):
		super(ExceptionNoSignMatch, self).__init__()
		self.message = ('[ExceptionNoSignMatch]\n	'
						+ 'The sign "' + sign 
						+ '" cannot be matched with any class ' 
						+ 'in wantted scanning modules.\n'
						+ '(The correspoding class may has not be defined' 
						+ ',or the filename extension is error.)\n')
		self.short_message = ('The sign "' + sign 
							+ '" cannot be matched with any class ' 
							+ 'in wantted scanning modules.\n'
							+ '(The correspoding class may has not be defined' 
							+ ',or the filename extension is error.)')