import numpy as np 
from googleapiclient.discovery import build
#from sklearn.feature_extraction.text import TfidfVectorizer 
#import heapq
import sys





def scrape_web(query, key, id):
    service = build(
        "customsearch", "v1", developerKey=key
    )

    res = (
        service.cse()
        .list(
            q=query,
            cx=id,
        )
        .execute()
    )
    
    links = []
    for result in res['items']:
        links.append(result)
    return links


def main():
    #/home/gkaraman/run <google api key> <google engine id> <precision> <query>
    #key = "AIzaSyC0vz_nYIczwBwNupqMrNhmBm4dQbX5Pbw"
    #id = "7260228cc892a415a"
    i = 1 
    google_api = sys.argv[0+i]
    google_engine = sys.argv[1+i]
    google_gemini_id = sys.argv[2+i]
    gem_span = sys.argv[3+i] #indiicates whether we are using span or bert 
    #for r: 1 indicates Schools_Attended, 2 indicates Work_For, 3 indicates Live_In, and 4 indicates Top_Member_Employees
    r = int(sys.argv[4+i]) 
    #t is a real num from 0 to 1 of extraction confidence threshold -> only used if BERT 
    t = float(sys.argv[5+i]) 
    #random seed query 
    q= sys.argv[6+i]
    #k is numper of tuples we want to output 
    k = int(sys.argv[7+i]) 

    #keeps track of urls already looked at 
    explored_urls = set()
    #tuples to be generated starts empty
    X_extracted_tuples = set()

    while True:
        links = scrape_web(inp,google_api, google_engine)
        #just get links that we have not looked at yet
        #desired_links = []
        for link in links:
            if link not in explored_urls:
                explored_urls.add(link)
                #now extract webpage, as long as no timeoute 

                #use beautiful soup to get text (only first 10,000 chars)

                #



        
        


if __name__ == "__main__":
    main()
