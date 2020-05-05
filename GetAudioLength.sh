#!/bin/bash  

# Author: Spencer Caplan
# Department of Linguistics, University of Pennsylvania
# Contact: spcaplan@sas.upenn.edu

cd '/home1/s/spcaplan/Desktop/TempLengthMeasure'

outputFile='/home1/s/spcaplan/Desktop/lengths.txt'
rm -f $outputFile

# shopt -s nullglob
FILES=/home1/s/spcaplan/Desktop/TempLengthMeasure/*.wav

for f in $FILES
do
	printf $f'\n'
	sox $f -n stat 2>&1 | sed -n 's#^Length (seconds):[^0-9]*\([0-9.]*\)$#\1#p' >> $outputFile
done
printf 'Run lengths\n\n'