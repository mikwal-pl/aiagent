#from functions.get_files_info import get_files_info
#from functions.get_file_content import get_file_content
#from functions.write_file import write_file
from functions.run_python_file import run_python_file

tests_get_files_info = [("calculator", "."), 
("calculator", "pkg"), 
("calculator", "/bin"),
("calculator", "../") 
]

tests_get_file_content = [("calculator", "main.py"),
("calculator", "pkg/calculator.py"),
("calculator", "/bin/cat"),
("calculator", "pkg/does_not_exist.py")]

tests_write_file = [("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
("calculator", "/tmp/temp.txt", "this should not be allowed")]

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
    #print(get_file_content("calculator", "lorem.txt"))