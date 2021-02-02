import requests
import nltk
from nltk.tokenize import word_tokenize
from collections import defaultdict
import sys
import math

class QuerySession():
    """
    # Class Params: 
        - InvertedList: Dictionary for each term that exists in the search-result collection. Contains calculated IDF, and weight
        - Query: Updated query terms
        - SearchResults: Tokenized results returned from Google Search API
        - Alpha, Beta, Gamma: Optional query hyperparams. Default set similar to textbook
    """
    def __init__(self, query, alpha = 1, beta = .75, gamma = .15):
        self.InvertedList = dict() # Store IDF later on as well as documents that exist in.
        self.SearchResults = dict()
        self.Query = [query]
        self.Alpha = alpha
        self.Beta = beta
        self.Gamma = gamma

    """
    # Function: PreprocessQueryResults
    # Params: Query results from Search API
    # Do: Preprocess raw query data and store as tokenized documents
    """
    def PreprocessQueryResults(self, QueryResults):
        """ 
        TODO: Need to discuss:
            - What elements of search are to be used to create terms? Titles? Snippets? Anything else?
        """
        print(self.Query)
        stopwords = set(nltk.corpus.stopwords.words('english')) #Fetch nltk stopwords

        toTokenize = ['title', 'snippet']
        for documentIndex in range(len(QueryResults['items'])): # Loop through each document
            tokenized_document = list()
            for section in toTokenize:
                text = QueryResults['items'][documentIndex][section]
                # print("About to preprocess section: ", section)
                text = word_tokenize(text) # Use ntlk to tokenize
                text = [word.lower() for word in text if ((len(word) > 2) and word not in stopwords)]
                tokenized_document += text
            print("For document ", documentIndex, " tokenized form is: ", tokenized_document)
            self.SearchResults[documentIndex] = tokenized_document
        
        # Lastly, update index after all documents have been tokenized
        return self.UpdateIndex()

    """
    # Function: UpdateIndex
    # Params: None
    # Do: Generate updated InvertedList to be used by Rocchio Algorithm
    # InvertedList Structure:
        {
            "term1": 
            {
                "IDF": log(len(SearchResults[items])/(len(self.InvertedList[RelevantDocs]) + len(self.InvertedList[NonRelevantDocs])))
                "Weight": = self.Beta/len(RelevantDocs) * tf-idf - self.Gamma/len(RelevantDocs) * tf-idf #Need to loop over each doc to calculate
                "RelevantDocs": {
                    "doc1": 4, # Can replace doc name with doc index within SearchResults.items
                    "doc3": 5,
                },
                "NonRelevantDocs": {
                    "doc2": 2,
                    "doc4": 1,
                }
            },
            "term2":...
        }
    """
    def UpdateIndex(self):
        relevantDocs = set([0,1,2,3,4])
        for documentIndex in self.SearchResults.keys():
            for word in self.SearchResults[documentIndex]:
                if word not in self.InvertedList: # Create new word entry if does not exist
                    self.InvertedList[word] = self.CreateNewIndex()
                if documentIndex not in relevantDocs:# Create new word entry if does not exist   <- TODO: Standardize how relevant/non-relevant docs are indicated
                    self.InvertedList[word]['RelevantDocs'][documentIndex] += 1
                else:
                    self.InvertedList[word]['NonRelevantDocs'][documentIndex] += 1

        for word in self.InvertedList.keys(): # Calculate IDF for each word entry in collection"
            self.InvertedList[word]['IDF'] = math.log10(len(self.SearchResults.keys())/(len(self.InvertedList[word]['RelevantDocs'].keys()) + len(self.InvertedList[word]['NonRelevantDocs'].keys())))
        return self.GetNewQuery()
        # return 

    """
    # Function: CreateNewIndex
    # Params: None
    # Do: Generates and returns empty template for new InvertedIndex entry
    """
    def CreateNewIndex(self):
        newEntry = dict()
        newEntry['IDF'] = None
        newEntry['Weight'] = 0
        newEntry['RelevantDocs'] = defaultdict(lambda:0)
        newEntry['NonRelevantDocs'] = defaultdict(lambda:0)
        return newEntry
    
    """
    # Function: GetNewQuery
    # Params: None
    # Do: Apply Rocchio Algorithm to update weights and return an updated Query based on top ranked weight
    # Source: Methodology for tf-idf based Rocchio: http://www.cs.cmu.edu/~wcohen/10-605/rocchio.pdf, 
    """
    def GetNewQuery(self):
        # TODO: Discuss if need to add alpha? Since we're not removing anything? Do we just calculate most relevant idf terms for each search? Seems like it? 
        for word in self.InvertedList.keys(): # For each word, calculate weight based on Rocchio for Relevant and Non-relevant documents
            idf = self.InvertedList[word]['IDF']
            for documentIndex in self.InvertedList[word]['RelevantDocs'].keys():
                tf = 1 + math.log10(self.InvertedList[word]['RelevantDocs'][documentIndex])
                self.InvertedList[word]['Weight'] += self.Beta/len(self.InvertedList[word]['RelevantDocs'].keys()) * tf * idf
            for documentIndex in self.InvertedList[word]['NonRelevantDocs'].keys():
                tf = self.InvertedList[word]['RelevantDocs'][documentIndex]
                self.InvertedList[word]['Weight'] -= self.Gamma/len(self.InvertedList[word]['NonRelevantDocs'].keys()) * tf * idf
        print(self.Query)
        appendedTerms = []
        appendedCount = 0
        sortedList = sorted(self.InvertedList, key=lambda word: self.InvertedList[word]['Weight'])
        print(sortedList)

        for word in sortedList:
            if word not in self.Query:
                self.Query.append(word)
                appendedCount += 1
            if appendedCount == 2:
                break
        # print(self.Query)
        return self.Query

if __name__ == "__main__":
    sesh = QuerySession(sys.argv[1])
    API_KEY = 'AIzaSyDNWorCRZlzJLmXMCjlFCmuYi9YMYN7XTA'
    ENGINE_ID = '85b4a45bc6204a22a'
    SEARCH_PARAMS = sys.argv[1]
    URL = 'https://www.googleapis.com/customsearch/v1?key=' + API_KEY + '&cx=' + ENGINE_ID + '&q=' + SEARCH_PARAMS
    searchResults = requests.get(url = URL).json()
    print(searchResults)
    newQuery = sesh.PreprocessQueryResults(searchResults)
    print(newQuery)

