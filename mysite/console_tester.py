import json
from idleonTaskSuggester import main

#main run with raw data copied from IE or IT. COMMENT OUT BEFORE PUBLISHING

itRawJSONpath =  '/home/Scoli/mysite/testing-data/idleonefficiency_PublicProfileJSON.json' #NO sorted list expected
itToolboxJSONpath = '/home/Scoli/mysite/testing-data/idleontoolbox_ToolboxJSON.json' #Sorted list expected
ieRawJSONpath = '/home/Scoli/mysite/testing-data/idleontoolbox_RawGameJSON.json' #Sorted list expected if they copy their JSON from the public profile, but not from their local profile

with open(itToolboxJSONpath, 'r') as inputFile:
    jsonData = json.load(inputFile)
inputFile.close()
if isinstance(jsonData, dict):
    results = main(jsonData)
else:
    print("jsonData is not a dict, it is a:", type(jsonData))

#main run with a username to look up in IE
#results = main("scoli")


#biggoleAdviceList = [generalList, w1list, w2list, w3list, w4list, w5list, w6list, w7list, w8list, pinchyList]
#print(results[0])
#print(results[1])
#print(results[2])
#print(results[3])
#print(results[4][0])
#print(results[5])
#print(results[6])
#print(results[7])
#print(results[8])
#print(results[9])