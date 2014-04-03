import os,re

def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            if ".pyc" not in filename:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

def get_functions(path,type):
    searchfile = open(path, "r")
    fn_list = []
    for line in searchfile:
        if re.search("def.*\):", line):
            if type == 1:    #ignore Setup functions in tests
                if re.search("setUp", line):
                    continue
            fn_list.append(line)
    return fn_list

def parse_fn(fn):
    fn = fn.replace('\n','')
    fn = fn.replace('def ','')
    fn = fn.replace(' ','')
    return fn

# Run the above function and store its results in a variable.   
file_paths = get_filepaths("src/")
for _file in file_paths:
    print _file
    for fn in get_functions(_file,0):
        print "\t" ,parse_fn(fn)

file_paths = get_filepaths("test/")
for _file in file_paths:
    print _file
    for fn in get_functions(_file,1):
        print "\t" ,parse_fn(fn)
