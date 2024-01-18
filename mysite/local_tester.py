from console_tester import getDataFromFile
from idleonTaskSuggester import main

def fullTest(testType):
    itRawJSONpath =  './testing-data/idleonefficiency_PublicProfileJSON.json' #NO sorted list expected
    itToolboxJSONpath = './testing-data/idleontoolbox_ToolboxJSON.json' #Sorted list expected
    ieRawJSONpath = './testing-data/idleontoolbox_RawGameJSON.json' #Sorted list expected if they copy their JSON from the public profile, but not from their local profile

    jsonTestResults = {}
    jsonTestList = [itRawJSONpath, itToolboxJSONpath, ieRawJSONpath]
    for testProfile in jsonTestList:
        #print("Console_Tester~ INFO Testing with JSON data from file:", testProfile)
        singleResult = main(getDataFromFile(testProfile), "consoleTest")
        if singleResult in jsonTestResults:
            jsonTestResults[singleResult] += 1
        else:
            jsonTestResults[singleResult] = 1

    goodPublicIETestResults = {}
    goodPublicIETestList = [
        "talentlessss", "dork1444", "vini07", "elandra_k", "redpaaaaanda", "tjsh11", "treason75", "pneumatus", "scolioli", "chalalaa", "gt35t3q4gta", "buffikun", "johs", "usernamebrand", "ocsisnarf", "ktnbtn", "sataneide", "shadoowz", "icyfoxkiller", "sythius", "scoli", "herusx", "campz", "gwuam", "weebgasm", "canabuddha", "rashaken", "nerfus", "soatok", "poppercone", "hockeyd14", "clevon", "dootn006"
        ]
    for testProfile in goodPublicIETestList:
        #print("Console_Tester~ INFO Testing with Public IE:", testProfile)
        try:
            singleResult = main(testProfile, testType)
        except Exception as reason:
            print("Console_Tester~ EXCEPTION Encountered during eval of testProfile:", testProfile, reason)
            singleResult = "ExceptionFail"
        if singleResult in goodPublicIETestResults:
            goodPublicIETestResults[singleResult] += 1
        else:
            goodPublicIETestResults[singleResult] = 1

    badPublicIETestResults = {}
    badPublicIETestList = [
        "thedyl", "test"
        ]
    for testProfile in badPublicIETestList:
        #print("Console_Tester~ INFO Testing with Public IE:", testProfile)
        try:
            singleResult = main(testProfile, testType)
        except Exception as reason:
            print("Console_Tester~ EXCEPTION Encountered during eval of testProfile:", testProfile, reason)
            singleResult = "ExceptionFail"
        if singleResult in badPublicIETestResults:
            badPublicIETestResults[singleResult] += 1
        else:
            badPublicIETestResults[singleResult] = 1

    fullTestResults = {
        "JSON Tests": jsonTestResults,
        "Good Public IE Tests": goodPublicIETestResults,
        "Bad Public IE Tests": badPublicIETestResults
        }

    for testGroup in fullTestResults:
        print("Console_Tester.fullTestResults", testGroup, ":", fullTestResults[testGroup])

fullTest("consoleTest")
#main("clevon", "web")
#print(main("scolioli", "web")[4][0])
#fullListPrint(main("usernamebrand", "web"))
#print(main("scoli", "consoleTest"))