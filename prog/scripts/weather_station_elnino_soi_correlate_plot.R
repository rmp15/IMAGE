library(ggplot2)

# get correct directory
setwd('~/git/IMAGE/output/minas_brazil/elnino/')

# load monthly and seasonal dataframes from python work
df_monthly_master  = read.csv('monthly_elnino_r_squared_values.csv')
df_season_master = read.csv('seasonal_elnino_r_squared_values.csv')

# plots

pdf('seasonal_values_r_by_station_nino_metric_sig_plot_R_version.pdf', paper='a4r', height=0, width=0)
print(ggplot(data=df_season_master) +
geom_point(size=2,aes(x=season, y=r_value, color=as.factor(station), shape=as.factor(sig))) +
ggtitle('') +
scale_x_continuous(breaks=c(0, 1), labels=c("wet", "dry")) +
scale_shape_discrete(guide=FALSE) +
scale_color_discrete(name='Rain gauge') +
geom_hline(yintercept=0, linetype='dashed') +
facet_wrap('elnino_metric') +
ylim(c(-0.5,0.5)) +
theme_bw() +  theme(legend.position="bottom"))
dev.off()

pdf('monthly_values_r_by_station_nino_metric_sig_plot_R_version.pdf', paper='a4r', height=0, width=0)
print(ggplot(data=df_monthly_master) +
geom_point(size=2,aes(x=month, y=r_value, color=as.factor(station), shape=as.factor(sig))) +
ggtitle('') +
scale_x_continuous(breaks=c(1:12), labels=c('J','F','M','A','M','J','J','A','S','O','N','D')) +
scale_shape_discrete(guide=FALSE) +
scale_color_discrete(name='Rain gauge') +
geom_hline(yintercept=0, linetype='dashed') +
ylim(c(-0.5,0.5)) +
facet_wrap('elnino_metric') +
theme_bw() +  theme(legend.position="bottom"))
dev.off()