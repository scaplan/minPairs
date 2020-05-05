from __future__ import division
import sys
import subprocess
import glob, os

## Author: Spencer Caplan, University of Pennsylvania
## Contact: spcaplan@sas.upenn.edu


outputFileNamesWithWordID = False
printDebugStatements = True

testFilesRun = False
counterSplice = True

def accessDictEntry(dictToCheck, entryToCheck):
	if entryToCheck in dictToCheck:
		return dictToCheck[entryToCheck]
	else:
		return 0


##
## Main method block
##
if __name__=="__main__":

	praat = "/home1/s/spcaplan/Documents/PRAAT/praat"
	#praat = "/usr/bin/praat"
	script = "create_continuum.praat"
	inputDir = "/mnt/nlpgridio2/nlp/users/spcaplan/VOT-editing/TrimmedWords/Targets/"
	outputDir = "/mnt/nlpgridio2/nlp/users/spcaplan/VOT-editing/OutputTargets-Edited-AllT"

	# all these in ms
	stepSize = int(5)
	minVOT = int(10)
	maxVOT = int(100)

	indexToNormDict = {}
	indexToCounterDict = {}
	indexToIDDIct = {}
	attestedIndexes = {}

	vowelSet = ['A','E']
	
	if testFilesRun:
		for vowel in vowelSet:
			for Tindex in range(1, 6):
				Tuid = 'T-' + vowel + '-' + str(Tindex)
				currTfile = inputDir + Tuid + '.wav'
				print currTfile
				if os.path.isfile(currTfile):
					for Dindex in range(1, 6):
						Duid = 'D-' + vowel + '-' + str(Dindex)
						currDfile = inputDir + Duid + '.wav'
						if os.path.isfile(currDfile):
							for vot in xrange(minVOT, maxVOT+1, stepSize):
								stepSizeSeconds = "%1.3f" % (vot/1000)
								output = outputDir+"/"+vowel+str(Tindex)+'_'+str(Dindex)+"_VOT_%i.wav" % vot
								subprocess.call([praat, script, Tuid, Duid, inputDir, stepSizeSeconds, output])
								print 'Processed: ' + output
		print 'Ran multi test files.'
		exit()
	else:

		for file in os.listdir(inputDir):
			if file.endswith(".wav"):
				fileAttributes = file.split("-")
				if len(fileAttributes) > 4:
					globalIndex = fileAttributes[0]
					localIndex = fileAttributes[1]
					phone = fileAttributes[2]
					trialType = fileAttributes[3]
					word = fileAttributes[4]
					word = word.replace('.wav','')

					if outputFileNamesWithWordID:
						indexToIDDIct[localIndex] = globalIndex + '-' + localIndex + '-' + phone + '-' + trialType + '-' + word
					else:
						indexToIDDIct[localIndex] = localIndex + '-' + trialType
					attestedIndexes[localIndex] = True
					if printDebugStatements:
						print file
						print globalIndex + '-' + localIndex + '-' + phone + '-' + trialType + '-' + word

					if phone == 'T':
						indexToNormDict[localIndex] = file
					elif phone == 'D':
						indexToCounterDict[localIndex] = file

		if printDebugStatements:
			print 'Onto execution loop...'
		for currIndex in attestedIndexes:
			print currIndex
			normFile = accessDictEntry(indexToNormDict, currIndex)
			if counterSplice:
				counterFile = accessDictEntry(indexToCounterDict, currIndex)
			else:
				counterFile = accessDictEntry(indexToNormDict, currIndex)
			idName = accessDictEntry(indexToIDDIct, currIndex)
			if normFile == 0 or counterFile == 0 or idName == 0:
				break
			if printDebugStatements:
				print 'Running: ' + normFile
			normFile = normFile[:-4]
			counterFile = counterFile[:-4]

			ambiguateScript = "ambiguateVoicingf0.praat"
			subprocess.call([praat, ambiguateScript, counterFile, inputDir, 80, 30, 1, output])

			for vot in xrange(minVOT, maxVOT+1, stepSize):
				stepSizeSeconds = "%1.3f" % (vot/1000)
				output = outputDir+"/"+idName+"_VOT_%i.wav" % vot
				subprocess.call([praat, script, normFile, counterFile, inputDir, stepSizeSeconds, output])

		print 'Completed.'
