import pandas as pd
import delivery1 as d

code_list = pd.read_csv('../data/possible_codes.csv')


###
# Resident_index
###
person_index_df = pd.DataFrame(d.create_row_resident(num=1000, code_list =  code_list))
person_index_df = d.split_DOB(person_index_df)

###
# House_index
###
house_index_df = pd.DataFrame(d.create_row_house(num=50, code_list =  code_list))

###
# CE_index
###
ce_index_df = pd.DataFrame(d.create_row_CE(num=5, code_list =  code_list))


#######
### CHECK
#######

#######
### Put people in houses 
########

#person_index_df = d.generate_house_for_person(person_index_df, house_index_df)
######


print(person_index_df.head())
print(house_index_df['Number_Of_Usual_Residents'].head())

#####
# Save file
#####

person_index_df.to_csv('../output/person_index.csv')
house_index_df.to_csv('../output/house_index.csv')
ce_index_df.to_csv('../output/ce_index.csv')



########
## Assigning houses to people 
########

# Easy to asign house to a person and then join after 

