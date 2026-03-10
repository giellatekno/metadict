"""
This script prompts the user to enter a class name and generates a new Python class file with the specified name in the 'classes' directory.
Additionally, it updates the 'classes/__init__.py' file to include an import statement for the newly created class.
If the class file already exists, the script notifies the user.
"""

import os

class_name = (
    input("Enter the name you want associated with the dictionary (one word): ")
    .strip()
    .replace(" ", "")
)
file_path = f"classes/{class_name.lower()}_parser.py"

if not os.path.exists(file_path):
    with open(file_path, "w") as f:
        f.write(f"""from utils.dataclasses import Article, Dictionary

class {class_name.capitalize()}Parser:
    def __init__(self, dictionary_id, file):
        self.dictionary = Dictionary(
            id=dictionary_id,
            name="",
            lang1="",
            lang2="",
            closed=True,
            author="",
            date_published="",
            isbn="",
        )
        self.articles = self.parse_dict(file)

    def get_parsed_data(self):
        return self.dictionary, self.articles
    
    def parse_dict(self, file):
        articles = []
        
        # Implement parsing logic here
        
        return articles
        
    def to_html(self):
        # Implement HTML formatting logic here
        pass
    """)
    print(f"Class {class_name} created in {file_path}")

    with open("classes/__init__.py", "a") as f:
        f.write(
            f"from .{class_name.lower()}_parser import {class_name.capitalize()}Parser\n"
        )
    print(f"Imported {class_name} in classes/__init__.py")

else:
    print("Class already exists!")
