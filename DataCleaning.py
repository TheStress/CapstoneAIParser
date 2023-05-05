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

def CreateManualList():
    allSkills = set()
    with open('Data\skillsManualTech.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 10
        for row in spamreader:
            allSkills.add(row[0])

    return allSkills

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

def WriteSearchListInception(skillList, outputPath):
    pasteString = "(\""
    currentString = "\" | \"".join(skillList)
    pasteString += currentString
    pasteString += "\")"
    with open(outputPath, 'w', errors='ignore') as output:
        output.write(pasteString)

def ParseJSONForDescriptions(sourcePathJSON, outputPath, outFileName="jobPost"):
    # Reading raw data
    with open(sourcePathJSON, 'r', errors='ignore', encoding="utf-8") as input:
        jobsDataset = json.load(input)

    # Parsing each job
    currentDoc = 0
    for job in jobsDataset:
        path = outputPath+"/"+outFileName+str(currentDoc)+".txt"
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
    # ParseJSONForDescriptions("Data/SWE/jobPostDatasetSWE_3_15_23.json", "Data/SWE/IndividualDocs", "SWEPost")
    allSkills = CreateManualList()
    upperSkills = Format(allSkills, "upper")
    lowerSkills = Format(allSkills, "lower")
    
    for skill in upperSkills:
        allSkills.add(skill)
    for skill in lowerSkills:
        allSkills.add(skill)

    WriteSearchListInception(allSkills, "InceptionPasteList/PasteList.txt")
    

    # WriteList(allSkills, "Data\skillsDataNew.csv") # data cleaning
    
    # counter = 0
    # currentDoc = 0
    # countLimit = 5000
    # skillList = set()
    # for skill in allSkills:
    #     skillList.add(skill)
    #     if counter > countLimit:
    #         outputPath = "InceptionPasteList/PasteList"+str(currentDoc)+".txt"
    #         WriteSearchListInception(skillList, outputPath)
    #         skillList.clear()
    #         counter = 0
    #         currentDoc += 1
    #     counter += 1




    print("hi")