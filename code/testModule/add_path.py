import sys
import os

def add_subfolder_to_path( project_base_folder):        
    ## checking the input to the make file 
    current_folder = sys.argv[0]

    # if(len(sys.argv) > 1): 
    #     run_file = sys.argv[1]
    # else: 
    #     raise NoFileSelectedException


    ## Add all subfolders of the project into the system path
    for x in os.walk(project_base_folder): 
        folder_subfolders = (x[0])
        if(folder_subfolders in sys.path): 
            pass
        else: 
            sys.path.insert(1 , folder_subfolders)

class NoFileSelectedException(Exception): 
    pass