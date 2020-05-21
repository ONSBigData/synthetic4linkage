import pandas as pd
import numpy as np
import random
from faker import Faker

random.seed(44)
np.random.seed(44)
Faker.seed(44)  # toggle based on faker version
fake = Faker('en_UK')
#fake.seed(44)

import datetime

#############
# generate data row by row
#############


def create_census_visitor(code_list, house_df, num=1):
    country_codes = code_list.iloc[:, 0].dropna().astype('int64')
    oa_codes = code_list.iloc[:, 3].dropna()
    output = pd.DataFrame([{"Visitor_ID": 'c'+ str(random.randint(10**18, 2**63-1)),
              'Household_ID': random.choice(range(house_df.shape[0])),
              'Visitor_First_Name': fake.first_name(),
              'Visitor_Last_Name': fake.last_name(),
              'date_time_obj': fake.date_between_dates(date_start=datetime.date(1904, 1, 1),
                                                       date_end=datetime.date(2019, 12, 31)),
              'Visitor_Sex': random.choice([1,2,-9,-7]),
              'Visitor_Address': fake.street_address() + ', ' + fake.city(),
              'Visitor_Address_Postcode': fake.postcode(),
              'Visitor_Address_Country': int(random.choice(country_codes)),
              'Visitor_Address_OA': random.choice(oa_codes),
              'Visitor_Address_UPRN': str(random.randint(0,((10**12)-1)))} for x in range(num)])
    output2 = split_DOB_visitor(output).copy()
    output2['QID'] = house_df.QID[output.Household_ID].__array__()
    output2['Household_ID'] = house_df.Household_ID[output.Household_ID].__array__()
    return output2


def create_ccs_visitor(code_list, house_df, num=1):
    country_codes = code_list.iloc[:, 0].dropna().astype('int64')
    output = pd.DataFrame([{"Visitor_ID": 'c' + str(random.randint(10 ** 18, 2**63-1)),
               'Household_ID': random.choice(range(house_df.shape[0])),
               'First_Name': fake.first_name(),
               'Last_Name': fake.last_name(),
               'date_time_obj': fake.date_between_dates(date_start=datetime.date(1904, 1, 1),
                                                        date_end=datetime.date(2019, 12, 31)),
               'Estimate_Age': random.choice([1,-8]),
               'Sex': random.choice([1, 2, -9, -7]),
               'Visitor_Address': fake.street_address() + ', ' + fake.city(),
               'Visitor_Address_Postcode': fake.postcode(),
               'Visitor_Address_Country': int(random.choice(country_codes)),
               'Visitor_Address_UPRN': str(random.randint(0, ((10 ** 12) - 1)))} for x in range(num)])
    output2 = split_DOB_visitor(output).copy()
    output2['QID'] = house_df.QID[output.Household_ID].__array__()
    output2['Household_ID'] = house_df.Household_ID[output.Household_ID].__array__()
    output2['Visitor_Age_Last_Birthday'] = output2['Visitor_Age']
    return pd.DataFrame(output2)

def split_DOB_visitor(person_index_df):
    person_index_df['Visitor_Day_Of_Birth'] = person_index_df.date_time_obj.apply(lambda x: x.day)
    person_index_df['Visitor_Month_Of_Birth'] = person_index_df.date_time_obj.apply(lambda x: x.month)
    person_index_df['Visitor_Year_Of_Birth'] = person_index_df.date_time_obj.apply(lambda x: x.year)
    person_index_df['Visitor_Age'] = person_index_df.date_time_obj.apply(calculate_age_on_31_12_2019)
    person_index_df = person_index_df.drop('date_time_obj', axis = 1)
    return person_index_df

def calculate_age_on_31_12_2019(born):
    today = datetime.date(2019, 12, 31)
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))