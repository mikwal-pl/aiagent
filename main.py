import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

prompt_given = False
for x in sys.argv[1:]:
    if x.startswith("--"):
        prompt_given = True
        prompt = x
if prompt_given == False:
    print("Prompt must be provided")
    sys.exit(1)


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]



def main():
    print("Hello from aiagent!")
    print("\n")
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt}")
        print("\n")
    print(response.text)
    if "--verbose" in sys.argv:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
