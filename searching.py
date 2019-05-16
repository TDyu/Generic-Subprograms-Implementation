#!/usr/bin/python3
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

class Searching(metaclass=ABCMeta):
	"""Use abc module to make Searching like a interface"""
	def __init__(self):
		super(Searching, self).__init__()

	@abstractmethod
	def linear_search(self, key, full=True):
		# O(n)
		pass

	@abstractmethod
	def binary_search(self, key):
		# O(log2 n) 
		pass