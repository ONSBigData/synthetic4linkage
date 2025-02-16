# synthetic4linkage
Creating synthetic data for testing clerical linkage interface

## Delivery 1 - generating data 
1. Generate ~10,000 fake people into the Person Index 
2. Generate 5,000 fake households into Household Index
3. Generate 500 fake CEs into CE Index
4. Assign people from the Person Index to each Household or CE
    1) Households should contain between 1 and 5 people
    2) CEs should contain between 6 and 49 people
5. Create some twins
6. Create households with shared surnames and with few shared first names
7. Copy a random 94% from the Person Index into the Census table and remove 3% of households/CEs
8. Copy a random 94% of the Person Index into the CCS table and remove people from 3% households while keeping the address info in CCS household/CE list ('dummy households')

## Delivery 2 - pertubation 
1. For records that appear in both census and CCS perturb on either record:
    1) 35% of forename variables
    2) 32% of surname variables
    3) 1% of sex variables
    4) 15% of day of birth
    5) 13% of month of birth
    6) 13% of year of birth
    7) 4% of postcodes
2. Swap the geography (i.e. edit household table) for 50 of the CCS addresses (to mimic people moving house).
3. 2% of people duplicated between 2 and 5 times in the same household (with a different person ID) and 5% to different households. Each instance should have a separate person ID


## Delivery 3 - relationships 

1. Set a relationship status for each of the assigned people in a census household. Note that a resident can only have a relationship status if in a household not if in a CE.

## Delivery 4 - visitors 

1. Add 200 Visitors records and link them randomly to the census households. (todo - make some of the census visitors (say 50) person records in CCS)
2. Add 200 Visitors records and link them randomly to the CCS households. (todo - make some of the CCS visitor records (say 50) person records in Census)

## Delivery 5 - cluster numbers
