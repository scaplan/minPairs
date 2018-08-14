from __future__ import division
import sys
import subprocess
import glob, os
import shutil

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

	inputDir = "/mnt/nlpgridio2/nlp/users/spcaplan/VOT-editing/TrimmedWords/Fillers/"
	outputDir = "/mnt/nlpgridio2/nlp/users/spcaplan/VOT-editing/OutputTargets-Edited/RenamedFillers/"

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

				oldFile = os.path.join(inputDir, file)

				newFileID = localIndex + '-' + trialType + '.wav'
				newOutFile = os.path.join(outputDir, newFileID)

				print oldFile
				print newOutFile
				print '\n'
				shutil.copy(oldFile, newOutFile)

	print 'Completed.'
	quit()
