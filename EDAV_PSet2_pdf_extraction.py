#%%
import tabula
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date

pd.set_option('display.max_columns', None)
#%%
# Define the path to the input PDF file
pdf_file_path = "/Users/yelene/Desktop/Grad school/Columbia/Classes/Git_repos/Exploratory_Data_Analysis_Visualization/Manhattan Community District Results.pdf" 

# Define the path to the output csv file
save_path = '/Users/yelene/Desktop/Grad school/Columbia/Classes/Git_repos/Exploratory_Data_Analysis_Visualization/non_QOL_man.csv'

# Define the page numbers to extract tables from
pages = 'all'

# Extract tables from the PDF file using tabula-py
tables = tabula.read_pdf(pdf_file_path, pages=pages)
print(len(tables))
tables
#%%

# Save each table for cleaning and concatenation
t1 = tables[0]
t2 = tables[1]
t3 = tables[2]
t4 = tables[3]
t5 = tables[4]
t6 = tables[5]
t7 = tables[6]

# Only need tables 1, 2, 4, 5, 6 upon review. Where 1 and 5 only have titles

#%%
# t1: contains title as rows, will use as a base for the table
non_qol_man = pd.DataFrame(columns=['QUALITY OF LIFE: NON-SAFETY INDICATORS']+list(t1.iloc[0])[2:])
non_qol_man

# Set up dict to iterate over needed tables
table_colname = {'t2':t2, 't4':t4, 't6':t6}

for key, table in table_colname.items():
    # Define cols for proper renaming
    cols = None
    if key =='t2':
        cols = list(non_qol_man.columns)
    elif key == 't4':
        cols = ['QUALITY OF LIFE: NON-SAFETY INDICATORS'] +  [ i[-3:] for i in t4.columns if 'CD' in i]
    elif key == 't6':
        cols = ['QUALITY OF LIFE: NON-SAFETY INDICATORS'] + list(t5.iloc[0])[:]

    # Get extraction index. Start is next row after where Quality of life is in the table
    start = int(table[table[table.columns.to_list()[0]]=='QUALITY OF LIFE: NON-SAFETY INDICATORS'].index[0]) + 1

    # Section to extract is 9 row long
    end = start+8

    # Extract data section to add
    temp = table.loc[start:end, :]

    if key == 't2':
        # only need the first, and last three columns
        temp = temp.iloc[:, [0, -3, -2, -1]]

        # Rename columns to match main dataframe
        temp.columns = cols

        # Add to main dataframe
        non_qol_man = pd.concat([non_qol_man, temp])

    else:
        # For the first table, we only need the first, and last three columns
        temp = temp.loc[start:end, :]

        # Rename columns to match main dataframe
        temp.columns = cols

        # Add to main dataframe, after other districts
        non_qol_man = pd.merge(non_qol_man, temp, on='QUALITY OF LIFE: NON-SAFETY INDICATORS', how='left')

# Save dataset
non_qol_man.to_csv(save_path, index=False)
