# -*- coding: utf-8 -*-

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

# --------------------
if __name__ == "__main__":
    #----- run the full app #   import main   for next line
    import main   # noqa  stops auto removal by pycln
# --------------------



# ------ local imports
import app_global_abc

# ------------------------------------------
class AppGlobal( app_global_abc.AppGlobalABC ):
    """
    use at class level ( do not _init_ ) for application globals,
    similar to but different from parameters
    some global functions
    """
    # class var supress liner messages and better anyway
    # snipper             = None      # populated by ...
    # cmd_processor       = None      # populated by ...
    # commands            = None      # populated by ...
    # double_buttons      = None      # populated by ...
    # do_transforms       = None      # populated by ...
    # snippeter           = None      # populated by ...  !! dup name or what
    # lat_long_clip       = ( 0., 0. )  # lat long clipboard
        # see picture_document
    parameters             = None      # populated by controller unless noted
    cmd_processor       = None      # populated by ...
    commands            = None      # populated by ...
    double_buttons      = None      # populated by ...
    do_transforms       = None      # populated by ...
    controller          = None



    # stuffdb.py
    # AppGlobal.controller   = self
    # AppGlobal.fatal_error   = None
    # AppGlobal.parameters    = self.parameters

    # a_qsql_db_access        = qsql_db_access.QsqlDbAccess( STUFFDB_CONNECTION_NAME )
    # AppGlobal.qsql_db_access  = a_qsql_db_access
         # AppGlobal.qsql_db_access.db


    # ----------------------------------------------
    def __init__(self,  controller  ):

        yyyyy  = 1/0    # this guy should not be created and this stops it



# ======================== eof ======================





