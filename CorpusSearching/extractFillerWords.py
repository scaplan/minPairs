#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Spencer Caplan
# Department of Linguistics, University of Pennsylvania
# Contact: spcaplan@sas.upenn.edu

import sys, math, os, random
reload(sys)
sys.setdefaultencoding('utf-8')

blacklistedPhones = {'t':1,'d':1}
blacklistedLetters = {'t':1,'d':1,'\'':1,'-':1,'.':1}

minFreq = 300
maxSyllLength = 3
minLetterLength = 4
maxLetterLength = 8

lexiconDict = {}
freqDict = {}

fillersToSample = 105

# IdNum,	Head,	Cob,	PronCnt,	PronStatus,	PhonStrsDISC,	PhonCVBr,	PhonSylBCLX
# 7,		aback,	59,		1,			P,			@-'b{k,			[V][CVC],	[@][b&k]

def removeStressAndBreaks(inputWord):
	cleanedWord = inputWord.replace('-', '')
	numSylls = len(inputWord) - len(cleanedWord) + 1
	cleanedWord = cleanedWord.replace('\'', '')
	cleanedWord = cleanedWord.replace('\"', '')
	return cleanedWord, numSylls

def readInLexicon(celexSource):
	with open(celexSource, 'r') as celexFile:
		currLine = celexFile.readline()

		# Skipping header
		currLine = celexFile.readline()
		while currLine:
			currTokens = currLine.split(',')
			if len(currTokens) >= 8:
				currWord = currTokens[1]
				currFreq = currTokens[2]

				if currWord[0] == '\"' or currWord[0].isupper():
					currLine = celexFile.readline()
					continue

				if int(currFreq) >= minFreq:
					currPhones, numSylls = removeStressAndBreaks(currTokens[5])
					containsBlacklistedPhon = False
					for phon in currPhones:
						if phon in blacklistedPhones:
							containsBlacklistedPhon = True

					# Also excluding words with orthographic 't' or 'd'
					for letter in currWord:
						if letter in blacklistedLetters:
							containsBlacklistedPhon = True

					if not containsBlacklistedPhon:
						if (numSylls <= maxSyllLength) and (len(currWord) >= minLetterLength) and (len(currWord) <= maxLetterLength):
							lexiconDict[currPhones] = currWord
							freqDict[currWord] = currFreq
			currLine = celexFile.readline()

##
## Main method block
##
if __name__=="__main__":

	# reading in epl.csv
	celexFileSource = sys.argv[1]
	#print celexFileSource
	readInLexicon(celexFileSource)

	#numCandidates = len(lexiconDict.keys())
	#print 'Num numCandidates:' + str(numCandidates)
	#for currPronounce in lexiconDict.keys():
	#	currOrthography = lexiconDict[currPronounce]
	#	print currOrthography


	# Now just take a random sample from this of the right length
	candidateList = lexiconDict.values()
	random.shuffle(candidateList)
	outputSet = candidateList[-fillersToSample:]

	for word in outputSet:
		print word
	
