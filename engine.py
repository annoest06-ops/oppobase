from google import genai
from google.genai import types
from dotenv import load_dotenv
import os 

load_dotenv()

GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')

client = genai.Client(api_key=GEMINI_API_KEY, vertexai=False)
print(repr(GEMINI_API_KEY))

#here  is prompt that instruct every things
# note: in the prompt include achievments,reference,question,personal_detail


                    # 1          2         3          4                5
def analysis_prompt(achievments,reference,question,personal_detail,instruction_prompt):
    # instruction_prompt gives all the information of how ai will execute this
    #of which it can even stay outside the function
  try:
    response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=instruction_prompt,
    config=types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.9,
        top_k=40,
        max_output_tokens=600,
        candidate_count=1,
        thinking_config=types.ThinkingConfig(thinking_level="MINIMAL"),
    )
)
    return response.text 
  except Exception as e:
    return f"An error occurred: {str(e)}"

# print(analysis_prompt(achievements,reference,question,personal_deatails,instruction_prompt))
