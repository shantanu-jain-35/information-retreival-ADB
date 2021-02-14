# Information-retreival-ADB
Designing an Information Retrieval Model with Precision @10

# Team Members

Phan Anh Nguyen (pn2363)

Shantanu Jain (slj2142)

# List of files:
+ QuerySession.py
+ user_relevance.py
+ transcript_1_"per se".txt
+ transcript_2_"brin".txt
+ transcript_3_"cases".txt
+ README.md

To install these files, run the following command in the Google VM terminal: 

**pip3 install beautifulsoup4 nltk lxml requests**

# Project design

Our product code is split into two files: A main driver ("user_relevance.py") and a defined QuerySession class for implementing the query modification ("RocchioSession.py") for each search iteration. The flow of our program works as follows: 

1. The user starts the program with a search term from the command line and desired precision level
2. Our driver will then call the Google Custom Search API on the provided query terms and display the top 10 results. Here we use the *lxml* as well as the *requests* library to call the API. 
3. User gets to rank the relevance for each of the presented documents based on a simple "Yes/No" feedback mechanism.
4. User feedback is consolidated.
5. A new QuerySession is instantiated and ingests the JSON file returned from the Google Custom Search API as well as the consolidated user feedback. 
6. Within QuerySession, we use the *beautifulsoup4* and *nltk* libraries to construct a vectorized representation of each document returned in the JSON and use that to construct the inverted list and carry out query modification (described in more detail below). We ultimately return an updated query vector to the driver for the next search iteration. 
7. Once search precision has reached the specified threshold, our driver will exit.

# Query-modification methodology

Our Query-modification technique utilizes the Rocchio algorithm explained in lecture. For each search iteration, we instantiate a QuerySession, which takes in the query results returned from the Search Engine API and creates an inverted list of all terms that exist within the 'Title' and 'Snippet' fields. Fields within the inverted list are: [IDF], [Weight], [RelevantDocs], [NonRelevantDocs]. 

We then assign individual document term weights to each of the terms that exist by calculating *tf-idf*. We then used Rocchio to generate a new set of weights for each term based on predetermined Beta and Gamma values. We eventually settled for **Beta = 0.75** and **Gamma=0.75**. Alpha values were not used as we were not allowed to modify or remove original query terms once inserted as per the assignment specifications. 

Finally, we sorted terms by weight and applied and applied several additional filters to determine the top 2 words to be appended to the query. Specifically, we used stemming to filter out potential repeat words (i.e: "Cases" and "Case") from being inserted into query updates, as well as preferred to add terms that existed in at least 2 relevant documents where possible. We noticed that the latter filter greatly increased our precision in the earlier iterations. 

# Google API Keys

[TO BE UPDATED IN SUBMISSION]