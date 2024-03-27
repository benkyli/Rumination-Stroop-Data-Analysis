import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

# Set up data frames
# NOTE: may need to remove participant 1, 7, and 46

df = pd.read_csv('data.csv') # used for getting rrs and bsri scores

standard_means = pd.read_csv('Standard_Emotion_Stroop.mean.csv') # means csv for each block and participants with all conditions. 
emotion_means = pd.read_csv("Emotion_Standard_Stroop.mean.csv")

# Create arrays containing labels of rrs and bsri columns
rrs_cols = [f'rumination_{i}' for i in range(1, 23)] # get the columns names of the RRS
bsri_cols = [f'bsri_{i}' for i in range(1, 9)]

# create rrs and bsri sum columns
df['rrs_sums'] = df[rrs_cols].sum(axis=1)
df['bsri_sums'] = df[bsri_cols].sum(axis=1)

# Separate counterbalanced groups
standard_first = df.loc[df['psy_group'] == 1]
emotion_first = df.loc[df['psy_group'] == 2]

########################################################################################################################

# Separate groups into high and low ruminators by finding medians. Then get row indices for the groups
# NOTE: this gets row indices, not the actual rows. Remove the .index to see row values.
             

    # standard first and emotion first indices
standard_first_trait_low = standard_first.loc[standard_first['rrs_sums'] < standard_first['rrs_sums'].median()].index
standard_first_trait_high = standard_first.loc[standard_first['rrs_sums'] > standard_first['rrs_sums'].median()].index
standard_first_state_low = standard_first.loc[standard_first['bsri_sums'] < standard_first['bsri_sums'].median()].index
standard_first_state_high = standard_first.loc[standard_first['bsri_sums'] > standard_first['bsri_sums'].median()].index

emotion_first_trait_low =  emotion_first.loc[emotion_first['rrs_sums'] <=  emotion_first['rrs_sums'].median()].index
emotion_first_trait_high = emotion_first.loc[emotion_first['rrs_sums'] >  emotion_first['rrs_sums'].median()].index
emotion_first_state_low =  emotion_first.loc[emotion_first['bsri_sums'] <= emotion_first['bsri_sums'].median()].index
emotion_first_state_high = emotion_first.loc[emotion_first['bsri_sums'] > emotion_first['bsri_sums'].median()].index

# means for each each condition in each block group
standard_first_trait_low_mean  = standard_means.iloc[standard_first_trait_low].mean()
standard_first_trait_high_mean = standard_means.iloc[standard_first_trait_high].mean()
standard_first_state_low_mean  = standard_means.iloc[standard_first_state_low].mean()
standard_first_state_high_mean = standard_means.iloc[standard_first_state_high].mean()

emotion_first_trait_low_mean  = emotion_means.iloc[emotion_first_trait_low].mean()
emotion_first_trait_high_mean = emotion_means.iloc[emotion_first_trait_high].mean()
emotion_first_state_low_mean  = emotion_means.iloc[emotion_first_state_low].mean()
emotion_first_state_high_mean = emotion_means.iloc[emotion_first_state_high].mean()

# sds for each condition in each block group
standard_first_trait_low_sd = standard_means.iloc[standard_first_trait_low].sem()
standard_first_trait_high_sd = standard_means.iloc[standard_first_trait_high].sem()
standard_first_state_low_sd = standard_means.iloc[standard_first_state_low].sem()
standard_first_state_high_sd = standard_means.iloc[standard_first_state_high].sem()

emotion_first_trait_low_sd =  emotion_means.iloc[emotion_first_trait_low].sem()
emotion_first_trait_high_sd = emotion_means.iloc[emotion_first_trait_high].sem()
emotion_first_state_low_sd =  emotion_means.iloc[emotion_first_state_low].sem()
emotion_first_state_high_sd = emotion_means.iloc[emotion_first_state_high].sem()

# Convert means and sds into dataframes... surely there's a better way to do this
standard_trait_mean = pd.DataFrame({'Conditions': standard_first_trait_high_mean.index, 'Low Rumination': standard_first_trait_low_mean.values,'High Rumination': standard_first_trait_high_mean.values})
standard_state_mean = pd.DataFrame({'Conditions': standard_first_state_high_mean.index, 'Low Rumination': standard_first_state_low_mean.values,'High Rumination': standard_first_state_high_mean.values})
emotion_trait_mean = pd.DataFrame({'Conditions': emotion_first_trait_high_mean.index, 'Low Rumination': emotion_first_trait_low_mean.values,'High Rumination': emotion_first_trait_high_mean.values})
emotion_state_mean = pd.DataFrame({'Conditions': emotion_first_state_high_mean.index, 'Low Rumination': emotion_first_state_low_mean.values,'High Rumination': emotion_first_state_high_mean.values})
means = [standard_trait_mean, standard_state_mean, emotion_trait_mean, emotion_state_mean]

