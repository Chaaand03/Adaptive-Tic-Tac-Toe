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

    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "user", "content": "What is your name?"},
    #     ],
    # )

    response = """
!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Homework Questions</title>
</head>
<body>

<!-- Easy Questions -->
<h3>Easy Questions</h3>

<!-- Question 1 -->
<p data-question="true">What are the two parts of the homework assignment?</p>
<ol type="a">
  <li data-answer="false">Part A and Part B</li>
  <li data-answer="true">Part 1 and Part 2</li>
  <li data-answer="false">Part I and Part II</li>
  <li data-answer="false">Section 1 and Section 2</li>
</ol>

<!-- Question 2 -->
<p data-question="true">What is prohibited in the completion of the programming portion?</p>
<ol type="a">
  <li data-answer="true">Use of any AI resources</li>
  <li data-answer="false">Collaboration with classmates</li>
  <li data-answer="false">Referencing online sources</li>
  <li data-answer="false">Using pre-existing code libraries</li>
</ol>

<!-- Question 3 -->
<p data-question="true">How should the comprehension portion be submitted?</p>
<ol type="a">
  <li data-answer="false">As handwritten submissions</li>
  <li data-answer="true">As a single PDF file on Gradescope</li>
  <li data-answer="false">Typed along with work on Moodle</li>
  <li data-answer="false">In individual text files</li>
</ol>

<!-- Question 4 -->
<p data-question="true">What should be done with the NotImplementedError() lines in the programming portion?</p>
<ol type="a">
  <li data-answer="false">Leave them unchanged</li>
  <li data-answer="false">Comment them out</li>
  <li data-answer="true">Delete and throw them</li>
  <li data-answer="false">Modify them for personal use</li>
</ol>

<!-- Question 5 -->
<p data-question="true">How should group members be added for submission?</p>
<ol type="a">
  <li data-answer="false">By directly emailing the instructor</li>
  <li data-answer="true">Through the Gradescope interface</li>
  <li data-answer="false">By creating a shared Google Drive folder</li>
  <li data-answer="false">Adding them manually in the PDF file</li>
</ol>

<!-- Medium Questions -->
<h3>Medium Questions</h3>

<!-- Question 6 -->
<p data-question="true">What is the deadline for submitting the comprehension portion?</p>
<ol type="a">
  <li data-answer="false">February 11th, 11:45 PM</li>
  <li data-answer="false">February 18th, 11:45 PM</li>
  <li data-answer="true">The deadline is not provided in the text</li>
  <li data-answer="false">February 1st, 11:45 PM</li>
</ol>

<!-- Question 7 -->
<p data-question="true">What must be added to the top of the Python Jupyter notebook file?</p>
<ol type="a">
  <li data-answer="false">Name and date of submission</li>
  <li data-answer="false">Name and email address</li>
  <li data-answer="true">Name and group number</li>
  <li data-answer="false">Group members' names and Unity IDs</li>
</ol>

<!-- Question 8 -->
<p data-question="true">Where can the programming portion be edited?</p>
<ol type="a">
  <li data-answer="false">Only on Moodle</li>
  <li data-answer="true">On Google Colab or on your own computer</li>
  <li data-answer="false">Exclusively on Gradescope</li>
  <li data-answer="false">On GitHub repositories</li>
</ol>

<!-- Question 9 -->
<p data-question="true">How should the comprehension portion be submitted if there are multiple group members?</p>
<ol type="a">
  <li data-answer="false">Each member should submit individually</li>
  <li data-answer="true">Only one member should upload it, adding group members at the end of the process</li>
  <li data-answer="false">All members should upload separately</li>
  <li data-answer="false">Each member should merge their responses into one PDF</li>
</ol>

<!-- Question 10 -->
<p data-question="true">What is required for the programming portion to ensure it produces the correct results?</p>
<ol type="a">
  <li data-answer="true">Filling in places marked "YOUR CODE HERE" or "YOUR ANSWER HERE"</li>
  <li data-answer="false">Adding extensive comments to the code</li>
  <li data-answer="false">Modifying the formatting of the code</li>
  <li data-answer="false">Including additional functions beyond the requirements</li>
</ol>

<!-- Difficult Questions -->
<h3>Difficult Questions</h3>

<!-- Question 11 -->
<p data-question="true">What action is considered a violation of academic integrity in the programming portion?</p>
<ol type="a">
  <li data-answer="false">Using pre-written Python libraries</li>
  <li data-answer="false">Consulting with classmates</li>
  <li data-answer="false">Modifying the original instructions</li>
  <li data-answer="true">Using any AI resources</li>
</ol>

<!-- Question 12 -->
<p data-question="true">How should the submission be named for the comprehension portion?</p>
<ol type="a">
  <li data-answer="false">G(assignment number) P(part number)</li>
  <li data-answer="true">G(homework group number) HW(homework number)</li>
  <li data-answer="false">Group_(group number)Assignment(assignment number)</li>
  <li data-answer="false">Submission_(date)_(group number)</li>
</ol>

<!-- Question 13 -->
<p data-question="true">What is the recommended method for editing the Jupyter notebook file?</p>
<ol type="a">
  <li data-answer="true">Editing on Google Colab or on your own computer</li>
  <li data-answer="false">Editing directly on the Moodle platform</li>
  <li data-answer="false">Editing using a text editor with limited features</li>
  <li data-answer="false">Editing through email attachments</li>
</ol>

<!-- Question 14 -->
<p data-question="true">What is the significance of adding group members at the end of the submission process?</p>
<ol type="a">
  <li data-answer="false">To notify the instructor of group collaboration</li>
  <li data-answer="true">To ensure all members are recognized for participation</li>
  <li data-answer="false">To indicate the order of group member contributions</li>
  <li data-answer="false">To validate the authenticity of the submission</li>
</ol>

<!-- Question 15 -->
<p data-question="true">What should be done if a question asks for an explanation or justification of an answer?</p>
<ol type="a">
  <li data-answer="false">Providing references only to online sources</li>
  <li data-answer="true">Giving a brief explanation using your own ideas or referencing the course textbook</li>
  <li data-answer="false">Ignoring the request and providing only the answer</li>
  <li data-answer="false">Consulting with group members for a collective response</li>
</ol>

</body>
</html>
"""

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

