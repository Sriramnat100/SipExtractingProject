import pandas as pd
import numpy as np
import textract
import os
import re
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
from rake_nltk import Rake

filename = 'lecture.pdf'

#opening and reading through file
pdfFileObj = open(filename,'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

#Determing Number of Pages for while loop
num_pages = pdfReader.numPages                
count = 0
text = ""

stop = 'References'   

#While loop iterates through each page
while count < num_pages:          
                 
    pageObj = pdfReader.getPage(count)
    
    count +=1
    
    text += pageObj.extractText()
    
    if re.search(text,stop):
        break
#Below if statement exists to check if the above library returned #words. It's done because PyPDF2 cannot read scanned files.

if text != "":
    text = text

r = Rake()  
r.extract_keywords_from_text(text)

phrases = r.get_ranked_phrases_with_scores()

#This Method was used by the RAKE library
table = pd.DataFrame(phrases,columns=['score','Phrase'])

table = table.sort_values('score',ascending=False)

topics = table.head(30)

print(table.head(30))


f= open("keywords.txt","w+")
f.write(topics)
