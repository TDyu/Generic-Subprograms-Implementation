#!/usr/bin/python3
# -*- coding: utf-8 -*-
import copy
import json
import codecs
from collections import deque

from sorting import Sorting
from searching import Searching
from utils import re_split, to_pinyin_dict, to_original_string

class DataType(object):
	"""docstring for DataType"""
	sign = ''
	def __init__(self):
		super(DataType, self).__init__()

	@classmethod
	def get_sign(cls):
		return cls.sign


class List(list, DataType, Sorting, Searching):
	"""list Implement Sorting and Searching"""
	sign = 'list'
	def __init__(self, inner_list):
		super(List, self).__init__()
		self.inner_list = inner_list

	def __sort(self, sort_type, reverse, pinyin):
		# relay station of total sort algorithm for List
		prepare_list = copy.deepcopy(self.inner_list)
		pinyin_dict = {}

		# change to pinyin
		if pinyin:
			pinyin_dict = to_pinyin_dict(prepare_list)

		# real sorting
		if sort_type == 'bubble':
			prepare_list = self.__bubble_sort(prepare_list)
		elif sort_type == 'selection':
			prepare_list = self.__selection_sort(prepare_list)
		elif sort_type == 'insertion':
			prepare_list = self.__insertion_sort(prepare_list)
		elif sort_type == 'merge':
			prepare_list = self.__merge_sort(prepare_list)
		elif sort_type == 'quick':
			prepare_list = self.__quick_sort(prepare_list)

		# deal with reversing
		if reverse:
			prepare_list.reverse()

		# change back
		if pinyin:
			prepare_list = to_original_string(prepare_list, pinyin_dict)

		return prepare_list

	def __bubble_sort(self, prepare_list):
		# 重複一直比, 比到沒有再需要交換的
		for i in range(len(prepare_list) - 1):
			for j in range(1, len(prepare_list) - i):
				if prepare_list[j - 1] > prepare_list[j]: 
					prepare_list[j - 1], prepare_list[j] = prepare_list[j], prepare_list[j - 1]
		return prepare_list

	def bubble_sort(self, reverse=False, pinyin=False):
		# О(n²)
		return self.__sort('bubble', reverse, pinyin)

	def __selection_sort(self, prepare_list):
		# 未排(右邊)找到最大, 放到排完(左邊)的後面
		for i in range(len(prepare_list)):
			current_max_index = i
			for j in range(i + 1, len(prepare_list)):
				if prepare_list[current_max_index] > prepare_list[j]:
					current_max_index = j
			prepare_list[i], prepare_list[current_max_index] = prepare_list[current_max_index], prepare_list[i]
		return prepare_list

	def selection_sort(self, reverse=False, pinyin=False):
		# О(n²)
		return self.__sort('selection', reverse, pinyin)

	def __insertion_sort(self, prepare_list):
		# 從還沒排的拿出來和排過的比較, 在排過的裡面從後往前掃，找到相應位置並插入
		for i in range(1, len(prepare_list)):
			key = prepare_list[i]
			j = i
			while j > 0 and key < prepare_list[j - 1]: 
				prepare_list[j] = prepare_list[j - 1]
				j -= 1
			prepare_list[j] = key
		return prepare_list

	def insertion_sort(self, reverse=False, pinyin=False):
		# О(n²)
		return self.__sort('insertion', reverse, pinyin)

	def __merge_sort(self, prepare_list):
		# 分割到剩下一個 -> 依大小各自合併 -> 遞歸 -> 最終合併
		def merge(left_list, right_list):
			merged_list = deque()
			left_list = deque(left_list)
			right_list = deque(right_list)

			while left_list and right_list:
				if left_list[0] <= right_list[0]:
					merged_list.append(left_list.popleft())
				else:
					merged_list.append(right_list.popleft())

			if right_list:
				merged_list.extend(right_list)
			else:
				merged_list.extend(left_list)

			return list(merged_list)

		if len(prepare_list) <= 1:
			return prepare_list

		middle_index = int(len(prepare_list) // 2)
		left_list = self.__merge_sort(prepare_list[:middle_index])
		right_list = self.__merge_sort(prepare_list[middle_index:])

		return merge(left_list, right_list)

	def merge_sort(self, reverse=False, pinyin=False):
		# O(n*log2 n)
		return self.__sort('merge', reverse, pinyin)

	def __quick_sort(self, prepare_list):
		# 分割 -> 找基準點 -> 遞歸 -> 合併
		if prepare_list == []:
			return prepare_list

		left_list = []
		right_list = []
		middle_item = prepare_list[0]

		for item in prepare_list[1:]:
			if item < middle_item:
				left_list.append(item)
			else:
				right_list.append(item)
		return self.__quick_sort(left_list) + [middle_item] + self.__quick_sort(right_list)

	def quick_sort(self, reverse=False, pinyin=False):
		# O(n*log2 n)
		return self.__sort('quick', reverse, pinyin)

	def linear_search(self, key, full=True):
		# O(n)
		# 一個一個和key比, 直到找到或所有都均找完
		found_indexes = []
		for item in self.inner_list:
			if full:
				# fully match
				if item == key:
					found_indexes.append(self.inner_list.index(item))
			else:
				# partially match
				if key in item:
					found_indexes.append(self.inner_list.index(item))
		return found_indexes

	def binary_search(self, key):
		# O(log2 n) 
		# 要是已經排序過的(小->大)
		# 只能全比 不能部分
		# 分成兩部份, key和中間的值比, 一樣就是找到, 小於再比前半段, 大於再比後半段
		
		# prepare_list = self.quick_sort()
		prepare_list = self.inner_list

		first_index = 0
		last_index = len(prepare_list) - 1
		found_index = -1

		while first_index <= last_index and found_index == -1:
			middle_index = (first_index + last_index) // 2
			if prepare_list[middle_index] == key:
				found_index = middle_index
			else:
				if key < prepare_list[middle_index]:
					last_index = middle_index - 1
				else:
					first_index = middle_index + 1

		return found_index

	def get_inner_list(self):
		return self.inner_list

	def __str__(self):
		return str(self.inner_list)


class Dictionary(dict, DataType, Sorting, Searching):
	"""dictImplement Sorting and Searching"""
	sign = 'dict'
	def __init__(self, inner_dict):
		super(Dictionary, self).__init__()
		self.inner_dict = inner_dict

	def bubble_sort(self, reverse=False, pinyin=False):
		# О(n²)
		key_list = list(self.inner_dict.keys())
		prepare_list = List(key_list)
		sorted_key_list = prepare_list.bubble_sort(reverse=reverse, pinyin=pinyin)
		sorted_dict = {}
		for key in sorted_key_list:
			sorted_dict[key] = self.inner_dict[key]
		return sorted_dict

	def selection_sort(self, reverse=False, pinyin=False):
		# О(n²)
		key_list = list(self.inner_dict.keys())
		prepare_list = List(key_list)
		sorted_key_list = prepare_list.selection_sort(reverse=reverse, pinyin=pinyin)
		sorted_dict = {}
		for key in sorted_key_list:
			sorted_dict[key] = self.inner_dict[key]
		return sorted_dict

	def insertion_sort(self, reverse=False, pinyin=False):
		# О(n²)
		key_list = list(self.inner_dict.keys())
		prepare_list = List(key_list)
		sorted_key_list = prepare_list.insertion_sort(reverse=reverse, pinyin=pinyin)
		sorted_dict = {}
		for key in sorted_key_list:
			sorted_dict[key] = self.inner_dict[key]
		return sorted_dict

	def merge_sort(self, reverse=False, pinyin=False):
		# O(n*log2 n)
		key_list = list(self.inner_dict.keys())
		prepare_list = List(key_list)
		sorted_key_list = prepare_list.merge_sort(reverse=reverse, pinyin=pinyin)
		sorted_dict = {}
		for key in sorted_key_list:
			sorted_dict[key] = self.inner_dict[key]
		return sorted_dict

	def quick_sort(self, reverse=False, pinyin=False):
		# O(n*log2 n)
		key_list = list(self.inner_dict.keys())
		prepare_list = List(key_list)
		sorted_key_list = prepare_list.quick_sort(reverse=reverse, pinyin=pinyin)
		sorted_dict = {}
		for key in sorted_key_list:
			sorted_dict[key] = self.inner_dict[key]
		return sorted_dict

	def linear_search(self, key, full=True):
		# O(n)
		key_list = list(self.inner_dict.keys())
		prepare_list = List(key_list)
		found_indexes = prepare_list.linear_search(key, full=full)
		found_dict_list = []
		if len(found_indexes) != 0:
			for found in found_indexes:
				value_dict = {}
				value_dict[prepare_list.get_inner_list()[found]] = self.inner_dict[prepare_list.get_inner_list()[found]]
				found_dict_list.append(value_dict)
		return found_dict_list

	def binary_search(self, key):
		# O(log2 n) 
		key_list = list(self.inner_dict.keys())
		prepare_list = List(key_list)
		found_index = prepare_list.binary_search(key)
		found_dict = {}
		if found_index != -1:
			found_dict[prepare_list.get_inner_list()[found_index]] = self.inner_dict[prepare_list.get_inner_list()[found_index]]
		return found_dict


class File(DataType):
	"""Parent class of all file type"""
	path = ''
	def __init__(self, path):
		super(File, self).__init__()
		self.path = path


class FileText(File, Sorting, Searching):
	"""docstring for FileText"""
	sign = 'txt'
	def __init__(self, path):
		super(FileText, self).__init__(path)
		self.data_list = self.__read_txt()
		self.prepare_list = List(self.data_list)

	def __read_txt(self):
		file = open(self.path, 'r', encoding='utf-8')
		data = file.read()
		data_list = re_split('[,，;；\n]', data)
		file.close()
		return data_list

	def bubble_sort(self, reverse=False, pinyin=False):
		# О(n²)
		return self.prepare_list.bubble_sort(reverse=reverse, pinyin=pinyin)

	def selection_sort(self, reverse=False, pinyin=False):
		# О(n²)
		return self.prepare_list.selection_sort(reverse=reverse, pinyin=pinyin)

	def insertion_sort(self, reverse=False, pinyin=False):
		# О(n²)
		return self.prepare_list.insertion_sort(reverse=reverse, pinyin=pinyin)

	def merge_sort(self, reverse=False, pinyin=False):
		# O(n*log2 n)
		return self.prepare_list.merge_sort(reverse=reverse, pinyin=pinyin)

	def quick_sort(self, reverse=False, pinyin=False):
		# O(n*log2 n)
		return self.prepare_list.quick_sort(reverse=reverse, pinyin=pinyin)

	def linear_search(self, key, full=True):
		# O(n)
		return self.prepare_list.linear_search(key, full=full)

	def binary_search(self, key):
		# O(log2 n) 
		return self.prepare_list.binary_search(key)


class FileXls(File, Sorting, Searching):
	"""docstring for FileXls"""
	sign = 'xls'
	def __init__(self, path):
		super(FileXls, self).__init__(path)

	def bubble_sort(self, reverse=False, pinyin=False):
		# О(n²)
		pass

	def selection_sort(self, reverse=False, pinyin=False):
		# О(n²)
		pass

	def insertion_sort(self, reverse=False, pinyin=False):
		# О(n²)
		pass

	def merge_sort(self, reverse=False, pinyin=False):
		# O(n*log2 n)
		pass

	def quick_sort(self, reverse=False, pinyin=False):
		# O(n*log2 n)
		pass

	def linear_search(self, key, full=True):
		# O(n)
		pass

	def binary_search(self, key):
		# O(log2 n) 
		pass


class FileXlsx(FileXls):
	"""docstring for FileXls"""
	sign = 'xlsx'
	def __init__(self, path):
		super(FileXlsx, self).__init__(path)


class FileCsv(File, Sorting, Searching):
	"""docstring for FileCsv"""
	sign = 'csv'
	def __init__(self, path):
		super(FileCsv, self).__init__(path)

	def bubble_sort(self, reverse=False, pinyin=False):
		# О(n²)
		pass

	def selection_sort(self, reverse=False, pinyin=False):
		# О(n²)
		pass

	def insertion_sort(self, reverse=False, pinyin=False):
		# О(n²)
		pass

	def merge_sort(self, reverse=False, pinyin=False):
		# O(n*log2 n)
		pass

	def quick_sort(self, reverse=False, pinyin=False):
		# O(n*log2 n)
		pass

	def linear_search(self, key, full=True):
		# O(n)
		pass

	def binary_search(self, key):
		# O(log2 n) 
		pass
	

class FileJson(File, Sorting, Searching):
	"""docstring for FileJson"""
	sign = 'json'
	def __init__(self, path):
		super(FileJson, self).__init__(path)
		self.data_dict = self.__read_json()
		self.prepare_dict = Dictionary(self.data_dict)

	def __read_json(self):
		file = codecs.open(self.path, 'rb+', encoding='utf-8')
		content = json.loads(file.read())
		file.close()
		return content

	def bubble_sort(self, reverse=False, pinyin=False):
		# О(n²)
		return self.prepare_dict.bubble_sort(reverse=reverse, pinyin=pinyin)

	def selection_sort(self, reverse=False, pinyin=False):
		# О(n²)
		return self.prepare_dict.selection_sort(reverse=reverse, pinyin=pinyin)

	def insertion_sort(self, reverse=False, pinyin=False):
		# О(n²)
		return self.prepare_dict.insertion_sort(reverse=reverse, pinyin=pinyin)

	def merge_sort(self, reverse=False, pinyin=False):
		# O(n*log2 n)
		return self.prepare_dict.merge_sort(reverse=reverse, pinyin=pinyin)

	def quick_sort(self, reverse=False, pinyin=False):
		# O(n*log2 n)
		return self.prepare_dict.quick_sort(reverse=reverse, pinyin=pinyin)

	def linear_search(self, key, full=True):
		# O(n)
		return self.prepare_dict.linear_search(key, full=full)

	def binary_search(self, key):
		# O(log2 n) 
		return self.prepare_dict.binary_search(key)


# if __name__ == '__main__':
# 	test = FileJson('test_data/test_json_ch.json')
# 	print(test.bubble_sort(reverse=True, pinyin=True))