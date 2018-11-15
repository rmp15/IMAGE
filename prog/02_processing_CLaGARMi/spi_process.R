rm(list=ls())

library(SPEI)

# break down the arguments from Rscript
args <- commandArgs(trailingOnly=TRUE)
slice = as.character(args[1])                   # slice = '01'
years_sim_1 = as.numeric(args[2])               # years_sim_1 = 4000 ; years_sim_2 = 6000
metric = as.character(args[3])                  # metric = 'pr'
continent = as.character(args[4])               # continent = 'euro'
scen = as.character(args[5])                    # scen = 'hist'
year_start = as.numeric(args[6])                # year_start = 1971
year_end = as.numeric(args[7])                  # year_end = 2000

# slice = '01' ; years_sim_1 = 4000 ; years_sim_2 = 6000 ; metric = 'pr' ; continent = 'euro' ;
# scen = 'hist'; year_start = 1971 ; year_end = 2000

# local file outputs from IMAGE (change for on wrfstore because of python's weird system)
image_output_local = '/Users/rmiparks/data/IMAGE/CLaGARMi/euro_cordex_output/'
file.loc.pr.hist = paste0(image_output_local,metric,'/out_',slice,'_y',years_sim_1,'_',continent,'_',scen,'_',year_start,'_',year_end,'_',metric,'_o.npy' )
file.loc.pr.sim = paste0(image_output_local,metric,'/out_',slice,'_y',years_sim_1,'_',continent,'_',scen,'_',year_start,'_',year_end,'_',metric,'_s.npy' )

# to enable reading of numpy files in R
library(reticulate)
np = import("numpy")

# load historical file and sim files
pr.hist = np$load(file.loc.pr.hist)
pr.sim = np$load(file.loc.pr.sim)

# load historical file and sim files
tasmax.hist = np$load(file.loc.tasmax.hist)
tasmax.sim = np$load(file.loc.tasmax.sim)

# concatenate 4000,6000 year files
# FIGURE OUT LATER

# # calculate monthly means through time
# month_days = c(31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
# month_end_inds = cumsum(month_days)

# REAL DATA

# test take one site and calculate SPI as test
site = pr.hist[1,,]
site.vector.obs = as.vector(t(site))

# create dataframe with year, month, precipitation
year.seq = rep(1:30, each=365)
month.seq = c(rep(1,31),rep(2,28),rep(3,31),rep(4,30),rep(5,31),rep(6,30),rep(7,31),rep(8,31),rep(9,30),rep(10,31),rep(11,30),rep(12,31))
dat.site = data.frame(year=year.seq,month=month.seq,precip=site.vector.obs)

# summarise precipitation by month
dat.site.summarised = ddply(dat.site,.(year,month),summarise,precip=sum(precip))

# convert to mm m-2 s-1 (currently in kg m-2 s-1) https://www.convertunits.com/from/kg/cm2/to/water+column+[millimeter]
# scale factor is 10,000
dat.site.summarised$precip = 10000 * dat.site.summarised$precip

library(ggplot2)
# ggplot(data=dat.site.summarised) + geom_line(aes(x=year,y=precip,group=month,color=month)) + facet_wrap(~month)

# use SPEI program to calculate SPI
spi_1 <- spi(dat.site.summarised[,'precip'], 1)
spi_3 <- spi(dat.site.summarised[,'precip'], 3)
spi_12 <- spi(dat.site.summarised[,'precip'], 12)

# SIM DATA
# NEED TO FIX A REFERENCE PERIOD using ref.start and ref.end in the arguments of

site = pr.sim[1,,]
site.vector.sim = as.vector(t(site))

num.years = dim(site)[1]

# create dataframe with year, month, precipitation
year.seq = rep(1:num.years, each=365)
month.seq = c(rep(1,31),rep(2,28),rep(3,31),rep(4,30),rep(5,31),rep(6,30),rep(7,31),rep(8,31),rep(9,30),rep(10,31),rep(11,30),rep(12,31))
dat.site = data.frame(year=year.seq,month=month.seq,precip=site.vector.sim)

# summarise precipitation by month
dat.site.summarised = ddply(dat.site,.(year,month),summarise,precip=sum(precip))

# convert to mm m-2 s-1 (currently in kg m-2 s-1) https://www.convertunits.com/from/kg/cm2/to/water+column+[millimeter]
# scale factor is 10,000
dat.site.summarised$precip = 10000 * dat.site.summarised$precip

library(ggplot2)
# ggplot(data=dat.site.summarised) + geom_line(aes(x=year,y=precip,group=month,color=month)) + facet_wrap(~month)

# use SPEI program to calculate SPI
spi_1 <- spi(dat.site.summarised[,'precip'], 1)
spi_3 <- spi(dat.site.summarised[,'precip'], 3)
spi_12 <- spi(dat.site.summarised[,'precip'], 12)

# SIM DATA WITH FIXED REFERENCE PERIOD

# create dataframe with year, month, precipitation
year.seq.long = rep(31:(num.years+30), each=365)
month.seq = c(rep(1,31),rep(2,28),rep(3,31),rep(4,30),rep(5,31),rep(6,30),rep(7,31),rep(8,31),rep(9,30),rep(10,31),rep(11,30),rep(12,31))

year.seq.long = c(year.seq, year.seq.long)
site.vector.long = c(site.vector.obs, site.vector.sim)

dat.site = data.frame(year=year.seq.long,month=month.seq,precip=site.vector.long)

# summarise precipitation by month
dat.site.summarised = ddply(dat.site,.(year,month),summarise,precip=sum(precip))

# convert to mm m-2 s-1 (currently in kg m-2 s-1) https://www.convertunits.com/from/kg/cm2/to/water+column+[millimeter]
# scale factor is 10,000
dat.site.summarised$precip = 10000 * dat.site.summarised$precip

library(ggplot2)
# ggplot(data=dat.site.summarised) + geom_line(aes(x=year,y=precip,group=month,color=month)) + facet_wrap(~month)

# use SPEI program to calculate SPI
spi_1 <- plot(spi(dat.site.summarised[,'precip'], 1, ref.start=c(1,1), ref.end=c(30,12)))
spi_3 <- spi(dat.site.summarised[,'precip'], 3, ref.start=c(1,1), ref.end=c(30,12))
spi_12 <- spi(dat.site.summarised[,'precip'], 12)