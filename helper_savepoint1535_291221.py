# succesfully extracted the df i wanted to csv

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

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
print('Len of dataframe', len(dataframes))
#print(dataframes)

# Build  from this...
# =============================================================================
# for df in dataframes:
#     if df.shape[0]>2:
#         print('yes')
#     else:
#         print('no')
# =============================================================================

# This leaves just the df, build on this
# =============================================================================
# clean_list = []
# for df in dataframes:
#     if df.shape[0]>2:
#         #print('yes')
#         clean_list.append(df)
#     else:
#         print('no')
# print(len(clean_list))
# print(clean_list)
# =============================================================================

# Proves you can't treat this data like a list
#https://appdividend.com/2020/01/21/python-list-contains-how-to-check-if-item-exists-in-list/
# =============================================================================
# print(clean_list)
# if 'Dark' in clean_list:
#     print("Yes, 'S Eductation' found in List : ", listA)
# else:
#     print("Nope, 'Dark' not found in the list")
# =============================================================================

# I came up with this... seems useful, build on it
# =============================================================================
# for df in dataframes:
#     if df.shape[0]>2:
#         print(df.columns)
#     else:
#         print('no')
# =============================================================================

# Progress point
# =============================================================================
# for df in dataframes:
#     if 'Invoice #' in df.columns:
#         print('Yipee')
#     else:
#         print('no')
# =============================================================================


""" The difference this time is that the data spans more than one page. 
    So while this approach works, it only gets the data from the 1st page.
    Need a solution to extend this across multiple pages.
"""
#------------------- Investigating why missing 1st row
# -- The 1st row if the 2nd df is missing as it is viewed as a header not
# -- 1st row. Need some way to get 1st row

# This finds the col len of target, then 
# concats any other same col len df    
concatdf = []        
for df in dataframes:
    if 'Invoice #' in df.columns:
        #print(df.shape[1])
        a = df.shape[1]
        for df in dataframes:
            if df.shape[1] == a:
                #print('yes')
                #print(df)
                concatdf.append(df)
                #print(concatdf)
            else:
                print('... the else... ', 'no')
#print('... the concat... ', concatdf) 

# This gets the header (aka 1st row) of the 2nd dataframe...
# Now need to append this to the previous output
header = []        
for df in dataframes:
    if 'Invoice #' in df.columns:
        #print(df.shape[1])
        a = df.shape[1]
        for df in dataframes:
            if df.shape[1] == a:
                #print('yes')
                #print(df.columns)
                header.append(df.columns)
#print(header)
#print(header[1:])
h = (header[1:])
dfheader = pd.DataFrame(h)
print('.... this is the missing row......', dfheader)


# Need to column headers from the 1st df
for df in dataframes:
    if 'Invoice #' in df.columns:
        #print(df.columns)
        a = df.columns
print('this is... ',a)


import numpy as np
dftt2 = pd.DataFrame(np.concatenate(concatdf))

# the new append part
dftt3 = dftt2.append(dfheader)

dftt3.columns = a
dftt3['Invoice Date'] = dftt3['Invoice Date'].astype('datetime64')
dftt3.sort_values(by='Invoice Date', ascending=True, inplace=True)
dftt4 = dftt3.reset_index(drop=True)
dftt4.to_csv('dftt4.csv')
#print('... dftt2 ...', dftt2)
print(' ...... create space  ...... create space ...... create space')
print(' ...... create space  ...... create space ...... create space')
print(' ...... create space  ...... create space ...... create space')
print(dftt4)
#print(dftt3.dtypes)

#------------------- Investigating why missing 1st row


