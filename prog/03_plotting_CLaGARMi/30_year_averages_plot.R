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

print(args)

years_sim_tot = years_sim1 + years_sim2

# short names for months
month.short <- c('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')

input.dir = '~/git/IMAGE/output/CLaGARMi/euro_cordex/figures_processing/'
output.dir = paste0('~/git/IMAGE/output/CLaGARMi/euro_cordex/figures/',metric,'/')

# create directory for output
ifelse(!dir.exists(output.dir), dir.create(output.dir, recursive=TRUE), FALSE)

# load data for both comparing entire sim and obs
dat.obs.sim.1 = read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim1,'yrs_obs_sim_merged.csv'))
dat.obs.sim.2 = read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim2,'yrs_obs_sim_merged.csv'))
dat.obs.sim.1$mean_value_sim1 = dat.obs.sim.1$mean_value_sim ; dat.obs.sim.1$mean_value_sim = NULL
dat.obs.sim.2$mean_value_sim2 = dat.obs.sim.2$mean_value_sim ; dat.obs.sim.2$mean_value_sim = NULL
dat.obs.sim.1$sd_value_sim1 = dat.obs.sim.1$sd_value_sim ; dat.obs.sim.1$sd_value_sim = NULL
dat.obs.sim.2$sd_value_sim2 = dat.obs.sim.2$sd_value_sim ; dat.obs.sim.2$sd_value_sim = NULL

dat.obs.sim = merge(dat.obs.sim.1,dat.obs.sim.2)

dat.obs.sim$mean_value_sim = (dat.obs.sim$mean_value_sim1*years_sim1 + dat.obs.sim$mean_value_sim2*years_sim2)/(years_sim1+years_sim2)
dat.obs.sim$sd_value_sim = (dat.obs.sim$sd_value_sim1*years_sim1 + dat.obs.sim$sd_value_sim2*years_sim2)/(years_sim1+years_sim2)

# remove unnecessary columns
dat.obs.sim$mean_value_sim1 = dat.obs.sim$mean_value_sim2 = dat.obs.sim$sd_value_sim1 = dat.obs.sim$sd_value_sim2= NULL
dat.obs.sim$X = NULL

# order by month and by site and fix row names
dat.obs.sim = dat.obs.sim[order(dat.obs.sim$month,dat.obs.sim$site),]
rownames(dat.obs.sim) = seq(1:nrow(dat.obs.sim))

# also load sim ensemble data and find mins and max from total combined years
dat.sim.ens.1 = read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim1,'yrs_sim_ens.csv'))
dat.sim.ens.2 = read.csv(paste0(input.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim2,'yrs_sim_ens.csv'))

dat.sim.ens.1 = ddply(dat.sim.ens.1,.(month,site),summarise,mean_max=max(mean_value), mean_min=min(mean_value),
                    sd_max=max(sd_value),sd_min=min(sd_value))
dat.sim.ens.2 = ddply(dat.sim.ens.2,.(month,site),summarise,mean_max=max(mean_value), mean_min=min(mean_value),
                    sd_max=max(sd_value),sd_min=min(sd_value))

dat.sim.ens = rbind(dat.sim.ens.1,dat.sim.ens.2)
dat.sim.ens = ddply(dat.sim.ens,.(month,site),summarise,mean_max=max(mean_max),mean_min=min(mean_min),
                    sd_max=max(sd_max),sd_min=min(sd_min))

dat.sim.ens = merge(dat.obs.sim,dat.sim.ens,by=c('month','site'),all.x=0)

if(metric%in%c('appt','tasmax')){
    dat.obs.sim$mean_value_obs = dat.obs.sim$mean_value_obs - 273.15
    dat.obs.sim$mean_value_sim = dat.obs.sim$mean_value_sim - 273.15
    dat.sim.ens$mean_value_obs = dat.sim.ens$mean_value_obs - 273.15
    dat.sim.ens$mean_value_sim = dat.sim.ens$mean_value_sim - 273.15
    dat.sim.ens$mean_max = dat.sim.ens$mean_max - 273.15
    dat.sim.ens$mean_min = dat.sim.ens$mean_min - 273.15
}

# add short names of months
dat.obs.sim$month.short <- mapvalues(dat.obs.sim$month,from=sort(unique(dat.obs.sim$month)),to=month.short)
dat.obs.sim$month.short <- reorder(dat.obs.sim$month.short,dat.obs.sim$month)
dat.sim.ens$month.short <- mapvalues(dat.sim.ens$month,from=sort(unique(dat.sim.ens$month)),to=month.short)
dat.sim.ens$month.short <- reorder(dat.sim.ens$month.short,dat.sim.ens$month)

# calculate mean bias and RMSE of variable simulated
bias.mean = with(dat.sim.ens,mean(mean_value_sim-mean_value_obs))
bias.sd = with(dat.sim.ens,mean(sd_value_sim-sd_value_obs))
rmse.mean = with(dat.sim.ens,mean((mean_value_sim-mean_value_obs)^2))
rmse.sd = with(dat.sim.ens,mean((sd_value_sim-sd_value_obs)^2))

print(c(bias.mean,bias.sd,rmse.mean,rmse.sd))

######### #########################
# Figure 2
#################################

pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim_tot,'yrs_mean.pdf'),paper='a4r',height=0,width=0)
print(ggplot() +
    geom_point(data=dat.obs.sim,aes(x=mean_value_obs,y=mean_value_sim),size=0.5) +
    geom_errorbar(data=dat.sim.ens,aes(x=mean_value_obs,ymax=mean_max,ymin=mean_min),alpha=0.2,col='dark blue') +
    geom_abline(col='red',alpha='0.5') +
    ggtitle(paste0(metric,' mean')) +
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

pdf(paste0(output.dir,metric,'_',continent,'_',scen,'_',start,'_',end,'_',years_sim_tot,'yrs_sd.pdf'),paper='a4r',height=0,width=0)
print(ggplot() +
    geom_point(data=dat.obs.sim,aes(x=sd_value_obs,y=sd_value_sim),size=0.5) +
    geom_errorbar(data=dat.sim.ens,aes(x=sd_value_obs,ymax=sd_max,ymin=sd_min),alpha=0.2,col='dark blue') +
    geom_abline(col='red',alpha='0.5') +
    ggtitle(paste0(metric,' sd')) +
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