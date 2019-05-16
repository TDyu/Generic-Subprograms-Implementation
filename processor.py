#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import inspect
import json

from exception import ExceptionModuleNotImport, ExceptionFilenameExtensionNotFound, ExceptionNoSignMatch
from utils import re_split
from data_type import List, Dictionary
import data_type
import sorting

class Processor(object):
	"""Like Factory Class
	Generate instance of the corresponding class type 
	which implements Sorting and Searching.
	"""
	def __init__(self, origianl_input, is_path=False):
		super(Processor, self).__init__()
		self.origianl_input = origianl_input
		self.original_type = type(origianl_input)
		self.modules_list = ['data_type']
		self.actual_instance = None
		self.actual_type = None
		self.is_path = is_path
		try:
			self.__transform()
		except ExceptionFilenameExtensionNotFound as e:
			raise e
		except AttributeError as e:
			raise e
		except ExceptionNoSignMatch as e:
			raise e
		else:
			pass
		finally:
			pass

	def get_actual_type_sign(self):
		return self.actual_instance.get_sign()

	def add_module(self, module_name):
		'''Add Module Wantted Scanning
		
		Add the module to modules list 
		that will be scanned when check type.
		
		Arguments:
			module_name {str} -- the module name
		
		Raises:
			ExceptionModuleNotImport -- If the module has not be imported.
		'''
		try:
			if 'data_type' not in sys.modules:
				raise ExceptionModuleNotImport(module_name)
		except ExceptionModuleNotImport as e:
			raise e
		else:
			self.modules_list.append(module_name)

	def __get_filename_extension(self):
		'''Get Filename Extension String
		
		Get the filename extension string from path(original input).
		
		Returns:
			str -- filename extension
		
		Raises:
			ExceptionFilenameExtensionNotFound -- If the filename extension 
				cannot be found in absolute path.
		'''
		index = self.origianl_input.rfind('.') + 1
		try:
			if index == -1:
				raise ExceptionFilenameExtensionNotFound(self.origianl_input)
		except ExceptionFilenameExtensionNotFound as e:
			raise e
		else:
			filename_extension = self.origianl_input[index:]
			return filename_extension

	def __parse_keyboard_data(self):
		if self.origianl_input[0] == '{' and self.origianl_input[-1] == '}':
			to_dict = json.loads(self.origianl_input)
			return Dictionary(to_dict)
		elif self.origianl_input[0] == '[' and self.origianl_input[-1] == ']':
			to_list = self.origianl_input[1:-1]
			rule = '[,]'
			splited_list = re_split(rule, to_list)
			return List(splited_list)
		else: 
			rule = '[,，;；\n]'
			splited_list = re_split(rule, self.origianl_input)
			return List(splited_list)

	def __parse_file_data(self, sign):
		'''Check Corresponding File Class Type
		
		Find the corresponding file class type in assigned module(s)
		according with sign.
		(ref. http://rrifx.com/post/python-moudle-all-class/)

		Arguments:
			sign {str} -- the filename extension

		Returns:
			Object -- found class type instance
		
		Raises:
			ExceptionNoSignMatch -- If the file sign(filename extension) 
				cannot be matched with any sign in custom class.
			AttributeError -- getSign() or getInstance() 
				had not be definded in the class.
		'''
		instance = None
		is_found = False
		try:
			for module_name in self.modules_list:
				model_moudle = sys.modules[module_name]
				for name, obj in inspect.getmembers(model_moudle):
					if inspect.isclass(obj) and sign == obj.get_sign():
						instance = obj(self.origianl_input)
						is_found = True
						break
				if is_found:
					break
			if not is_found:
				raise ExceptionNoSignMatch(sign)
		except AttributeError as e:
			raise AttributeError('The custom class may have forgotten to define "sign".')
		except ExceptionNoSignMatch as e:
			raise e
		else:
			return instance

	def __transform(self):
		sign = None
		instance = None
		try:
			if self.is_path:
				sign = self.__get_filename_extension()
				instance = self.__parse_file_data(sign)
			else:
				instance = self.__parse_keyboard_data()
		except ExceptionFilenameExtensionNotFound as e:
			raise e
		except AttributeError as e:
			raise e
		except ExceptionNoSignMatch as e:
			raise e
		else:
			self.actual_instance = instance
			self.actual_type = type(self.actual_instance)
		finally:
			pass

	def bubble_sort(self, reverse=False, pinyin=False):
		# О(n²)
		return self.actual_instance.bubble_sort(reverse=reverse, pinyin=pinyin)

	def selection_sort(self, reverse=False, pinyin=False):
		# О(n²)
		return self.actual_instance.selection_sort(reverse=reverse, pinyin=pinyin)

	def insertion_sort(self, reverse=False, pinyin=False):
		# О(n²)
		return self.actual_instance.insertion_sort(reverse=reverse, pinyin=pinyin)

	def merge_sort(self, reverse=False, pinyin=False):
		# O(n*log2 n)
		return self.actual_instance.merge_sort(reverse=reverse, pinyin=pinyin)

	def quick_sort(self, reverse=False, pinyin=False):
		# O(n*log2 n)
		return self.actual_instance.quick_sort(reverse=reverse, pinyin=pinyin)

	def linear_search(self, key, full=True):
		# O(n)
		return self.actual_instance.linear_search(key, full=full)

	def binary_search(self, key):
		# O(log2 n) 
		return self.actual_instance.binary_search(key)

	def __str__(self):
		string = 'original data: ' + str(self.origianl_input) + '\n'
		string += 'original type: ' + str(self.original_type) + '\n'
		string += 'actual instance: ' + str(self.actual_instance) + '\n'
		string += 'actual type: ' + str(self.actual_type) + '\n'
		return string


# if __name__ == '__main__':
# 	pass