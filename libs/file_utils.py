#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 26 09:35:57 2025

@author: russ and chat
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 25 09:21:26 2025

@author: russ not quite vibe coded




"""

# ---- tof


from functools import partial
from dataclasses import dataclass
from typing import Callable, Any, Dict, Optional
from pathlib import Path



# ---- lets define some useful filtering functions -- use with partial as in test
def all_true( file_name, *, invert_logic = False):
    """always true unless logic is inverted  """
    return not invert_logic


# ------------------------------
def file_name_has_extension( file_name, *, ext_list, invert_logic = False ):
    """
    Checks if a filename ends with any of the provided extensions.
    note use of lower
    'extensions' should be a list/tuple of strings like ['.py', '.txt']

    foo    = partial( file_name_has_extension,  [".py"]  )

    """
    # Convert list to tuple because str.endswith() requires a tuple for multiple suffixes
    is_true     = str(file_name).lower().endswith(tuple(ext.lower() for ext in ext_list ))

    if invert_logic:
        return not is_true
    else:
        return is_true


# def file_name_starts_with( file_name, *, prefix_list ) :
#     """
#     Checks if a filename has a prefix on prefix_list

#     'prefix_list' should be a list/tuple of strings
#     """

#     file_path           = Path( file_name )
#     file_path_name      = file_path.name
#     for i_prefix in prefix_list:
#         if file_path_name.startswith( i_prefix ):
#             return True
#     return False

# ------------------------------
def fewer_slashes( file_name, ):
    """
    sort of sucks, but for now works
    """
    file_name    = file_name.replace( "///", "/" )
    file_name    = file_name.replace( "//",  "/" )
    return file_name

# ------------------------------
def file_name_starts_with( file_name, *, prefix_list ):
    """
    Checks if a filename has a prefix in prefix_list.
    Handles both string paths and Path objects.
    """
    # Convert list to tuple: str.startswith() accepts a tuple for bulk checking
    return Path(file_name).name.startswith(tuple(prefix_list))

# ----------------------------
def path_name_starts_with( path_name, *, prefix_list = [ "txt" ], invert_logic  = False ):
    """
    Checks if a name, file or dir,  has a prefix in prefix_list.
    Handles both string paths and Path objects.
    invert logic for exclusing
    """
    # Convert list to tuple: str.startswith() accepts a tuple for bulk checking
    # name      = Path(path_name).name


    is_true   = Path(path_name).name.startswith(tuple(prefix_list))

    if invert_logic:
        print( f">>>{not is_true} {Path(path_name).name}" )
        return not is_true
    else:
        print( f">>>{is_true} {Path(path_name).name}" )
        is_true

# ----------------------------
def file_iterator_for_all( root_dir,   ):
    """
    any file any depth
    could make variations on this with a file and or dir filter
    """

    file_filter         = all_true
    dir_filter          = all_true

    fi_config           = FileFilterConfig(
                                file_ok     = file_filter,
                                dir_ok      = dir_filter,
                                max_depth   = -1,
                                initial_dir = root_dir )

    file_iterator    = FileIterator(  config = fi_config   )

    return file_iterator

# ----------------------------
def file_iterator_for_py( root_dir,   ):
    """
    any file except
            __pycache__
            virtual env   =  .venv.
            hidden        = .xxxx


            zz
    any depth

    """

    file_filter         = all_true
    dir_filter          = path_name_starts_with( )

    fi_config           = FileFilterConfig(
                                file_ok     = file_filter,
                                dir_ok      = dir_filter,
                                max_depth   = -1,
                                initial_dir = root_dir )

    file_iterator    = FileIterator(  config = fi_config   )

    return file_iterator




# ----------------------------
@dataclass
class FileFilterConfig:
    """
    Stores the criteria for the file search with all fields optional.
    """
    # Predicates
    file_ok: Optional[Callable[[Path], bool]] = None
    dir_ok:  Optional[Callable[[Path], bool]] = None

    # Logic and Data
    file_action: Optional[Callable[..., None]] = None
    more_args_dict: Optional[Dict[str, Any]]   = None

    # Pathing and Constraints
    initial_dir:  Optional[Path]     = None
    initial_dest: Optional[Path]     = None   #or in more args?

    max_depth:    Optional[int]      = None

# may want a class or data class like thing as the thing that come back from next


