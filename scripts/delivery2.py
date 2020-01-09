import pandas as pd
import numpy as np
import random
random.seed(a=42)


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

