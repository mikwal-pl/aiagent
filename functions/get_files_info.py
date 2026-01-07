import os
import sys
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory="calculator", directory="."):
    #print(f"directory_abspath: {os.path.abspath(directory)}")
    test_path = os.path.join(working_directory, directory)
    dirpath = os.path.join(os.path.abspath(working_directory), directory)
    #print(f"dirpath: {dirpath}")
    #print(f"testpath: {os.path.abspath(test_path)}")
    results = []
    #match directory:
        #case ("."):
            #print("Result for current directory:")
        #case _:
            #print(f"Result for '{directory}' directory:")
    if not (os.path.abspath(test_path)).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(os.path.expanduser(dirpath)):
        return f'Error: "{directory}" is not a directory'
    for file in os.listdir(dirpath):
        filepath = os.path.join(dirpath, file)
        info = [file, os.path.getsize(filepath), os.path.isdir(filepath)]
        results.append(info)
        #print(f"- {file}: file_size={os.path.getsize(filepath)} bytes, is_dir={os.path.isdir(filepath)}")
    return results

    

