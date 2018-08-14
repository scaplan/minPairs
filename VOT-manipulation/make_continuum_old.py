from __future__ import division
import sys
import subprocess
import glob, os

## Author: Spencer Caplan, University of Pennsylvania
## Contact: spcaplan@sas.upenn.edu

def accessDictEntry(dictToCheck, entryToCheck):
	if entryToCheck in dictToCheck:
		return dictToCheck[entryToCheck]
	else:
		return 0


##
## Main method block
##
if __name__=="__main__":

	praat = "/usr/bin/praat"
	script = "create_continuum.praat"
	#inputDir = "in_dir/"
	inputDir = "in_dir/test-items/"
	outputDir = "output_continuum"

	# all these in ms
	stepSize = int(5)
	minVOT = int(10)
	maxVOT = int(100)

	indexToNormDict = {}
	indexToCounterDict = {}
	indexToIDDIct = {}
	attestedIndexes = {}

	for file in os.listdir(inputDir):
		if file.endswith(".wav"):
			fileAttributes = file.split("-")
			#print file
			if len(fileAttributes) > 3:
				index = fileAttributes[0]
				word = fileAttributes[1]
				contextSide = fileAttributes[2]
				normOrCounter = fileAttributes[3]
				print normOrCounter
				normOrCounter = normOrCounter.replace('.wav','')

				indexToIDDIct[index] = index + '-' + word + '-' + contextSide
				print file
				print index + '-' + word + '-' + contextSide + '-' + normOrCounter

				if index not in attestedIndexes:
					 attestedIndexes[index] = True

				if normOrCounter == 'norm' or normOrCounter == 't':
					indexToNormDict[index] = file
				elif normOrCounter == 'counter'or normOrCounter == 'd':
					indexToCounterDict[index] = file



	for currIndex in attestedIndexes:
		normFile = accessDictEntry(indexToNormDict, currIndex)
		counterFile = accessDictEntry(indexToCounterDict, currIndex)
		idName = accessDictEntry(indexToIDDIct, currIndex)
		if normFile == 0 or counterFile == 0 or idName == 0:
			break
		print 'Running: ' + normFile
		normFile = normFile[:-4]
		counterFile = counterFile[:-4]
		for vot in xrange(minVOT, maxVOT+1, stepSize):
			stepSizeSeconds = "%1.3f" % (vot/1000)
			output = outputDir+"/"+idName+"_modToken_VOT_%i.wav" % vot
			subprocess.call([praat, script, normFile, counterFile, inputDir, stepSizeSeconds, output])
	quit()

	#############
	fileList = ['1-tie-L','2-tie-L','10-tier-R','11-tier-R','13-tune-L','14-tune-L','19-tongue-L']
	# '2-tie-L',''
	stepSize = int(10)
	minVOT = int(10)
	maxVOT = int(85)

	for idName in fileList:
		print 'Running: ' + idName
		tentFile = idName + '-norm-token'
		dentFile = idName + '-counter-token'
		print stepSize
		print minVOT
		print maxVOT
		for vot in xrange(minVOT, maxVOT+1, stepSize):
			stepSizeSeconds = "%1.3f" % (vot/1000)
			output = outputDir+"/"+idName+"_modToken_VOT_%i.wav" % vot
			subprocess.call([praat, script, tentFile, dentFile, inputDir, stepSizeSeconds, output])
