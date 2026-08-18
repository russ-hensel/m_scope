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



from datetime import datetime


# ---- imports local -- then constants


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
    file_name           = os.path.join(  f"{prefix}{time_marker()}" )
    return file_name

# -------------------------------
def test1():

    value    = gen_fn_stem( "2026-08-16_red2" )
    print( value )

    value    = gen_fn_stem( "2026_08_16_red2" )
    print( value )

# for tests, move
if __name__ == '__main__':

    test1()


# ---- eof ---------------------------


