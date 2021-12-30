
import os as os 
#print(os.getcwd)
#analyzeDocResponse

import json


# Works - as in reads and prints JSON
# =============================================================================
# # https://stackoverflow.com/questions/20199126/reading-json-from-a-file
# with open("analyzeDocResponse.json") as json_file:
#     json_data = json.load(json_file)
#     print(json_data)
# =============================================================================
    

with open("analyzeDocResponse.json") as json_file:
    json_data = json.load(json_file)
    #print(json_data)
    doc = json_data

#print(doc)
