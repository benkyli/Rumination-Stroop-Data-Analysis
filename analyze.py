import pandas as pd
import matplotlib.pyplot as plt

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
# create graphs showing difference in reaction times for low and high ruminators across all conditions and groups

# create lablels for each rumination group. Standard refers to the counterbalancing group that started with standard Stroop. Emotion is the group that started with emotional Stroop.
standard_labels = ['standard_first_trait_low', 'standard_first_trait_high', 'standard_first_state_low', 'standard_first_state_high']
emotion_labels = ['emotion_first_trait_low', 'emotion_first_trait_high', 'emotion_first_state_low', 'emotion_first_state_high']

# Separate groups into high and low ruminators by finding medians. Then get row indices for the groups
# NOTE: this only gets row indices; remove the .index to see row values.
# NOTE: had to include > 0  condition because a participant had a missing rrs submission
standard_first_trait_low_idx = standard_first.loc[(standard_first['rrs_sums'] < standard_first['rrs_sums'].median()) & (standard_first['rrs_sums'] > 0)].index
standard_first_trait_high_idx = standard_first.loc[(standard_first['rrs_sums'] > standard_first['rrs_sums'].median()) & (standard_first['rrs_sums'] > 0)].index
standard_first_state_low_idx = standard_first.loc[standard_first['bsri_sums'] < standard_first['bsri_sums'].median()].index
standard_first_state_high_idx = standard_first.loc[standard_first['bsri_sums'] > standard_first['bsri_sums'].median()].index

emotion_first_trait_low_idx =  emotion_first.loc[emotion_first['rrs_sums'] <  emotion_first['rrs_sums'].median()].index
emotion_first_trait_high_idx = emotion_first.loc[emotion_first['rrs_sums'] >=  emotion_first['rrs_sums'].median()].index
emotion_first_state_low_idx =  emotion_first.loc[emotion_first['bsri_sums'] < emotion_first['bsri_sums'].median()].index
emotion_first_state_high_idx = emotion_first.loc[emotion_first['bsri_sums'] >= emotion_first['bsri_sums'].median()].index

standard_idx = [standard_first_trait_low_idx, standard_first_trait_high_idx, standard_first_state_low_idx, standard_first_state_high_idx]
emotion_idx = [emotion_first_trait_low_idx, emotion_first_trait_high_idx, emotion_first_state_low_idx, emotion_first_state_high_idx]

# means and standard errors of the means for each each condition in each block group
# NOTE: the loop below will be using values from the labels lists and the index lists. These assume that the length of all these lists are the same.
means = {}
sems = {}

for i in range(len(standard_labels)):
    means[standard_labels[i]] = standard_means.iloc[standard_idx[i]].mean()
    means[emotion_labels[i]] = emotion_means.iloc[emotion_idx[i]].mean()

    sems[standard_labels[i]] = standard_means.iloc[standard_idx[i]].sem()
    sems[emotion_labels[i]] = emotion_means.iloc[emotion_idx[i]].sem()


# combine means and sems from each rumination group into their own data frame based on counter balance condition 
standard_means_labels = ['standard_trait_mean', 'standard_state_mean'] 
emotion_means_labels = ['emotion_trait_mean', 'emotion_state_mean']
standard_sems_labels = ['standard_trait_sem', 'standard_state_sem']
emotion_sems_labels = ['emotion_trait_sem', 'emotion_state_sem']
combined_means = {}
combined_sems = {}
# NOTE: this implementation assumes that the rumination groups are divided evenly (into low vs high for each counterbalancing condition and state or trait)
# NOTE: the index (i) is combining low and high rumination groups into a single dataframe. The i * 2 is used to retrieve the original labels, which were ordered in low-high pairs based on rumination type (trait then state)
for i in range(len(standard_means_labels)):         
    combined_means[standard_means_labels[i]] = pd.DataFrame({'Conditions': means[standard_labels[i * 2]].index, 'Low Rumination': means[standard_labels[i * 2]].values,'High Rumination': means[standard_labels[i * 2 + 1]].values})
    combined_means[emotion_means_labels[i]] = pd.DataFrame({'Conditions': means[emotion_labels[i * 2]].index, 'Low Rumination': means[emotion_labels[i * 2]].values,'High Rumination': means[emotion_labels[i * 2 + 1]].values})

    combined_sems[standard_sems_labels[i]] = pd.concat([sems[standard_labels[i * 2]].rename('Low Rumination'), sems[standard_labels[i * 2 + 1]].rename('High Rumination')], axis=1)
    combined_sems[emotion_sems_labels[i]] = pd.concat([sems[emotion_labels[i * 2]].rename('Low Rumination'), sems[emotion_labels[i * 2 + 1]].rename('High Rumination')], axis=1)

