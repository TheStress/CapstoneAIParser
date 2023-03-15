import csv
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import json
#nltk.download('punkt')
def CreateSkillListKaggle():
    allSkills = set()
    print("skill list")
    #Skill List from kaggle
    with open('RawKaggleData\Job Skill List\Jobs_skills_data_set_edited.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 10
        for row in spamreader:
            for skill in row[1].split(","):
                for skill1 in skill.split("/"):
                    skill1 = skill1.replace('"', "")
                    skill1 = skill1.strip()
                    allSkills.add(skill1)
    #Skill List linkedin
    with open('RawKaggleData\LinkedInList\linkedin_skill.csv', newline='', errors='ignore') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            # print(row)
            allSkills.add(row[0])
    
    return allSkills

def CreateSkillListOStar():
    return

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

def WriteList(skillList):
    #Writing List
    print("writing")
    with open('Data\skillsDataNew.csv', 'w', newline='', errors='ignore') as csvfile:
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
    with open("Data\SWE\jobPostDatasetSWE_3_15_23.json", 'r') as input:
        jobsDataset = json.load(input)

    with open("Data\SWE\jobPostDatasetSWE_3_15_23CLEAN.txt", 'w', errors='ignore') as output:
        for job in jobsDataset:
            fullDescription = ""
            fullDescription += job["description"] + '\n'
            for item in job["job_highlights"]:
                fullDescription += '\n'.join(item["items"])
            # print(fullDescription)
            output.write(fullDescription)

if __name__ == "__main__":
    # ParseJSONForDescriptions()
    # WriteList(CreateSkillList()) # data cleaning
    WriteSearchListInception()
    print("test")