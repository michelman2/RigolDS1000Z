import sys
import os
from pathlib import Path
""" 
    The file makes paths avaiable to python interpreter
    has to be added before using a project hierarchy
"""

def add_subfolder_to_path( project_base_folder):        

    """ 
        Function iterates over all folders and subfolders of
        current folder and add everything to the path
        
    """
    for x in os.walk(project_base_folder): 
        folder_subfolders = (x[0])
        if(folder_subfolders in sys.path): 
            pass
        else: 
            sys.path.insert(1 , folder_subfolders)





path = Path(os.getcwd()).parent
add_subfolder_to_path(path)