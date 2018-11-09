library(maptools)
library(mapproj)
library(rgeos)
library(rgdal)
library(RColorBrewer)
library(ggplot2)
library(raster)
library(sp)
library(plyr)
library(graticule)
library(spatialEco)

# load map and points

europe = readOGR(dsn=path.expand("~/git/IMAGE/data/shapefiles/Europe/"),layer='Europe')
original.proj <- proj4string(europe)

# load csv with  grid values
grid <- read.csv('~/git/IMAGE/output/CLaGARMi/euro_cordex/lonlat/euro_lonlat.csv')
names(grid)[1] = 'ID'

# establish overlap of each country


# add extra column with counrty ID
ggplot(data=grid,aes(x=lon,y=lat)) +
    # geom_point() +
    geom_text(aes(label=ID),size=0.5)