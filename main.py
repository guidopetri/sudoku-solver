#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python 3.6.4

# import pandas as pd
# import numpy as np
# import matplotlib
#import codecs
import itertools
#import requests

#APIlink='https://sugoku.herokuapp.com/board?difficulty=easy'

allPossibilities = list('123456789')

class Cell():
	def __init__(self,value,locationY,locationX):
		self.location = (locationY,locationX)
		self.possibilities = list(allPossibilities)
		self.value = value
		self.square = squareFinder(self.location)
		self.solved = False

	def calculatePossibilities(self,allCells):
		if self.value != '0':
			self.possibilities = list(self.value)
			self.solved = True
		else:
			for columnCell in (x for x in allCells if x.location[0] == self.location[0]):
				if columnCell.value != '0':
					try:
						self.possibilities.remove(columnCell.value)
					except ValueError:
						pass
			for rowCell in (x for x in allCells if x.location[1] == self.location[1]):
				if rowCell.value != '0':
					try:
						self.possibilities.remove(rowCell.value)
					except ValueError:
						pass
			for squareCell in (x for x in allCells if x.square == self.square):
				if squareCell.value != '0':
					try:
						self.possibilities.remove(squareCell.value)
					except ValueError:
						pass
		return

	def setValue(self):
		if len(self.possibilities) == 1:
			self.value = self.possibilities[0]
		return

# class Unit():
# 	def __init__(self,unitType,cellsList):
# 		if unitType in ['row','col','square']:
# 			self.unitType = unitType
# 		else:
# 			raise ValueError("type of unit incompatible")
# 		if len(cellsList) != 9:
# 			raise ValueError("not enough cells in unit!")
# 		self.cellsList = cellsList
# 		self.valid = False
# 		self.testValidity()

# 	def testValidity(self):
# 		count = 0
# 		runOn = []
# 		for cell in cellsList:
# 			count += int(cell.value)
# 			runOn.append(int(cell.value))
# 		if count != 45:
# 			raise AssertionError("sum doesn't equal 45")
# 		if sorted(runOn) != [1,2,3,4,5,6,7,8,9]:
# 			raise AssertionError("doesn't contain 1-9")
# 		self.valid = True

def squareFinder(location):
	squareID = 0
	if location in itertools.product(range(0,3),range(0,3)):
		squareID = 1
	if location in itertools.product(range(0,3),range(3,6)):
		squareID = 2
	if location in itertools.product(range(0,3),range(6,9)):
		squareID = 3
	if location in itertools.product(range(3,6),range(0,3)):
		squareID = 4
	if location in itertools.product(range(3,6),range(3,6)):
		squareID = 5
	if location in itertools.product(range(3,6),range(6,9)):
		squareID = 6
	if location in itertools.product(range(6,9),range(0,3)):
		squareID = 7
	if location in itertools.product(range(6,9),range(3,6)):
		squareID = 8
	if location in itertools.product(range(6,9),range(6,9)):
		squareID = 9
	return squareID

samplePuzzle = [
	['0','3','9','1','0','6','2','0','0'],
	['6','0','4','5','0','0','0','0','0'],
	['0','5','0','0','2','0','0','6','0'],
	['0','1','2','0','9','0','5','4','0'],
	['9','0','0','0','0','0','0','0','1'],
	['0','4','7','0','3','0','8','2','0'],
	['0','6','0','0','7','0','0','9','0'],
	['0','0','0','0','0','3','1','0','4'],
	['0','0','3','9','0','4','6','8','0']
	]

allCellsList = []

rowNumber = 0
for row in samplePuzzle:
	colNumber = 0
	for number in row:
		allCellsList.append(Cell(number,colNumber,rowNumber))
		colNumber +=1
	rowNumber +=1

notSolved = True
while notSolved:
	notSolved = False
	for cell in allCellsList:
		cell.calculatePossibilities(allCellsList)
		cell.setValue()
		if cell.solved == False:
			notSolved = True

print("solved")
for cell in allCellsList:
	print(cell.value,cell.location)