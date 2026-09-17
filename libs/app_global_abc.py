# -*- coding: utf-8 -*-
# ---- tof
"""
Purpose:

    currently may only be used in clipboard app
        but move into others

    part of my ( rsh ) library of reusable code
    a library module for multiple applications
	allows any module access to a set of application global values and functions
	typical use:
	from app_global import AppGlobal

    watch out this often uses injected values
    	self.parameters    = AppGlobal.parameters

        app_db    AppDB

    object should not register themselves ... should be done by
    thier createro
    perhaps add a register function

"""

# ---- Imports

import abc
#from   tkinter    import messagebox
import logging
import os
import sys
import webbrowser
from pathlib import Path
from subprocess import Popen

import os_services
import psutil

# may not be using next
try:
    import parameters
    PARAMETERS = parameters.PARAMETERS

except Exception as an_except:

    PARAMETERS = None



# ---- begin functions
# ----------------------------------------------
def addLoggingLevel( levelName, levelNum, methodName = None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

     How to add a custom loglevel to Python's logging facility - Stack Overflow
     *>url  https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobbering of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """

    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        #raise AttributeError('{} already defined in logging module'.format(levelName))
        return   # assume already set up ok -- could cause error in contaminated environment

    if hasattr(logging, methodName):
        raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, *args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot )

# ------------------------
class NoLoggerLogger( ):
    """
    a temporary logger before we have a proper logger
    implement some of the methods of the logger
    just some of the protocol not all of this
    log(level, msg, *args, **kwargs)¶
    perhaps import module and use its constants which seem not to be
    CRITICAL 50 ERROR  40   WARNING 30  INFO  20  DEBUG 10 NOTSET 0

    """
    __log_later             = []         # tuples for logging after logger is set
    # ----------------------------------------------
    @classmethod
    def info( cls, msg ):
        """
        mirror logger.info in limited way
        """
        cls.log( logging.INFO, msg )

    # ----------------------------------------------
    @classmethod
    def debug( cls, msg ):
        """
        mirror logger.debug in limited way
        """
        cls.log( logging.DEBUG, msg )

    # ----------------------------------------------
    @classmethod
    def log( cls, level, msg, *args, **kwargs ):
        """
        mirror logger.log in limited way
        """
        arg_set  = ( level, msg, )  # not clear how to get rest, for now discard
        #rint( f"{arg_set[0]} >> {arg_set[1]}" )
        cls.__log_later.append( arg_set )

    # ----------------------------------------------
    @classmethod
    def log_saved_for_later( cls, logger ):
        """
        now have a logger so spit out the saved up stuff if any
        may or may not print
        ?? add some indent
        """
        for arg_set in cls.__log_later :
            print( f"log_saved_for_later {arg_set[ 0 ]} {arg_set[ 1 ]}" )
            logger.log( arg_set[ 0 ], arg_set[ 1 ] )


# ========================== Begin Class ================================
class UserCancel( Exception ):
    """
    if part way though an operation user wishes to cancel
    think not used, if is used put in rhslib !!
    """
    def __init__(self, arg):
        # Set some exception information
        self.msg = arg


# ------------------------------------------
class AppGlobalABC( abc.ABC ):
    """
    use at class level ( do not _init_ ) for application globals, similar to but different from parameters
    some global functions
    """
    force_log_level         = 99        # value to force logging, high but not for errors

    # ----------- other important objects typically registered by their inits -- define as none to help document

    controller              = None      # populated by the controller
    parameters              = None      # populated by parameters
    gui                     = None      # populated by the gui
    gui_toolbox             = None      # populated by the controller
    logger                  = None      # populated by the controller
    logger                  = NoLoggerLogger  # can use for now with limited calls, then dumps later ...
    fll                     = force_log_level      #  AppGlobal.fll

    helper                  = None      # populated externally by...
    #helper_thread_id        = None      # set by run in helper thread
    main_thread_id          = None
    logger_id               = None      # populated by the controller
    scheduled_event_list    = None      # populated externally by... -- think dead

    parameter_dicts         = {}        # set up in parameters ????? -- see and example std setup some where

    db_file_name            = None      # initially fetched from controller, later gui may update  this is a bad idea -- drop
    lock_db_file_name       = False     # just an idea, needs functions like check_lock_db_file_name  located where !!
    file_reader             = None
#    live_graph_opt          = 1         # 1 = all in helper                this is just an experiment

    # consider branch on os

    # atom     /usr/bin/flatpak run --branch=stable --arch=x86_64 --command=atom --file-forwarding io.atom.Atom @@ %F @@
    # Brackets     /usr/bin/flatpak run --branch=stable --arch=x86_64 --command=brackets --file-forwarding io.brackets.Brackets @@ %F @@
    # gedit             gedit
    # idle           idle
    # l3afpad        l3afpad
    # leafpad        ??
    # mousepad       mousepad
    # notepadqq      ???
    # nano           nano
    # sublime text   /opt/sublime_text/sublime_text %F  ??

    # Notepad ++     ??
    # xedit          xedit
    # xed             xed

    text_editors            =  []

    if sys.platform.startswith( "lin"): # assume linux for now

        linux_editors       =  [    "xed",
                                        "gedit",
                                        "leafpad",
                                        "mousepad",
                                    ]
        text_editors        = text_editors + linux_editors

    else: # windows? Apple?
          # I do not know what to do for apple so just throw everything in here

        win_editors         =  [ r"D:\apps\Notepad++\notepad++.exe",
                                    r"C:\apps\Notepad++\notepad++.exe",
                                    "notepad++.exe",
                                  ]

        text_editors        = text_editors  + win_editors

    # text_editors            =  [ r"D:\apps\Notepad++\notepad++.exe", r"C:\apps\Notepad++\notepad++.exe", "notepad++.exe",
    #                              r"gedit", r"xed", r"leafpad", r"mousepad", ]

    file_text_editor        = os_services.OSCall( text_editors,  )

    # too soon to call a parameters not defined need to do later
    #file_text_editor.add_command( parameters.ex_editor )

    # add_prog                = AppGlobal.parameters.ex_editor
    # if add_prog is not None:
    #     text_editors        = text_editors + text_editors

    # file_explorers  not in parameters as yet
    file_explorers          = [ r"explorer", "nemo", "xfe", "pcmanfm", ]
    file_explorer           = os_services.OSCall( file_explorers ) # !! need linux add and parameters

    # cls not yet defined
    # this gives the name notice to force_log_level... perhaps a better name might be used
    addLoggingLevel( "Notice", force_log_level, methodName=None)

    # self registering when created, not great
    app_file                = None
    app_db                  = None
    app_dir                 = None

    # ----------------------------------------------
    def __init__(self,  controller  ):

        y  = 1/0    # this guy should not be created and this stops it
        pass

    # ----------------------------------------------
    @classmethod
    def set_logger( cls, logger ):
        """
        set the system logger once setup, empty NoLoggerLogger

        """
        #print( "set logger" )
        cls.logger    = logger
        NoLoggerLogger.log_saved_for_later( logger )

    # ----------------------------------------------
    @classmethod
    def set_gui_toolbox( cls, gui_toolbox ):
        """
        think not needed or used

        """
        print( "set set_gui_toolbox delete me???" )
        cls.gui_toolbox    = gui_toolbox
        if   gui_toolbox =="qt":
            pass
        elif gui_toolbox == "tk":
            pass

    # ----------------------------------------------
    @classmethod
    def restart( cls,  ):
        """
        restart for anything needed if app does a restart

        """
        pass

    # ----------------------------------------------
    @classmethod
    def parameter_tweaks( cls,  ):
        """
        call if necessary at end of parameters -- may make init unnecessary
        AppGlobal.parameters needs to be populated -- cls.parameters
        """


        # cls.text_editors            = [   r"D:\apps\Notepad++\notepad++.exe", r"C:\apps\Notepad++\notepad++.exe",
        #                               r"gedit", r"xed", r"leafpad"   ]   # or init from parameters or put best guess first

        # cls.text_editors.insert( 0,  cls.parameters.ex_editor  )
        # cls.ix_text_editor          = -1
        # cls.working_editor          = None

        #rint( f"parameter tweaks finish me" ) # "{cls.text_editors}" )

        # file_explorer  not in parameters as yet
        cls.file_text_editor.add_command( cls.parameters.ex_editor )

    # ----------------------------------------------
    @classmethod
    def show_process_memory( cls, call_msg = "", log_level = None, print_it = False ):
        """
        log and/or print memory usage
        """
        process      = psutil.Process(os.getpid())    #  import psutil
        mem          = process.memory_info().rss
        # convert to mega and format
        mem_mega     = mem/( 1e6 )
        msg          = f"{call_msg}process memory = {mem_mega:10,.2f} mega bytes "
        if print_it:
            print( msg )
        if not ( log_level is None ):
            cls.logger.log( log_level,  msg )
        msg           =  f"{mem_mega:10,.2f} mega bytes "
        return ( mem, msg )

    # ----------------------------------------------
    @classmethod
    def log_if_wrong_thread( cls, id, msg = "forgot to include msg", main = True ):
        """
        debugging aid
        check if called by intended thread
        main thread must be set first
        ex:   AppGlobal.log_if_wrong_thread( threading.get_ident(), msg = msg, main = True  )
        """
        on_main = ( id == cls.main_thread_id )

        if main:
            ok  = on_main
        else:
            ok = not( on_main )

        if not ok:
            msg    = f"In wrong thread = {cls.name_thread( id )}: + {msg}"
            cls.logger.log( cls.force_log_level,  msg )

    # ----------------------------------------------
    @classmethod
    def name_thread( cls, id, ):
        """
        return thread name Main/Helper
        ex call:  AppGlobal.name_thread( threading.get_ident(),  )
        """
        if  cls.main_thread_id is None:
            y= 1/0   # cheap exception when main_thread not set up

        if id == cls.main_thread_id:
            ret = f"Main"
        else:
            ret = f"Helper"

        return ret

    # ----------------------------------------------
    @classmethod
    def thread_logger( cls, id, call_msg = "", log_level = None ):
        """
        debugging aid
        log a message, identifying which thread it came from
        ex call: AppGlobal.thread_logger( threading.get_ident(), "here we are", 50  )
        """
        thread_name   = cls.name_thread( id )
        msg           = f"in {thread_name} thread>> {call_msg}"

        if not ( log_level is None ):
            cls.logger.log( log_level,  msg )

    # ----------------------------------------------
    @classmethod
    def about( cls,   ):
        """
        		show about box -- might be nice to make simple to go to url ( help button )
                here for the apps that still use it

        need to determine if we are in tk or qt ... but this shoud be moved to qt_extension
        """
        url_msg   =  r"coming soon not at http://www.opencircuits.com/TBD"
        if cls.controller:
            app_msg   = ( f"move to _ext  {cls.controller.app_name}  version:{cls.controller.version} "
                        "\n  by Russ Hensel\n" )
        else:
            app_msg   = ( f"An application of some sort"
                        "\n  by Russ Hensel\n" )

        __, mem_msg   = cls.show_process_memory( )

        msg  =    ( f"{app_msg} \n  Memory in use {mem_msg}"
                   "\n  Check <Help> or \n     {url_msg} \n     for more info." )
        #messagebox.showinfo( "About", msg,  )
        print( msg )
        #   tried ng: width=20  icon = "spark_plug_white.ico"


    # ---- open things
    # ----------------------------------------------
    @classmethod
    def os_open_html_file( cls, a_file ):
        """
        could work for url ??
        may require more path name ??
        often fail on unix use open url
        """
        #cls.file_text_editor.os_call( txt_file )

        print( f"popopen {a_file}"   )
        ret = os.popen( a_file )

    # ----------------------------------------------
    @classmethod
    def os_popen_file( cls, a_file ):
        """
        may want to add arguments .... and other versions ??
        """
        #cls.file_text_editor.os_call( txt_file )
        print( f"popopen {a_file}"   )
        ret = os.popen( a_file )

    # ----------------------------------------------
    @classmethod
    def os_open_url( cls,  url  ):
        """
		what it says
        """
        ret  = webbrowser.open( url, new=0, autoraise=True )

    # ----------------------------------------------
    @classmethod
    def os_open_help_file( cls, help_file ):
        """
		what it says
        see parameters for different types of files and naming that will work with this
        """
        #help_file            = self.parameters.help_file
        if help_file.startswith( "http:" ) or help_file.startswith( "https:" ):
            ret  = webbrowser.open( help_file, new=0, autoraise=True )    # popopen might also work with a url
            #rint( f"help http: {help_file} returned {ret}")
            return

        a_join        = Path(Path( help_file ).parent.absolute() ).joinpath( Path( help_file ).name )
#        print( f"a_join {type( a_join )} >>{a_join}<<" )

        #if a_join.endswith( ".txt" ):
        if a_join.suffix.endswith( ".txt" ):
            cls.os_open_txt_file( str(a_join) )
            return

        file_exists   = os.path.exists( a_join )
        print( f"file {a_join} exists >>{file_exists}<<" )
        #full_path     = Path( help_file ).parent.absolute()
#        print( f"a_join {a_join}" )
        help_file     = str( a_join )

        ret = os.popen( help_file )
#        print( f"help popopen  {help_file} returned {ret}")

    # ----------------------------------------------
    @classmethod
    def os_open_txt_file( cls, txt_file ):
        """
        open a text file with system configured editor
        will work with path?
        what if file does not exist -- editor may try to create
        AppGlobal.os_open_txt_file( txt_file )
        connect_to      = partial( AppGlobal.os_open_txt_file,  txt_file = txt_file )
        """
        if  isinstance( txt_file, Path ):
            # need a string if i get a path then....

            txt_file  = str( txt_file.absolute() )
            txt_file  = str( txt_file )
        cls.file_text_editor.os_call( txt_file )

    # ----------------------------------------------
    @classmethod
    def os_open_a_snip_file( cls, a_snip_file ):
        """
        open a snip file with system configured editor
        AppGlobal.os_open_a_snip_file( fn )
        this is used by the clipboard
        """
        proc = Popen( [ cls.parameters.snip_editor, a_snip_file ] )

    #  # ----------------- debugging ----------------
    # def to_str():
    #     """
    #     !! is static or class or what research and fix
    #     debug aid, but dead
    #     convert some of AppGlobals contents to a string for debugging - left over from some other app
    #     might revive or delete
    #     """
    #     a_string   = (   "AppGlobal" +  str ( AppGlobal.parameter_dicts )  )

    #     return a_string

    # ----------------------------------------------
    @classmethod
    def get_info_str( cls, ):

        a_string  = "Info on AppGlobal cls.values"
        a_string  = f"{a_string}\n    gui              >{cls.gui}<"
        a_string  = f"{a_string}\n    parameters       >{cls.parameters}<"
        a_string  = f"{a_string}\n    logger           >{cls.logger}<"
        a_string  = f"{a_string}\n    file_reader      >{cls.file_reader}<"
        a_string  = f"{a_string}\n    text_editors     >{cls.text_editors}<"

        return a_string

    # #--------------------------------
    # def print_me():
    #     sys.stdout.flush()
    #     print("========== AppGlobal =================")
    #     print( AppGlobal.to_str( ) )
    #     sys.stdout.flush()

    #--------------------------------
    @classmethod
    def print_debug( cls, msg  ):  #
        """
        very temp
        all should be removed
        """
        print( msg, flush = True )
        cls.logger.debug( msg )

    #--------------------------------
    @classmethod
    def write_gui( cls, msg  ):  #
        """
        !! good idea bad idea?  -- at least test for gui
        """
        cls.gui.write_gui( msg )
        print( "AppGlobal.write_gui", msg, flush = True )
        cls.logger.debug( msg )

# ==============================================
if __name__ == '__main__':
    """
    run the app
    """
    1/0
    # import structured_notes
    # structured_notes.main(  )


# ======================== eof ======================

