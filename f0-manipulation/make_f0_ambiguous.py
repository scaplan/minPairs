from __future__ import division
import sys
import subprocess
import glob, os

## Author: Spencer Caplan, University of Pennsylvania
## Contact: spcaplan@sas.upenn.edu

testFilesRun = True
trainFilesRun = True

f0Points =	{
  "dye": 212.3754281,
  "deer": 229.3977268,
  "dip": 237.0918733,
  "dune": 217.1612444,
  "doom": 223.6404873,
  "dab": 193.3206255,
  "dime": 206.2018954,
  "dole": 217.0756111,
  "dung": 203.5563402,
  "door": 241.0337896, 
  "dough": 196.9191154,
  "down": 202.4441466,
  "dub": 193.0592886,
  "dummy": 220.1143828,
  "dally": 212.8853595,
  "dusk": 236.1520498,
  "do": 238.6023055,
  "deck": 215.746278,
  "deem": 220.7977129,
  "dense": 209.477845,
  "dare": 220.53128,
  "dangle": 210.9669027,
  "D-A-1": 203.02216,
  "D-A-2": 221.7977523,
  "D-A-3": 197.1101185,
  "D-E-1": 220.6334759,
  "D-E-2": 213.158324,
  "D-E-3": 227.0219074,
  "D-A-4": 213.790623,
  "D-A-5": 213.790623,
  "D-E-4": 213.790623,
  "D-E-5": 213.790623
}

##
## Main method block
##
if __name__=="__main__":
	if (len(sys.argv) < 7):
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
	script = scriptSourceDir+"caplan-f0.script"
	#inputDirTrain = "/home1/s/spcaplan/Dropbox/penn_CS_account/MinPairs/f0-manipulation/SI2/"
	#inputDirTest = "/home1/s/spcaplan/Dropbox/penn_CS_account/MinPairs/f0-manipulation/SI2-TestItems/"
	#outputDirTrain = "/home1/s/spcaplan/Dropbox/penn_CS_account/MinPairs/f0-manipulation/Caplan-f0-out/"
	#outputDirTest = "/home1/s/spcaplan/Dropbox/penn_CS_account/MinPairs/f0-manipulation/Caplan-f0-out-test/"

	vowelSet = ['A','E']
	
	if testFilesRun:
		for vowel in vowelSet:
			# change this indexing depending on which test
			# files are being manipulated
			for Dindex in range(1, 6):
				inputFileToPraat = 'D-' + vowel + '-' + str(Dindex)
				currDfile = inputDirTest + inputFileToPraat + '.wav'
				if os.path.isfile(currDfile):
					onsetf0 = str(f0Points.get(inputFileToPraat))
					output = outputDirTest+inputFileToPraat+"-f0norm"
					print 'Going to call PRAAT...'+inputFileToPraat+' with f0 of: '+onsetf0
					subprocess.call([praat, script, inputFileToPraat, inputDirTest, onsetf0, output])
		print 'Ran multi test files.'
	
	if trainFilesRun:
		for file in os.listdir(inputDirTrain):
			if file.endswith(".wav"):
				fileAttributes = file.split("-")
				if len(fileAttributes) > 4:
					phone = fileAttributes[2]
					word = fileAttributes[4]
					word = word.replace('.wav','')
					inputFileToPraat = file[:-4]

					if phone == 'D':
						onsetf0 = str(f0Points.get(word))
						output = outputDirTrain+inputFileToPraat+"-f0norm"
						print 'Going to call PRAAT...'+word+' with f0 of: '+onsetf0
						subprocess.call([praat, script, inputFileToPraat, inputDirTrain, onsetf0, output])

		print 'Ran train files.'
	quit()