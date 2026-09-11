#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 18:10:02 2026

utils is lame, reorganize
"""

# ---- tof

# # --------------------
# if __name__ == "__main__":
#     import main   # noqa  stops auto removal by pycln
# # --------------------

# ---- imports

import sys
import os
from   pathlib import Path

from qtpy.QtWidgets import ( QMessageBox, )

from datetime       import datetime
from qtpy.QtCore    import QDate

# ---- imports local -- then constants

# -------------------------------
def read_file_to_list( file_name ):
    """
    what it says --
        return none if fails
        utils.read_file_to_list( file_name )  # import utils
    """
    try:
        with open( file_name, "r" ) as a_file:
            file_as_list = list( a_file )
            # print( f"{file_as_list}"  )

    except:

        msg_box_msg    = f"Could not open file {file_name}"
        msg_box        = QMessageBox()
        msg_box.setIcon( QMessageBox.Information )
        msg_box.setText(  msg_box_msg  )
        msg_box.setWindowTitle( "File Read Failed" )
        msg_box.setStandardButtons( QMessageBox.Ok )

        ret             = msg_box.exec_()
        #rint( f"{ret = }" )
        return None

    return file_as_list

# -------------------------------
def get_setup_from_file( file_name ):
    """
    parse file backwards to find setup string
    setup_id         = "get from user",

        setup_id         = utils.get_setup_from_file( file_name )
        return
            setup_id or "" if not founc
    """
    a_list    = read_file_to_list( file_name )

    if not a_list:
        return ""

    for i_line in reversed( a_list ):
        #rint( i_line )
        i_line   = i_line.strip( )
        splits   = i_line.split( "=" )

        if len( splits ) != 2:
            continue

        parm   = splits[ 0 ].strip()
        if parm == "setup_id":
            setup  = splits[1]
            setup  = setup[ 2 : -2 ]        # remove comma on end and quoted
            print( f"get_setup_from_file() found setup >{setup}<")
            break

    else:
        setup  = ""

    return setup

# -------------------------------
def get_item_code( file_name  ):
    """
    what it says
        2026_09_06_sdfdsf_162911.txt


    """
    #return datetime.now().strftime( "%Y%m%d_%H%M%S" )
    a_path     = Path( file_name )
    name       = a_path.name
    splits     = name.split( "_" )

    if  len( splits ) < 5 :
        item_code  = ""

    else:
        item_code  = splits[3]

    return item_code

# -------------------------------
def get_date_code_as_date( file_name  ):
    """
    what it says
        2026_09_06_sdfdsf_162911.txt
        0123456789
        return
            qdate or None

    """
    #return datetime.now().strftime( "%Y%m%d_%H%M%S" )
    a_path     = Path( file_name )
    stem       = a_path.stem

    if not len( stem ) >= 9:
        return None

    date_string     = stem[ :9 ]
    # splits        = stem.split( "_" )

    try:
        qdate           = QDate.fromString(date_string, "yyyy_MM_dd")

    except:
        return None

    return qdate



    # date_edit.setDate

    # if  len( splits ) != 3 :
    #     return None

    # else:
    #     item_code  = splits[3]

    # return item_code





# -------------------------------
def extract_related_fn( file_name, extension ):
    """
    extract_related_path( ) use str if that is what you need
        similar function
        # our_path            = Path( file_name )
        # file_name_note      = f"{our_path.parent}/{our_path.stem}{extension}"


    """
    our_path        = Path( file_name )
    file_name       = f"{our_path.parent}/{our_path.stem}{extension}"
    return file_name

    # #wrong cannot put extension in there
    # temp_path     = Path( file_name )
    # parent        = temp_path.parent
    # name          = temp_path.name
    # stem          = temp_path.stem

    # if extension:
    #     file_path     = temp_path.joinpath(  parent,  stem, extension, )

    # else:
    #     file_path     = temp_path.joinpath(  parent,  stem, )

    # return file_path

# -------------------------------
def date_time_marker(  ):
    """
    what it says -- sortable, no characters that annoy a file system
    """
    return datetime.now().strftime( "%Y%m%d_%H%M%S" )

# -------------------------------
def time_marker(  ):
    """
    what it says -- sortable, no characters that annoy a file system
    """
    return datetime.now().strftime( "_%H%M%S" )  # or could truncate

# -------------------------------
def gen_fn_stem( prefix ):
    """
    prefix  a string used as prefix
        file_stem    = utils.gen_fn_stem( prefix )  # import utils
    """
    file_name           = os.path.join( f"{prefix}{time_marker()}" )
    return file_name

# -------------------------------
def test1():

    value    = gen_fn_stem( "2026-08-16_red2" )
    print( value )

    value    = gen_fn_stem( "2026_08_16_red2" )
    print( value )

    value     = extract_related_fn( "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/m_scope/temp_photo/2026_09_07_ff_073617.jpg", extension  = ".txt" )
    print( value )


# -------------------------------
def test2():
    """ may fail if not in qapplication
    """
    file_name      = "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/m_scope/temp_photo/2026_09_09_wed_080623.txt"
    a_list         = read_file_to_list( file_name )
    print( a_list )

    item_code      = get_item_code( file_name )
    print( item_code )


    value         = get_setup_from_file( file_name )
    print( value )

# for tests, move
if __name__ == '__main__':

    test1()
    test2()

# ---- eof ---------------------------


