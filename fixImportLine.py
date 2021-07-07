import os

FOLDER = os.path.join(os.getcwd(), "ui")

lineToInsert = "from . import Resource_rc"

for currentPath, folders, files in os.walk(FOLDER):
    for file in files:
        extension = file.split(".")[1]
        if extension == "py" and file != "__init_.py" and file != "Resource_rc.py":
            with open(os.path.join(currentPath, file), mode="r", newline="\n") as f:
                lines = f.readlines()
                lines[-1] = lineToInsert
            
            with open(os.path.join(currentPath, file), mode="w", newline="\n") as f:
                f.writelines(lines)
    break