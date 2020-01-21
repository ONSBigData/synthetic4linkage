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


def create_census_visitor(code_list, house_num, num=1):
    country_codes = code_list.iloc[:, 0].dropna().astype('int64')
    oa_codes = code_list.iloc[:, 3].dropna()
    output = [{"Visitor_ID": random.randint(10**18, ((10**19)-1)),
              'Household_ID': random.choice(house_num),
              'Visitor_First_Name': fake.first_name(),
              'Visitor_Last_Name': fake.last_name(),
              'date_time_obj': fake.date_between_dates(date_start=datetime.date(1904, 1, 1),
                                                       date_end=datetime.date(2019, 12, 31)),
              'Visitor_Sex': random.choice([1,2,-9,-7]),
              'Visitor_Address': fake.street_address()+', '+fake.city(),
              'Visitor_Address_Postcode': fake.postcode(),
              'Visitor_Address_Country': int(random.choice(country_codes)),
              'Visitor_Address_OA': random.choice(oa_codes),
              'Alternative_Address_UPRN': random.randint(0,((10**12)-1))}]
    output2 = split_DOB_visitor(pd.DataFrame(output))
    return output2


def create_ccs_visitor(code_list, house_num, num=1):
    country_codes = code_list.iloc[:, 0].dropna().astype('int64')
    output = [{"Visitor_ID": random.randint(10 ** 18, ((10 ** 19) - 1)),
               'Household_ID': random.choice(house_num),
               'First_Name': fake.first_name(),
               'Last_Name': fake.last_name(),
               'date_time_obj': fake.date_between_dates(date_start=datetime.date(1904, 1, 1),
                                                        date_end=datetime.date(2019, 12, 31)),
               'Estimate_Age': random.choice([1,-8]),
               'Sex': random.choice([1, 2, -9, -7]),
               'Visitor_Address': fake.street_address() + ', ' + fake.city(),
               'Visitor_Address_Postcode': fake.postcode(),
               'Visitor_Address_Country': int(random.choice(country_codes)),
               'Alternative_Address_UPRN': random.randint(0, ((10 ** 12) - 1))}]
    output2 = split_DOB_visitor(pd.DataFrame(output))
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