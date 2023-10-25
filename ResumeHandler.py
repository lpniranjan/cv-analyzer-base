from PyPDF2 import PdfReader,PdfFileReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# Analyze resumes
#Single resume analysis

def GetSingleResumeResult(pdfDoc, userQuestion,jobTitle):   
     pdfDict = dict()
     pdfReader = PdfReader(pdfDoc)
     pdfName = pdfDoc.name
     pdfText = ""
     for pdfPage in pdfReader.pages:
          pdfText += pdfPage.extract_text() 

     texts = GetCVTextChunkAnalysis(pdfText)

     pdfAnalysis = GetResumeAnalysis(userQuestion, texts)
     linkedinURL = GetResumeAnalysis("what is the LinkedIn URL of this resume?", texts)
     if "The LinkedIn URL of this resume is" in linkedinURL: 
      linkedinURL = linkedinURL.replace("The LinkedIn URL of this resume is", "")     
     if "This resume does not have a LinkedIn URL." in linkedinURL or "There is no LinkedIn URL in this resume." in linkedinURL: 
      linkedinURL = ""
     
     githubURL = GetResumeAnalysis("what is the github URL of this resume?", texts)
     if "The GitHub URL of this resume is" in githubURL: 
      githubURL = githubURL.replace("The GitHub URL of this resume is", "") 
     if "This resume does not have a GitHub URL." in githubURL or "There is no GitHub URL in this resume." in githubURL: 
      githubURL = ""

     facebookURL = GetResumeAnalysis("what is the FaceBook URL of this resume?", texts)
     if "The Facebook URL of this resume is" in facebookURL: 
      facebookURL = facebookURL.replace("The Facebook URL of this resume is", "") 
     if "This resume does not have a Facebook URL." in facebookURL or "There is no Facebook URL in this resume." in facebookURL: 
      facebookURL = ""

     candidateEmail = GetResumeAnalysis("what is the candidate email of this resume?", texts).replace("The candidate email is ", "")
     jobDescription = GetJobDescription(jobTitle)
     pdfDict[pdfName] = [{ 'analysis': pdfAnalysis, 'jobDescription': jobDescription, 'linkedinURL': linkedinURL, 'githubURL': githubURL, 'facebookURL': facebookURL, 'candidateEmail': candidateEmail }]
          
     return pdfDict 

def GetCVTextChunkAnalysis(cvContent):

     text_splitter = CharacterTextSplitter(
     separator="\n",
     chunk_size= 800,
     chunk_overlap=200,
     length_function=len
     )
     texts = text_splitter.split_text(cvContent)
     return texts

def GetResumeAnalysis(userQuestion, texts):
     cvAnalysis =""

     embeddings = OpenAIEmbeddings()
     document_search = FAISS.from_texts(texts,embeddings)
     
     chain = load_qa_chain(OpenAI(), chain_type="stuff")
     query = "{jdTitle}".format(jdTitle = userQuestion)
     docs = document_search.similarity_search(query)
     cvAnalysis = chain.run(input_documents=docs,question=query)
     return cvAnalysis

def GetJobDescription(jobTitle):
     cvAnalysis =""
     llm = OpenAI(temperature=0.9)

     prompt = PromptTemplate(
     input_variables=["jobTitle"],
     template="What is the description of {jobTitle} ?",
     )
     chain = LLMChain(llm=llm, prompt=prompt)
     cvAnalysis = chain.run({"jobTitle":jobTitle})
     return cvAnalysis

#End single resume analysis

#Multple resume analysis

def GetResumeResult(pdfDocs, userQuestion):   
     pdfDict = dict()
     for pdfDoc in pdfDocs:
          pdfReader = PdfReader(pdfDoc)
          pdfName = pdfDoc.name
          pdfText = ""
          for pdfPage in pdfReader.pages:
               pdfText += pdfPage.extract_text() 

          pdfAnalysis = GetCVTextAnalysis(pdfText, userQuestion)
          jobDescription = GetJobDescription('.NET developer')
          pdfDict[pdfName] = [{ 'analysis': pdfAnalysis, 'JD': jobDescription }]
     
     return pdfDict  


def GetCVTextAnalysis(cvContent, userQuestion):
     cvAnalysis =""

     text_splitter = CharacterTextSplitter(
     separator="\n",
     chunk_size= 800,
     chunk_overlap=200,
     length_function=len
     )
     texts = text_splitter.split_text(cvContent)

     embeddings = OpenAIEmbeddings()
     document_search = FAISS.from_texts(texts,embeddings)
     
     chain = load_qa_chain(OpenAI(), chain_type="stuff")
     query = "{jdTitle}".format(jdTitle = userQuestion)
     docs = document_search.similarity_search(query)
     cvAnalysis = chain.run(input_documents=docs,question=query)
     return cvAnalysis

#End multiple resume analysis