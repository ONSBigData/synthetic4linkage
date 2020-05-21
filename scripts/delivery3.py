import pandas as pd
import numpy as np
import random
from faker import Faker

random.seed(43)
np.random.seed(43)
Faker.seed(43)  # toggle based on faker version
fake = Faker('en_UK')
#fake.seed(43)

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


def add_passport(census_table, passport_file = 'data/other_passport.csv'):
    code_passport = pd.read_csv(passport_file, header = None, dtype = {0 : str})[0]
    output = pd.DataFrame([{'Passport': random.choice(['-7', '-9', '1000', '1000', '1000', '1100', '1010', '1110', '0100', '0110', '0010', '0001']),
               'Other_Passport_Held': random.choice(['-7', '-9'])}  for x in  range(census_table.shape[0])])
    output.loc[output.Passport.isin(['1010', '1110', '0110', '0010']), 'Other_Passport_Held'] =\
        [random.choice(['-7', '-9']+ code_passport.tolist()) for x in range(sum(output.Passport.isin(['1010', '1110', '0110', '0010'])))]
    census_table['Passport'] = output.Passport
    census_table['Other_Passport_Held'] = output.Other_Passport_Held
    return census_table

def assign_census_address_var(house_id):
  if (house_id == ''):
    residence_type = 2
  else: residence_type =  1
  return residence_type

def add_ccs_house_type(ccs_table):
    output = pd.DataFrame([{'Census_Address_Accommodation_Type': random.choice([1, 2, 3, 4, 5, 6, 7, -9, -7]),
        'Census_Address_Ownership_Type': random.choice([1, 2, 3, 4, 5, -9, -7]),
        'Any_Relationship': random.choice([1, 2, -9,])}  for x in  range(ccs_table.shape[0])])
    ccs_table['Census_Address_Accommodation_Type'] = output.Census_Address_Accommodation_Type
    ccs_table['Census_Address_Ownership_Type'] = output.Census_Address_Ownership_Type
    ccs_table['Any_Relationship'] = output.Any_Relationship
    subset = np.random.choice([True, False], size=ccs_table.shape[0], p=[.10, 1 - .10])

    ccs_table.loc[subset, 'Accommodation_Type'] =  -9
    ccs_table.loc[subset, 'Ownership_Type'] = -9
    ccs_table.loc[~subset, 'Census_Address'] = -9
    ccs_table.loc[~subset, 'Census_Address_Postcode'] = -9
    ccs_table.loc[~subset, 'Census_Address_Country'] = -9
    ccs_table.loc[~subset, 'Census_Address_Indicator'] = -9
    ccs_table.loc[~subset, 'Census_Address_UPRN'] = -9
    ccs_table.loc[~subset, 'Census_Address_Output_Area'] = -9
    ccs_table.loc[~subset, 'Census_Address_Count'] = -9
    ccs_table.loc[~subset, 'Census_Address_Count_Verify'] = -9
    ccs_table.loc[~subset, 'Census_Address_Ownership_Type'] = -9
    ccs_table.loc[~subset, 'Census_Address_Accommodation_Type'] = -9

    ccs_table = ccs_table.drop('From_Dummy', axis = 1)

    return ccs_table