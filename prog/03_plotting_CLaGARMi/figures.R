library(ggplot2)
library(plyr)

# TEMPORARY
month.short <- c('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')

# need to generalise to any location any ensemble etc.
var = 'huss'

input.dir = '~/git/IMAGE/output/CLaGARMi/euro_cordex/figures_processing/'
output.dir = '~/git/IMAGE/output/CLaGARMi/euro_cordex/figures/'

#################################
# Figure 2
#################################

# load data for both comparing entire sim and obs, as well as sim ensemble data GENERALISE
dat.obs.sim = read.csv(paste0(input.dir,'/',var,'_euro_hist_1971_2000_obs_sim_merged.csv'))
dat.sim.ens = read.csv(paste0(input.dir,'/',var,'_euro_hist_1971_2000_sim_ens.csv'))
dat.sim.ens = ddply(dat.sim.ens,.(month,site),summarise,mean_max=max(mean_value), mean_min=min(mean_value),
                    sd_max=max(sd_value),sd_min=min(sd_value))
dat.sim.ens = merge(dat.obs.sim,dat.sim.ens,by=c('month','site'),all.x=0)

# add short names of months
dat.obs.sim$month.short <- mapvalues(dat.obs.sim$month,from=sort(unique(dat.obs.sim$month)),to=month.short)
dat.obs.sim$month.short <- reorder(dat.obs.sim$month.short,dat.obs.sim$month)
dat.sim.ens$month.short <- mapvalues(dat.sim.ens$month,from=sort(unique(dat.sim.ens$month)),to=month.short)
dat.sim.ens$month.short <- reorder(dat.sim.ens$month.short,dat.sim.ens$month)

pdf(paste0(output.dir,var,'_mean.pdf'),paper='a4r',height=0,width=0)
print(ggplot() +
    geom_point(data=dat.obs.sim,aes(x=mean_value_obs,y=mean_value_sim),size=0.5) +
    geom_errorbar(data=dat.sim.ens,aes(x=mean_value_obs,ymax=mean_max,ymin=mean_min),alpha=0.2,col='dark blue') +
    geom_abline(col='red',alpha='0.5') +
    ggtitle(paste0(var,' mean')) +
    xlab('CORDEX') + ylab('IMAGE simulated') +
    facet_wrap(~month.short,scale='free') +
    theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
    plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
    panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
    panel.border = element_rect(colour = "black"),strip.background = element_blank(),
    legend.position = 'bottom',legend.justification='center',
    legend.background = element_rect(fill="gray90", size=.5, linetype="dotted")))
dev.off()

#################################
# Figure 3
#################################

pdf(paste0(output.dir,var,'_sd.pdf'),paper='a4r',height=0,width=0)
print(ggplot() +
    geom_point(data=dat.obs.sim,aes(x=sd_value_obs,y=sd_value_sim),size=0.5) +
    geom_errorbar(data=dat.sim.ens,aes(x=sd_value_obs,ymax=sd_max,ymin=sd_min),alpha=0.2,col='dark blue') +
    geom_abline(col='red',alpha='0.5') +
    ggtitle(paste0(var,' sd')) +
    xlab('CORDEX') + ylab('IMAGE simulated') +
    facet_wrap(~month.short,scale='free') +
    theme_bw() + theme(panel.grid.major = element_blank(),axis.text.x = element_text(angle=0),
    plot.title = element_text(hjust = 0.5),panel.background = element_blank(),
    panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
    panel.border = element_rect(colour = "black"),strip.background = element_blank(),
    legend.position = 'bottom',legend.justification='center',
    legend.background = element_rect(fill="gray90", size=.5, linetype="dotted")))
dev.off()

#################################
# Figure 4
#################################