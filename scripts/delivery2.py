import pandas as pd
import numpy as np
import random
from faker import Faker

random.seed(42)
np.random.seed(42)
Faker.seed(42)  # toggle based on faker version
fake = Faker('en_UK')
#fake.seed(42)

import string

# overall missingness in string variables and typo prevalence
GEN_MISS = .03
GEN_TYPO = .02

#############
### creating ccs records with new id's
#############

def CCS_scramble(df_people, df_house, df_ce, df_que):
    house_dict = {x: 'h' + str(random.randint(10 ** 16, ((10 ** 17) - 1))) for x in df_house.Household_ID}
    ce_dict = {x: 'c' + str(random.randint(10 ** 16, ((10 ** 17) - 1))) for x in df_ce['CE_ID']}
    qid_dict = {x: 'q' + str(random.randint(10 ** 15, ((10 ** 16) - 1))) for x in df_que['QID']}
    df_people2 = df_people.copy()
    df_people2['Resident_ID'] = ['c'+str(x) for x in random.sample(range(10 ** 18, 2**63-1), df_people2.shape[0])]
    df_people2 = df_people2.replace({"Household_ID": house_dict})
    df_people2 = df_people2.replace({"CE_ID": ce_dict})
    df_people2 = df_people2.replace({"QID": qid_dict})
    df_house2 = df_house.copy().replace({"Household_ID": house_dict})
    df_house2 = df_house2.replace({"QID": qid_dict})
    df_ce2 = df_ce.copy().replace({"CE_ID": ce_dict})
    df_ce2 = df_ce2.replace({"QID": qid_dict})
    df_que2 = df_que.copy().replace({"QID": qid_dict})
    return reformat_ccs_people(df_people2), reformat_ccs_house(df_house2, df_que2), df_ce2, df_que2

def reformat_ccs_people(df_people):
    df_people = df_people.drop(['1_Year_Ago_Address', '1_Year_Ago_Address_Country','1_Year_Ago_Address_OA',
                                '1_Year_Ago_Address_Postcode', '1_Year_Ago_Address_Type', '1_Year_Ago_Address_UPRN',
                                'Armed Forces Indicator', 'Census Return Method', 'Country_Of_Birth',
                                'Country_Of_Birth_UK', 'Marital_Status', 'SIC','SOC',
                                'Workplace_Address', 'Workplace_Address_Country',
                                'Workplace_Address_Postcode', 'Workplace_Address_UPRN',
                                'Workplace_Type'                                ], axis=1)

    df_people = df_people.rename(columns={"Activity_Last_Week":"Activity_Last_Week_For_CCS",
                                        'Ethnic Group (five category)':'Ethnic Group (five category - CCS)',
                                        'Ethnicity: Tick Box':'Ethnicity: Tick Box (CCS)',
                                        'Marital_Status_CCS':'Marital_Status'   })
    return df_people


def reformat_ccs_house(df_house, df_quest):
    df_house = df_house.rename(columns={"Any_Relationship_CCS": "Any_Relationship",
                                        'Number_Of_Residents': 'Resident_Count'})
    # have to retrieve address from df_quest!
    address_dict = {df_quest.QID[x]:df_quest.Address[x]  for x in range(df_quest.shape[0])}
    df_house['Census_Address'] = df_house['QID'].map(address_dict)
    postcode_dict = {df_quest.QID[x]: df_quest.Address_Postcode[x] for x in range(df_quest.shape[0])}
    df_house['Census_Address_Postcode'] = df_house['QID'].map(postcode_dict)
    uprn_dict = {df_quest.QID[x]:df_quest.UPRN[x]  for x in range(df_quest.shape[0])}
    df_house['Census_Address_UPRN'] = df_house['QID'].map(uprn_dict)
    area_dict = {df_quest.QID[x]: df_quest.Output_Area[x] for x in range(df_quest.shape[0])}
    df_house['Census_Address_Output_Area'] = df_house['QID'].map(area_dict)

    df_house['Census_Address_Country'] = [random.choice( range(100, 1000))  for x in range(df_house.shape[0])]
    df_house['Census_Address_Indicator'] = random.sample(  range(0,((10**12)-1)) , df_house.shape[0])
    df_house['Resident_Count_Verify'] = df_house['Resident_Count']
    df_house['Census_Address_Count'] = [random.choice(range(0,99)) for x in range(df_house.shape[0])]
    df_house['Census_Address_Count_Verify'] = df_house['Census_Address_Count']
    df_house['Ownership_Type'] = [random.choice([1,2,3,4,5,-7,-9]) for x in  range(df_house.shape[0])]
    return df_house


