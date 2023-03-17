# import spacy

# nlp_ner = spacy.load("model-best")

# doc = nlp_ner("""
# Qualifications
# •
# Bachelor’s degree in Computer Science, Computer Engineering, Software Engineering, Electrical Engineering, Wireless Engineering, Information Security, Mathematics, Digital Arts & Sciences or related field
# •
# GPA of 3.0 or greater
# Responsibilities
# •
# Apply computer science, engineering, and mathematical analysis concepts and principles in the development of software for the target application
# •
# Work closely with cross functional members of the engineering organization to develop and evaluate interfaces between hardware and software, and operational performance requirements and design of the overall system
# •
# Support and participate in all phases of the software development life cycle, including requirements analysis, design, implementation, integration, and test of embedded software for real-time control of advanced tactical radio equipment
# •
# Develop software test procedures, software programs, and related documentation
# •
# Utilize modeling tools and equipment to establish operating data, conduct experimental tests, and evaluate results
# •
# Participate in peer reviews, identify, track and repair defects
# •
# Utilize a variety of software languages (i.e., C++, C#, C, Java, Ruby, HTML5, XML, SQL, Perl, Python, Ajax, Qt) on Windows, Linux, mobile platforms, and embedded real time operating systems (VxWorks, Linux, QNX, Integrity, Windows CE, and others for Motorola, Intel, TI, and custom processor designs)
# Job description
# Description:

# Job Description
# • Apply computer science, engineering, and mathematical analysis concepts and principles in the development of software for the target application
# • Work closely with cross functional members of the engineering organization to develop and evaluate interfaces between hardware and software, and operational performance requirements and design of the overall system
# • Support and participate in all phases of the software development life cycle, including requirements analysis, design, implementation, integration, and test of embedded software for real-time control of advanced tactical radio equipment
# • Develop software test procedures, software programs, and related documentation
# • Utilize modeling tools and equipment to establish operating data, conduct experimental tests, and evaluate results
# • Participate in peer reviews, identify, track and repair defects
# • Utilize a variety of software languages (i.e., C++, C#, C, Java, Ruby, HTML5, XML, SQL, Perl, Python, Ajax, Qt) on Windows, Linux, mobile platforms, and embedded real time operating systems (VxWorks, Linux, QNX, Integrity, Windows CE, and others for Motorola, Intel, TI, and custom processor designs)

# Qualifications:
# • Bachelor’s degree in Computer Science, Computer Engineering, Software Engineering, Electrical Engineering, Wireless Engineering, Information Security, Mathematics, Digital Arts & Sciences or related field
# • GPA of 3.0 or greater

# Preferred Skills:
# • One or more of the following: C++, C#, C, Java, Ruby, JEE, HTML5, XML, SQL, Qt, Windows, .NET, Unix, Linux, SOA, RTOS, Real-Time Controls, Wireless, Software Security, Robotics, OOA/OOD, Hadoop, Android, Embedded Systems""")

# colors = {"SKILL": "#F67DE3"}
# options = {"colors": colors} 

# spacy.displacy.render(doc, style="ent", options= options, jupyter=True)



import spacy
from spacy import displacy
from spacy.util import filter_spans
from spacy.tokens import DocBin
import DataCleaning
import json

# nlp = spacy.load("en_core_web_sm")
# doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

nlp = spacy.blank("en") # load a new spacy model
doc_bin = DocBin() # create a DocBin object

trainingData = DataCleaning.TSVParser()
# print(json.dumps(trainingData[0], indent=4))
doc = nlp.make_doc(trainingData[0]["text"])


entities = []
for start, end, word, label in trainingData[0]["annotations"]:
    print(start, end, word,label)
    span = doc.char_span(start, end, label=label, alignment_mode="strict")
    if span is None:
        print("Skipping entity")
    else:
        entities.append(span)
filtered_ents = filter_spans(entities)
doc.ents = filtered_ents 
doc_bin.add(doc)

# print(nlp.pipe_names)

# for ent in doc:
#     print(ent.text)
# Visualizer
html = displacy.render(doc, style="ent", page=True)
with open('visualizer.html', 'w') as htmlOutput:
    htmlOutput.write(html)
    htmlOutput.close()
