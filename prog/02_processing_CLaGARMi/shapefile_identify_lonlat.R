rm(list=ls())

# arguments to finish
contintent = 'euro'

library(plyr)
library(reticulate)
library(ggplot2)
library(maptools)
library(mapproj)
library(graticule)
library(rgeos)
library(rgdal)
library(RColorBrewer)
library(ggplot2)
library(plyr)
library(scales)

###############################################################
# PREPARING MAP
###############################################################

# for theme_map
#devtools::source_gist("33baa3a79c5cfef0f6df")
theme_map <- function(base_size=9, base_family=""){
    require(grid)
    theme_bw(base_size=base_size,base_family=base_family) %+replace%
    theme(axis.line=element_blank(),
    axis.text=element_blank(),
    axis.ticks=element_blank(),
    axis.title=element_blank(),
    panel.background=element_blank(),
    panel.border=element_blank(),
    panel.grid=element_blank(),
    panel.margin=unit(0,"lines"),
    plot.background=element_blank(),
    legend.justification = c(0,0),
    legend.position = c(0,0)
    )
}


# load shapefile
map <- readOGR(dsn="../../data/shapefiles/ne_10m_admin_0_countries",layer="ne_10m_admin_0_countries")
original.proj <- proj4string(map)
euro <- map[map$CONTINENT %in% c("Europe"),]

# function to isolate single country polygon to finish
france = euro[euro$GEOUNIT %in% c("France"),]
spain = euro[euro$GEOUNIT %in% c("Spain"),]

# fortify to prepare for ggplot
euro.fortify <- fortify(euro)
spain.fortify = fortify(spain)
world.fortify = fortify(map)

# load lonlat file for IMAGE
grid = read.csv('~/git/IMAGE/output/CLaGARMi/euro_cordex/lonlat/euro_lonlat.csv')
names(grid)[1] = 'ID'

# plot for refrence of grid IDs
# ggplot() + geom_text(data=grid,aes(x=lon,y=lat,label=ID),size=3)

# fix where western Mallorca should be in the map to fix the grid points
# western Mallorca is  ID = 104, lon = -12.15, lat = -9.79
# real value is lon = 3, lat = 39.6
grid$lon = grid$lon + 15.15
grid$lat = grid$lat + (39.6+9.79)

# create a graticule from grid points for Europe
grat <- graticule(lons=grid$lon,lats=grid$lat,xlim=c(min(grid$lon),max(grid$lon)),ylim=c(min(grid$lat),max(grid$lat)),proj=original.proj)
grat.fortify = fortify(grat)


# plot fortified europe map
ggplot() +
    # geom_text(data=grid,aes(x=lon,y=lat,label=ID),size=3) +
    geom_point(data=grid,aes(x=lon,y=lat),size=1) +
    # geom_polygon(data=subset(euro.fortify),aes(x=long,y=lat,group=group),linetype=2,size=0) +
    theme_map()
    # geom_polygon(data=subset(spain.fortify),aes(x=long,y=lat,group=group),linetype=2,size=0)

