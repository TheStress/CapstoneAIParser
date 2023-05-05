''' 
TASK: Getting more aquatned with the data and how python parses it with nlp

(0) https://www.kaggle.com/code/sanabdriss/nlp-extract-skills-from-job-descriptions/notebook

(1) https://www.kaggle.com/datasets/maneeshdisodia/employment-skills
(2) https://www.kaggle.com/datasets/murugeshm1/job-skills-prediction-data-set-with-company 
(3) https://www.kaggle.com/sunnykusawa/job-data

(4) https://serpapi.com/blog/scrape-google-jobs-organic-results-with-python/

(5) https://github.com/jneidel/job-titles

Possible Strategies
- creating a list of skills and keywords
    - specifying for each job (requires a job classifier)
- having and actual skills classifier

Methods with databases
- parse through skill list (2) and add to lineked in list (1)
- using this list you can label the skills using 


List of jobs to get
- software engineer
- full stack engineer
- back end engineer
- front end engineer
- data analyist
- data engineer
- mobile developer

jobPostDatasetSWE_3_15_23.json (20 searches x 10 results = 200 postings -> starting)

https://newscatcherapi.com/blog/train-custom-named-entity-recognition-ner-model-with-spacy-v3
https://itnext.io/nlp-named-entity-recognition-ner-with-spacy-and-python-dabaf843cab2

https://www.grammarly.com/blog/engineering/category/nlp-ml/ (for possible grammar suggester)
'''
from serpapi import GoogleSearch
import os, json

params = {
	'api_key': '0c7714dec6a0749f6f81c7032cd15c0f7de73c0fc753de6f8c2ec85191b10253', # https://serpapi.com/manage-api-key
	# https://site-analyzer.pro/services-seo/uule/
	'uule': 'w+CAIQICINVW5pdGVkIFN0YXRlcw',		# encoded location (USA)
	'q': 'front end developer',              		# search query
    'hl': 'en',                         		# language of the search
    'gl': 'us',                         		# country of the search
	'engine': 'google_jobs',					# SerpApi search engine
	'start': 0								# pagination after 5 searches
}

google_jobs_results = []

count = 20
while count > 0:
    search = GoogleSearch(params)   			# where data extraction happens on the SerpApi backend
    result_dict = search.get_dict() 			# JSON -> Python dict
    
    if 'error' in result_dict:
        break
    for result in result_dict['jobs_results']:
        google_jobs_results.append(result)

    params['start'] += 10
    count -= 1

with open("Data\FrontEnd\jobPostDatasetFrontEnd_5_5_23.json", "w") as outfile:
    outfile.write(json.dumps(google_jobs_results, indent=4))
# print(json.dumps(google_jobs_results, indent=2, ensure_ascii=False))