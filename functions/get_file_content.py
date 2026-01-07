import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="displays content of a file within a specified filepath, constrained to the working directory. If file's length is over 10 000 characters, the content displayes is shortened to the first 10 000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath of the file to get content of, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    new_path = os.path.join(working_directory, file_path)
    #print(f"Working directory: {os.path.abspath(working_directory)}")
    #print(f"file_path: {os.path.abspath(file_path)}")
    #print(f"new_path: {new_path}")
    if not (os.path.abspath(new_path)).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(new_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    with open(new_path) as f:
        contents = f.read()
        if len(contents) > 10000:
            return f"{contents[:10000]} [...File '{file_path}' truncated at 10000 characters]"
        else:
            return contents



if __name__ == "__main__":
    get_file_content("calculator", "main.py")