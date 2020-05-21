import pandas as pd
import numpy as np
import random
from faker import Faker

random.seed(41)
np.random.seed(41)
Faker.seed(41)  # toggle based on faker version
fake = Faker('en_UK')
#fake.seed(41)

import datetime

#############
# generate data row by row
#############


def create_row_resident(code_list, num=1):
    country_codes = code_list.iloc[:, 0].dropna()
    soc_codes = code_list.iloc[:, 1].dropna()
    sic_codes = code_list.iloc[:, 2].dropna()
    oa_codes = code_list.iloc[:,3].dropna()
    output = [{"Resident_ID": 'c'+str(random.randint(10**18, 2**63-1)),
              'Household_ID': None,
              'CE_ID': None,
              'QID' : None,
              'First_Name': fake.first_name(),
              'Middle_Name': '-9' if random.random() < .5 else fake.first_name(),
              'Last_Name': fake.last_name(),
              'date_time_obj': fake.date_between_dates(date_start=datetime.date(1904, 1, 1),
                                                       date_end=datetime.date(2019, 12, 31)),
              'Country_Of_Birth': int(random.choice(country_codes)),
              'Country_Of_Birth_UK': random.choice([1,2,-9,-7]),
              'Sex': random.choice([1,2,-9,-7]),
              'Marital_Status': random.choice([-9,-7]+[x for x in range(1,18)]),
              'Marital_Status_CCS': random.choice([-9,-7]+[x for x in range(1,10)]),
              'Residence_Type':  random.choice([1,2]),
              'Ethnic Group (five category)': random.choice([1,2,3,4,5,-9]),
              'Ethnicity: Tick Box': random.choice([-9]+[x for x in range(1,20)]),
              'Alternative_Address_Type': ''.join([ str(random.choice([0,1])) for x in range(0,8)]),
              'Alternative_Address_Indicator': random.choice([1,2,3,-7,-9]),
              'Alternative_Address': fake.street_address()+', '+fake.city(),
              'Alternative_Address_Postcode': fake.postcode(),
              'Alternative_Address_Country': int(random.choice(country_codes)),
              'Alternative_Address_OA': random.choice(oa_codes),
              'Alternative_Address_UPRN': str(random.randint(0,((10**12)-1))),
              '1_Year_Ago_Address_Type':  random.choice([1,2,3,4,5,-7,-9]),
              '1_Year_Ago_Address': fake.street_address()+', '+fake.city(),
              '1_Year_Ago_Address_Postcode': fake.postcode(),
              '1_Year_Ago_Address_Country': int(random.choice(country_codes)),
              '1_Year_Ago_Address_OA': random.choice(oa_codes),
              '1_Year_Ago_Address_UPRN': str(random.randint(0,((10**12)-1))),
              'Workplace_Type': random.choice([1,2,3,4,-7,-9]),
              'Workplace_Address': fake.street_address()+', '+fake.city(),
              'Workplace_Address_Postcode': fake.postcode(),
              'Workplace_Address_Country': int(random.choice(country_codes)),
              'Workplace_Address_UPRN': str(random.randint(0,((10**12)-1))),
              'Activity Last Week':  random.choice([-9]+[x for x in range(1,8)]),
              'In_Full_Time_Education': random.choice([1,2,-7,-9]),
              'Is_HH_Term_Time_Address': random.choice([1,2,3,-7,-9]),
              'Armed Forces Indicator':  random.choice([1,2,3,-8]),
              'SIC':  int(random.choice(sic_codes)),
              'SOC':  int(random.choice(soc_codes)),
              'Census Return Method':  random.choice([1,2,3,4])} for y in range(num)]
    output2 = split_DOB(pd.DataFrame(output))
    output2['Cluster_num'] = range(num)
    return output2

def create_row_house(code_list, num=1):
  oa_codes = code_list.iloc[:, 3].dropna()
  output = [{'Household_ID': 'h' + str(random.randint(10**16, ((10**17)-1))),
              'QID': 'q' + str(random.randint(10**15, ((10**16)-1))),
              'Accommodation_Type':random.choice([1, 2, 3, 4, 5, 6, 7, -9, -7, -3]),
              'Number_Of_Residents':random.choice([1,1,1,2,2,2,2,2,3,4,5]),
              'Ownership_Type':random.choice([1, 2, 3, 4, 5, -9, -7]),
              'From_Dummy': 0,
              'Any_Relationships_CCS':None} for x in range(num)]
  return pd.DataFrame(output)

