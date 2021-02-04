import os
import sys
import pprint
from googleapiclient.discovery import build

CLIENT_KEY = sys.argv[1]
ENGINE_KEY = sys.argv[2]
PRECISION = float(sys.argv[3])
QUERY = sys.argv[4]

# def processArguments():
#     clientKey = sys.argv[1]
#     engineKey = sys.argv[2]
#     precision = sys.argv[3]
#     originalQuery = sys.argv[4]
#     return (clientKey, engineKey, precision, originalQuery)

# def userRelevance(clientKey, engineKey, precision, originalQuery):
#     print("Parameters:")
#     print("Client Key\t=\t", clientKey)
#     print("Engine Key\t=\t", engineKey)
#     print("Query     \t=\t", originalQuery)
#     print("Precision \t=\t", precision)
#     service = build("customsearch", "v1", developerKey=clientKey)
#     res = service.cse().list(
#       q=originalQuery,
#       cx=engineKey,
#     ).execute()
#     pprint.pprint(res['items'][0]['link'])
#     pprint.pprint(res['items'][0]['title'])
#     pprint.pprint(res['items'][0]['snippet'])

def userFeedback():
    """
    Control function which calls other functions.
    :Parameters:
        :None
    :Returns:
        :None
    """
    currentPrecision = 0
    currentQuery = QUERY
    userFeedbackSet = {}
    while True:
        print("Parameters:")
        print("Client Key\t=\t", CLIENT_KEY)
        print("Engine Key\t=\t", ENGINE_KEY)
        print("Query     \t=\t", currentQuery)
        print("Precision \t=\t", str(PRECISION))
        print("Google Search Results: ")
        print("=======================")
        userFeedbackSet = executeGoogleQuery(currentQuery)
        currentPrecision = len(userFeedbackSet['relevantDocuments'])/10.0
        if currentPrecision >= PRECISION or currentPrecision == 0:
            # TODO: Check what the reference implementation does in this scenario.
            print("The desired precision level reached.")
            break
        print("=======================")
        print("FEEDBACK SUMMARY:")
        print("Precision: ", currentPrecision)
        print("Still below the desired precision of ", PRECISION)
        # TODO: The reference implementation has two such print statements. 
        # Either it prints them twice, or prints them at regular intervals.
        print("Indexing Results...")
        break
        # currentQuery += expandQueryKeywords(resultSet)

def executeGoogleQuery(query):
    """
    Executes google query and takes user feedback on the relevance of the results
    :Parameters:
        :query: string, the query to search using the google api
    :Returns:
        :{relevantDocuments, googleResults}: dictionary, containing the following:
            - relevantDocuments: list, of all the relevant documents identified by the user
            - googleResults: list, of all the results obtained by using the query
    """
    relevantCount = 0
    relevantDocumentSet = []
    service = build("customsearch", "v1", developerKey=CLIENT_KEY)
    res = service.cse().list(
      q=query,
      cx=ENGINE_KEY,
    ).execute()
    resultSet = res['items']
    for index in range(10):
        print("Result " + str(index + 1))
        print("[")
        print(" URL: ", resultSet[index]['link'])
        print(" Title: ", resultSet[index]['title'])
        print(" Summary: ", resultSet[index]['snippet'])
        print("]")
        print("Relevant(Y/N): ")
        userInput = input()
        checkUserInput = checkRelevance(userInput)
        if checkUserInput:
            relevantDocumentSet.append(index)
    return {"relevantDocuments": relevantDocumentSet,"googleResults": resultSet}

def checkRelevance(userInput):
    valid = {"yes": True, "y": True, "ye": True, "Y": True, "YES": True,
             "no": False, "n": False, "N": False, "NO": False}
    return valid[userInput]

def main():
    userFeedback()

if __name__ == "__main__":
    main()

# Tasks to perform
# 1. Start the loop (10) for the said query with the following in every iteration
#   1. Print the parameters
#   2. Google Search Results
#   3. Each item in the google result -- title, link, snippet
#   4. Relevant feedback
# 2. End of the loop. Calculate precision. Check precision conditions and take action.
