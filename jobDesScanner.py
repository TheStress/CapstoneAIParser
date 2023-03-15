import csv
import nltk
import DataCleaning

nltk.download('punkt')
nltk.download("stopwords")

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

description = ""
description = open("Data\jobDescription.txt", 'r').read()

stop_words = set(stopwords.words("english"))

# description = sent_tokenize(description)
description = word_tokenize(description)
# print(description)

filtered_list = set([word for word in description if word.casefold() not in stop_words])
# print(filtered_list)

keywords = filtered_list.intersection(DataCleaning.CreateSkillList())

print(keywords)