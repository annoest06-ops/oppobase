import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


                    # 1          2         3          4                5
def analysis_prompt(achievments, reference, question, personal_detail, instruction_prompt):
    try:
        response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=600,
    messages=[{"role": "user", "content": instruction_prompt}],
    extra_body={"temperature": 0.7}
)
        return response.content[0].text

    except anthropic.RateLimitError as e:
        print(f"[AI RATE LIMIT] {e}")
        return "Our AI coach is a bit busy right now. Please try again in a moment."

    except anthropic.APITimeoutError as e:
        print(f"[AI TIMEOUT] {e}")
        return "The AI coach took too long to respond. Please try again."

    except anthropic.APIConnectionError as e:
        print(f"[AI CONNECTION ERROR] {e}")
        return "We couldn't reach the AI coach right now. Please check back shortly."

    except anthropic.AuthenticationError as e:
        print(f"[AI AUTH ERROR] {e}")
        return "AI coaching is temporarily unavailable. Please contact support."

    except anthropic.APIStatusError as e:
        print(f"[AI API ERROR] status={e.status_code} body={e.response}")
        return "Something went wrong generating your coaching tip. Please try again."

    except Exception as e:
        print(f"[AI UNEXPECTED ERROR] {e}")
        return "An unexpected error occurred. Please try again later."