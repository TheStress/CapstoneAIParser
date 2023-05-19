import spacy
from spacy import displacy
from spacy.util import filter_spans
from spacy.tokens import DocBin
import DataCleaning
import json

'''
STARTING CONFIG
python -m spacy init fill-config base_config.cfg newConfig.cfg

TRAINING COMMAND
python -m spacy train config.cfg --output ./output --paths.train ./training.spacy --paths.dev ./testing.spacy
'''

def WriteHTML(doc):
    colors = {"SKILL": "#F67DE3"}
    options = {"colors": colors} 

    html = displacy.render(doc, style="ent", options= options, page=True)
    with open('visualizer.html', 'w') as htmlOutput:
        htmlOutput.write(html)
        htmlOutput.close()

def CreateDocs(dataSet, isTrainingData):
    nlp = spacy.blank("en")
    docs = []
    for data in dataSet:
        if(data["isTrainingData"] == isTrainingData):
            data["text"] = data["text"].replace("/"," ")
            doc = nlp(data["text"])
            entities = []
            hasAnnotations = False
            for start, end, word, label in data["annotations"]:
                span = doc.char_span(start, end, label=label, alignment_mode="expand")
                if span is None:
                    print(data["text"][start-10:end+10])
                    print(data["text"][start:end])
                    print("Skipping entity")
                else:
                    hasAnnotations = True
                    entities.append(span)
            if hasAnnotations:
                filtered_ents = filter_spans(entities)
                doc.ents = filtered_ents 
                docs.append(doc)
    return docs

def CreateTrainingData(outputPathTraining, outputPathTesting):
    trainingData = DataCleaning.GetTSVData(0.75)
    
    docBin = DocBin() # create a DocBin object
    docs = CreateDocs(trainingData, True)
    
    WriteHTML(docs)
    for doc in docs:
        docBin.add(doc)
    docBin.to_disk(outputPathTraining) # save the docbin object
    
    docBin = DocBin() # create a DocBin object
    docs = CreateDocs(trainingData, False)
    for doc in docs:
        docBin.add(doc)
    docBin.to_disk(outputPathTesting) # save the docbin object



def GetDoc():
    return"""
    Qualifications
    •
    Bachelor’s degree in Computer Science, Computer Engineering, Software Engineering, Electrical Engineering, Wireless Engineering, Information Security, Mathematics, Digital Arts & Sciences or related field
    •
    GPA of 3.0 or greater
    Responsibilities
    •
    Apply computer science, engineering, and mathematical analysis concepts and principles in the development of software for the target application
    •
    Work closely with cross functional members of the engineering organization to develop and evaluate interfaces between hardware and software, and operational performance requirements and design of the overall system
    •
    Support and participate in all phases of the software development life cycle, including requirements analysis, design, implementation, integration, and test of embedded software for real-time control of advanced tactical radio equipment
    •
    Develop software test procedures, software programs, and related documentation
    •
    Utilize modeling tools and equipment to establish operating data, conduct experimental tests, and evaluate results
    •
    Participate in peer reviews, identify, track and repair defects
    •
    Utilize a variety of software languages (i.e., C++, C#, C, Java, Ruby, HTML5, XML, SQL, Perl, Python, Ajax, Qt) on Windows, Linux, mobile platforms, and embedded real time operating systems (VxWorks, Linux, QNX, Integrity, Windows CE, and others for Motorola, Intel, TI, and custom processor designs)
    Job description
    Description:

    Job Description
    • Apply computer science, engineering, and mathematical analysis concepts and principles in the development of software for the target application
    • Work closely with cross functional members of the engineering organization to develop and evaluate interfaces between hardware and software, and operational performance requirements and design of the overall system
    • Support and participate in all phases of the software development life cycle, including requirements analysis, design, implementation, integration, and test of embedded software for real-time control of advanced tactical radio equipment
    • Develop software test procedures, software programs, and related documentation
    • Utilize modeling tools and equipment to establish operating data, conduct experimental tests, and evaluate results
    • Participate in peer reviews, identify, track and repair defects
    • Utilize a variety of software languages (i.e., C++, C#, C, Java, Ruby, HTML5, XML, SQL, Perl, Python, Ajax, Qt) on Windows, Linux, mobile platforms, and embedded real time operating systems (VxWorks, Linux, QNX, Integrity, Windows CE, and others for Motorola, Intel, TI, and custom processor designs)

    Qualifications:
    • Bachelor’s degree in Computer Science, Computer Engineering, Software Engineering, Electrical Engineering, Wireless Engineering, Information Security, Mathematics, Digital Arts & Sciences or related field
    • GPA of 3.0 or greater

    Preferred Skills:
    • One or more of the following: C++, C#, C, Java, Ruby, JEE, HTML5, XML, SQL, Qt, Windows, .NET, Unix, Linux, SOA, RTOS, Real-Time Controls, Wireless, Software Security, Robotics, OOA/OOD, Hadoop, Android, Embedded Systems"""

if __name__ == "__main__":
    
    CreateTrainingData("spaCyTesting/training.spacy", "spaCyTesting/testing.spacy")

    # nlp_ner = spacy.load("spacyTesting/model-last")

    # doc = nlp_ner(GetDoc())

    # WriteHTML(doc)
    
    print("hi")