rm(list=ls())

library(ggplot2)
library(plyr)

# break down the arguments from Rscript
args <- commandArgs(trailingOnly=TRUE)
slice <- as.character(args[1])
years_sim1 <- as.numeric(args[2])
years_sim2 <- as.numeric(args[3])
metric <- as.character(args[4])
continent <- as.character(args[5])
scen <- as.character(args[6])
start <- as.numeric(args[7])
end <- as.numeric(args[8])

# slice = '01' ; years_sim1 = 4000 ; years_sim2 = 6000 ; metric = 'tasmax' ; continent = 'euro' ; scen = 'hist' ; start = 1971 ;end = 2000

print(args)

years_sim_tot = years_sim1 + years_sim2

# short names for months
month.short <- c('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')

input.dir = '~/git/IMAGE/output/CLaGARMi/euro_cordex/figures_processing/'
output.dir = '~/git/IMAGE/output/CLaGARMi/euro_cordex/figures/'

# HEATWAVES

# load data for both comparing entire sim and obs
dat.obs= read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_obs_intensity_return_periods_europe.csv'))
# dat.obs.mean = ddply(dat.obs,.(return_period),summarise,days_over=mean(days_over))
# dat.sim= read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim1,'yrs_sim_intensity_return_periods_europe.csv'))
dat.sim= read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_1000yrs_sim_intensity_return_periods_europe.csv'))
# dat.sim.mean = ddply(dat.sim,.(return_period),summarise,days_over=mean(days_over))
# average observations over entire

#################################
# FIGURE 8
#################################

# plot entire europe with each line a square in CORDEX
pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_obs_intensity_return_periods.pdf'),paper='a4r',height=0,width=0)
ggplot() +
    geom_line(data=dat.obs,aes(x=return_period,y=days_over))+
    guides(color=FALSE,size=FALSE) +
    xlab('Return period (years)') + ylab('Heat wave duration (days)') +
    ggtitle('Whole domain') +
    scale_x_log10() +
    theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
    plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
    panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
    panel.border = element_rect(colour = "black"),strip.background = element_blank(),
    legend.position = 'bottom',legend.justification='center',
    legend.background = element_rect(fill="gray90", size=.5, linetype="dotted"))
dev.off()

pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim_tot,'yrs_obs_sim_intensity_return_periods_europe.pdf'),paper='a4r',height=0,width=0)
ggplot() +
    geom_line(data=dat.sim,aes(x=return_period,y=days_over),linetype='longdash')+
    geom_line(data=dat.obs,aes(x=return_period,y=days_over))+
    guides(color=FALSE,size=FALSE) +
    xlab('Return period (years)') + ylab('Heat wave duration (days)') +
    ggtitle('Whole domain') +
    scale_x_log10() +
    theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
    plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
    panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
    panel.border = element_rect(colour = "black"),strip.background = element_blank(),
    legend.position = 'bottom',legend.justification='center',
    legend.background = element_rect(fill="gray90", size=.5, linetype="dotted"))
dev.off()

# DROUGHT

# load data for both comparing entire sim and obs
dat.obs= read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_obs_drought_intensity_return_periods_europe.csv'))
# dat.obs.mean = ddply(dat.obs,.(return_period),summarise,days_over=mean(days_over))
# dat.sim= read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim1,'yrs_sim_intensity_return_periods_europe.csv'))
dat.sim= read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_1000yrs_sim_drought_intensity_return_periods_europe.csv'))
# dat.sim.mean = ddply(dat.sim,.(return_period),summarise,days_over=mean(days_over))
# average observations over entire

#################################
# FIGURE 8
#################################

# plot entire europe with each line a square in CORDEX
pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_obs_intensity_return_periods.pdf'),paper='a4r',height=0,width=0)
ggplot() +
    geom_line(data=dat.obs,aes(x=return_period,y=days_over))+
    guides(color=FALSE,size=FALSE) +
    xlab('Return period (years)') + ylab('Heavy preciptation duration (days)') +
    ggtitle('Whole domain') +
    scale_x_log10() +
    theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
    plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
    panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
    panel.border = element_rect(colour = "black"),strip.background = element_blank(),
    legend.position = 'bottom',legend.justification='center',
    legend.background = element_rect(fill="gray90", size=.5, linetype="dotted"))
dev.off()

pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim_tot,'yrs_obs_sim_intensity_return_periods_europe.pdf'),paper='a4r',height=0,width=0)
ggplot() +
    geom_line(data=dat.sim,aes(x=return_period,y=days_over),linetype='longdash')+
    geom_line(data=dat.obs,aes(x=return_period,y=days_over))+
    guides(color=FALSE,size=FALSE) +
    xlab('Return period (years)') + ylab('Low precepitation duration (days)') +
    ggtitle('Whole domain') +
    # scale_x_log10() +
    theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
    plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
    panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
    panel.border = element_rect(colour = "black"),strip.background = element_blank(),
    legend.position = 'bottom',legend.justification='center',
    legend.background = element_rect(fill="gray90", size=.5, linetype="dotted"))
dev.off()
