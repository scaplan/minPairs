form Create VOT continuum
     sentence tentFilename input
     sentence dentFilename input
     sentence splitDir input # directory of split stimuli
     positive stepSize
     sentence outputFilename input
endform

# read files
do("Read from file...", splitDir$+tentFilename$+".wav")
selectObject("Sound "+tentFilename$)
do("Rename...", "tent")

do("Read from file...", splitDir$+dentFilename$+".wav")
selectObject("Sound "+dentFilename$)
do("Rename...", "dent")

selectObject("Sound tent")
end = do("Get nearest zero crossing...", 1, stepSize)
do("Extract part...", 0, end, "Rectangular", 1.0, "no")
selectObject("Sound tent_part")
do("Rename...", "output1")

selectObject("Sound dent")
start = do("Get nearest zero crossing...", 1, stepSize)
end = do("Get end time")
do("Extract part...", start, end, "Rectangular", 1.0, "no")
selectObject("Sound dent_part")
do("Rename...", "output2")

selectObject("Sound output1", "Sound output2")
do("Concatenate")

selectObject("Sound chain")
do("Save as WAV file...", outputFilename$)
