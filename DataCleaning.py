'''
Credits: https://github.com/neuged/webanno_tsv (TSV Parser) jk didnt use it
'''

import csv
import nltk
import json
import conllu
import pandas as pd
import os
import spacy
from spacy import displacy
import string

def RemoveEscapeStrings(inputString):
    output = inputString
    output = output.replace("\n", "")
    output = output.encode("ascii", "ignore")
    return output.decode()

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
    #Skill List from kaggle
    # with open('RawData\OStar\Skills.csv', 'r') as csvFile:
    #     reader = csv.reader(csvFile, delimiter=',', quotechar='"')
    #     for row in reader:
    #         allSkills.add(row[3])
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
    # MAYBE LATER
    # escapeStrings = ["\n", "\u2022", "\u2019", "\u2013"]import spacy
    nlp = spacy.load("en_core_web_sm")


    print("parsing")
    # Reading raw data
    with open("Data\SmallJobPostTest\jobPostDataset.json", 'r', errors='ignore', encoding="utf-8") as input:
        jobsDataset = json.load(input)

    # Parsing each job
    currentDoc = 0
    for job in jobsDataset:
        path = "Data\SmallJobPostTest\IndividualDocs\jobPost"+str(currentDoc)+".txt"
        print(path)

        # writing each job
        with open(path, 'w', errors='ignore') as output:
            fullDescription = ""
            fullDescription += job["description"] + " "
            for item in job["job_highlights"]:
                for itemText in item["items"]:
                    fullDescription += itemText + " "

            # Processing escape characters out of data
            fullDescription = RemoveEscapeStrings(fullDescription)

            output.write(fullDescription)
        currentDoc += 1

def TSVParser():
    trainingData = []
    for i in range(20):
        path = "Data/SmallJobPostTest/LabeledDataTSV/annotation/jobPost" + str(i) + ".txt" + "/admin.tsv"
        text = ""
        annotations = []

        #Parsing data for annotations
        if(os.path.exists(path)):
            with open(path, 'r') as csvInput:
                data = csv.reader(csvInput, delimiter='\t', quotechar="~")
                for row in data:
                    if(len(row) > 1):
                        if(row[3] == "SKILL"):
                            holder = row[1].split("-")
                            oneAnnotation = [int(holder[0]), int(holder[1]), row[2], row[3]]
                            annotations.append(oneAnnotation)
        else:
            print(path + "(Does not exist)")

        # Reading text from source
        path = "Data\SmallJobPostTest\LabeledDataTSV\source\jobPost" + str(i) + ".txt"
        if(os.path.exists(path)):
            with open(path, 'r') as sourceInput:
                text = sourceInput.read()
        else:
            print(path + "(Does not exist)")

        doc = {"id": i, "annotations": annotations, "text": text}
        trainingData.append(doc)

    return trainingData

def OutputDoc(inputDoc):
    colors = {"SKILL": "#F67DE3"}
    options = {"colors": colors} 
            
    html = displacy.render(inputDoc, style="ent", options= options, page=True)
    with open('visualizer.html', 'w') as htmlOutput:
        htmlOutput.write(html)
        htmlOutput.close()

if __name__ == "__main__":
    # test = "\u0394"
    # testing = test.encode("utf-8")
    # print(test)
    ParseJSONForDescriptions()
    # WriteList(CreateSkillListOStar(), "Data\skillsDataNew.csv") # data cleaning
    # WriteSearchListInception(CreateSkillListOStar())
    # nlp = spacy.blank("en")
    # escapeChars = set()
    # for item in TSVParser():
    #     found = False
    #     index = 0
    #     print(repr(item["text"]))
        # for character in item["text"]:
        #     if(found == True):
        #         if(character == 'u'):
        #             escapeChars.add(item["text"][index-1:index+4])
        #         found = False
        #     if(character == "\\"):
        #        found = True
        #     index += 1
        # for annotation in item["annotations"]:
        #     doc = nlp.make_doc(item["text"])
        #     entities = []
            
            # for start, end, word, label in item["annotations"]:
                
            #     span = doc.char_span(start, end, label=label, alignment_mode="strict")
            #     if span is None:
            #         # print(data["id"], start, end, word, label)
            #         print("Skipping entity")
            #     else:
            #         hasAnnotations = True
            #         entities.append(span)

            # break

            # holder = item["text"]
            # if item["text"] == holder:
            #     print("good")
            # else:
            #     print("bad")
            # if item["text"][annotation[0]:annotation[1]] == annotation[2] :
            #     print(annotation)
            #     print(item["text"][annotation[0]:annotation[1]], annotation[2])

    # for escape in escapeChars:
    #     print(escape)
    
    # doc = nlp("I like New York")
    # ents = []
    # span = doc.char_span(7, 15, label="GPE")
    # assert span.text == "New York"
    # ents.append(span)
    # doc.ents = ents
    # OutputDoc(doc)