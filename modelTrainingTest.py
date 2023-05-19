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

# output spacy doc as HTML
def WriteHTML(doc):
    colors = {"SKILL": "#F67DE3"}
    options = {"colors": colors} 

    html = displacy.render(doc, style="ent", options= options, page=True)
    with open('visualizer.html', 'w') as htmlOutput:
        htmlOutput.write(html)
        htmlOutput.close()

# Creates docs using dataset, can specify if it should be labeled as training or test
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

# Creating training data with output paths 
def CreateTrainingData(outputPathTraining, outputPathTesting):
    trainingData = DataCleaning.GetTSVData(0.75) # Training split parameter
    
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

if __name__ == "__main__":
    
    CreateTrainingData("spaCyTesting/training.spacy", "spaCyTesting/testing.spacy")

    # nlp_ner = spacy.load("spacyTesting/model-last")

    # doc = nlp_ner(GetDoc())

    # WriteHTML(doc)
    
    print("hi")