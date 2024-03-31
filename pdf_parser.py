import os

import PyPDF2
import openai
from dotenv import load_dotenv
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
import os

from openai import OpenAI

load_dotenv()

# Read from the PDF file
pdf_file = open('sample.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)
num_pages = len(pdf_reader.pages)
detected_text = ''

for page_num in range(num_pages):
    page_obj = pdf_reader.pages[page_num]
    detected_text += page_obj.extract_text() + '\n\n'

pdf_file.close()

detected_text = """
I had installed packages with python 3.9.7 but this version was causing issues so I switched to Python 3.10. When I installed the langhcain it was in python 3.9.7 directory. If yo run pip show langchain, you get this
"""


open_ai_api_key = os.getenv("OPEN_AI_API_KEY")

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# texts = text_splitter.create_documents([detected_text])
#
# directory = 'index_store'
# vector_index = FAISS.from_documents(texts, OpenAIEmbeddings())
# vector_index.save_local(directory)
#
# vector_index = FAISS.load_local('index_store', OpenAIEmbeddings())
# retriever = vector_index.as_retriever(search_type="similarity", search_kwargs={"k":6})
# qa_interface = RetrievalQA.from_chain_type(llm=ChatOpenAI(openai_api_key=open_ai_api_key), chain_type="stuff", retriever=retriever, return_source_documents=True)
#
# response = qa_interface(
#     "List some questions from the content"
# )



system_msg = ""

query = """
summarize content.
"""

open_ai_api_key = os.getenv("OPEN_AI_API_KEY")
openai.api_key = open_ai_api_key

user_msg = detected_text + "\n\n" + query

print(open_ai_api_key)
client = OpenAI(
    # This is the default and can be omitted
    api_key=open_ai_api_key,
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "What is your name?"},
    ],
)

print(response)
