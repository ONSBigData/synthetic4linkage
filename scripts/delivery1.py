import pandas as pd
import numpy as np
import datetime

import random
random.seed(a=42)

from faker import Faker
#Faker.seed(42)
fake = Faker('en_UK')
fake.seed(42) # please toggle depending on Faker version

#############
# generate data row by row
#############


def create_row_resident(code_list, num=1):
    country_codes = code_list.iloc[:, 0].dropna()
    soc_codes = code_list.iloc[:, 1].dropna()
    sic_codes = code_list.iloc[:, 2].dropna()
    oa_codes = code_list.iloc[:,3].dropna()
    output = [{"Resident_ID": str(random.randint(10**18, ((10**19)-1))),
              'Household_ID': None,
              'CE_ID': None,
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
  output = [{'Household_ID': str(random.randint(10**16, ((10**17)-1))),
              'Household_Address': fake.street_address()+', '+fake.city(),
              'Household_Address_Postcode': fake.postcode(),
              'Household_OA': random.choice(oa_codes),
              'Household_UPRN': str(random.randint(0,((10**12)-1))),
              'Accomodation_Type':random.choice([1, 2, 3, 4, 5, 6, 7, -9, -7, -3]),
              'Number_Of_Usual_Residents':random.choice([1,1,1,2,2,2,2,2,3,4,5]),
              'Ownership_Type':random.choice([1, 2, 3, 4, 5, -9, -7]),
              'From_Dummy': 0,
              'Any_Relationships_CCS':None} for x in range(num)]
  return pd.DataFrame(output)

def create_row_CE(code_list, num=1):
  oa_codes = code_list.iloc[:, 3].dropna()
  output = [{'CE_ID': str(random.randint(10**16, ((10**17)-1))),
              'CE_Address': fake.street_address()+', '+fake.city(),
              'CE_Address_Postcode': fake.postcode(),
              'CE_OA': random.choice(oa_codes),
              'CE_UPRN': str(random.randint(0,((10**12)-1))),
              'Nature_Of_Establishment': random.choice(list(range(1,23))+[-9, -7]),
              'Number_Of_Residents': random.randint(6,49)} for x in range(num)]
  return pd.DataFrame(output)


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


def generate_list_of_repeated_house_ids(df, id_column_name = 'Household_ID', num_column_name = 'Number_Of_Usual_Residents'):
  # first create a giant list where every house id 
  list_of_ids_repeated = []
  for house_id, no_residents in zip(df[id_column_name],df[num_column_name]): 
    id_repeated = [house_id for i in range(no_residents)]
    list_of_ids_repeated = list_of_ids_repeated + id_repeated
  return list_of_ids_repeated


def generate_house_for_person(person_index_df, house_index_df, ce_index_df):
  # generate list of all house ids to use
  list_of_ids_repeated = generate_list_of_repeated_house_ids(house_index_df)
  # total number of house ids to be assigned
  length_of_list_of_items_repeated = len(list_of_ids_repeated)
  # total number of items we need in any one column
  number_of_items = person_index_df.shape[0]
  # the nans we need to tag on the end to fill the column
  ## Now we want to nan a small percentage of values randomly so they can live in CEs
  how_many_nans_do_we_need = number_of_items - length_of_list_of_items_repeated
  #prop = int(shorter_list_of_ids_repeated * 0.2)
  list_of_nans = ['' for x in range(how_many_nans_do_we_need)]
  # all house id column values 
  list_of_ids_repeated_correct_length = list_of_ids_repeated + list_of_nans
  # put it in the df 
  person_index_df['Household_ID'] = list_of_ids_repeated_correct_length
  ##########
  ### CE_ID column
  ##########
  # STEP 1: Generate list of nans same length as list of house ids
  first_ce_nans = ['' for x in range(length_of_list_of_items_repeated)]
  # STEP 2: Generate long list of repeated CE ids
  list_of_ce_ids_repeated = generate_list_of_repeated_house_ids(ce_index_df, id_column_name = 'CE_ID', num_column_name = 'Number_Of_Residents')
  length_of_list_of_ce_ids_repeated = len(list_of_ce_ids_repeated)
  # STEP 3: find number of extra nans needed to fill the column
  how_many_nans_for_last_ce = number_of_items - (length_of_list_of_items_repeated+length_of_list_of_ce_ids_repeated)
  last_ce_nans = ['' for x in range(how_many_nans_for_last_ce)]
  # STEP 4: Put all the list together
  ce_id_list = first_ce_nans + list_of_ce_ids_repeated + last_ce_nans
  person_index_df['CE_ID'] = ce_id_list
  person_index_df = person_index_df.dropna(how = 'all', subset = ['Household_ID','CE_ID'])
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
                  'Household_UPRN': "UPRN",
                  'Number_Of_Usual_Residents': "Number_Of_Residents"}
  df_people.rename(rename_dict)
  return df_people
