import pandas as pd
import numpy as np
import random
from faker import Faker

random.seed(43)
np.random.seed(43)
#Faker.seed(43)  # toggle based on faker version
fake = Faker('en_UK')
fake.seed(43)

#############
### creting census relationship table
#############


def relationships_unit(id_list):
    output = [{"Resident_ID": id_list[y],
               'Related_Resident_ID': id_list[x],
               'Relationship': random.choice([-7, -9]+[i for i in range(1,13)])}
              for x in range(1, len(id_list)) for y in range(0, x)]
    return output


def generate_relationships(census_table):
    output = pd.DataFrame(columns= ['Resident_ID', 'Related_Resident_ID', 'Relationship'])
    for h in census_table.Household_ID.unique():
        id_list = census_table.loc[census_table.Household_ID == h, 'Resident_ID'].tolist()
        if ((len(id_list) > 1) & (h!='')):
            output = output.append(relationships_unit(id_list))
    return output


def add_passport(census_table, passport_file = '../data/other_passport.csv'):
    code_passport = pd.read_csv(passport_file, header = None, dtype = {0 : str})[0]
    output = pd.DataFrame([{'Passport': random.choice(['-7', '-9', '1000', '1100', '1010', '1110', '0100', '0110', '0010', '0001']),
               'Other_Passport_Held': random.choice(['-7', '-9'])}  for x in  range(census_table.shape[0])])
    output.loc[output.Passport.isin(['1010', '1110', '0110', '0010']), 'Other_Passport_Held'] =\
        [random.choice(['-7', '-9']+ code_passport.tolist()) for x in range(sum(output.Passport.isin(['1010', '1110', '0110', '0010'])))]
    census_table['Passport'] = output.Passport
    census_table['Other_Passport_Held'] = output.Other_Passport_Held
    return census_table