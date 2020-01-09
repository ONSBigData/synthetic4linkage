import pandas as pd
import numpy as np
import random
random.seed(a=42)


#############
### creating ccs records with new id's
#############

def CCS_scramble(df_people, df_house, df_ce):
    house_dict = {x: random.randint(10 ** 16, ((10 ** 17) - 1)) for x in df_house['Household_ID']}
    ce_dict = {x:random.randint(10 ** 16, ((10 ** 17) - 1)) for x in df_ce['CE_ID']}
    df_people['Resident_ID'] = random.sample(range(10 ** 16, ((10 ** 17) - 1)), df_people.shape[0])
    df_people = df_people.replace({"Household_ID": house_dict})
    df_people = df_people.replace({"CE_ID": ce_dict})
    df_house = df_house.replace({"Household_ID": house_dict})
    df_ce = df_ce.replace({"CE_ID": ce_dict})
    return df_people, df_house, df_ce


#############
### Extra functionality
#############

def common_surnames_in_house(df):
    count = 0
    for count in range(df.shape[0] - 1):
        random_num = random.choice([1, 1, 0])  # one in three chnace of repeating last name
        if ((df['Household_ID'].iloc[count] == df['Household_ID'].iloc[count + 1]) and (
            df['Household_ID'].iloc[count] != np.nan) and (random_num == 1)):
            df['Last_Name'].iloc[count + 1] = df['Last_Name'].iloc[count]
        count = count + 1
    return df