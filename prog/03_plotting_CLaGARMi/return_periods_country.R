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
country <- as.character(args[9])

# slice = '01' ; years_sim1 = 4000 ; years_sim2 = 6000 ; metric = 'appt' ; continent = 'euro' ; scen = 'hist' ; start = 1971 ;end = 2000

print(args)

years_sim_tot = years_sim1 + years_sim2

# short names for months
# month.short <- c('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')

input.dir = '~/git/IMAGE/output/CLaGARMi/euro_cordex/figures_processing/'
output.dir = '~/git/IMAGE/output/CLaGARMi/euro_cordex/figures/'

# list of countries used
countries = c('Europe', 'Sweden', 'UK', 'Spain', 'Italy', 'Romania')

# HEATWAVES DURATION

###################################
# LOAD DATA
# #################################

# # load data for both comparing entire sim and obs
# dat.obs= read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_obs_intensity_return_periods_europe.csv'))
# dat.sim= read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_4000yrs_sim_intensity_return_periods_europe.csv'))
# dat.sim.sub = read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_30yrs_subsets_4000yrs_sim_intensity_return_periods_europe.csv'))

# entire duration of heat waves
dat.sim.country.all = data.frame()
for (i in countries){

    dat.sim.country.current                     = read.csv(paste0(input.dir,metric,'_',continent,'_',hist,'_1971_2000_10000yrs_sim_intensity_return_periods_',i,'.csv'))
    dat.sim.country.current$scen                = 'historical'
    dat.sim.country.rcp45.2021.current          = read.csv(paste0(input.dir,metric,'_',continent,'_rcp45_2021_2050_10000yrs_sim_intensity_return_periods_',i,'.csv'))
    dat.sim.country.rcp45.2021.current$scen     = 'RCP4.5 2021-2050'
    dat.sim.country.rcp45.2071.current          = read.csv(paste0(input.dir,metric,'_',continent,'_rcp45_2071_2100_10000yrs_sim_intensity_return_periods_',i,'.csv'))
    dat.sim.country.rcp45.2071.current$scen     = 'RCP4.5 2071-2100'
    dat.sim.country.rcp85.2021.current          = read.csv(paste0(input.dir,metric,'_',continent,'_rcp85_2021_2050_10000yrs_sim_intensity_return_periods_',i,'.csv'))
    dat.sim.country.rcp85.2021.current$scen     = 'RCP8.5 2021-2050'
    dat.sim.country.rcp85.2071.current          = read.csv(paste0(input.dir,metric,'_',continent,'_rcp85_2071_2100_10000yrs_sim_intensity_return_periods_',i,'.csv'))
    dat.sim.country.rcp85.2071.current$scen     = 'RCP8.5 2071-2100'

    dat.sim.country = rbind(dat.sim.country.current,dat.sim.country.rcp45.2021.current,dat.sim.country.rcp45.2071.current,
                                dat.sim.country.rcp85.2021.current,dat.sim.country.rcp85.2071.current)
    dat.sim.country$country = i
    dat.sim.country.all = rbind(dat.sim.country.all,dat.sim.country)

}

# 30 year subsets for each country for historical subsets
dat.sim.sub.country.all = data.frame()
dat.obs.country.all = data.frame()

for (i in countries){

    dat.obs.country.current = read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_obs_intensity_return_periods_',i,'.csv'))
    dat.obs.country.current$country = i
    dat.obs.country.all = rbind(dat.obs.country.all,dat.obs.country.current)
    do.call("<-", list(paste0('dat.obs.',i,'.current'), dat.obs.country.current))

    dat.sim.sub.country.current = read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_30yrs_subsets_10000yrs_sim_intensity_return_periods_',i,'.csv'))
    dat.sim.sub.country.current$country = i
    dat.sim.sub.country.all = rbind(dat.sim.sub.country.all,dat.sim.sub.country.current)
    do.call("<-", list(paste0('dat.sim.sub.',i,'.current'), dat.sim.sub.country.current))

    # dat.sim.sub.country.rcp45.2021 = read.csv(paste0(input.dir,metric,'_',continent,'_rcp45_2021_2050_30yrs_subsets_10000yrs_sim_intensity_return_periods_',country,'.csv'))
    # dat.sim.sub.country.rcp85.2021 = read.csv(paste0(input.dir,metric,'_',continent,'_rcp85_2021_2050_30yrs_subsets_10000yrs_sim_intensity_return_periods_',country,'.csv'))
    # dat.sim.sub.country.rcp45.2071 = read.csv(paste0(input.dir,metric,'_',continent,'_rcp45_2071_2100_30yrs_subsets_10000yrs_sim_intensity_return_periods_',country,'.csv'))
    # dat.sim.sub.country.rcp85.2071 = read.csv(paste0(input.dir,metric,'_',continent,'_rcp85_2071_2100_30yrs_subsets_10000yrs_sim_intensity_return_periods_',country,'.csv'))
}

