#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
from pypinyin import lazy_pinyin # https://pypi.python.org/pypi/pypinyin

def re_split(rule, string):
	splited_list = re.split(rule, string)
	return splited_list

def judge_english(key):  
	return all(ord(c) < 128 for c in key)  

def pinyin_str(ch_str):
	# 若是中文則取字首拼音, 英文則全取
	list_pinyin = []
	for i in ch_str:
		if i == ' ':
			continue
		elif judge_english(i):
			list_pinyin.append(i)
		else:
			list_pinyin.append(lazy_pinyin(i)[0])

	string = ''
	for i in list_pinyin:
		string += i[0]
	return string

def to_pinyin_dict(prepare_list):
	# record pinyin with original string
	pinyin_dict = {}
	for i in range(len(prepare_list)):
		ori = prepare_list[i]
		prepare_list[i] = pinyin_str(prepare_list[i])
		pinyin_dict[prepare_list[i]] = ori
	return pinyin_dict

def to_original_string(prepare_list, pinyin_dict):
	for i in range(len(prepare_list)):
		prepare_list[i] = pinyin_dict[prepare_list[i]]
	return prepare_list

def to_string(original_data, is_sorting=True, is_dict=False):
	string = ''
	if type(original_data) is list:
		if not is_sorting and len(original_data) == 0:
			return '無符合對象'
		if not is_sorting and is_dict:
			for dictionary in original_data:
				string += str(dictionary) + '\n'
		else:
			for item in original_data:
				if original_data.index(item) != len(original_data) - 1:
					if not is_sorting:
						string += '分割後第 ' + str(item + 1) + ' 個\n'
					else:
						string += str(item) + '\n'
				else:
					if not is_sorting:
						string += '分割後第 ' + str(item + 1) + ' 個'
					else:
						string += str(item)
	elif type(original_data) is dict:
		if not is_sorting and len(original_data) == 0:
			return '無符合對象'
		string = str(original_data)
	else:
		if not is_sorting:
			if original_data == -1:
				return '無符合對象'
			else:
				string += '分割後第 ' + str(original_data + 1) + ' 個'
	return string

# if __name__ == '__main__':
# 	test = '左xx'
# 	print(pinyin_str(test))