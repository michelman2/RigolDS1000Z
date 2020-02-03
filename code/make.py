import sys 
import os
import importlib


class NoFileSelectedException(Exception): 
    pass 

## checking the input to the make file 
current_folder = sys.argv[0]

if(len(sys.argv) > 1): 
    run_file = sys.argv[1]
else: 
    raise NoFileSelectedException


## Add all subfolders of the project into the system path
for x in os.walk(os.getcwd()): 
    folder_subfolders = (x[0])
    if(folder_subfolders in sys.path): 
        pass
    else: 
        sys.path.insert(1 , folder_subfolders)


## Running the file

## run_file
try: 
    ## using run_file like this to preserve sys.path as the run_file is running
    ## IMPORTANT: if the imported file is not a python module, it will raise an error after sourcing the file
    ## A module is made by adding a __init__.py file (might remain empty) in a folder
    mod = __import__(run_file)

except Exception as e:     
    raise 
