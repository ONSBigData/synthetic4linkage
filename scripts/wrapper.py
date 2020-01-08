import pandas as pd
import scripts.delivery1 as d
code_list = pd.read_csv('data/possible_codes.csv')

person_index_df = pd.DataFrame(d.create_row(num=10, code_list =  code_list))
person_index_df = d.split_DOB(person_index_df)

#######
### CHECK
#######

print(person_index_df.head())

#####
# Save file
#####

person_index_df.to_csv('../output/person_index.csv')