# ------------------------------
class FileIterator:
    def __init__(self, *, config: FileFilterConfig ):
        """
        This itterates down a directory tree with some selection ( which is really very complete )
        set

        root_dir   = starting directory
        in the FileFilterConfig
            the depth
            max_depth = 0: It will only look at files in the root_dir. It will see subdirectories but refuse to enter them because 0 < 0 is False.

            max_depth = -1: for unlimited

            max_depth = float('inf'):   "unlimited" depth   Since any integer will always be less than infinity, the check will always pass.

            a function that says if the file is ok, based on anything but see some utils above
            a function that says if the directory is ok, again based on anything


            file_filter        = partial( file_name_has_extension,  ext_list = [ "py"] )



            dir_filter         = partial( path_name_starts_with, prefix_list = [ "old" ], invert_logic = True )

        # or all_true
        file_filter     = file_utils.all_true
        dir_filter      = file_utils.all_true

        fi_config        = file_utils.FileFilterConfig(
                        file_ok   = file_filter,
                        dir_ok    = dir_filter,
                        max_depth = 2  )


        file_utils.FileIterator( root_dir = "./", config = fi_config   )

        for ix, i_file in enumerate( file_iterator):
            print( f"{ix} {i_file}" )


        """
        self.root_dir   = Path( config.initial_dir )
        self.config     = config

        # Initialize the stack
        if self.config.dir_ok( self.root_dir ):
            self.stack = [[self.root_dir.iterdir(), 0]]

        else:
            self.stack = []

        pass

    # ------------------------------
    def __iter__(self):
        return self

    # ------------------------------
    def __next__(self):
        """
        think return path objects need to double check

        """
        while self.stack:
            current_iter, current_depth = self.stack[-1]

            try:
                entry = next(current_iter) # what is it  -- a path

                if entry.is_dir():
                    # Use config to check if we should enter this directory
                    if ( ( self.config.max_depth <0 or current_depth < self.config.max_depth ) and
                            ( self.config.dir_ok(entry) ) ):
                        self.stack.append([entry.iterdir(), current_depth + 1])
                        return entry   # we may need to deal with them as well
                        print( "do we get here =============================================")
                    else:
                        continue

                # Use config to check if we should return this file
                if entry.is_file() and self.config.file_ok(entry):
                    return entry

            except StopIteration:
                self.stack.pop()

            except PermissionError:
                self.stack.pop()

        raise StopIteration

# ---- tests
# -----------------------------
def rpt_test( correct, function,  path, ):

    """
    """
    test_correct   = function( path )
    is_ok  = test_correct == correct
    if is_ok:
        is_ok = "ok"

    else:
        is_ok = "NG"

    msg    = f"{is_ok} {test_correct} {path}"
    print( msg )

# -----------------------------
def test_file_iterator():

    """
    # --- How to use it now ---
    this makes filters from scratch, we might
    instead want to use the ones at top of file
        will have another test using that


    """
    # 1. Define your filter logic
    def my_file_filter( path ):   return path.suffix == '.py'

    def my_dir_filter( path ):    return 'temp' not in path.name

    # 2. Package it into a config object
    config = FileFilterConfig(
        file_ok   = my_file_filter,
        dir_ok    = my_dir_filter,
        max_depth = 2
                       )
    file_iterator    = FileIterator( root_dir = "./", config = config   )
    for i_file in file_iterator:
        print( f"{i_file}" )

# --------------------------------
def test_file_iterator_2():

    """
    # --- How to use it now ---
    this makes filters from partial


    """
    root_dir    = "./"
    root_dir    = "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib"
    root_dir    = "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/autoexec"

    print( f"test_file_iterator_2  {root_dir}")

    # Define your filter logic functions
    my_file_filter        = partial( file_name_has_extension,  ext_list = [ "py"] )
          #  .py only
    # my_file_filter        = all_true

    my_dir_filter         = partial( path_name_starts_with, prefix_list = [ "old" ], invert_logic = True )
    # my_dir_filter         = all_true
    # my_dir_filter         = partial( all_true, invert_logic = False )

    # 2. Package it into a config object
    config = FileFilterConfig(
        file_ok     = my_file_filter,
        dir_ok      = my_dir_filter,
        initial_dir = root_dir,
        max_depth   = -1,
                       )
    file_iterator    = FileIterator( config = config   )
    for ix, i_file in enumerate( file_iterator ):
        print( f"    {ix} {i_file}   {i_file.is_dir() = }" )


    print( "test_file_iterator_2 done")