###################################
# PLOT FIGURE
# #################################

# one line per scenario

pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim_tot,'yrs_obs_sim_intensity_return_periods_',country,'_scenarios.pdf'),paper='a4r',height=0,width=0)
ggplot() +
    geom_line(data=dat.sim.country.all,aes(x=return_period,y=days_over,group=scen,color=scen),alpha=0.3) +
    xlab('Return period (years)') + ylab('Heat wave duration (days)') +
    facet_wrap(~country) +
    scale_fill_manual(values=colors.subinjuries[c(1,2,3,4,5)]) +
    guides(fill=guide_legend(title="",nrow=1)) +
    theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
    plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
    panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
    panel.border = element_rect(colour = "black"),strip.background = element_blank(),
    legend.position = 'bottom',legend.justification='center',
    legend.background = element_rect(fill="gray90", size=.5, linetype="dotted"))
dev.off()

# historical 30-year chunks

pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim_tot,'yrs_obs_sim_intensity_return_periods_countries_boxplots_scenarios.pdf'),paper='a4r',height=0,width=0)
ggplot() +
    geom_line(data=dat.sim.sub.country.all,aes(x=return_period,y=days_over,group=subset),alpha=0.3,color='light blue')+
    geom_boxplot(data=subset(dat.sim.sub.country.all),aes(x=return_period, y=days_over,group=return_period),alpha=0.5, color='red') +
    geom_line(data=dat.obs.country.all,aes(x=return_period,y=days_over),size=1,linetype=1) +
3    guides(color=FALSE,size=FALSE) +
    xlab('Return period (years)') + ylab('Heat wave duration (days)') +
    scale_x_log10() +
    facet_wrap(~country) +
    theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
    plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
    panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
    panel.border = element_rect(colour = "black"),strip.background = element_blank(),
    legend.position = 'bottom',legend.justification='center',
    legend.background = element_rect(fill="gray90", size=.5, linetype="dotted"))
dev.off()






















# LEGACY BELOW

