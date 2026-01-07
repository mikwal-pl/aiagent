import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs a python file utilizing additional arguments (if provided) within a specified filepath, constrained to the working directory. ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The filepath of the file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Additional arguments to be used when running the file, such as function variables or prompts.",
            )
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    abs_work_dir = os.path.abspath(working_directory)
    new_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not new_path.startswith(abs_work_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(new_path):
        return f'Error: File "{file_path}" not found.'
    if not new_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        command = ["python", new_path]
        if args:
            command.extend(args)
        process = subprocess.run(command, capture_output=True, timeout=30, text=True, cwd=os.path.abspath(working_directory), )
        if not process.stdout and not process.stderr:
            return "No output produced"
        results = []
        if process.stdout:
            results.append(f"STDOUT:\n{process.stdout}")
        if process.stderr:
            results.append(f"STDERR:\n{process.stderr}")
        if process.returncode != 0:
            results.append(f"Process exited with code {process.returncode}")
        return "\n".join(results)
    except Exception as e:
        return f"Error: executing Python file: {e}"