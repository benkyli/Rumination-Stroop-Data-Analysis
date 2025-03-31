# Data Analysis of the Impacts of Emotional Processing and Rumination on the Emotional Stroop task

##### This repository contains the data analysis for my thesis on the effects of emotional processing and rumination on the Stroop task. The experiment was hosted on PsyToolKit and participants were recruited through Prolific.

## Data Files
##### *data.csv* contains the scores for the rumination surveys and other important participant data.

##### The files *Emotion_Standard_Stroop.mean.csv* and *Standard_Emotion_Stroop.mean.csv* are the average Stroop reaction times for the experiment's 2 counterbalancing groups. People started with either emotional Stroop or standard Stroop trials. They would complete the remaining condition after the first set of trials.

## Analysis Files 

##### *analyze.py* created graphs of the data and created the files *stroop_emotion_trials.csv* and *stroop_standard_trials.csv*. These files were used to create mixed linear models using the file *stroopanalysis.R*

## Data Representation
##### The graphs in the *graphs* folder show the rumination scores of each condition group and the average Stroop times for each counterbalancing condition.

##### The *Regression Tables* folder contains mixed linear models of the data.