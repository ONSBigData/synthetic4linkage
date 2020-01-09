import pandas as pd
import delivery1 as d

code_list = pd.read_csv('../data/possible_codes.csv')


###
# Resident_index
###
person_index_df = pd.DataFrame(d.create_row_resident(num=3000, code_list =  code_list))
person_index_df = d.split_DOB(person_index_df)

###
# House_index
###
house_index_df = pd.DataFrame(d.create_row_house(num=500, code_list =  code_list))

print(house_index_df.head())

###
# CE_index
###
ce_index_df = pd.DataFrame(d.create_row_CE(num=50, code_list =  code_list))


#######
### CHECK
#######

#######
### Put people in houses 
########

person_index_df = d.generate_house_for_person(person_index_df, house_index_df, ce_index_df)
######



# assign residence type 
person_index_df['Residence_Type'] = person_index_df['Household_ID'].apply(d.assign_residence_type)

# Common last names 
person_index_df = d.common_surnames_in_house(person_index_df)


####
### Join addresses 
####

person_index_df = d.join_to_populate_addresses(person_index_df, house_index_df)



print(person_index_df.head())
#print(person_index_df.tail())
#print(person_index_df[['Household_ID','Last_Name']].head(10))
#print(person_index_df[['Household_ID','Last_Name']].tail(10))

#####
# Save file
#####

person_index_df.to_csv('../output/person_index.csv')
house_index_df.to_csv('../output/house_index.csv')
ce_index_df.to_csv('../output/ce_index.csv')



########
## Make a big table of everything 
########

# Easy to asign house to a person and then join after 