standard_trait_sd = pd.concat([standard_first_trait_low_sd.rename('Low Rumination'), standard_first_trait_high_sd.rename('High Rumination')], axis=1)
standard_state_sd = pd.concat([standard_first_state_low_sd.rename('Low Rumination'), standard_first_state_high_sd.rename('High Rumination')], axis=1)
emotion_trait_sd =  pd.concat([emotion_first_trait_low_sd.rename('Low Rumination'), emotion_first_trait_high_sd.rename('High Rumination')], axis=1)
emotion_state_sd =  pd.concat([emotion_first_state_low_sd.rename('Low Rumination'), emotion_first_state_high_sd.rename('High Rumination')], axis=1)
sds = [standard_trait_sd, standard_state_sd, emotion_trait_sd, emotion_state_sd]

block_labels = [['Standard', 'RRS'], ['Standard', 'BSRI'], ['Emotional', 'RRS'], ['Emotional', 'BSRI']]

# Started with standard Stroop graph
for block in range(len(means)):
    mean = means[block]
    sd = sds[block]
    block_label = block_labels[block]
    ax = mean.plot(x='Conditions', y = ['Low Rumination', 'High Rumination'], kind = 'bar', yerr=sd, rot = 0, color=['cornflowerblue', 'maroon'], width=0.65)
    plt.ylim(bottom=500) # limit y-min to see differences better
    # add bar values
    for i, p in enumerate(ax.patches):
        ax.annotate(str(int(p.get_height())), (p.get_x() * 1.005, p.get_height() + 43))
    plt.ylabel('Reaction time (ms)')
    plt.title(f'Reaction Times Starting with {block_label[0]} Stroop ({block_label[1]} groups)')

plt.show()

###############################################################################################################
# Checking other factors

# checking ages of each rumination group NOTE: about the same all around. Doesn't seem to be a confounding variable
# print(df.iloc[standard_first_trait_low]['age_1'].mean())
# print(df.iloc[standard_first_trait_high]['age_1'].mean())
# print(df.iloc[emotion_first_trait_low]['age_1'].mean())
# print(df.iloc[emotion_first_trait_high]['age_1'].mean())

# checking gender distribution of each rumination group; NOTE: might need these values later, distribution is male skewed.
standard_first_trait_low_sex = df.iloc[standard_first_trait_low]['sex_1'];   #   print(f'total = {len(standard_first_trait_low)}'," Males: ", (standard_first_trait_low_sex == 1).sum(), 'Females: ',(standard_first_trait_low_sex == 2).sum())   
standard_first_trait_high_sex = df.iloc[standard_first_trait_high]['sex_1']; #   print(f'total = {len(standard_first_trait_high)}', " Males: ", (standard_first_trait_high_sex == 1).sum(), 'Females: ',(standard_first_trait_high_sex == 2).sum()) 
standard_first_state_low_sex = df.iloc[standard_first_state_low]['sex_1'];   #   print(f'total = {len(standard_first_state_low)}', " Males: ", (standard_first_state_low_sex == 1).sum(), 'Females: ',(standard_first_state_low_sex == 2).sum()) 
standard_first_state_high_sex = df.iloc[standard_first_state_high]['sex_1']; #   print(f'total = {len(standard_first_state_high)}', " Males: ", (standard_first_state_high_sex == 1).sum(), 'Females: ',(standard_first_state_high_sex == 2).sum()) 
#
emotion_first_trait_low_sex = df.iloc[ emotion_first_trait_low]['sex_1'];    #  print(f'total = {len(emotion_first_trait_low)}'," Males: ", (  emotion_first_trait_low_sex == 1).sum(), 'Females: ',(emotion_first_trait_low_sex == 2).sum())  
emotion_first_trait_high_sex = df.iloc[emotion_first_trait_high]['sex_1'];   # print(f'total = {len( emotion_first_trait_high)}', " Males: ", (emotion_first_trait_high_sex == 1).sum(), 'Females: ',(emotion_first_trait_high_sex == 2).sum()) 
emotion_first_state_low_sex = df.iloc[ emotion_first_state_low]['sex_1'];    #  print(f'total = {len(emotion_first_state_low)}', " Males: ", ( emotion_first_state_low_sex == 1).sum(), 'Females: ',(emotion_first_state_low_sex == 2).sum()) 
emotion_first_state_high_sex = df.iloc[emotion_first_state_high]['sex_1'];   # print(f'total = {len( emotion_first_state_high)}', " Males: ", (emotion_first_state_high_sex == 1).sum(), 'Females: ',(emotion_first_state_high_sex == 2).sum()) 
