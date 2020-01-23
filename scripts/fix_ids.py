import pandas as pd
import random
random.seed(a=45)

cens_old = pd.read_csv('../output_old/census_residents.csv')
ccs_old= pd.read_csv('../output_old/ccs_residents.csv')
census_house = pd.read_csv('../output_old/census_households.csv')
ccs_house = pd.read_csv('../output_old/ccs_households.csv')
census_rel = pd.read_csv('../output_old/census_relationships.csv')

census_house_dict = {x//100: str(x) for x in census_house.Household_ID}
ccs_house_dict = {x//100: str(x) for x in ccs_house.Household_ID}
cens_dict= {x//10000: str(random.randint(10 ** 18, 2**63-1)) for x in cens_old.Resident_ID}
ccs_dict = {x//10000: str(random.randint(10 ** 18, 2**63-1)) for x in ccs_old.Resident_ID}

def apply_dict(df1, column_name, dicti, const = 100):
    df=df1.copy()
    df[column_name] = df[column_name].astype('uint64')//const
    return df.replace({column_name: dicti})

cens_new = apply_dict(cens_old, 'Resident_ID', cens_dict, 10000)
cens_new['Household_ID'] = cens_new.Household_ID.astype('uint64')
cens_new['CE_ID'] = cens_new.CE_ID.astype('uint64')
cens_new.to_csv('../output2/census_residents.csv', index = False)
ccs_new = apply_dict(ccs_old, 'Resident_ID', ccs_dict, 10000)
ccs_new['Household_ID'] = ccs_new.Household_ID.astype('uint64')
ccs_new['CE_ID'] = ccs_new.CE_ID.astype('uint64')
ccs_new.to_csv('../output2/ccs_residents.csv', index = False)
cens_rel_new = apply_dict(apply_dict(census_rel, 'Resident_ID', cens_dict, 10000), 'Related_Resident_ID', cens_dict, 10000)
cens_rel_new.to_csv('../output2/census_relationships.csv', index = False)

c1_old = pd.read_csv('../output_old/1 output of deterministic and probabilistic persons.csv')
c2_old = pd.read_csv('../output_old/2 Output for deterministic households and associative people and households.csv')
c3_old = pd.read_csv('../output_old/3 output for threshold finding or matchkey QA.csv')
c4_old = pd.read_csv('../output_old/4 output of presearch persons.csv')
c5_old = pd.read_csv('../output_old/5 output for clerical search.csv')
c6_old = pd.read_csv('../output_old/6 Output for census to census.csv')

c1_new =  apply_dict(c1_old, 'Resident_ID', cens_dict, 10000)
c1_new_s =  apply_dict(c1_old, 'Resident_ID', ccs_dict, 10000)
c1_new.Resident_ID[c1_new['Datasource']=='CCS'] = c1_new_s.Resident_ID[c1_new['Datasource']=='CCS']
c2_new =  apply_dict(apply_dict(apply_dict(apply_dict(c2_old, 'Census_Resident_ID', cens_dict, 10000), 'CCS_Resident_ID', ccs_dict, 10000), 'Census_Household_ID', census_house_dict, 100), 'CCS_Household_ID', ccs_house_dict, 100)
c3_new =  apply_dict(apply_dict(c3_old, 'Census_resident_ID', cens_dict, 10000), 'CCS_resident_ID', ccs_dict, 10000)
c4_new =  apply_dict(apply_dict(c4_old, 'Census_resident_ID', cens_dict, 10000), 'CCS_resident_ID', ccs_dict, 10000)
c5_new =  apply_dict(c5_old, 'ID', cens_dict, 10000)
c5_new_s =  apply_dict(c5_old, 'ID', ccs_dict, 10000)
c5_new.ID[c5_new['Datasource']=='CCS'] = c5_new_s.ID[c5_new['Datasource']=='CCS']
c6_new =  apply_dict(apply_dict(c6_old, 'Census Resident ID_target', cens_dict, 10000), 'Census Resident ID_candidate', cens_dict, 10000)






c1_new.sort_values('Datasource').to_csv('../output2/1 output of deterministic and probabilistic persons.csv', index = False)
c2_new.to_csv('../output2/2 Output for deterministic households and associative people and households.csv', index = False)
c3_new.to_csv('../output2/3 output for threshold finding or matchkey QA.csv', index = False)
c4_new.to_csv('../output2/4 output of presearch persons.csv', index = False)
c5_new.to_csv('../output2/5 output for clerical search.csv', index = False)
c6_new.to_csv('../output2/6 Output for census to census.csv', index = False)