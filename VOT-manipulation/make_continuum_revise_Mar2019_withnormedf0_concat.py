from __future__ import division
import sys
import subprocess
import glob, os

## Author: Spencer Caplan, University of Pennsylvania
## Contact: spcaplan@sas.upenn.edu


outputFileNamesWithWordID = False
printDebugStatements = True

testFilesRun = True
trainFilesRun = True

def accessDictEntry(dictToCheck, entryToCheck):
	if entryToCheck in dictToCheck:
		return dictToCheck[entryToCheck]
	else:
		return 0


##
## Main method block
##
if __name__=="__main__":
	if (len(sys.argv) < 6):
		print('incorrect number of arguments')
		exit(0)

	# currently at: /home1/s/spcaplan/Documents/PRAAT/praat
	praat = sys.argv[1]
	scriptSourceDir = sys.argv[2]
	inputDirTrain = sys.argv[3]
	inputDirTest = sys.argv[4]
	outputDirTrain = sys.argv[5]
	outputDirTest = sys.argv[6]

	#praat = "/home1/s/spcaplan/Documents/PRAAT/praat"
	#praat = "/usr/bin/praat"
	script = scriptSourceDir+"create_continuum_concat.praat"

	# all these in ms
	stepSize = int(5)
	minVOT = int(10)
	maxVOT = int(100)
	vocoidOffset= int(50)
	vocoidOffsetSeconds = "%1.3f" % (vocoidOffset/1000)

	indexToNormDict = {}
	indexToCounterDict = {}
	indexToIDDIct = {}
	attestedIndexes = {}

	vowelSet = ['A','E']
	
	if testFilesRun:
		for vowel in vowelSet:
			for Tindex in range(1, 6):
				Tuid = 'T-' + vowel + '-' + str(Tindex)
				currTfile = inputDirTest + Tuid + '.wav'
				print currTfile
				if os.path.isfile(currTfile):
					for Dindex in range(1, 6):
						Duid = 'D-' + vowel + '-' + str(Dindex) + '-f0norm'
						currDfile = inputDirTest + Duid + '.wav'
						print currDfile
						if os.path.isfile(currDfile):
							for vot in xrange(minVOT, maxVOT+1, stepSize):
								stepSizeSeconds = "%1.3f" % (vot/1000)
								vocoidOffsetSeconds = "%1.3f" % (vocoidOffset/1000)
								if vocoidOffsetSeconds > stepSizeSeconds:
									vocoidOffsetSeconds = stepSizeSeconds
								output = outputDirTest+vowel+str(Tindex)+'_'+str(Dindex)+"_f0norm_VOT_%i.wav" % vot
								subprocess.call([praat, script, Tuid, Duid, inputDirTest, stepSizeSeconds, vocoidOffsetSeconds, output])
								print 'Processed: ' + output
				else:
					print 'Cannot find Tfile: '+currTfile
		print 'Ran multi test files.'
	
	if trainFilesRun:
		for file in os.listdir(inputDirTrain):
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
				vocoidOffsetSeconds = "%1.3f" % (vocoidOffset/1000)
				if vocoidOffsetSeconds > stepSizeSeconds:
					vocoidOffsetSeconds = stepSizeSeconds
				output = outputDirTrain+idName+"_f0norm_VOT_%i.wav" % vot
				subprocess.call([praat, script, normFile, counterFile, inputDirTrain, stepSizeSeconds, vocoidOffsetSeconds, output])
		print 'Ran train files.'

	print 'Completed VOT manipulation.'
	quit()
