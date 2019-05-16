#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import time

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.constants import INSERT, END

from exception import ExceptionModuleNotImport, ExceptionFilenameExtensionNotFound, ExceptionNoSignMatch
from processor import Processor
from utils import to_string


if __name__ == '__main__':
	WINDOW_TITLE = 'General Sorting & Searching'
	WINDOW_SIZE = '800x600'
	WINDOW = tk.Tk()
	WINDOW.title(WINDOW_TITLE)
	# window size
	# WINDOW.geometry(WINDOW_SIZE)

	intro_string = '''【使用說明】
	請在Input的輸入區域輸入檔案路徑(txt or json)或是直接輸入(數字/文字/list/dict)。
	並請選擇相對應需要的選項。

	輸入說明: 
		txt/直接輸入(數字/文字): 以逗號(全型/半型)、分號(全型/半型)、換行為分割(假如需要)。
		直接輸入(list): 前後為[], 中間為數字/文字(以半型逗號為分割)。
		直接輸入(dict): 同json檔標準。
		json: 遵循json檔標準, 以一組組{key: value}為分割(假如需要)。
	
	特殊說明:
		Binary Sorting: Input的資料須為已經排序過的(ASCII小到大)否則可能有誤。
		json檔的sorting以key為排序標準。
		txt/直接輸入的searching, 會輸出符合搜尋結果的是分割後第幾個。
		json檔的searching, 會將符合搜尋結果的那一組{key: value}輸出。
	'''
	ttk.Label(WINDOW, text=intro_string).grid(column=0, columnspan=2)

	# label for input scrolledtext
	ttk.Label(WINDOW, text='Input').grid(column=0, row=1)
	# label for output scrolledtext
	ttk.Label(WINDOW, text='Output').grid(column=1, row=1)

	# scrolledtext width
	SCROLL_WIDTH = 50
	# scrolledtext height
	SCROLL_HEIGHT = 20
	# input scrolledtext
	SCROLL_INPUT = scrolledtext.ScrolledText(WINDOW, width=SCROLL_WIDTH, height=SCROLL_HEIGHT, wrap=tk.WORD)
	SCROLL_INPUT.grid(column=0, row=2)
	# output scrolledtext
	SCROLL_OUTPUT = scrolledtext.ScrolledText(WINDOW, width=SCROLL_WIDTH, height=SCROLL_HEIGHT, wrap=tk.WORD)
	SCROLL_OUTPUT.grid(column=1, row=2)

	ttk.Label(WINDOW, text='請選擇是輸入路徑還是直接輸入').grid(column=0, row=3)
	choose_input_way = tk.StringVar()
	CHOOSE_LIST_INPUT_WAY = ttk.Combobox(WINDOW, textvariable=choose_input_way, state='readonly')
	CHOOSE_LIST_INPUT_WAY['values'] = ('路徑', '直接輸入')
	CHOOSE_LIST_INPUT_WAY.grid(column=0, row=4)
	CHOOSE_LIST_INPUT_WAY.current(0)

	ttk.Label(WINDOW, text='請選擇要排序還是搜尋').grid(column=1, row=3)
	choose_execute_way = tk.StringVar()
	CHOOSE_LIST_EXECUTE_WAY = ttk.Combobox(WINDOW, textvariable=choose_execute_way, state='readonly')
	CHOOSE_LIST_EXECUTE_WAY['values'] = ('Sorting', 'Searching')
	CHOOSE_LIST_EXECUTE_WAY.grid(column=1, row=4)
	CHOOSE_LIST_EXECUTE_WAY.current(0)

	ttk.Label(WINDOW, text='請選擇排序方法').grid(column=0, row=5)
	choose_sorting_way = tk.StringVar()
	CHOOSE_LIST_SORTING_WAY = ttk.Combobox(WINDOW, textvariable=choose_sorting_way, state='readonly')
	CHOOSE_LIST_SORTING_WAY['values'] = ('Bubble Sort', 'Selection Sort', 'Insertion Sort', 'Merge Sort', 'Quick Sort')
	CHOOSE_LIST_SORTING_WAY.grid(column=0, row=6)
	CHOOSE_LIST_SORTING_WAY.current(0)

	ttk.Label(WINDOW, text='請選擇排序順序').grid(column=1, row=5)
	choose_reverse = tk.StringVar()
	CHOOSE_LIST_REVERS = ttk.Combobox(WINDOW, textvariable=choose_reverse, state='readonly')
	CHOOSE_LIST_REVERS['values'] = ('ASCII 小->大', 'ASCII 大->小', '拼音 小->大', '拼音 大->小')
	CHOOSE_LIST_REVERS.grid(column=1, row=6)
	CHOOSE_LIST_REVERS.current(0)

	ttk.Label(WINDOW, text='請選擇搜尋方法').grid(column=0, row=7)
	choose_searching_way = tk.StringVar()
	CHOOSE_LIST_SEARCHING_WAY = ttk.Combobox(WINDOW, width=20, textvariable=choose_searching_way, state='readonly')
	CHOOSE_LIST_SEARCHING_WAY['values'] = ('Linear Search(部分匹配)', 'Linear Search(完全匹配)', 'Binary Search(完全匹配)')
	CHOOSE_LIST_SEARCHING_WAY.grid(column=0, row=8)
	CHOOSE_LIST_SEARCHING_WAY.current(0)

	ttk.Label(WINDOW, text='若要搜尋, 請輸入要搜尋的內容(若輸入為json檔/dictionary, 則請輸入要搜尋的key)').grid(column=1, row=7)
	key = tk.StringVar()
	TEXT_ENTRY_KEY = ttk.Entry(WINDOW, width=20, textvariable=key)
	TEXT_ENTRY_KEY.grid(column=1, row=8)

	def execute():
		SCROLL_OUTPUT.delete('1.0', END)
		original_input = SCROLL_INPUT.get('1.0', 'end-1c')
		result = ''
		start = None
		end = None
		elapsed = None
		is_dict = False

		# is path or not
		is_path = True
		if choose_input_way.get() == '路徑':
			is_path = True
		else:
			is_path = False
		# sorting or searching
		is_sorting = True
		if choose_execute_way.get() == 'Sorting':
			is_sorting = True
		else:
			is_sorting = False

		# sorting way
		sorting_way = choose_sorting_way.get()

		# reverse or no
		is_reverse = False
		is_pinyin = False
		way = choose_reverse.get()
		if way == 'ASCII 小->大':
			is_reverse = False
			is_pinyin = False
		elif way == 'ASCII 大->小':
			is_reverse = True
			is_pinyin = False
		elif way == '拼音 小->大':
			is_reverse = False
			is_pinyin = True
		elif way == '拼音 大->小':
			is_reverse = True
			is_pinyin = True

		# searching way
		searching_way = 'linear'
		is_full = False
		way = choose_searching_way.get()
		if way == 'Linear Search(部分匹配)':
			searching_way = 'linear'
			is_full = False
		elif way == 'Linear Search(完全匹配)':
			searching_way = 'linear'
			is_full = True
		elif way == 'Binary Search(完全匹配)':
			searching_way = 'binary'
			is_full = True
		try:
			processor = Processor(original_input, is_path=is_path)
			sign = processor.get_actual_type_sign()
			if sign == 'dict' or sign == 'json':
				is_dict = True
			else:
				is_dict = False
			start = time.time()
			if is_sorting:
				if sorting_way == 'Bubble Sort':
					result = processor.bubble_sort(reverse=is_reverse, pinyin=is_pinyin)
				elif sorting_way == 'Selection Sort':
					result = processor.selection_sort(reverse=is_reverse, pinyin=is_pinyin)
				elif sorting_way == 'Insertion Sort':
					result = processor.insertion_sort(reverse=is_reverse, pinyin=is_pinyin)
				elif sorting_way == 'Merge Sort':
					result = processor.merge_sort(reverse=is_reverse, pinyin=is_pinyin)
				elif sorting_way == 'Quick Sort':
					result = processor.quick_sort(reverse=is_reverse, pinyin=is_pinyin)
			else:
				if searching_way == 'linear':
					result = processor.linear_search(key.get(), full=is_full)
				else:
					result = processor.binary_search(key.get())
			end = time.time()
			elapsed = end - start
		except Exception as e:
			SCROLL_OUTPUT.insert(END, '請檢查Input或是對應選項的正確性。')
		else:
			if not is_sorting and key.get() == '':
				result = '請輸入要搜尋的內容或key'
			else:
				result = to_string(result, is_sorting=is_sorting, is_dict=is_dict)
				if is_sorting:
					result += '\n\n[' + sorting_way + ' finished in ' + str(elapsed) + 's.]'
				else:
					result += '\n\n[' + searching_way + ' searching finished in ' + str(elapsed) + 's.]'
			SCROLL_OUTPUT.insert(END, result)
		finally:
			pass
	BUTTON_EXECUTE = ttk.Button(WINDOW, text='執行', command=execute)
	BUTTON_EXECUTE.grid(column=0, columnspan=2)

	# show window
	WINDOW.mainloop()