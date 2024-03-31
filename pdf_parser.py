import os
import PyPDF2
import openai
from dotenv import load_dotenv
import bs4 as bs
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
import os

from openai import OpenAI

def parse_pdf_questions(pdf_file):
    load_dotenv()

    # Read from the PDF file

    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    detected_text = ''

    for page_num in range(num_pages):
        page_obj = pdf_reader.pages[page_num]
        detected_text += page_obj.extract_text() + '\n\n'

    pdf_file.close()

    print(detected_text)

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
    Generate 5 each easy , medium and difficult multiple choice questions from the above content. Give in HTML format along with questions having data-question attribute true and answers having the data-attribute set to true for correct answer
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
            {"role": "user", "content": query},
        ],
    )

    print(response)



    soup = bs.BeautifulSoup(response, 'lxml')
    questions = soup.find_all(attrs={"data-question": True})
    questions_text = []
    for item in questions:
        questions_text.append(item.text.strip())

    answers_text = []
    correct_answers_text = []

    answers = soup.select("[data-answer]")
    for item in answers:
        answers_text.append(item.text.strip())
        if item["data-answer"] == "true":
            correct_answers_text.append(item.text.strip())

    data = {}
    data["questions"] = questions_text
    data["answers"] = answers_text
    data["correct_answers"] = correct_answers_text

    return data

