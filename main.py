# -*- coding: utf-8 -*-
"""
launcher for the app


"""


import os



import adjust_path   # noqa  stops auto removal by pycln

#

# Get the directory of the current .py file
script_dir = os.path.dirname( os.path.abspath(__file__) )

# Change the current working directory to the script's directory
os.chdir(script_dir)

print(os.getcwd())  # Prints the new working directory

import m_scope


#print( f"sys.argv  = >>>{sys.argv}<<< ")

m_scope.main()

# ---- eof


