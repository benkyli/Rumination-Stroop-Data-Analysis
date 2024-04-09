import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set up data frames

df = pd.read_csv('data.csv') # used for getting rrs and bsri scores
# print(df['age_1'].mean()) # mean age of all participants
# print(df['age_1'].min()) # minimum age of all participants
# print(df['age_1'].max()) # maximum age of all participants

standard_means = pd.read_csv('Standard_Emotion_Stroop.mean.csv') # means csv for each block and participants with all conditions. 
emotion_means = pd.read_csv('Emotion_Standard_Stroop.mean.csv')

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
        # NOTE: had to include > 0  condition because of empty RRS of participant 1 (index = 0)
standard_first_trait_low = standard_first.loc[(standard_first['rrs_sums'] < standard_first['rrs_sums'].median()) & (standard_first['rrs_sums'] > 0)].index
standard_first_trait_high = standard_first.loc[(standard_first['rrs_sums'] > standard_first['rrs_sums'].median()) & (standard_first['rrs_sums'] > 0)].index
standard_first_state_low = standard_first.loc[standard_first['bsri_sums'] < standard_first['bsri_sums'].median()].index
standard_first_state_high = standard_first.loc[standard_first['bsri_sums'] > standard_first['bsri_sums'].median()].index

emotion_first_trait_low =  emotion_first.loc[emotion_first['rrs_sums'] <  emotion_first['rrs_sums'].median()].index
emotion_first_trait_high = emotion_first.loc[emotion_first['rrs_sums'] >=  emotion_first['rrs_sums'].median()].index
emotion_first_state_low =  emotion_first.loc[emotion_first['bsri_sums'] < emotion_first['bsri_sums'].median()].index
emotion_first_state_high = emotion_first.loc[emotion_first['bsri_sums'] >= emotion_first['bsri_sums'].median()].index

# check median values
# print('standard-first rrs: ', standard_first['rrs_sums'].median())
# print('standard-first bsri: ', standard_first['bsri_sums'].median())
# print('emotion-first rrs: ', emotion_first['rrs_sums'].median())
# print('emotion-first bsri: ', emotion_first['bsri_sums'].median())

# means for each each condition in each block group
standard_first_trait_low_mean  = standard_means.iloc[standard_first_trait_low].mean()
standard_first_trait_high_mean = standard_means.iloc[standard_first_trait_high].mean()
standard_first_state_low_mean  = standard_means.iloc[standard_first_state_low].mean()
standard_first_state_high_mean = standard_means.iloc[standard_first_state_high].mean()

emotion_first_trait_low_mean  = emotion_means.iloc[emotion_first_trait_low].mean()
emotion_first_trait_high_mean = emotion_means.iloc[emotion_first_trait_high].mean()
emotion_first_state_low_mean  = emotion_means.iloc[emotion_first_state_low].mean()
emotion_first_state_high_mean = emotion_means.iloc[emotion_first_state_high].mean()

# SEMS for each condition in each block group; yeah... the labels saying sd below are inaccurate 
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

# # Started with standard Stroop graph
# for block in range(len(means)):
#     mean = means[block]
#     sd = sds[block]
#     block_label = block_labels[block]
#     ax = mean.plot(x='Conditions', y = ['Low Rumination', 'High Rumination'], kind = 'bar', yerr=sd, rot = 0, color=['cornflowerblue', 'maroon'], width=0.65)
#     plt.ylim(bottom=500) # limit y-min to see differences better
#     # add bar values
#     for i, p in enumerate(ax.patches):
#         ax.annotate(str(int(p.get_height())), (p.get_x() * 1.005, p.get_height() + 43))
#     plt.ylabel('Reaction time (ms)')
#     plt.title(f'Reaction Times Starting with {block_label[0]} Stroop ({block_label[1]} groups)')

# # Uncomment this line to show graphs
# # plt.show()

###############################################################################################################
# Checking other factors; age and sex

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

#################################################################################
# Separating standard Stroop trial means and emotional Stroop trial means into separate CSVs for linear mixed models

# NOTE: naming conventions before this block of code had "standard_[whatever]" and "emotion_[whatever]" refer to the BLOCK order of standard-first or emotion-first
# use of "standard" and "emotion" from here on refer to the TRIAL type. So all standard trials go into standard_rows and all emotion trials go into emotion_rows
standard_rows = []
emotion_rows = []