def reformat_ccs_ce(df_ce):
#    df_ce = df_ce.drop('CE_UPRN', axis =1)
    return df_ce


def lose_records(df_people, df_house, df_ce, df_quest, prop = .06, prop2= .03, keep = False):
    subset_house = random.sample(df_house.Household_ID.tolist(), round(df_house.shape[0]*(1-prop2)))
    subset_ce = random.sample(df_ce.CE_ID.tolist(), round(df_ce.shape[0] *(1- prop2)))
    new_people = df_people.loc[(df_people.Household_ID. isin(subset_house)) | (df_people.CE_ID.isin(subset_ce))]\
        .sample(frac = 1 - prop, replace=False, random_state=42).copy()
    if keep:
        new_house = df_house.copy()
        new_ce = df_ce.copy()
        new_quest = df_quest.copy()
        # new_house.loc[(df_house.Household_ID.isin(subset_house)), 'From_Dummy'] = 1
    else:
        new_house = df_house.loc[df_house.Household_ID.isin(subset_house)].copy()
        new_ce = df_ce.loc[df_ce.CE_ID.isin(subset_ce)].copy()
        new_quest = df_quest.loc[df_quest.QID.isin(new_people.QID)].copy()
    return new_people, new_house, new_ce, new_quest


#############
### Extra functionality
#############

def common_surnames_in_house_(df):
    # modifying a subset - not quite right use of loc
    count = 0
    for count in range(df.shape[0] - 1):
        random_num = random.choice([1, 1, 0])  # one in three chnace of repeating last name
        if ((df['Household_ID'].iloc[count] == df['Household_ID'].iloc[count + 1]) and (
            df['Household_ID'].iloc[count] != np.nan) and (random_num == 1)):
            df['Last_Name'].iloc[count + 1] = df['Last_Name'].iloc[count]
        count = count + 1
    return df


def common_surnames_in_house(df):
    house_list = df.Household_ID.dropna().unique().tolist()
    subset = random.sample(house_list, round(len(house_list)/2))
    for h in subset:
        df.loc[df.Household_ID == h, 'Last_Name'] = fake.last_name()
    return df

def common_firstnames_in_house(df):
    house_list = df.Household_ID.dropna().unique().tolist()
    subset = random.sample(house_list, round(len(house_list)/2))
    msk = ([True, True, False, False]*len(house_list)*2)[0:df.shape[0]]
    # msk to choose only some of the family members to share first name
    for h in subset:
        df.loc[(df.Household_ID == h) & msk, 'First_Name'] = fake.first_name()
    return df


def create_duplicates(df, num=50, change_house=False, twin=False):
    subset = df.iloc[random.sample(range(df.shape[0]), num)].copy().reindex()
    subset['Resident_ID'] = ['c'+ str(x) for x in random.sample(range(10 ** 18, ((10 ** 19) - 1)), num)]
    if twin:
        subset['First_Name'] = random.sample(df.First_Name.tolist(), num)
    if change_house:
        sameseed = random.randint(0, 10^12)
        random.seed(sameseed)
        subset['Household_ID'] = random.sample(df.Household_ID[df.Household_ID != ''].tolist(), num)
        random.seed(sameseed)
        subset['QID'] = random.sample(df.QID[df.Household_ID != ''].tolist(), num)
        subset['CE_ID'] = None
    return df.append(subset)


###############
# pertubations as listed in delivery 2.1
###############

def simple_typos(word):
    ix = random.choice(range(len(word)))
    new_word = ''.join([word[w] if w != ix else random.choice(string.ascii_letters) for w in range(len(word))])
    return new_word


