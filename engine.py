from google import genai
from dotenv import load_dotenv
import os 

load_dotenv()

GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')

client = genai.Client(api_key=GEMINI_API_KEY)

#here  is prompt that instruct every things
# note: in the prompt include achievments,reference,question,personal_detail


                    # 1          2         3          4                5
def analysis_prompt(achievments,reference,question,personal_detail,instruction_prompt):
    # instruction_prompt gives all the information of how ai will execute this
    #of which it can even stay outside the function
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=instruction_prompt,
        config=""# this ensure limits the token,temperature,and easiest
    )

    return response.text 
achievements='i created software at school for grading'
reference="after saw the greatest challenging in grading at my school i use my passion in technology as the weapon to make the solution there where i made system software for gradding and i called it amanah grading"
question='tell me the time you notice the challenge in you community and desicide to make an action?'
personal_deatails='im a computer scince student,i won a science fair competition first position'
instruction_prompt=f"provide the proper guidance on the best way this student can understand the question:{question} and answer it based on the following information:achievements:{achievements},reference:{reference},personal_deatails:{personal_deatails}"

#print(analysis_prompt(achievements,reference,question,personal_deatails,instruction_prompt))
