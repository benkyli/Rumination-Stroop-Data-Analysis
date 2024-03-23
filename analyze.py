import pandas as pd

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

# Separate groups into high and low ruminators by finding medians
# NOTE: this gets row indices, not the actual rows. Remove the .index for the whole table.
# ex: standard_first_trait_low = standard_first.loc[standard_first['rrs_sums'] < standard_first['rrs_sums'].median()]
                        # if you want to see the medians:                    
                                # print('standard rrs median: ', standard_first['rrs_sums'].median())
                                # print('standard bsri median: ', standard_first['bsri_sums'].median())
                                # print('emotion rrs median: ', emotion_first['rrs_sums'].median())
                                # print('emotion bsri median: ', emotion_first['bsri_sums'].median())

    # standard first and emotion first indices
standard_first_trait_low = standard_first.loc[standard_first['rrs_sums'] < standard_first['rrs_sums'].median()].index
standard_first_trait_high = standard_first.loc[standard_first['rrs_sums'] > standard_first['rrs_sums'].median()].index
standard_first_state_low = standard_first.loc[standard_first['bsri_sums'] < standard_first['bsri_sums'].median()].index
standard_first_state_high = standard_first.loc[standard_first['bsri_sums'] > standard_first['bsri_sums'].median()].index

emotion_first_trait_low =  emotion_first.loc[emotion_first['rrs_sums'] <  emotion_first['rrs_sums'].median()].index
emotion_first_trait_high = emotion_first.loc[emotion_first['rrs_sums'] >  emotion_first['rrs_sums'].median()].index
emotion_first_state_low =  emotion_first.loc[emotion_first['bsri_sums'] < emotion_first['bsri_sums'].median()].index
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

# print statements if you want to see the means
# print(standard_first_trait_low_mean)
# print(standard_first_trait_high_mean)
# print(standard_first_state_low_mean)
# print(standard_first_state_high_mean)

# print(emotion_first_trait_low_mean)
# print(emotion_first_trait_high_mean)
# print(emotion_first_state_low_mean)
# print(emotion_first_state_high_mean)

###############################################################################################################

# checking ages of each rumination group NOTE: about the same all around. Doesn't seem to be a confounding variable
# print(df.iloc[standard_first_trait_low]['age_1'].mean())
# print(df.iloc[standard_first_trait_high]['age_1'].mean())
# print(df.iloc[emotion_first_trait_low]['age_1'].mean())
# print(df.iloc[emotion_first_trait_high]['age_1'].mean())

# checking gender distribution of each rumination group; NOTE: might need these values later, distribution seems skewed.
standard_first_trait_low_sex = df.iloc[standard_first_trait_low]['sex_1'];    #  print(f'total = {len(standard_first_trait_low)}'," Males: ", (standard_first_trait_low_sex == 1).sum())  # 23 total | 16 male, 7 female 
standard_first_trait_high_sex = df.iloc[standard_first_trait_high]['sex_1'];  #  print(f'total = {len(standard_first_trait_high)}', " Males: ", (standard_first_trait_high_sex == 1).sum()) # 23 total | 12 male, 11 female 
standard_first_state_low_sex = df.iloc[standard_first_state_low]['sex_1'];    #  print(f'total = {len(standard_first_state_low)}', " Males: ", (standard_first_state_low_sex == 1).sum()) # 23 total | 18 male, 5 female 
standard_first_state_high_sex = df.iloc[standard_first_state_high]['sex_1'];  #  print(f'total = {len(standard_first_state_high)}', " Males: ", (standard_first_state_high_sex == 1).sum()) # 23 total | 10 male, 13 female 
#
emotion_first_trait_low_sex = df.iloc[ emotion_first_trait_low]['sex_1'];     # print(f'total = {len(emotion_first_trait_low)}'," Males: ", (  emotion_first_trait_low_sex == 1).sum())  # 21 total | 12 male, 9 female 
emotion_first_trait_high_sex = df.iloc[emotion_first_trait_high]['sex_1'];    #print(f'total = {len( emotion_first_trait_high)}', " Males: ", (emotion_first_trait_high_sex == 1).sum()) # 21 total | 15 male, 6 female 
emotion_first_state_low_sex = df.iloc[ emotion_first_state_low]['sex_1'];     # print(f'total = {len(emotion_first_state_low)}', " Males: ", ( emotion_first_state_low_sex == 1).sum()) # 21 total | 12 male, 9 female 
emotion_first_state_high_sex = df.iloc[emotion_first_state_high]['sex_1'];    #print(f'total = {len( emotion_first_state_high)}', " Males: ", (emotion_first_state_high_sex == 1).sum()) # 21 total | 15 male, 6 female 



# Get standard deviations to plot