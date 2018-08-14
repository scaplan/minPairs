from __future__ import division
import sys
import subprocess
import glob, os

## Author: Spencer Caplan, University of Pennsylvania
## Contact: spcaplan@sas.upenn.edu


outputFileNamesWithWordID = False
printDebugStatements = True

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
	#inputDir = "/mnt/nlpgridio2/nlp/users/spcaplan/VOT-editing/TrimmedWords/Targets/"
	inputDir = "/mnt/nlpgridio2/nlp/users/spcaplan/VOT-editing/TrimmedWords/TestItems/"
	#inputDir = "/mnt/nlpgridio2/nlp/users/spcaplan/VOT-editing/NormalizedVolumeTrimmedWords/Targets/"
	#inputDir = "in_dir/test-items/"
	#outputDir = "output_continuum"
	#outputDir = "/mnt/nlpgridio2/nlp/users/spcaplan/VOT-editing/OutputTargets-Edited/OriginalVolume"
	#outputDir = "/mnt/nlpgridio2/nlp/users/spcaplan/VOT-editing/OutputTargets-Edited/NormalizedVolume"
	outputDir = "/mnt/nlpgridio2/nlp/users/spcaplan/VOT-editing/OutputTargets-Edited/NewTestItems"

	# all these in ms
	stepSize = int(5)
	minVOT = int(10)
	maxVOT = int(100)

	indexToNormDict = {}
	indexToCounterDict = {}
	indexToIDDIct = {}
	attestedIndexes = {}

	vowelSet = ['A','E']

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
		counterFile = accessDictEntry(indexToCounterDict, currIndex)
		idName = accessDictEntry(indexToIDDIct, currIndex)
	#	if printDebugStatements:
	#		print 'Trying Norm: ' + normFile
	#		print 'Trying Counter: ' + counterFile
	#		print 'Trying id: ' + idName
		if normFile == 0 or counterFile == 0 or idName == 0:
			break
		if printDebugStatements:
			print 'Running: ' + normFile
		normFile = normFile[:-4]
		counterFile = counterFile[:-4]
		for vot in xrange(minVOT, maxVOT+1, stepSize):
			stepSizeSeconds = "%1.3f" % (vot/1000)
			output = outputDir+"/"+idName+"_VOT_%i.wav" % vot
			subprocess.call([praat, script, normFile, counterFile, inputDir, stepSizeSeconds, output])

	print 'Completed.'
	quit()

	#############
	# Crusty old code below (kept for reference purposes)
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