# prepare labels for graphing
means_labels = standard_means_labels + emotion_means_labels
sems_labels = standard_sems_labels + emotion_sems_labels
block_labels = [['Standard', 'RRS'], ['Standard', 'BSRI'], ['Emotional', 'RRS'], ['Emotional', 'BSRI']]
ns = [[22, 23], [23, 23], [19, 20], [19, 20] ] # participants for low and high groups respectively

# graph the react times per Stroop condition
for block in range(len(means_labels)):
    mean = combined_means[means_labels[block]]
    sem = combined_sems[sems_labels[block]]
    block_label = block_labels[block]
    ax = mean.plot(x='Conditions', y = ['Low Rumination', 'High Rumination'], kind = 'bar', yerr=sem, rot = 0, color=['cornflowerblue', 'maroon'], width=0.65)
    leg = ax.legend()
    leg.get_texts()[0].set_text(f'Low Rumination (n={ns[block][0]})')
    leg.get_texts()[1].set_text(f'High Rumination (n={ns[block][1]})')
    plt.ylim(bottom=500) # limit y-min to see differences better
    # add bar values
    for i, p in enumerate(ax.patches):
        ax.annotate(str(int(p.get_height())), (p.get_x() * 1.005, p.get_height() + 43))
    plt.ylabel('Average Reaction Time (ms)')
    plt.title(f'Reaction Times Starting with {block_label[0]} Stroop ({block_label[1]} groups)')

# plt.show() # uncomment this to just see the reaction time graphs without the graphs below

#######################################################################################################################
# check median values; uncomment if you wish to see the medians per group
# print('standard-first rrs: ', standard_first['rrs_sums'].median())
# print('standard-first bsri: ', standard_first['bsri_sums'].median())
# print('emotion-first rrs: ', emotion_first['rrs_sums'].median())
# print('emotion-first bsri: ', emotion_first['bsri_sums'].median())

###############################################################################################################
# Checking distribution of sexes in each condition; uncomment the print statements to see

# checking gender distribution of each rumination group; NOTE: might need these values later, distribution is male skewed.
standard_first_trait_low_sex = df.iloc[standard_first_trait_low_idx]['sex_1'];   #   print(f'total = {len(standard_first_trait_low_idx)}'," Males: ", (standard_first_trait_low_sex == 1).sum(), 'Females: ',(standard_first_trait_low_sex == 2).sum())   
standard_first_trait_high_sex = df.iloc[standard_first_trait_high_idx]['sex_1']; #   print(f'total = {len(standard_first_trait_high_idx)}', " Males: ", (standard_first_trait_high_sex == 1).sum(), 'Females: ',(standard_first_trait_high_sex == 2).sum()) 
standard_first_state_low_sex = df.iloc[standard_first_state_low_idx]['sex_1'];   #   print(f'total = {len(standard_first_state_low_idx)}', " Males: ", (standard_first_state_low_sex == 1).sum(), 'Females: ',(standard_first_state_low_sex == 2).sum()) 
standard_first_state_high_sex = df.iloc[standard_first_state_high_idx]['sex_1']; #   print(f'total = {len(standard_first_state_high_idx)}', " Males: ", (standard_first_state_high_sex == 1).sum(), 'Females: ',(standard_first_state_high_sex == 2).sum()) 
#
emotion_first_trait_low_sex = df.iloc[ emotion_first_trait_low_idx]['sex_1'];    #  print(f'total = {len(emotion_first_trait_low_idx)}'," Males: ", (  emotion_first_trait_low_sex == 1).sum(), 'Females: ',(emotion_first_trait_low_sex == 2).sum())  
emotion_first_trait_high_sex = df.iloc[emotion_first_trait_high_idx]['sex_1'];   # print(f'total = {len( emotion_first_trait_high_idx)}', " Males: ", (emotion_first_trait_high_sex == 1).sum(), 'Females: ',(emotion_first_trait_high_sex == 2).sum()) 
emotion_first_state_low_sex = df.iloc[ emotion_first_state_low_idx]['sex_1'];    #  print(f'total = {len(emotion_first_state_low_idx)}', " Males: ", ( emotion_first_state_low_sex == 1).sum(), 'Females: ',(emotion_first_state_low_sex == 2).sum()) 
emotion_first_state_high_sex = df.iloc[emotion_first_state_high_idx]['sex_1'];   # print(f'total = {len( emotion_first_state_high_idx)}', " Males: ", (emotion_first_state_high_sex == 1).sum(), 'Females: ',(emotion_first_state_high_sex == 2).sum()) 

