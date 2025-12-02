import os

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
