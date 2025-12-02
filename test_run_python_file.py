from functions.run_python_file import run_python_file


tests_run_python_file = [("calculator", "main.py"),
("calculator", "main.py", ["3 + 5"]),
("calculator", "tests.py"),
("calculator", "../main.py"),
("calculator", "nonexistent.py"),
("calculator", "lorem.txt")]

if __name__ == "__main__":
    print(run_python_file("calculator", "main.py"))
    for args in tests_run_python_file:
        try:
            print(run_python_file(*args))
        except Exception as e:
            print(e)