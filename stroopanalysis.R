# linear mixed models for stroop and emotional stroop analysis

library(lme4)
library(simr)
library(sjPlot)
library(tidyverse)
set.seed(1234)

# initialize dataframes
df <- read.csv("stroop_standard_trials.csv")
df2 <- read.csv("stroop_emotion_trials.csv")

# rrs standard trials
m <- lmer(
  mean_RT ~ counterbalancing_group * congruency * RRS_group * age * sex
    + (1 | prolific_ID),
  data = df
)

# save table to html
tab_model(m, file = "rrs_standard_trials.doc")


# rrs emotion trials
m2 <- lmer(
  mean_RT ~ counterbalancing_group * valence * RRS_group * age * sex
    + (1 | prolific_ID),
  data = df2
)

tab_model(m2, file = "rrs_emotion_trials.html") # , file = "blahblah.doc") #change this so it saves to your desired directory

# bsri standard trials
m3 <- lmer(
  mean_RT ~ counterbalancing_group * congruency * BSRI_group * age * sex
    + (1 | prolific_ID),
  data = df
)

tab_model(m3, file = "bsri_standard_trials.html")

# bsri emotion trials
m4 <- lmer(
  mean_RT ~ counterbalancing_group * valence * BSRI_group * age * sex
    + (1 | prolific_ID),
  data = df2
)

tab_model(m4, file = "bsri_emotion_trials.html")


sumtable <- summary(m)
plot_model(m)
plot_model(m, type = "est")
