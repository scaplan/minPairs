## Import (packages)
library(ggplot2)
library(Hmisc)
library(lme4)
library(dplyr)
library(tidyr)


sourceDir = 'C:\\Users\\Spencer\\Desktop\\VOT'
totalInputFile = 'celex_tdPairs.csv'
setwd(sourceDir)
minPairData=read.table(totalInputFile,header=FALSE,sep=",", quote = "", skipNul = TRUE,fill = TRUE, comment.char = "", check.names = FALSE)


names(minPairData)[names(minPairData) == 'V1'] <- 'WordOne'
names(minPairData)[names(minPairData) == 'V2'] <- 'PronOne'
names(minPairData)[names(minPairData) == 'V3'] <- 'RawFreqOne'
names(minPairData)[names(minPairData) == 'V4'] <- 'WordTwo'
names(minPairData)[names(minPairData) == 'V5'] <- 'PronTwo'
names(minPairData)[names(minPairData) == 'V6'] <- 'RawFreqTwo'

minPairData <- mutate(minPairData, RawFreqOne=RawFreqOne+1)
minPairData <- mutate(minPairData, RawFreqTwo=RawFreqTwo+1)

minPairData <- mutate(minPairData, MinFreq=pmin(RawFreqOne,RawFreqTwo))
minPairData <- mutate(minPairData, LogFreqOne=log2(RawFreqOne))
minPairData <- mutate(minPairData, LogFreqTwo=log2(RawFreqTwo))
minPairData <- mutate(minPairData, LogFreqDiff=abs(LogFreqOne-LogFreqTwo))

write.csv(minPairData, file = "celex_tdPairs_withLogFreq.csv", quote=FALSE)