#----------------------
def test_file_iterator_for_all():

    """
    for all


    """
    root_dir    = "./"
    root_dir    = "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib"

    print( f"test_file_iterator_for_all  {root_dir}")
    file_iterator    = file_iterator_for_all(  root_dir = root_dir   )

    for ix, i_file in enumerate( file_iterator):
        print( f"    {ix} {i_file}  {i_file.is_dir()}" )

    print( "test_file_iterator_for_all done")


# def test():


#     # 3. Pass the config to the iterator
#     files = FileIterator('/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib', config)
#     #files = FileIterator('/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib', is_python_file, max_depth=2)
#     for f in files:
#         print(f)

#-------------------
def test_has_entension( ):


    ext_list    = [ "txt",  "py",  ]
    msg         = ( f"\ntest_has_entension with {ext_list = }\n")
    print( msg )


    file_name     =  "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/data_hidden.py"

    print(  f"{file_name_has_extension( file_name, ext_list=  ext_list) = } {file_name}" )


    file_name     =  "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/data_hidden.txt"

    print(  f"{file_name_has_extension( file_name, ext_list=  ext_list) = } {file_name}" )


    file_name     =  "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/data_hidden.xml"

    print(  f"{file_name_has_extension( file_name, ext_list=  ext_list) = } {file_name}" )


    foo          = partial( file_name_has_extension, ext_list =  ext_list  )


    file_name     =  "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/data_hidden.xml"

    print(  f"{foo( file_name,) = } {file_name}" )

    file_name     =  "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/data_hidden.py"

    print(  f"{foo( file_name,) = } {file_name}" )

    print( "==== end ==== \n")

#-------------------------------
def test_file_name_starts_with( )    :

    prefix_list_    = [ "data",  "hidden",  ]
    msg         = ( f"\test_file_name_starts_with with {prefix_list_ = }\n")
    print( msg )

    file_name       =  "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/data_hidden.py"

    print(  f"{file_name_starts_with( file_name, prefix_list=  prefix_list_) = } {file_name}" )

    prefix_list_    = [ "xdata",  "hidden",  ]
    msg             = ( f"\test_file_name_starts_with with {prefix_list_ = }\n")
    print( msg )

    file_name       =  "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/data_hidden.py"

    print(  f"{file_name_starts_with( file_name, prefix_list=  prefix_list_) = } {file_name}" )

#-------------------------------
def test_file_name_starts_with_partial( )    :

    prefix_list    = [ "data",  "hidden",  ]
    msg         = ( f"\ntest_file_name_starts_with_partial with {prefix_list = }\n")
    print( msg )

    partial_filter   = partial( file_name_starts_with, prefix_list = prefix_list )

    file_name       =  "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/data_hidden.py"

    print(  f"{partial_filter( file_name,) }  {file_name} " )

    prefix_list_    = [ "xdata",  "hidden",  ]
    msg             = ( f"\ntest_file_name_starts_with_partial with {prefix_list_ = }\n")
    print( msg )


    partial_filter   = partial( file_name_starts_with, prefix_list = prefix_list )

    file_name       =  "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/data_hidden.py"
    print(  f"{partial_filter( file_name,) }  {file_name} " )


#-------------------------------
def test_path_name_starts_with_partial( )    :
    """


    """
    prefix_list    = [ "__pycache__",  ".",  ]
    msg         = ( f"\test_path_name_starts_with_partial with {prefix_list = }\n")
    print( msg )

    partial_filter   = partial( path_name_starts_with, prefix_list = prefix_list, invert_logic  = True )

    file_name       =  "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/.venv"
    rpt_test( False, partial_filter, file_name )

    file_name       =  "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/old"
    rpt_test( True, partial_filter, file_name )

    file_name       =  "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/__pycache__"
    rpt_test( False, partial_filter, file_name )

    # prefix_list_    = [ "xdata",  "hidden",  ]
    # msg             = ( f"\ntest_file_name_starts_with_partial with {prefix_list_ = }\n")
    # print( msg )


    # partial_filter   = partial( path_name_starts_with_partial, prefix_list = prefix_list )

    # file_name       =  "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/data_hidden.py"
    # print(  f"{partial_filter( file_name,) }  {file_name} " )







# ---- run a test(s)
# --------------------
if __name__ == "__main__":

    """
    at some low level of testing thse things work
    """
    # ---- ........functions
    #test_has_entension()
    # test_file_name_starts_with()

    # ---- .       iterator

    #test_file_iterator()

    #test_file_iterator_2()
    #test_file_name_starts_with_partial()
    test_path_name_starts_with_partial()
    # test_file_iterator_for_all()

    print( "all done")



# ---- eof