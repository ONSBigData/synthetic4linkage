import pandas as pd
from delivery1 import *
from delivery2 import *
from delivery3 import *
from delivery4 import *

code_list = pd.read_csv('../data/possible_codes.csv')


###
# Resident, house and CE indices
###
person_index_df = create_row_resident(num=30000, code_list = code_list)
house_index_df = create_row_house(num=5000, code_list =  code_list)
ce_index_df = create_row_CE(num=500, code_list =  code_list)


#######
### CHECK
#######
#print(person_index_df.head())
#print(house_index_df.head())

#######
### Put people in houses 
########

person_index_df = generate_house_for_person(person_index_df, house_index_df, ce_index_df)
######

# assign residence type 
person_index_df['Residence_Type'] = person_index_df['Household_ID'].apply(assign_residence_type)

# Shared family names
person_index_df = common_surnames_in_house(person_index_df)
person_index_df = common_firstnames_in_house(person_index_df)
person_index_df = create_duplicates(person_index_df, num=50, twin=True)

####
### Join addresses 
####

#person_index_df = join_to_populate_addresses(person_index_df, house_index_df)

#print(person_index_df.head())
#print(person_index_df.tail())
#print(person_index_df[['Household_ID','Last_Name']].head(10))
#print(person_index_df[['Household_ID','Last_Name']].tail(10))


#####
# duplicate for CCS with modified ID's
#####

ccs_people, ccs_house, ccs_ce = lose_records(*CCS_scramble(person_index_df, house_index_df, ce_index_df), keep=True)
census_people, census_house, census_ce = lose_records(person_index_df, house_index_df, ce_index_df, keep=False)

#####
#create duplicated people
#####

ccs_people = create_duplicates(create_duplicates(ccs_people, num= round(ccs_people.shape[0]*.02), change_house= False),
                               num= round(ccs_people.shape[0]*.05),change_house =True)

census_people = create_duplicates(create_duplicates(census_people, num= round(census_people.shape[0]*.02), change_house= False),
                               num= round(census_people.shape[0]*.05),change_house =True)


#####
# required pertubations on both sides
#####

ccs_people = add_missing_codes_to_some(pertubation21(ccs_people))
census_people = add_missing_codes_to_some(census_people)
ccs_house = add_missing_codes_to_address(perturb_geography(ccs_house))
census_house = add_missing_codes_to_address(census_house)


#####
# Create relationships from census table
#####

census_relationships = generate_relationships(census_people)


#####
# Create visitor tables
#####

census_visitor = create_census_visitor(code_list, house_num = census_house.Household_ID.__array__(), num=200)
ccs_visitor = create_ccs_visitor(code_list, house_num = ccs_house.Household_ID.__array__(), num=200)

#####
# Save files
#####

census_people.sort_values('Cluster_num').to_csv('../output2/census_residents.csv', index = False)
census_house.to_csv('../output2/census_households.csv', index = False)
census_ce.to_csv('../output2/census_ce.csv', index = False)
census_relationships.to_csv('../output2/census_relationships.csv', index = False)
census_visitor.to_csv('../output2/census_visitors.csv', index = False)
ccs_people.sort_values('Cluster_num').to_csv('../output2/ccs_residents.csv', index = False)
ccs_house.to_csv('../output2/ccs_households.csv', index = False)
ccs_ce.to_csv('../output2/ccs_ce.csv', index = False)
ccs_visitor.to_csv('../output2/ccs_visitors.csv', index = False)