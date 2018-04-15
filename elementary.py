#Function that takes Company name as input and outputs a "sentiment score" and
#a pandas dataframe of the 3 most relevant articles;

import os
import sys
import json
from watson_developer_cloud import DiscoveryV1
import numpy as np
import pandas as pd

def mydearwatson(input_seller):
    input_seller = str(input_seller)


    # --- Authentication ----
    discovery = DiscoveryV1(
        username="60dd891d-9f19-4fd2-bb8a-912add37f1b4",
        password="tN4F1bLcMzQH",
        version="2017-11-07"
    )
    #--- Need to write a function to read seller ------

    query_string = 'enriched_text.entities.text:' + input_seller + ', labor|labour'
    qopts = {'query': query_string, 'counts':'10'}
    my_query = discovery.query('system', 'news-en', qopts)

    #query returns a sorted list of upto potentially 50 objects-
    #(default is 10 as is the case here) sorted in decresing order-
    #of relevance or "confidence":  a % value assigned based-
    #on potential relevance of every phrase in said URL

    #no of matches
    number = np.int(my_query["matching_results"])

    relevance = [my_query["results"][i]['result_metadata']['score'] for i in range(3)]
    titles = [my_query["results"][i]["title"] for i in range(3)]
    urls = [my_query["results"][i]["url"] for i in range(3)]
    orgs = []
    for i in range(3):
        try:
            orgs.append(my_query["results"][i]["forum_title"])
        except KeyError:
            orgs.append(None)

    #whether or not link is  'positive', 'negative' or 'neutral'
    label = [my_query["results"][i]['enriched_text']['sentiment']['document']['label'] for i in range(3)]

    #let's define a pandas dataframe:

    po = pd.DataFrame(list(zip(label,titles,urls,orgs,relevance)), columns = ['Sentiment','Title','URL','Source','Relevance'] )


    #Getting an aggregate score
    scoooore = np.mean([my_query["results"][i]['enriched_text']['sentiment']['document']['score'] for i in range(10)])
    output_string = 'IBM Watson Discovery News API estimates {} matches for {} with a total weighted sentiment of {:.1f}'
    output_string = output_string.format(number, input_seller, scoooore)
    return(po,output_string)

if __name__ == '__main__':
    comp = 'Patagonia'
    a, b = mydearwatson(comp)
    print(b)
    print(a)
