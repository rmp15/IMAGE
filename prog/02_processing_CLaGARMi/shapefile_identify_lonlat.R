rm(list=ls())

library(plyr)
library(reticulate)
library(ggplot2)
library(maptools)
library(mapproj)
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

# load lonlat file for IMAGE
