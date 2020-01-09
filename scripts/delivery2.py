import pandas as pd
import numpy as np
import datetime

import random
random.seed(a=42)

from faker import Faker
#Faker.seed(42)
fake = Faker('en_UK')
#fake.seed(42) # please toggle depending on Faker version


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
### creting census relationship table
#############


def relationships_unit(id_list):
    output = [{"Resident_ID": id_list[y],
               'Related_Resident_ID': id_list[x],
               'Relationship': random.choice([-7, -9]+[i for i in range(1,13)])} for x in range(1, len(id_list)) for y in range(0, x)]
    return output


def generate_relationships(census_table):
    output = pd.DataFrame(columns= ['Resident_ID', 'Related_Resident_ID', 'Relationship'])
    for h in census_table['Household_ID'].unique():
        id_list = census_table['Resident_ID'].loc[census_table['Household_ID'] == h].tolist()
        if len(id_list) > 1:
            output = output.append(relationships_unit(id_list))
    return output

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