def pertubation21(ccs_people):
    # for each variable, first we replace some completely

    subset = np.random.choice([True, False], size=ccs_people.shape[0], p=[.20, 1-.20])
    ccs_people.loc[subset,'First_Name'] = random.sample(ccs_people.First_Name.tolist(), sum(subset))

    subset = np.random.choice([True, False], size=ccs_people.shape[0], p=[.20, 1-.20])
    ccs_people.loc[subset,'Last_Name'] = random.sample(ccs_people.Last_Name.tolist(), sum(subset))

    subset = np.random.choice([True, False], size=ccs_people.shape[0], p=[.02, 1-.02])
    ccs_people.loc[subset,'Sex'] = random.sample(ccs_people.Sex.tolist(), sum(subset))

    subset = np.random.choice([True, False], size=ccs_people.shape[0], p=[.15, 1-.15])
    ccs_people.loc[subset,'Resident_Day_Of_Birth'] = random.sample(ccs_people.Resident_Day_Of_Birth.tolist(), sum(subset))

    subset = np.random.choice([True, False], size=ccs_people.shape[0], p=[.13, 1-.13])
    ccs_people.loc[subset,'Resident_Month_Of_Birth'] = random.sample(ccs_people.Resident_Month_Of_Birth.tolist(), sum(subset))

    subset = np.random.choice([True, False], size=ccs_people.shape[0], p=[.13, 1-.13])
    ccs_people.loc[subset,'Resident_Year_Of_Birth'] = random.sample(ccs_people.Resident_Year_Of_Birth.tolist(), sum(subset))

    return ccs_people

def add_missing_codes_to_some(ccs_people):
    # introduce missingness and typos on both sides

    subset = np.random.choice([True, False], size=ccs_people.shape[0], p=[3*GEN_TYPO, 1-3*GEN_TYPO])
    ccs_people.loc[subset,'First_Name'] = ccs_people.loc[subset,'First_Name'].transform(simple_typos)
    subset = np.random.choice([True, False], size=ccs_people.shape[0], p=[GEN_MISS, 1-GEN_MISS])
    ccs_people.loc[subset,'First_Name'] = -9

    subset = np.random.choice([True, False], size=ccs_people.shape[0], p=[3*GEN_TYPO, 1-3*GEN_TYPO])
    ccs_people.loc[subset,'Last_Name'] = ccs_people.loc[subset,'Last_Name'].transform(simple_typos)
    subset = np.random.choice([True, False], size=ccs_people.shape[0], p=[GEN_MISS, 1 - GEN_MISS])
    ccs_people.loc[subset, 'Last_Name'] = -9

    subset = np.random.choice([True, False], size=ccs_people.shape[0], p=[GEN_MISS, 1 - GEN_MISS])
    ccs_people.loc[subset, 'Resident_Day_Of_Birth'] = -9
    subset = np.random.choice([True, False], size=ccs_people.shape[0], p=[GEN_MISS, 1 - GEN_MISS])
    ccs_people.loc[subset, 'Resident_Month_Of_Birth'] = -9
    subset = np.random.choice([True, False], size=ccs_people.shape[0], p=[GEN_MISS, 1 - GEN_MISS])
    ccs_people.loc[subset, 'Resident_Year_Of_Birth'] = -9

    return ccs_people

def perturb_geography(ccs_house):
    #swaping houses for 50 (2%) of households
    subset = np.random.choice([True, False], size=ccs_house.shape[0], p=[.02, 1 - .02])
    ccs_house.loc[subset, 'QID'] = random.sample(ccs_house.loc[subset, 'QID'].tolist(), sum(subset))

    #  adding errors
    subset = np.random.choice([True, False], size=ccs_house.shape[0], p=[.02, 1-.02])
    ccs_house.loc[subset,'Address_Postcode'] = random.sample(ccs_house.Address_Postcode.tolist(), sum(subset))
    subset = np.random.choice([True, False], size=ccs_house.shape[0], p=[.02, 1 - .02])
    ccs_house.loc[subset, 'Address'] = random.sample(ccs_house.Address.tolist(),sum(subset))

    return ccs_house

def add_missing_codes_to_address(ccs_house):
    #introduce missingness and typos on both sides
    subset = np.random.choice([True, False], size=ccs_house.shape[0], p=[GEN_TYPO, 1-GEN_TYPO])
    ccs_house.loc[subset,'Address_Postcode'] = ccs_house.loc[subset,'Address_Postcode'].transform(simple_typos)
    subset = np.random.choice([True, False], size=ccs_house.shape[0], p=[GEN_MISS, 1-GEN_MISS])
    ccs_house.loc[subset,'Address_Postcode'] = -9

    subset = np.random.choice([True, False], size=ccs_house.shape[0], p=[GEN_TYPO, 1 - GEN_TYPO])
    ccs_house.loc[subset, 'Address'] = ccs_house.loc[subset, 'Address'].transform(simple_typos)
    subset = np.random.choice([True, False], size=ccs_house.shape[0], p=[GEN_MISS, 1 - GEN_MISS])
    ccs_house.loc[subset, 'Address'] = -9

    return ccs_house