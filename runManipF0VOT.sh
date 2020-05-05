#!/bin/bash  

# Author: Spencer Caplan
# Department of Linguistics, University of Pennsylvania
# Contact: spcaplan@sas.upenn.edu

#### Directories would need to be updated to reflect your local machine in order to run

f0ScriptDir='/home1/s/spcaplan/Dropbox/penn_CS_account/MinPairs/f0-manipulation/'
f0ScriptName='make_f0_ambiguous.py'

VOTScriptDir='/home1/s/spcaplan/Dropbox/penn_CS_account/MinPairs/VOT-manipulation/'
#VOTScriptName='make_continuum_revise_Mar2019_withnormedf0.py'
VOTScriptName='make_continuum_revise_Mar2019_withnormedf0_concat.py'

f0inputDirTrain='/home1/s/spcaplan/Dropbox/penn_CS_account/MinPairs/f0-manipulation/SI2/'
f0inputDirTest='/home1/s/spcaplan/Dropbox/penn_CS_account/MinPairs/f0-manipulation/SI2-TestItems/'
f0outputDirTrain='/mnt/nlpgridio2/nlp/users/spcaplan/VOT-editing/NormalizedF0-March2019/TargetItems/'
f0outputDirTest='/mnt/nlpgridio2/nlp/users/spcaplan/VOT-editing/NormalizedF0-March2019/TestItems/'

VOTinputDirTrain=$f0outputDirTrain
VOTinputDirTest=$f0outputDirTest
#VOToutputDirTrain='/mnt/nlpgridio2/nlp/users/spcaplan/VOT-editing/NormalizedF0-March2019/Both-VOT-and-F0/TargetItems/'
#VOToutputDirTest='/mnt/nlpgridio2/nlp/users/spcaplan/VOT-editing/NormalizedF0-March2019/Both-VOT-and-F0/TestItems/'
VOToutputDirTrain='/mnt/nlpgridio2/nlp/users/spcaplan/VOT-editing/NormalizedF0-March2019/Both-VOT-and-F0-concat/TargetItems/'
VOToutputDirTest='/mnt/nlpgridio2/nlp/users/spcaplan/VOT-editing/NormalizedF0-March2019/Both-VOT-and-F0-concat/TestItems/'

scriptSource='/home1/s/spcaplan/Dropbox/penn_CS_account/MinPairs'
praatSource='/home1/s/spcaplan/Documents/PRAAT/praat'

cd $scriptSource
echo 'Executing from: '$scriptSource

echo 'Starting f0'
python $f0ScriptDir$f0ScriptName $praatSource $f0ScriptDir $f0inputDirTrain $f0inputDirTest $f0outputDirTrain $f0outputDirTest

echo 'Starting VOT'
python $VOTScriptDir$VOTScriptName $praatSource $VOTScriptDir $VOTinputDirTrain $VOTinputDirTest $VOToutputDirTrain $VOToutputDirTest

echo 'Completed'