from backend import get_file_content
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

chat = model.start_chat(
    history=[
        {"role": "user", "parts": '''You are a helping chat bot on the Supreme Court of India website

Instructions:

1. Always return a dictionary as the output

2. {'user_type': 'backend'/'frontend', 'search_directory': True/False, 'diary_no': int, 'year': int, 'doc_type': 'daily_order'/'judgement'/'case_status'/'office_report', 'date': DD/MM/YYYY, 'chat': string}

3. search_directory: if true then python backend will search and return the doc to the user, false if user dont ask for any document.

4. search_directory, diary_no, year, doc_type should be deduced from the conversation with the frontend user. 

5. doc_type: None will by default all the information available about the case, date: 00/00/0000 returns documents for all days, all months and all years

6. Diary no. and year are required fields and in case of multiple diary no. int/int/int...  format should be used and corresponding years should be given in the same format, the no. of / in year and diary no. should be the same.

7. user_type parameter describe which user the response is forwarded to, if user type is backend then chat field should be empty and search_directory should be enabled. backend should only be contacted if needed to retrive the info. Else user type = frontend if normal conversation is going on.

8. All conversation other than concerning of case related information should be avoided by saying "I'm here to help with case related information"

9. Chat response should be given to the frontend user in there native language(22 scheduled languages) use english otherwise. 


Start a new session with the dictionary {'user_type': 'frontend', search_directory: False, 'diary_no': None, 'year': None, 'doc_type': None, 'date': '00/00/0000' , 'chat':  "How may I help you"}
Just return the dictionary, with no formatting
START NOW'''},

        {"role": "model", "parts": "{'user_type': 'frontend', 'search_directory': False, 'diary_no': None, 'year': None, 'doc_type': None, 'date': '00/00/0000', 'chat': 'How may I help you?'}"}
    ]
)



def call_api(prompt:str):
    response = chat.send_message(prompt)
    # print(response.text)
    response = eval(response.text)

    user = response["user_type"]
    return user, response

def get_response(user:str, prompt:str):
    
    if(user == "frontend"):
        prompt = f''' 'user': {user}, 'chat': {prompt}'''
    elif(user == "backend"):
        prompt = f''' 'user': {user}, 'response': {prompt}'''

    user, response = call_api(prompt)
    print(user)
    print(response)
    if (user == "frontend"):
        # print(response["chat"])
        return response["chat"] #Chat Field from the dictionary (String)
    
    elif(user == "backend"):
        prompt = get_file_content(response) #give dictionary
        print(prompt)
        prompt = f'''{prompt}'''
        # response = get_response(user= "backend", prompt=prompt)
        # print(response)
        return prompt
        
