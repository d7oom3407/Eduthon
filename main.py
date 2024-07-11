import streamlit as st
import google.generativeai as genai
import pandas as pd

GEMINI_API = '**********'

def gemini(input, df=None, num_team=5, history=''):
    genai.configure(api_key="GEMINI-API)

    # Set up the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    convo = model.start_chat(history=[
    {
        "role": "user",
        "parts": [history]
    },
    {
        "role": "model",
        "parts": ["حسناً!"]
    },
    ])

    convo.send_message(input)
    return convo.last.text

df = pd.read_excel('students_data.xlsx')

df = df.drop('ID', axis=1)

chat_history = f"heres a database about students containing their skills, and proformence in the project in respect to their task. im going to ask you about them. if I asked you about a certain student, tell me about their strengths and weaknesses. an example of how you can know a weakness they have is if they were given a task for the project and they did not preform well on it. i may give you a project description, if i do, i want you to give me the best split of students that fit the projects skill level, requirements, and description. each group must contain 5 members, in one team. do not put any effects in your response. i expect your response to be fully in arabic, so translate anything that is written in english. do not say a word in english. {df}"
project_history = f"Im going to give you a project discreption and i want you to tell me what skills does the team doing the project need to have. if possible, give what level of skill proffeciency is required for the project. for example: 10% business analysis, 30% data architicture, 90% front-end development, and dont be limited to these skills, this is just an example. i expect your response to be fully in arabic, so translate anything that is written in english. do not say a word in english."

user_input = st.text_input('ماهو وصف المشروع؟')
if st.button('إرسال المشروع'):
    res = gemini(user_input, history=project_history)
    st.write(res)

user_input1 = st.text_input('من هو الطالب الذي تريد السؤال عنه؟')
if st.button('إرسال الطالب'):
    res = gemini(user_input1, history=chat_history)
    st.write(res)
    