def create_row_CE(code_list, num=1):
  oa_codes = code_list.iloc[:, 3].dropna()
  output = [{'CE_ID': 'e' + str(random.randint(10**16, ((10**17)-1))),
              'QID': 'q' + str(random.randint(10**15, ((10**16)-1))),
              'Nature_Of_Establishment': random.choice(list(range(1,23))+[-9, -7]),
              'Number_Of_Residents': random.randint(6,49)} for x in range(num)]
  return pd.DataFrame(output)


def create_row_questionnaire(code_list, QIDs=None):
  num = len(QIDs)
  oa_codes = code_list.iloc[:, 3].dropna()
  output = pd.DataFrame( [{'Address':fake.street_address()+'\n'+fake.city(),
              'Address_Postcode': fake.postcode(),
              'Output_Area': random.choice(oa_codes),
              'UPRN': str(random.randint(0,((10**12)-1)))} for x in range(num)])
  output['Address_Raw'] = output['Address'] + '\n' + output['Address_Postcode']
  output['QID'] = QIDs
  return output

############
# date of birth from object
############

def calculate_age_on_31_12_2019(born):
    today = datetime.date(2019, 12, 31)
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def split_DOB(person_index_df):
    person_index_df['Resident_Day_Of_Birth'] = person_index_df.date_time_obj.apply(lambda x: x.day)
    person_index_df['Resident_Month_Of_Birth'] = person_index_df.date_time_obj.apply(lambda x: x.month)
    person_index_df['Resident_Year_Of_Birth'] = person_index_df.date_time_obj.apply(lambda x: x.year)
    person_index_df['Resident_Age'] = person_index_df.date_time_obj.apply(calculate_age_on_31_12_2019)
    person_index_df['full_DOB'] = person_index_df.date_time_obj.apply(lambda x: x.strftime("%d%m%Y"))
    person_index_df = person_index_df.drop('date_time_obj', axis = 1)
    return person_index_df



#########
## Asigning houses to people 
##########

# assign house id to resident id randomly 
# unless the house id has been used more than 
# the number of times in total number of usual residents 


# create a list of random house ids where the number of times the ID apears 
# is less than or equal to the number of residents


def generate_list_of_repeated_house_rows(df, num_column_name = 'Number_Of_Residents'):
  # first create a giant list where every house id 
  list_of_ids_repeated = [ row_num  for row_num in range(df.shape[0]) for i in range(df[num_column_name][row_num])]
  return list_of_ids_repeated


def generate_house_for_person(person_index_df, house_index_df, ce_index_df):
  # generate list of all house ids to use
  list_of_rows_repeated = generate_list_of_repeated_house_rows(house_index_df)
  # the nans we need to tag on the end to fill the column
  num_nans_needed = person_index_df.shape[0] - len(list_of_rows_repeated)
  # put it in the df 
  person_index_df['Household_ID'] = [x for x in house_index_df['Household_ID'][list_of_rows_repeated]]+['' for x in range(num_nans_needed)]
  ##########
  ### CE_ID column
  ##########
  # STEP 1: Generate list of nans same length as list of house ids
  first_ce_nans = ['' for x in range(len(list_of_rows_repeated))]
  # STEP 2: Generate long list of repeated CE ids
  list_of_ces_repeated = generate_list_of_repeated_house_rows(ce_index_df, num_column_name = 'Number_Of_Residents')
  # STEP 3: find number of extra nans needed to fill the column
  last_ce_nans = ['' for x in range(person_index_df.shape[0] - len(list_of_rows_repeated) -len(list_of_ces_repeated))]
  # STEP 4: Put all the list together
  person_index_df['CE_ID'] = first_ce_nans + [x for x in ce_index_df['CE_ID'][list_of_ces_repeated]] + last_ce_nans
  person_index_df['QID'] = [x for x in house_index_df['QID'][list_of_rows_repeated]] + \
                           [x for x in ce_index_df['QID'][list_of_ces_repeated]] + last_ce_nans
  person_index_df = person_index_df.dropna(subset = ['QID'])
  return person_index_df

###
# Properly assign residence type column
###

def assign_residence_type(house_id):
  if (house_id == ''):
    residence_type = 2
  else: residence_type =  1
  return residence_type



########
### Joining address
##########
def join_to_populate_addresses(df_people, df_houses):
  df_people = df_people.join(df_houses, on = 'Household_ID', how = 'left', rsuffix = 'house')
  df_people.drop('Household_IDhouse', axis = 1)
  rename_dict = {'Household_Address': "Address", 
                  'Household_Address_Postcode': "Address_Postcode",
                  'Household_OA': "OA", 
                  'Household_UPRN': "UPRN"}
  df_people.rename(rename_dict)
  return df_people