######################################################################################
# Create graphs of the mean rumination scores per counterbalancing group.
# order = standard low, standard high, emotion low, emotion high

# rrs groups
rrs_group_labels = [standard_first_trait_low_idx, standard_first_trait_high_idx, emotion_first_trait_low_idx, emotion_first_trait_high_idx]
rrs_group_means = [df.iloc[group]['rrs_sums'].mean() for group in rrs_group_labels]
rrs_group_stds = [df.iloc[group]['rrs_sums'].std() for group in rrs_group_labels]
# bsri groups
bsri_group_labels = [standard_first_state_low_idx, standard_first_state_high_idx, emotion_first_state_low_idx, emotion_first_state_high_idx]
bsri_group_means = [df.iloc[group]['bsri_sums'].mean() for group in bsri_group_labels]
bsri_group_stds = [df.iloc[group]['bsri_sums'].std() for group in bsri_group_labels]

# create data frame from data above to plot rrs groups
rrs_df = pd.DataFrame()
rrs_df['Rumination Level'] = ['Low', 'High']
rrs_df['standard_first_rrs'] = [rrs_group_means[0], rrs_group_means[1]] 
rrs_df['emotion_first_rrs'] =  [rrs_group_means[2], rrs_group_means[3]]
rrs_df['standard_first_std'] = [rrs_group_stds[0], rrs_group_stds[1]]
rrs_df['emotion_first_std'] =  [rrs_group_stds[2], rrs_group_stds[3]]

ax = rrs_df.plot.bar(x='Rumination Level',
                     y= ['standard_first_rrs', 'emotion_first_rrs'],
                     yerr=rrs_df[['standard_first_std', 'emotion_first_std']].T.values,
                     rot = 0,
                     color=['purple', 'gold'], 
                     width=0.65
                     )

for i, p in enumerate(ax.patches):
    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + 0.075, p.get_height()+ rrs_group_stds[i]+1))
leg = ax.legend(loc='upper left')
leg.get_texts()[0].set_text('Standard-first')
leg.get_texts()[1].set_text('Emotion-first')
plt.ylabel('RRS mean score')
plt.title('Mean RRS Scores based on Rumination and Counterbalancing Group')

# create data frame from data above to plot bsri groups
bsri_df = pd.DataFrame()
bsri_df['Rumination Level'] = ['Low', 'High']
bsri_df['standard_first_bsri'] = [bsri_group_means[0], bsri_group_means[1]] 
bsri_df['emotion_first_bsri'] =  [bsri_group_means[2], bsri_group_means[3]]
bsri_df['standard_first_std'] = [bsri_group_stds[0], bsri_group_stds[1]]
bsri_df['emotion_first_std'] =  [bsri_group_stds[2], bsri_group_stds[3]]

ax = bsri_df.plot.bar(x='Rumination Level',
                     y= ['standard_first_bsri', 'emotion_first_bsri'],
                     yerr=bsri_df[['standard_first_std', 'emotion_first_std']].T.values,
                     rot = 0,
                     color=['purple', 'gold'], 
                     width=0.65
                     )

for i, p in enumerate(ax.patches):
    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + 0.075, p.get_height()+ bsri_group_stds[i]+1))