# # plot entire europe with each line a square in CORDEX
# pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_obs_intensity_return_periods.pdf'),paper='a4r',height=0,width=0)
# ggplot() +
#     geom_line(data=dat.obs,aes(x=return_period,y=days_over))+
#     guides(color=FALSE,size=FALSE) +
#     xlab('Return period (years)') + ylab('Heat wave duration (days)') +
#     ggtitle('Whole domain') +
#     scale_x_log10() +
#     theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
#     plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
#     panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
#     panel.border = element_rect(colour = "black"),strip.background = element_blank(),
#     legend.position = 'bottom',legend.justification='center',
#     legend.background = element_rect(fill="gray90", size=.5, linetype="dotted"))
# dev.off()
#
# # dat.sim.sub$density = get_density(dat.sim.sub$return_period,dat.sim.sub$days_over)
#
# pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim_tot,'yrs_obs_sim_intensity_return_periods_europe.pdf'),paper='a4r',height=0,width=0)
# ggplot() +
#     geom_line(data=dat.sim.sub,aes(x=return_period,y=days_over,group=subset,color=subset),alpha=0.3)+
#     # geom_hex(data=dat.sim.sub,aes(x=return_period,y=days_over,color=subset),alpha=0.3,bins=70)+
#     geom_jitter(data=dat.sim.sub,aes(x=return_period,y=days_over,color=subset),alpha=0.3)+
#     # geom_boxplot(data=subset(dat.sim.sub),aes(x=return_period,y=days_over),alpha=0.3)+
#     # geom_line(data=dat.sim,aes(x=return_period,y=days_over),linetype='longdash',size=1)+
#     geom_line(data=dat.obs,aes(x=return_period,y=days_over),size=1)+
#     guides(color=FALSE,size=FALSE) +
#     xlab('Return period (years)') + ylab('Heat wave duration (days)') +
#     ggtitle('Whole domain') +
#     scale_x_log10() +
#     theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
#     plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
#     panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
#     panel.border = element_rect(colour = "black"),strip.background = element_blank(),
#     legend.position = 'bottom',legend.justification='center',
#     legend.background = element_rect(fill="gray90", size=.5, linetype="dotted"))
# dev.off()
#
# pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim_tot,'yrs_obs_sim_intensity_return_periods_europe_boxplots.pdf'),paper='a4r',height=0,width=0)
# ggplot() +
#     geom_line(data=dat.sim.sub,aes(x=return_period,y=days_over,group=subset,color=subset),alpha=0.3)+
#     # geom_hex(data=dat.sim.sub,aes(x=return_period,y=days_over,color=subset),alpha=0.3,bins=70)+
#     geom_jitter(data=dat.sim.sub,aes(x=return_period,y=days_over,color=subset),alpha=0.3)+
#     geom_boxplot(data=subset(dat.sim.sub),aes(x=return_period, y=days_over,group=return_period),alpha=0.3)+
#     # geom_line(data=dat.sim,aes(x=return_period,y=days_over),linetype='longdash',size=1)+
#     geom_line(data=dat.obs,aes(x=return_period,y=days_over),size=1)+
#     guides(color=FALSE,size=FALSE) +
#     xlab('Return period (years)') + ylab('Heat wave duration (days)') +
#     ggtitle('Whole domain') +
#     scale_x_log10() +
#     theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
#     plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
#     panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
#     panel.border = element_rect(colour = "black"),strip.background = element_blank(),
#     legend.position = 'bottom',legend.justification='center',
#     legend.background = element_rect(fill="gray90", size=.5, linetype="dotted"))
# dev.off()
#
# pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim_tot,'yrs_obs_sim_intensity_return_periods_uk.pdf'),paper='a4r',height=0,width=0)
# ggplot() +
#     geom_line(data=dat.sim.sub,aes(x=return_period,y=days_over,group=subset,color=subset),alpha=0.3)+
#     # geom_line(data=dat.sim.one,aes(x=return_period,y=days_over),linetype='longdash',size=1) +
#     geom_line(data=dat.obs.one,aes(x=return_period,y=days_over),size=1) +
#     geom_jitter(data=dat.sim.sub.one,aes(x=return_period,y=days_over,color=subset),alpha=0.3) +
#     guides(color=FALSE,size=FALSE) +
#     xlab('Return period (years)') + ylab('Heat wave duration (days)') +
#     ggtitle('UK') +
#     scale_x_log10() +
#     theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
#     plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
#     panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
#     panel.border = element_rect(colour = "black"),strip.background = element_blank(),
#     legend.position = 'bottom',legend.justification='center',
#     legend.background = element_rect(fill="gray90", size=.5, linetype="dotted"))
# dev.off()
#
# pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim_tot,'yrs_obs_sim_intensity_return_periods_uk_boxplots.pdf'),paper='a4r',height=0,width=0)
# ggplot() +
#     geom_line(data=dat.sim.sub,aes(x=return_period,y=days_over,group=subset,color=subset),alpha=0.3)+
#     geom_boxplot(data=subset(dat.sim.sub.one),aes(x=return_period, y=days_over,group=return_period),alpha=0.3)+
#     geom_line(data=dat.obs.one,aes(x=return_period,y=days_over),size=1) +
#     geom_jitter(data=dat.sim.sub.one,aes(x=return_period,y=days_over,color=subset),alpha=0.3) +
#     guides(color=FALSE,size=FALSE) +
#     xlab('Return period (years)') + ylab('Heat wave duration (days)') +
#     ggtitle('UK') +
#     scale_x_log10() +
#     theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
#     plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
#     panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
#     panel.border = element_rect(colour = "black"),strip.background = element_blank(),
#     legend.position = 'bottom',legend.justification='center',
#     legend.background = element_rect(fill="gray90", size=.5, linetype="dotted"))
# dev.off()
#
# pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim_tot,'yrs_obs_sim_intensity_return_periods_portugal.pdf'),paper='a4r',height=0,width=0)
# ggplot() +
#     geom_line(data=dat.sim.sub.port,aes(x=return_period,y=days_over,group=subset,color=subset),alpha=0.3)+
#     # geom_line(data=dat.sim.one,aes(x=return_period,y=days_over),linetype='longdash',size=1) +
#     geom_line(data=dat.obs.port,aes(x=return_period,y=days_over),size=1) +
#     geom_jitter(data=dat.sim.sub.port,aes(x=return_period,y=days_over,color=subset),alpha=0.3) +
#     guides(color=FALSE,size=FALSE) +
#     xlab('Return period (years)') + ylab('Heat wave duration (days)') +
#     ggtitle('Portugal') +
#     scale_x_log10() +
#     theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
#     plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
#     panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
#     panel.border = element_rect(colour = "black"),strip.background = element_blank(),
#     legend.position = 'bottom',legend.justification='center',
#     legend.background = element_rect(fill="gray90", size=.5, linetype="dotted"))
# dev.off()
#
# pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim_tot,'yrs_obs_sim_intensity_return_periods_portugal_boxplots.pdf'),paper='a4r',height=0,width=0)
# ggplot() +
#     geom_line(data=dat.sim.sub.port,aes(x=return_period,y=days_over,group=subset,color=subset),alpha=0.3)+
#     geom_boxplot(data=subset(dat.sim.sub.port),aes(x=return_period, y=days_over,group=return_period),alpha=0.3)+
#     geom_line(data=dat.obs.port,aes(x=return_period,y=days_over),size=1) +
#     # geom_jitter(data=dat.sim.sub.port,aes(x=return_period,y=days_over,color=subset),alpha=0.3) +
#     guides(color=FALSE,size=FALSE) +
#     xlab('Return period (years)') + ylab('Heat wave duration (days)') +
#     ggtitle('Portugal') +
#     scale_x_log10() +
#     theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
#     plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
#     panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
#     panel.border = element_rect(colour = "black"),strip.background = element_blank(),
#     legend.position = 'bottom',legend.justification='center',
#     legend.background = element_rect(fill="gray90", size=.5, linetype="dotted"))
# dev.off()
#
# pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim_tot,'yrs_obs_sim_intensity_return_periods_portugal_boxplots_scenarios.pdf'),paper='a4r',height=0,width=0)
# ggplot() +
#     geom_line(data=dat.sim.sub.port,aes(x=return_period,y=days_over,group=subset,color=subset),alpha=0.3)+
#     geom_boxplot(data=subset(dat.sim.sub.port),aes(x=return_period, y=days_over,group=return_period),alpha=0.3)+
#     geom_line(data=dat.obs.port,aes(x=return_period,y=days_over),size=1) +
#     # geom_jitter(data=dat.sim.sub.port,aes(x=return_period,y=days_over,color=subset),alpha=0.3) +
#     guides(color=FALSE,size=FALSE) +
#     xlab('Return period (years)') + ylab('Heat wave duration (days)') +
#     ggtitle('Portugal') +
#     scale_x_log10() +
#     theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
#     plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
#     panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
#     panel.border = element_rect(colour = "black"),strip.background = element_blank(),
#     legend.position = 'bottom',legend.justification='center',
#     legend.background = element_rect(fill="gray90", size=.5, linetype="dotted"))
# dev.off()

