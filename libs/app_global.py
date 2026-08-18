# -*- coding: utf-8 -*-

# ---- tof

"""
Purpose:
    part of my ( rsh ) library of reusable code
    a library module for multiple applications
	allows any module access to a set of application global values and functions
	typical use:
	from app_global import AppGlobal

    watch out this often uses injected values
    	self.parameters    = AppGlobal.parameters

        app_db    AppDB



"""


# #from   tkinter    import messagebox
# import logging
# import os
# # ---- imports
# import sys
# import webbrowser
# from pathlib import Path
# from subprocess import Popen

# import os_call
# import psutil

import app_global_abc



# ------------------------------------------
class AppGlobal( app_global_abc.AppGlobalABC ):
    """
    all has been moved to abc, implement this yourself if
    you want extensions



    use at class level ( do not _init_ ) for application globals, similar to but different from parameters
    some global functions
    all in abc
    implement your own if you need something special or use this,
    make sure your path is set so you get the right one

    """



# ==============================================
if __name__ == '__main__':
    """
    run the app
    """
    1/0
    # import structured_notes
    # structured_notes.main(  )


# ======================== eof ======================

# ---- eof