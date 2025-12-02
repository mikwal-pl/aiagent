import os

def get_file_content(working_directory, file_path):
    new_path = os.path.join(os.path.abspath(working_directory), file_path)
    #print(f"Working directory: {os.path.abspath(working_directory)}")
    #print(f"file_path: {os.path.abspath(file_path)}")
    #print(f"new_path: {new_path}")
    if not new_path.startswith(os.path.abspath(working_directory)):
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