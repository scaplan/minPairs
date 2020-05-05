# This script will globally change the pitch and duration of all the AIFF files (with no extension) in the given directory

# If the quality is bad try changing the minimum pitch  or maximum pitch

form Global change to Fo and duration
   comment Changes will be made to ALL the files in the directory
   comment Files must be AIFF with no extension
   sentence Directory  cjdisk:test:
   sentence Output_Directory  cjdisk:testout:
   sentence Fo_expression self*1.0
   positive Duration_factor 1.0
   comment Analysis parameters for Fo
   positive minimum_Fo 75
   positive maximum_Fo 300
   boolean Play_after_synthesis 1
endform

fomin = 'minimum_Fo'
fomax = 'maximum_Fo'

Create Strings as file list... list 'directory$'*
numberOfFiles = Get number of strings
for ifile to numberOfFiles
   select Strings list
   sound$ = Get string... ifile
   call fodurnchange
endfor
select Strings list
Remove

#Read from file...         cjdisk:test:wewere
procedure fodurnchange
#
Read from file... 'directory$''sound$'
#initial analysis locating pitch pulses etc
select Sound 'sound$'
durn = Get duration

#create Pitch and Manipulation objects
select Sound 'sound$'
To Pitch... 0.01 fomin fomax
plus Sound 'sound$'
To Manipulation... fomin
select Pitch 'sound$'
#apply the appropriate transformation to the Pitch object
Formula... 'fo_expression$'

#turn it into a PitchTier and place it into the Manipulation object
select Pitch 'sound$'
Down to PitchTier
select Manipulation 'sound$'
plus PitchTier 'sound$'
Replace pitch tier

if duration_factor <> 1.0
	Create DurationTier... newdurn 0 'durn'
	Add point... 0 'duration_factor'
	select Manipulation 'sound$'
	plus DurationTier newdurn
	Replace duration tier
endif

#resynthesise with new pitch and duration contour
select Manipulation 'sound$'
Get resynthesis (PSOLA)
if play_after_synthesis = 1
   Play
endif

Write to AIFC file... 'output_Directory$''sound$'.f'fo_expression$'.d'duration_factor'
select all
minus Strings list
Remove
endproc


