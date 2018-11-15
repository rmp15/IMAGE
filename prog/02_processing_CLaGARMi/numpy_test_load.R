# some arguments here to automate loading process of which files etc

# to enable reading of numpy files in R
library(reticulate)
np <- import("numpy")

file.loc = # SOME FILE LOCATION DEFINED BY ARGUMENTS
mat <- np$load(file.loc)

# how to concatenate 4000,6000 year files