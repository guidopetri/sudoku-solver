#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python 3.6.4

#unit rule (only possible in that cell of the unit)
#intersection
#http://www.sudokuslam.com/hints.html

import itertools
import requests
import sys
import logging
import time
import json

logging.basicConfig(level=logging.DEBUG)

APIlink="https://sugoku.herokuapp.com/board?difficulty=easy"

allPossibilities = list('123456789')

class Cell():
	def __init__(self,value,locationY,locationX):
		self.location = (locationX,locationY)
		self.possibilities = list(allPossibilities)
		self.value = str(value)
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

logging.debug("getting puzzle")

page = requests.get(APIlink)
if page.status_code != 200:
	sys.exit()

logging.debug("puzzle acquired")

print(page.text)

sudokuPuzzle = page.json()['board']#[list('000000000'),list('080050030'),list('302009504'),list('400000200'),list('060080090'),list('001000003'),list('506800402'),list('010090070'),list('000000000')]#

logging.debug("puzzle: %s"%sudokuPuzzle)

#print(json.dumps({'board':sudokuPuzzle}))
onlineSolution = requests.post('https://sugoku.herokuapp.com/grade',page.text)
print(onlineSolution.text)
sys.exit()

allCellsList = []

rowNumber = 0
for row in sudokuPuzzle:
	colNumber = 0
	for number in row:
		allCellsList.append(Cell(number,colNumber,rowNumber))
		colNumber +=1
	rowNumber +=1

logging.debug("starting solve")
startTime = time.time()

notSolved = True
while notSolved:
	if time.time()-startTime >= 3:
		logging.debug("taking too long, aborting")
		for cell in allCellsList:
			print(cell.value,cell.location,cell.square,cell.possibilities)
		sys.exit()
	notSolved = False
	for cell in allCellsList:
		cell.calculatePossibilities(allCellsList)
		cell.setValue()
		if cell.solved == False:
			notSolved = True

logging.debug("solved")
solutionDict = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
for cell in allCellsList:
	solutionDict[cell.location[0]].append(int(cell.value))
	#print(cell.value,cell.location)

print(solutionDict, "\n")

solution = []

for i in range(0,9):
	solution.append(solutionDict[i])

print(solution)

data = {'board':solution}
print(json.dumps(data))
response = requests.post('https://sugoku.herokuapp.com/validate',json.dumps(data))

print(response.text)

onlineSolution = requests.post('https://sugoku.herokuapp.com/solve',json.dumps({'board':sudokuPuzzle}))
print(onlineSolution.text)