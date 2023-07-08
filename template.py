import os
import logging
from pathlib import Path

'''template.py creates the required folder structure automatically'''

logging.basicConfig(level=logging.INFO,format='[%(asctime)s]: %(message)s:')

file_list = [
    # src folder
    "src/__init__.py",
    # src/logging file
    "src/logging.py",
    # src/exception file
    "src/exception.py",
    # src/utils file
    "src/utils.py",

    # src/components folder
    "src/components/__init__.py",
    # src/pipeline folder
    "src/pipeline/__init__.py",
]

for file in file_list:
    filepath = Path(file)
    filedir,filename=os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Created directory {filedir} for the file {filename}")
    
    if (not os.path.exists(filepath)):
        with open(filepath,'w') as f:
            pass
        logging.info(f"Created empty file {filename}")
    
    else:
        logging.info(f"{filename} already exists")

