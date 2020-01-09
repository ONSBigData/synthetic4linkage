import pandas as pd
import numpy as np
import random
random.seed(a=42)
from faker import Faker
#Faker.seed(42)
fake = Faker('en_UK')
fake.seed(42)


#############
### creating ccs records with new id's
#############

def CCS_scramble(df_people, df_house, df_ce):
    house_dict = {x: random.randint(10 ** 16, ((10 ** 17) - 1)) for x in df_house.Household_ID}
    ce_dict = {x:random.randint(10 ** 16, ((10 ** 17) - 1)) for x in df_ce['CE_ID']}
    df_people['Resident_ID'] = random.sample(range(10 ** 16, ((10 ** 17) - 1)), df_people.shape[0])
    df_people = df_people.replace({"Household_ID": house_dict})
    df_people = df_people.replace({"CE_ID": ce_dict})
    df_house = df_house.replace({"Household_ID": house_dict})
    df_ce = df_ce.replace({"CE_ID": ce_dict})
    return df_people, df_house, df_ce

def lose_records(df_people, df_house, df_ce, prop = .06, prop2= .03, keep = False):
    subset_house = random.sample(df_house.Household_ID.tolist(), round(df_house.shape[0]*(1-prop2)))
    subset_ce = random.sample(df_ce.CE_ID.tolist(), round(df_ce.shape[0] *(1- prop2)))
    new_people = df_people.loc[(df_people.Household_ID. isin(subset_house)) | (df_people.CE_ID.isin(subset_ce))].sample(frac = 1 - prop, replace=False, random_state=42)
    if keep:
        new_house = df_house
        new_ce = df_ce
        new_house.loc[(df_house.Household_ID.isin(subset_house)), 'From_Dummy'] = 1
    else:
        new_house = df_house.loc[df_house.Household_ID.isin(subset_house)]
        new_ce = df_ce.loc[df_ce.CE_ID.isin(subset_ce)]
    return new_people, new_house, new_ce


#############
### Extra functionality
#############

def common_surnames_in_house_(df):
    # modifying a subset - not quite right use of loc
    count = 0
    for count in range(df.shape[0] - 1):
        random_num = random.choice([1, 1, 0])  # one in three chnace of repeating last name
        if ((df['Household_ID'].iloc[count] == df['Household_ID'].iloc[count + 1]) and (
            df['Household_ID'].iloc[count] != np.nan) and (random_num == 1)):
            df['Last_Name'].iloc[count + 1] = df['Last_Name'].iloc[count]
        count = count + 1
    return df


def common_surnames_in_house(df):
    house_list = df.Household_ID.dropna().unique().tolist()
    subset = random.sample(house_list, round(len(house_list)/2))
    for h in subset:
        df.loc[df.Household_ID == h, 'Last_Name'] = fake.last_name()
    return df

def common_firstnames_in_house(df):
    house_list = df.Household_ID.dropna().unique().tolist()
    subset = random.sample(house_list, round(len(house_list)/2))
    msk = ([True, True, False, False]*len(house_list)*2)[0:df.shape[0]]
    # msk to choose only some of the family members to share first name
    for h in subset:
        df.loc[(df.Household_ID == h) & msk, 'First_Name'] = fake.first_name()
    return df


def create_duplicates(df, num=50, change_house=False, twin=False):
    subset = df.iloc[random.sample(range(df.shape[0]), num)].copy()
    subset['Resident_ID'] = random.sample(range(10 ** 18, ((10 ** 19) - 1)), num)
    if twin:
        subset['First_Name'] = random.sample(df.First_Name.tolist(), num)
    if change_house:
        subset['Household_ID'] = random.sample(df.Household_ID.dropna().tolist(), num)
        subset['CE_ID'] = None
    return df.append(subset)