# Loop through each participant
for index, row in df.iterrows():

    psy_group = row['psy_group']
    # exclude removed participants (removed participants have no psy_group value)
    if pd.isnull(psy_group):
        continue # go to next row

    # get means and rumination groups based on counterbalancing group
    # people in standard-first group
    if psy_group == 1:
        means = standard_means.iloc[index] # get means row using index
        # get rrs group
        if index in standard_first_trait_low:
            rrs_group = 0
        elif index in standard_first_trait_high:
            rrs_group = 1
        else:
            # this else statement is included for the edge case of participant 1 who had no RRS data
            # all other participants with a psy_group have both rrs and bsri data
            rrs_group = 'NaN'

        # get bsri group
        if index in standard_first_state_low:
            bsri_group = 0
        else:
            bsri_group = 1

    # people in emotion_first group
    else:
        means = emotion_means.iloc[index]
        # rrs group
        if index in emotion_first_trait_low:
            rrs_group = 0
        else:
            rrs_group = 1
        # bsri group
        if index in emotion_first_state_low:
            bsri_group = 0
        else:
            bsri_group = 1
        
    # order of row values; these will be column names later:
    # ['psytoolkit_ID', 'prolific_ID', 'counterbalancing_group', 'congruency', 'mean_RT', 'RRS_score', 'RRS_group', 'BSRI_score', 'BSRI_group']
        # NOTE: conditions will be standard: [congruent = 0, incongruent = 1], emotion: [negative = 0, neutral = 1, positive = 2]
    # Loop through congruency conditions to produce 2 rows per participant
    congruencies = ['congruent', 'incongruent'] # these will be used as keys
    for idx, congruency in enumerate(congruencies):
        # NOTE: idx in this case will denote the congruency condition.
        standard_row = [row['participant'], row['PROLIFIC_PID'], psy_group, idx, means[congruency], row['rrs_sums'], rrs_group, row['bsri_sums'], bsri_group]
        standard_rows.append(standard_row)
    # Loop through valence conditions; produces 3 rows per participant
    valences = ['negative', 'neutral', 'positive']
    for idx, valence in enumerate(valences):
        emotion_row = [row['participant'], row['PROLIFIC_PID'], psy_group, idx, means[valence], row['rrs_sums'], rrs_group, row['bsri_sums'], bsri_group]
        emotion_rows.append(emotion_row)

# create dataframes for exporting to csv
    # NOTE: technically, the standard and emotion trials could all be in 1 file if we assign the valences to 3, 4, 5 and make the column name 'condition'. 
    # I'll keep it separated, for organization purposes 
columns_standard = ['psytoolkit_ID', 'prolific_ID', 'counterbalancing_group', 'congruency', 'mean_RT', 'RRS_score', 'RRS_group', 'BSRI_score', 'BSRI_group']
columns_emotion =  ['psytoolkit_ID', 'prolific_ID', 'counterbalancing_group', 'valence', 'mean_RT', 'RRS_score', 'RRS_group', 'BSRI_score', 'BSRI_group']

df_standard_trials = pd.DataFrame(standard_rows, columns=columns_standard)
df_emotion_trials = pd.DataFrame(emotion_rows, columns=columns_emotion)

# Convert the dataframes into csv files; uncomment these if you want to create the files. 
# df_standard_trials.to_csv('stroop_standard_trials.csv', index=False)
# df_emotion_trials.to_csv('stroop_emotion_trials.csv', index=False)

######################################################################################
# Create mean_rt based on group. Mean of all conditions together, not separate like before
# order: trait low, trait high, state low, state high
standard_means_labels = [standard_first_trait_low_mean, standard_first_trait_high_mean, standard_first_state_low_mean, standard_first_state_high_mean]
emotion_means_labels = [emotion_first_trait_low_mean, emotion_first_trait_high_mean, emotion_first_state_low_mean, emotion_first_state_high_mean]   
standard_group_means = [groupmean.mean() for groupmean in standard_means_labels]
emotion_group_means = [groupmean.mean() for groupmean in emotion_means_labels]

# get sd
standard_sd_labels = [standard_means.iloc[standard_first_trait_low].std(), standard_means.iloc[standard_first_trait_high].std(), standard_means.iloc[standard_first_state_low].std(), standard_means.iloc[standard_first_state_high].std()]
emotion_sd_labels = [emotion_means.iloc[emotion_first_trait_low].std(), emotion_means.iloc[emotion_first_trait_high].std(), emotion_means.iloc[emotion_first_state_low].std(), emotion_means.iloc[emotion_first_state_high].std()]
standard_group_stds = [groupstd.std() for groupstd in standard_sd_labels]

print(standard_group_stds)

xlabels = ["Low", "High"]

low_trait = [standard_group_means[0], emotion_group_means[0]]
high_trait = [standard_group_means[1], emotion_group_means[1]]
low_state = [standard_group_means[2], emotion_group_means[2]]
high_state = [standard_group_means[3], emotion_group_means[3]]

x = np.arange(2) # positions for x ticks
width = 0.27

ax = plt.subplot()
ax.bar(x, low_trait, width)
ax.bar(x + width, high_trait, width)
ax.set_ylabel("Mean reaction time (ms)")
ax.set_xticks(x + width/2) # only have 2 labels
ax.set_xticklabels(xlabels)
plt.show()




# standard_trait_low_rum_mean = standard_trait_mean['Low Rumination'].mean()