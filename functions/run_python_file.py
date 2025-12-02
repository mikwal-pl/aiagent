import os
import subprocess

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