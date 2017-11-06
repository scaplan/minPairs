#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Spencer Caplan
# Department of Linguistics, University of Pennsylvania
# Contact: spcaplan@sas.upenn.edu

import sys, math, os, subprocess, glob, operator, collections
reload(sys)
sys.setdefaultencoding('utf-8')
import unicodedata
from unicodedata import normalize

#phoneStringSearch = 'sIs'
phoneStringSearch = 'sEs'
searchLength = len(phoneStringSearch)

lexiconDict = {}
freqDict = {}
searchMatchDict = {}

# IdNum,	Head,	Cob,	PronCnt,	PronStatus,	PhonStrsDISC,	PhonCVBr,	PhonSylBCLX
# 7,		aback,	59,		1,			P,			@-'b{k,			[V][CVC],	[@][b&k]

def removeStressAndBreaks(inputWord):
	cleanedWord = inputWord.replace('-', '')
	cleanedWord = cleanedWord.replace('\'', '')
	cleanedWord = cleanedWord.replace('\"', '')
	return cleanedWord

def readInLexicon(celexSource):
	with open(celexSource, 'r') as celexFile:
		currLine = celexFile.readline()
		while currLine:
			currTokens = currLine.split(',')
			if len(currTokens) >= 8:
				currWord = currTokens[1]
				currFreq = currTokens[2]
				currPhones = removeStressAndBreaks(currTokens[5])
				lexiconDict[currPhones] = currWord
				freqDict[currWord] = currFreq
				if phoneStringSearch == currPhones[-searchLength:]:
					searchMatchDict[currPhones] = currWord
				
			currLine = celexFile.readline()

##
## Main method block
##
if __name__=="__main__":

	# reading in epl.csv
	celexFileSource = sys.argv[1]
	#print celexFileSource
	readInLexicon(celexFileSource)

	print 'Num words:' + str(len(lexiconDict.keys()))
	print 'Searching for: ' + phoneStringSearch
	print 'Num matches: ' + str(len(searchMatchDict)) + '\n'
	for currMatch in searchMatchDict.keys():
		currWord = searchMatchDict[currMatch]
		currFreq = freqDict[currWord]
		toPrint = currWord + ', ' + currMatch + ', ' + currFreq
		print toPrint