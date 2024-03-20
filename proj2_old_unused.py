import numpy as np 
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
#from sklearn.feature_extraction.text import TfidfVectorizer 
#import heapq
import sys
import spacy
import create_entity_pairs

spacy2bert = { 
        "ORG": "ORGANIZATION",
        "PERSON": "PERSON",
        "GPE": "LOCATION", 
        "LOC": "LOCATION",
        "DATE": "DATE"
        }

bert2spacy = {
        "ORGANIZATION": "ORG",
        "PERSON": "PERSON",
        "LOCATION": "LOC",
        "CITY": "GPE",
        "COUNTRY": "GPE",
        "STATE_OR_PROVINCE": "GPE",
        "DATE": "DATE"
        }

def extract_tuples(input_text,existing_entities):
    #using spacy -> convert text to possible tuples
    # can identify numeric entities->including companies, locations, organizations and products
    #first, turn text into sentences -> # Apply spacy model to raw text (to split to sentences, tokenize, extract entities etc.)
    nlp = spacy.load("en_core_web_lg")  
    sentences = nlp(input_text).sents
    #now, I think depending on if spanbert or dictionary, we build them 
    new_tuples = set()
    for sentence in sentences: 
        sentence_tuples = create_entity_pairs(sentence, existing_entities, window_size=40)
        for tup in sentence_tuples:
            if tup not in new_tuples:
                new_tuples.add(tup)  
    return list(new_tuples)


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
    #tuples to be generated starts empty -> use a dictionary to hold onto highest value 
    X_extracted_tuples = {}

    while True:
        links = scrape_web(q,google_api, google_engine)
        #just get links that we have not looked at yet
        #desired_links = []
        for link in links:
            if link not in explored_urls:
                explored_urls.add(link)
                #now extract webpage, as long as no timeoute 
                with open(link) as fp:
                    soup = BeautifulSoup(fp, 'html.parser')
                #use beautiful soup to get text (only first 10,000 chars)
                text = soup.get_text()[0:10000]

                #split the text into sentences and extract named entities -> use spaCy
                if gem_span == 'spanbert':
                    new_tuples = spanbert_extract_tuples(text,)
                
                #if spanbert bert do: 

                #if gemini do: 
                elif gem_span == 'gemini':
                    print("gemini")
                    #call gemini function 
                else:
                    print("wrong type input")








        
        


if __name__ == "__main__":
    main()
