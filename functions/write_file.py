import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="overwrites the content of a file within the specified filepath, constrained to the working directory. If the file doesn't exist beforehand, it is created.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath of the file to overwrite the content of, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="New content to be written into the file",
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    new_path = os.path.join(os.path.abspath(working_directory), file_path)
    if not new_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    #if not os.path.isfile(new_path):
        #return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
    except Exception as e:
        return f"Error: {e}"
    try:
        with open(new_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
