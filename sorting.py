#!/usr/bin/python3
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

class Sorting(metaclass=ABCMeta):
	"""Use abc module to make Sorting like a interface"""
	def __init__(self):
		super(Sorting, self).__init__()

	@abstractmethod
	def bubble_sort(self, reverse=False, pinyin=False):
		# О(n²)
		pass

	@abstractmethod
	def selection_sort(self, reverse=False, pinyin=False):
		# О(n²)
		pass

	@abstractmethod
	def insertion_sort(self, reverse=False, pinyin=False):
		# О(n²)
		pass

	@abstractmethod
	def merge_sort(self, reverse=False, pinyin=False):
		# O(n*log2 n)
		pass

	@abstractmethod
	def quick_sort(self, reverse=False, pinyin=False):
		# O(n*log2 n)
		pass