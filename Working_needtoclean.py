
import os as os 
#print(os.getcwd)
#analyzeDocResponse

import json


""" JSON output from textract """
with open("analyzeDocResponse.json") as json_file:
    json_data = json.load(json_file)
    #print(json_data)
    doc = json_data
#print(doc)

""" Pre-processing """
#https://maxhalford.github.io/blog/textract-table-to-pandas/
def map_blocks(blocks, block_type):
    return {
        block['Id']: block
        for block in blocks
        if block['BlockType'] == block_type
    }
blocks = doc['Blocks']
tables = map_blocks(blocks, 'TABLE')
cells = map_blocks(blocks, 'CELL')
words = map_blocks(blocks, 'WORD')
selections = map_blocks(blocks, 'SELECTION_ELEMENT')

def get_children_ids(block):
    for rels in block.get('Relationships', []):
        if rels['Type'] == 'CHILD':
            yield from rels['Ids']
            
 
""" JSON to df """            
import pandas as pd
pd.set_option('display.max_columns', None)

dataframes = []
for table in tables.values():

    # Determine all the cells that belong to this table
    table_cells = [cells[cell_id] for cell_id in get_children_ids(table)]

    # Determine the table's number of rows and columns
    n_rows = max(cell['RowIndex'] for cell in table_cells)
    n_cols = max(cell['ColumnIndex'] for cell in table_cells)
    content = [[None for _ in range(n_cols)] for _ in range(n_rows)]

    # Fill in each cell
    for cell in table_cells:
        cell_contents = [
            words[child_id]['Text']
            if child_id in words
            else selections[child_id]['SelectionStatus']
            for child_id in get_children_ids(cell)
        ]
        i = cell['RowIndex'] - 1
        j = cell['ColumnIndex'] - 1
        content[i][j] = ' '.join(cell_contents)

    # We assume that the first row corresponds to the column names
    dataframe = pd.DataFrame(content[1:], columns=content[0])
    dataframes.append(dataframe)            
#print('Len of dataframe', len(dataframes))
print(dataframes)

# Same process, looking for the df i want & canning the rest
# These are the values from textract, textract2 & now textract3
# =============================================================================
# lst = ['Start date','Invoice #', 'Date', 'lemon']
# check = lst
# for df in dataframes:
#     for x in check:
#         if x in df.columns:
#             print('Yipee')
#         else:
#             print('no')
# =============================================================================
      
# Progressing the above      
# ended up scapping the approach of trying to make this work across
# the previous tt
clean_list = []
for df in dataframes:
    #for x in check:
    if 'Date' in df.columns:
        #print('Yipee')
        clean_list.append(df)
    else:
        print('no')            
#print(clean_list)            

for df in clean_list:
    #print (df.columns)
    col = df.columns


import numpy as np
# lets make it a df, then look to drop the duplicate row (the header)
#df = pd.DataFrame(clean_list) # Read this error
df = pd.DataFrame(np.concatenate(clean_list))
df.columns = col
#print(df)
print('....... gap ........')
#print(df)
#df.to_csv('df.csv')

# Need to find the 'total' row 
#a = 'Total' in df['Date'].values
df['mask'] = df['Date'].str.contains(('total'),case=False)
print(df)

#https://thispointer.com/python-pandas-how-to-drop-rows-in-dataframe-by-conditions-on-column-values/
# Get names of indexes for which column Date has value Total
#indexNames = df[df['Date'] == 'Total' ].index
indexNames = df[df['mask'] == True ].index
print(indexNames)
# Delete these row indexes from dataFrame
#.... these two should be there... but rem in testing below
df.drop(indexNames , inplace=True)
df.to_csv('df.csv')
print(df)
