import os
import sys
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

prompt = ""
args = []
for x in sys.argv[1:]:
    if not x.startswith("--"):
        args.append(x)
prompt = " ".join(args)
if prompt == "":
    print("Prompt must be provided")
    sys.exit(1)
verbose = False
if "--verbose" in sys.argv:
    verbose = True


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
)

def call_function(function_call_part, verbose_arg=False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    function_args["working_directory"] = "./calculator"
    print(function_args)
    functions_dict = {"get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
    }
    functions_list = ["get_file_content", "get_files_info", "run_python_file", "write_file"]
    if verbose_arg:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f"Calling function: {function_name}")
    if function_name not in functions_dict:
        return types.Content(
        role="tool",
        parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},)],)
    #elif function_name == "get_files_info":
        #function_result = get_files_info(**function_args)
        #return types.Content(
        #role="tool",
        #parts=[
        #types.Part.from_function_response(
           # name=function_name,
           # response={"result": function_result},)],)
    else:
        function_result = functions_dict[function_name](**function_args)
        return types.Content(
        role="tool",
        parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},)],)


def main():
    print("Hello from aiagent!")
    print("\n")
    if verbose:
        print(f"User prompt: {prompt}")
        print("\n")
    count = 0
    while count < 20:
        count +=1
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
                )
            for c in response.candidates:
                messages.append(c.content)
            if not response.function_calls and response.text:
                print(f"Agent response: {response.text}")
                break
            if response.usage_metadata == None:
                raise RuntimeError("Error: An API request likely failed. Please try again in a moment")
            if response.function_calls:
                #responses_list = []
                for call in response.function_calls:
                    print("MODEL CALLED:", call.name, call.args)
                    results = call_function(call, verbose)
                    if results.parts[0].function_response.response:
                        #responses_list.extend(results.parts)
                        messages.append(results)
                    else:
                        raise Exception("Fatal error occured")
                    if verbose:
                        print(f"-> {results.parts[0].function_response.response}")
                    print("\n")
                #messages.append(types.Content(role="user", parts=responses_list))
                if not response.text:
                    print("No text response, agent called functions instead")
            if response.text:
                print(f"Agent response: {response.text}")
                print("\n")
            print("---Conversation so far---")
            for m in messages:
                print(f"Role: {m.role}")
                for p in m.parts:
                    print("  text:", getattr(p, "text", None))
                    print("  call:", getattr(p, "function_call", None))
                    print("  resp:", getattr(p, "function_response", None))
            print("===========================")
        except Exception as e:
            print(e)
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