# DROUGHT

# # load data for both comparing entire sim and obs
# dat.obs= read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_obs_drought_intensity_return_periods_europe.csv'))
# # dat.obs.mean = ddply(dat.obs,.(return_period),summarise,days_over=mean(days_over))
# # dat.sim= read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim1,'yrs_sim_intensity_return_periods_europe.csv'))
# dat.sim= read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_1000yrs_sim_drought_intensity_return_periods_europe.csv'))
# # dat.sim.mean = ddply(dat.sim,.(return_period),summarise,days_over=mean(days_over))
# average observations over entire

#################################
# FIGURE 8
#################################

# # plot entire europe with each line a square in CORDEX
# pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_obs_intensity_return_periods.pdf'),paper='a4r',height=0,width=0)
# ggplot() +
#     geom_line(data=dat.obs,aes(x=return_period,y=days_over))+
#     guides(color=FALSE,size=FALSE) +
#     xlab('Return period (years)') + ylab('Heavy preciptation duration (days)') +
#     ggtitle('Whole domain') +
#     scale_x_log10() +
#     theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
#     plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
#     panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
#     panel.border = element_rect(colour = "black"),strip.background = element_blank(),
#     legend.position = 'bottom',legend.justification='center',
#     legend.background = element_rect(fill="gray90", size=.5, linetype="dotted"))
# dev.off()
#
# pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim_tot,'yrs_obs_sim_intensity_return_periods_europe.pdf'),paper='a4r',height=0,width=0)
# ggplot() +
#     geom_line(data=dat.sim,aes(x=return_period,y=days_over),linetype='longdash')+
#     geom_line(data=dat.obs,aes(x=return_period,y=days_over))+
#     guides(color=FALSE,size=FALSE) +
#     xlab('Return period (years)') + ylab('Low precepitation duration (days)') +
#     ggtitle('Whole domain') +
#     # scale_x_log10() +
#     theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
#     plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
#     panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
#     panel.border = element_rect(colour = "black"),strip.background = element_blank(),
#     legend.position = 'bottom',legend.justification='center',
#     legend.background = element_rect(fill="gray90", size=.5, linetype="dotted"))
# dev.off()
