import pandas as pd
import numpy as np
import random
random.seed(a=42)

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
    for h in census_table['Household_ID'].unique():
        id_list = census_table['Resident_ID'].loc[census_table['Household_ID'] == h].tolist()
        if len(id_list) > 1:
            output = output.append(relationships_unit(id_list))
    return output