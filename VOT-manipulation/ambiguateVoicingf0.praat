form Ambiguate voicing cues f0
     sentence filename input
     sentence splitDir input # directory of split stimuli
     positive endEditTime
     positive hertzBoost
     positive direction
     sentence outputFilename input
endform


startTime = Get start time
endTime = Get end time
numberOfTimeSteps = (endTime - startTime) / 0.05
writeInfoLine: " tmin tmax mean fmin fmax stdev"
for step to numberOfTimeSteps
    tmin = startTime + (step - 1) * 0.05
    tmax = tmin + 0.05
    mean = Get mean: tmin, tmax, "Hertz"
    minimum = Get minimum: tmin, tmax, "Hertz", "Parabolic"
    maximum = Get maximum: tmin, tmax, "Hertz", "Parabolic"
    stdev = Get standard deviation: tmin, tmax, "Hertz"
    appendInfoLine: fixed$ (tmin, 6), " ", fixed$ (tmax, 6), " ", fixed$ (mean, 2),
    ... " ", fixed$ (minimum, 2), " ", fixed$ (maximum, 2), " ", fixed$ (stdev, 2)
endfor