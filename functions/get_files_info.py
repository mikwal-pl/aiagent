import os
import sys

#project_path = "/home/lamahl/aiagent"
#argument = "."
#if len(sys.argv) > 1:
    #argument = sys.argv[1]

#print("Test:" + os.path.abspath("../"))

def get_files_info(working_directory, directory="."):
    #print(f"directory_abspath: {os.path.abspath(directory)}")
    test_path = os.path.join(working_directory, directory)
    dirpath = os.path.join(os.path.abspath(working_directory), directory)
    #print(f"dirpath: {dirpath}")
    #print(f"testpath: {os.path.abspath(test_path)}")
    match directory:
        case ("."):
            print("Result for current directory:")
        case _:
            print(f"Result for '{directory}' directory:")
    if not (os.path.abspath(test_path)).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(os.path.expanduser(dirpath)):
        return f'Error: "{directory}" is not a directory'
    for file in os.listdir(dirpath):
        filepath = os.path.join(dirpath, file)
        print(f"- {file}: file_size={os.path.getsize(filepath)} bytes, is_dir={os.path.isdir(filepath)}")

    

