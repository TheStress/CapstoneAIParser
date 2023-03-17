'''
Credits: https://github.com/neuged/webanno_tsv (TSV Parser)
'''

import csv
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import json
import conllu
import pandas as pd
import os
from webanno_tsv import Document, Annotation
from dataclasses import replace
from webanno_tsv import webanno_tsv_read_file, Document
#nltk.download('punkt')
def CreateSkillListKaggle():
    allSkills = set()
    print("skill list")
    #Skill List from kaggle
    with open('RawData\Kaggle\Job Skill List\Jobs_skills_data_set_edited.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 10
        for row in spamreader:
            for skill in row[1].split(","):
                for skill1 in skill.split("/"):
                    skill1 = skill1.replace('"', "")
                    skill1 = skill1.strip()
                    allSkills.add(skill1)
    #Skill List linkedin
    with open('RawData\Kaggle\LinkedInList\linkedin_skill.csv', newline='', errors='ignore') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            # print(row)
            allSkills.add(row[0])
    
    return allSkills

def CreateSkillListOStar():
    allSkills = set()
    print("O Star List")
    validJobList = ['Computer Programmers', 'Software Developers', 'Software Quality Assurance Analysts and Testers', 'Web Developers', 'Web and Digital Interface Designers']
    #Skill List from kaggle
    with open('RawData\OStar\Skills.csv', 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        for row in reader:
            allSkills.add(row[3])
    with open("RawData\OStar\Technology Skills.csv", 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        for row in reader:
            if(row[0][0:2] == '15'):
                allSkills.add(row[2])
    return allSkills

def Format(allSkills, type = ""):
    # adding all versions UPPER -> lower -> First
    newSkillList = set()
    for skill in allSkills:
        if(type == "upper"):
            newSkillList.add(skill.upper())
        if(type == "lower"):
            newSkillList.add(skill.lower())
        if(type == "first"):
            skill = skill.lower()
            capital = True
            newSkill = ""
            for c in skill:
                if (c == ' ' or c == '-'):
                    capital = True
                else:
                    if(capital):
                        c = c.upper()
                        capital = False
                newSkill += c
            newSkillList.add(newSkill)
    return newSkillList

def WriteList(skillList, location):
    #Writing List
    print("writing")
    with open(location, 'w', newline='', errors='ignore') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in skillList:
            spamwriter.writerow([i])

def WriteSearchListInception(skillList):
    pasteString = "("
    currentString = "\" | \"".join(skillList)
    pasteString += currentString
    pasteString += "\")"
    with open("testingPasteUpper.txt", 'w', errors='ignore') as output:
        output.write(pasteString)

def ParseJSONForDescriptions():
    print("parsing")
    with open("Data\SmallJobPostTest\jobPostDataset.json", 'r') as input:
        jobsDataset = json.load(input)
    currentDoc = 0
    for job in jobsDataset:
        path = "Data\SmallJobPostTest\IndividualDocs\jobPost"+str(currentDoc)+".txt"
        print(path)
        with open(path, 'w', errors='ignore') as output:
            fullDescription = ""
            fullDescription += job["description"] + '\n'
            for item in job["job_highlights"]:
                fullDescription += '\n'.join(item["items"])
            # print(fullDescription)
            output.write(fullDescription)
        currentDoc += 1

def ConllUScanner(dataPath):

    return
def TSVParser():
    trainingData = []
    for i in range(1):
        path = "Data/SmallJobPostTest/LabeledDataTSV/annotation/jobPost" + str(0) + ".txt" + "/admin.tsv"
        # print(path)
        if(os.path.exists(path)):
            with open(path, 'r') as csvInput:
                data = csv.reader(csvInput, delimiter='\t', quotechar="~")
                text = ""
                annotations = []

                #Parsing data
                for row in data:
                    if(len(row) > 1):
                        # if(row[3] == "SKILL"):
                            holder = row[1].split("-")
                            oneAnnotation = [int(holder[0]), int(holder[1]), row[2], row[3]]
                            annotations.append(oneAnnotation)
                    elif(len(row) == 1):
                        if(row[0][:6] == "#Text="):
                            text += row[0][6:]
                # print(annotations)
                # print(text)
                doc = {"annotations": annotations, "text": text}
                trainingData.append(doc)

    return trainingData

if __name__ == "__main__":
    # ParseJSONForDescriptions()
    # WriteList(CreateSkillListOStar(), "Data\skillsDataNew.csv") # data cleaning
    # WriteSearchListInception()
    # WriteSearchListInception(CreateSkillListOStar())

    # ConllUScanner()
    with open("Data\SmallJobPostTest\IndividualDocs\jobPost0.txt", 'r') as file:
        data = csv.reader(file)
        for item in TSVParser():
            for annotation in item["annotations"]:
                print(annotation)
                print(test[annotation[0]:annotation[1]], annotation[2])
            print(item["text"])

    doc = webanno_tsv_read_file('Data/SmallJobPostTest/LabeledDataTSV/annotation/jobPost0.txt/admin.tsv')
    for annotations in doc.annotations:
        print(annotations)
    for token in doc.tokens:
        print(token.sentence_idx, token.idx, token.start, token.end, token.text.encode("utf-8"))
    # for token in doc.tokens:
    #     print(token)

    # Prints:
    # 1 2
    # 2 2

    # for annotation in doc.match_annotations(layer='Layer2'):
    #     print(annotation.layer, annotation.field, annotation.label)

    # # Prints:
    # # Layer2 Field3 XYZ

    # for annotation in doc.match_annotations(sentence=doc.sentences[0]):
    #     print(annotation.layer, annotation.field, annotation.label)

    # # Prints:
    # # Layer1 Field1 ABC
    # # Layer2 Field3 XYZ

    # # Some lookup functions for convenience are on the Document instance
    # doc.token_sentence(token[0])
    # doc.sentence_tokens(doc.sentence[0])
    # doc.annotation_sentences(doc.annotations[0])