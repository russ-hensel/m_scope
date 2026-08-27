#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:34:13 2024

@author: russ


import adjust.path
"""
# ---- imports

import sys
import os
import socket

VERBOSE   = 10
APP_DIR   = "/m_scope"

# adjust according to where I am -- in progress
hostname              = socket.gethostname()
cwd                   = os.getcwd()
me                    = __file__
adjust_path_file      = __file__


print( hostname )


VERBOSE   = 50

if VERBOSE > 20:
    print( f"in {adjust_path_file   = }")
    print( f"{cwd                   = }")
    print( f"{hostname              = }")

try:
    # ---- next needs to match the app
    ix   = cwd.index( APP_DIR )
    print( ix )

    src_root   = cwd[ : ix   ]
    print( f"in try {src_root = }" )

    print( "................................................." )

except ValueError as error:
    # Access the first argument (the message)
    error_message = error.args[0]
    print(f"fallback to hostname")

    # fallbak may bo out of use out of date

    if   hostname == "russ-ThinkPad-P72":
        src_root         = "/mnt/WIN_D/russ/0000/python00/python3"

    elif hostname == "theprof":
        src_root         = r"D:/russ\0000\python00\python3"


    elif hostname == "fattony":
        src_root         = "/media/russ/j_sg_bigcase/sync_py_3"

    elif hostname == "millhouse-mint":
        src_root         = "/media/russ/j_sg_bigcase/sync_py_3"
        src_root         = "/home/russ/sync_with_fattony/python3"

    else:
        src_root         = "/mnt/WIN_D/russ/0000/python00/python3"

    #src_root         = r"d:\russ\0000\python00\python3"


# least important at top
sys.path.insert( 1, f"{src_root}/rshlib/in_spect" )
sys.path.insert( 1, f"{src_root}/rshlib" )

sys.path.insert( 1, f"{src_root}/pyqt_by_example" )
sys.path.insert( 1, f"{src_root}/pyqt_by_example/tabs/more" )


sys.path.insert( 1, "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/pyqt_by_example" )
sys.path.insert( 1, "/home/russ/sync_with_bulldog/_projects/pyqt_by_example/image_overlay_view.py" )
sys.path.insert( 1, "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/pyqt_by_example/tabs/more" )
sys.path.insert( 1, "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/rshlib_qt" )
sys.path.insert( 1, "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/utils" )
sys.path.insert( 1, "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/app_services" )

sys.path.insert( 1,  "./libs" )                # libs for github repo

sys.path.insert( 1, f"{src_root}/rshlib/test/"  )
sys.path.insert( 1, f"{src_root}/rshlib/rshlib_qt/" )
sys.path.insert( 1, f"{src_root}/rshlib/app_services/" )


sys.path.insert( 1, f"{src_root}/rshlib/in_spect" )
sys.path.insert( 1, f"{src_root}/rshlib/utils" )

sys.path.insert( 1, f"./tabs/basic_widgets" )
sys.path.insert( 1, f"./tabs/book_fitz" )

#sys.path.insert( 1, f"{src_root}/rshlib/app_services" )

sys.path.insert( 1, f"{src_root}/_examples" )

sys.path.insert( 1, f"{src_root}/stuffdb" )
#sys.path.insert( 1, f"{src_root}/stuffdb/qt_tabs" )


# /mnt/WIN_D/russ/0000/python00/python3/qt5_by_example/tabs/

sys.path.insert( 1, f"{src_root}/stuffdb/data_dict_src" )
sys.path.insert( 1, f"{src_root}/stuffdb/sql" )
#/mnt/WIN_D/Russ/0000/python00/python3/qt5_by_example
# /mnt/WIN_D/Russ/0000/python00/python3/qt_by_example


#sys.path.insert( 1, f"{src_root}/qt5_by_example" )

# print( "your path has been adjusted fron qt5_by_example on theProf Mint from qt5_by_example" )
# for i_path in sys.path:
#     print( f"{i_path = }")

print( "end your path has been adjusted by qt5_by_example" )

pass   # for debug
# comment in out
if VERBOSE > 9:
    print( "    path now:" )
    for i_path in sys.path:
        print( "        ", i_path )


# --- eof






