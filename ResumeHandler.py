from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI


# Analyze resumes
def GetResumeResult(pdfDocs, userQuestion):   
     pdfDict = dict()
     for pdfDoc in pdfDocs:
          pdfReader = PdfReader(pdfDoc)
          pdfName = pdfDoc.name
          pdfText = ""
          for pdfPage in pdfReader.pages:
               pdfText += pdfPage.extract_text() 

          pdfAnalysis = GetCVTextAnalysis(pdfText, userQuestion)
          #pdfSentiment = testSent.GetSentimentScore(pdfAnalysis)
          pdfDict[pdfName] = [{ 'analysis': pdfAnalysis, 'sentiment': '' }]
     
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


