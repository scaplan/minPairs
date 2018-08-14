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

blockRhoticCluster = False

lexiconDict = {}
freqDict = {}

phoneOneOnsetDict = {}
phoneTwoOnsetDict = {}

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

				if blockRhoticCluster:
					if len(currPhones) > 1:
						currOnset = currPhones[0]
						if currOnset == phoneOne and currPhones[1] != 'r':
							phoneOneOnsetDict[currPhones] = currWord
						elif currOnset == phoneTwo and currPhones[1] != 'r':
							phoneTwoOnsetDict[currPhones] = currWord
				else:
					currOnset = currPhones[0]
					if currOnset == phoneOne:
						phoneOneOnsetDict[currPhones] = currWord
					elif currOnset == phoneTwo:
						phoneTwoOnsetDict[currPhones] = currWord
			currLine = celexFile.readline()

def printPairToCSV(pronounceOne, pronounceTwo):
	wordOne = phoneOneOnsetDict[pronounceOne]
	wordTwo = phoneTwoOnsetDict[pronounceTwo]
	freqOne = freqDict[wordOne]
	freqTwo = freqDict[wordTwo]

	toPrint = wordOne + ',' + pronounceOne + ',' + str(freqOne) + ',' + wordTwo + ',' + pronounceTwo + ',' + str(freqTwo)
	print toPrint

##
## Main method block
##
if __name__=="__main__":

	# reading in epl.csv
	celexFileSource = sys.argv[1]
	phoneOne = sys.argv[2]
	phoneTwo = sys.argv[3]
	#print celexFileSource
	readInLexicon(celexFileSource)

	numMinPairs = 0

	print 'Num words:' + str(len(lexiconDict.keys()))
	print phoneOne + ' onset: ' + str(len(phoneOneOnsetDict.keys()))
	print phoneTwo + ' onset: ' + str(len(phoneTwoOnsetDict.keys()))
	print ''
	for tPronounce in phoneOneOnsetDict.keys():
		phoneList = list(tPronounce)
		phoneList[0] = phoneTwo
		dPronounce = "".join(phoneList)
		if dPronounce in phoneTwoOnsetDict:
			printPairToCSV(tPronounce, dPronounce)
			numMinPairs += 1

	print '\nnumMinPairs: ' + str(numMinPairs)