leg = ax.legend(loc='upper left')
leg.get_texts()[0].set_text('Standard-first')
leg.get_texts()[1].set_text('Emotion-first')
plt.ylabel('BSRI mean score')
plt.title('Mean BSRI Scores based on Rumination and Counterbalancing Group')

plt.show() # show all graphs

#################################################################################
# Create CSV files separating the standard Stroop trial means and emotional Stroop trial means for linear mixed model analysis

# NOTE: naming conventions before this block of code had "standard_[whatever]" and "emotion_[whatever]" refer to the BLOCK order of standard-first or emotion-first
# use of "standard" and "emotion" from here on refer to the TRIAL type. So all standard trials or emotion trials are group together, regardless of counterbalancing condition
standard_rows = []
emotion_rows = []

# Loop through each participant
for index, row in df.iterrows():

    # exclude removed participants (removed participants with no psy_group value)
    if pd.isnull(psy_group):
        continue # go to next row

    # create variables for rrs_sum and counter balancing group
    rrs_sum = row['rrs_sums']
    psy_group = row['psy_group']

    # get means and rumination groups based on counterbalancing group
    # psy group 1 is standard-first group
    if psy_group == 1:
        means = standard_means.iloc[index] # get means row using index
        # get rrs group
        if index in standard_first_trait_low_idx:
            rrs_group = 0
        elif index in standard_first_trait_high_idx:
            rrs_group = 1
        else:
            # this else statement is included for the edge case of participants who had no RRS data
            # all other participants with a psy_group have both rrs and bsri data
            rrs_group = 'NaN'
            rrs_sum = 'NaN'

        # get bsri group
        if index in standard_first_state_low_idx:
            bsri_group = 0
        else:
            bsri_group = 1

    # people in emotion_first group
    else:
        means = emotion_means.iloc[index]
        # rrs group
        if index in emotion_first_trait_low_idx:
            rrs_group = 0
        else:
            rrs_group = 1
        # bsri group
        if index in emotion_first_state_low_idx:
            bsri_group = 0
        else:
            bsri_group = 1
        
    # order of row values
    # ['psytoolkit_ID', 'prolific_ID', 'counterbalancing_group', 'conditions', 'mean_RT', 'RRS_score', 'RRS_group', 'BSRI_score', 'BSRI_group', 'sex', 'age']
        # NOTE: conditions for standard: [congruent = 0, incongruent = 1], emotion: [negative = 0, neutral = 1, positive = 2]
 
    congruencies = ['congruent', 'incongruent'] # these will be used as keys
    for idx, congruency in enumerate(congruencies):
        # NOTE: idx in this case will denote the congruency condition.
        standard_row = [row['participant'], row['PROLIFIC_PID'], psy_group, idx, means[congruency], rrs_sum, rrs_group, row['bsri_sums'], bsri_group, row['sex_1'], row['age_1']]
        standard_rows.append(standard_row)

    # Loop through valence conditions
    valences = ['negative', 'neutral', 'positive']
    for idx, valence in enumerate(valences):
        emotion_row = [row['participant'], row['PROLIFIC_PID'], psy_group, idx, means[valence], rrs_sum, rrs_group, row['bsri_sums'], bsri_group, row['sex_1'], row['age_1']]
        emotion_rows.append(emotion_row)

# create dataframes for exporting to csv
    # NOTE: The standard and emotion trials could be grouped into 1 file and denoted through another column, but I will separate them for organization purposes.
columns_standard = ['psytoolkit_ID', 'prolific_ID', 'counterbalancing_group', 'congruency', 'mean_RT', 'RRS_score', 'RRS_group', 'BSRI_score', 'BSRI_group', 'sex', 'age']
columns_emotion =  ['psytoolkit_ID', 'prolific_ID', 'counterbalancing_group', 'valence', 'mean_RT', 'RRS_score', 'RRS_group', 'BSRI_score', 'BSRI_group', 'sex', 'age']

df_standard_trials = pd.DataFrame(standard_rows, columns=columns_standard)
df_emotion_trials = pd.DataFrame(emotion_rows, columns=columns_emotion)

# Convert the dataframes into csv files; uncomment these lines if you want to create the files. 
# df_standard_trials.to_csv('stroop_standard_trials.csv', index=False)
# df_emotion_trials.to_csv('stroop_emotion_trials.csv', index=False)