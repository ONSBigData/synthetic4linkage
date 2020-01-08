import pandas as pd
import numpy as np
import datetime

import random
random.seed(a=42)

from faker import Faker
Faker.seed(42)
fake = Faker('en_UK')
#fake.seed(42) # please toggle depending on Faker version

#############
# generate data row by row
#############


def create_row_resident(code_list, num=1):
  country_codes = code_list.iloc[:, 0].dropna()
  soc_codes = code_list.iloc[:, 1].dropna()
  sic_codes = code_list.iloc[:, 2].dropna()
  output = [{"Resident_ID": random.randint(10**18, ((10**19)-1)),
              'Household_ID': None,
              'CE_ID': None,
              'First_Name': fake.first_name(),
              'Middle_Name': fake.first_name(),  # we may remove some
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
              'Alternative_Address_Type':None,
              'Alternative_Address_Indicator': random.choice([1,2,3,-7,-9]),
              'Alternative_Address': fake.street_address()+', '+fake.city(),
              'Alternative_Address_Postcode': fake.postcode(),
              'Alternative_Address_Country': int(random.choice(country_codes)),
              'Alternative_Address_OA':None,
              'Alternative_Address_UPRN': random.randint(0,((10**12)-1)),
              '1_Year_Ago_Address_Type':  random.choice([1,2,3,4,5,-7,-9]),
              '1_Year_Ago_Address': fake.street_address()+', '+fake.city(),
              '1_Year_Ago_Address_Postcode': fake.postcode(),
              '1_Year_Ago_Address_Country': int(random.choice(country_codes)),
              '1_Year_Ago_Address_OA':None,
              '1_Year_Ago_Address_UPRN': random.randint(0,((10**12)-1)),
              'Workplace_Type': random.choice([1,2,3,4,-7,-9]),
              'Workplace_Address': fake.street_address()+', '+fake.city(),
              'Workplace_Address_Postcode': fake.postcode(),
              'Workplace_Address_Country': int(random.choice(country_codes)),
              'Workplace_Address_UPRN': random.randint(0,((10**12)-1)),
              'Activity Last Week':  random.choice([-9]+[x for x in range(1,8)]),
              'In_Full_Time_Education': random.choice([1,2,-7,-9]),
              'Is_HH_Term_Time_Address': random.choice([1,2,3,-7,-9]),
              'Armed Forces Indicator':  random.choice([1,2,3,-8]),
              'SIC':  int(random.choice(sic_codes)),
              'SOC':  int(random.choice(soc_codes)),
              'Census Return Method':  random.choice([1,2,3,4])} for x in range(num)]
  return output


def create_row_house(code_list, num=1):
  output = [{'Household_ID': random.randint(10**16, ((10**17)-1)),
              'Household_Address': fake.street_address()+', '+fake.city(),
              'Household_Address_Postcode': fake.postcode(),
              'Household_OA': None,
              'Household_UPRN': random.randint(0,((10**12)-1)),
              'Accomodation_Type':random.choice([1, 2, 3, 4, 5, 6, 7, -9, -7, -3]),
              'Number_Of_Usual_Residents':random.choice([1,1,1,2,2,2,2,2,3,4,5]),
              'Ownership_Type':random.choice([1, 2, 3, 4, 5, -9, -7]),
              'From_Dummy':None,
              'Any_Relationships_CCS':None} for x in range(num)]
  return output

def create_row_CE(code_list, num=1):
  output = [{'CE_ID': random.randint(10**16, ((10**17)-1)),
              'CE_Address': fake.street_address()+', '+fake.city(),
              'CE_Address_Postcode': fake.postcode(),
              'CE_OA': None,
              'CE_UPRN': random.randint(0,((10**12)-1)),
              'Nature_Of_Establishment': random.choice(list(range(1,23))+[-9, -7]),
              'Number_Of_Residents': random.randint(6,49)} for x in range(num)]
  return output


############
# date of birth from object
############

def calculate_age_on_31_12_2019(born):
    today = datetime.date(2019, 12, 31)
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def split_DOB(person_index_df):
    person_index_df['Resident_Day_Of_Birth'] = person_index_df['date_time_obj'].apply(lambda x: x.day)
    person_index_df['Resident_Month_Of_Birth'] = person_index_df['date_time_obj'].apply(lambda x: x.month)
    person_index_df['Resident_Year_Of_Birth'] = person_index_df['date_time_obj'].apply(lambda x: x.year)
    person_index_df['Resident_Age'] = person_index_df['date_time_obj'].apply(calculate_age_on_31_12_2019)
    person_index_df['full_DOB'] = person_index_df['date_time_obj'].apply(lambda x: x.strftime("%d%m%Y"))
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

def generate_house_for_person(person_index_df, house_index_df):
  list_of_ids_repeated = generate_list_of_repeated_house_ids(house_index_df)
  number_of_items = person_index_df.shape[0]
  shorter_list_of_ids_repeated = random.sample(list_of_ids_repeated, number_of_items)
  ## Now we want to nan a small percentage of values randomly so they can live in CEs
  #prop = int(shorter_list_of_ids_repeated * 0.2)
  person_index_df['Household_ID'] = shorter_list_of_ids_repeated
  return person_index_df
