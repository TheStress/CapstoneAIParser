# CapstoneAIParser
## About
This is the work from start to finish involved with training a Named Entity Classifier to extract the relavent keywords from job postings that an ATS system may use to filter out applicant resuems.

## Process and Technology
1. serpAPI to gather job postings from Google Jobs
2. Python to clean up the data and prepare it for labeling
3. INCEPTION to label the hard and soft skills in the job postings
4. spaCy framework to train NER classifier for the final product

# Installation instructions
```
pip install -U pip setuptools wheel
pip install -U spacy[cuda80]
python -m spacy download en_core_web_sm
```
