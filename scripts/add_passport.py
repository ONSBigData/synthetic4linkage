import pandas as pd
import random

# in this script only two new columns are generated and the two csvs are combine in terminal
# using paste -d , output/census_residents_old.csv output2/passports.csv > output/census_residents.csv

code_passport = pd.read_csv('../data/other_passport.csv', header = None, dtype = {0 : str})[0]
output = [{'Passport': random.choice(['-7', '-9', '1000', '1100', '1010', '0100', '0110', '0010', '0001']),
           'Other_Passport_Held': random.choice(['-7', '-9', random.choice(code_passport)])}  for x in  range(60770)]
pd.DataFrame(output).to_csv('../output2/passports.csv', index = False)

