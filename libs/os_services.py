#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
Created on Fri Mar  7 08:39:58 2025

@author: russ
"""


# ---- imports

from subprocess import Popen

#from   pathlib    import Path
#import os
#import psutil


#import traceback

# try:
#     import parameters
#     PARAMETERS = parameters.PARAMETERS

# except Exception as an_except:

#     PARAMETERS = None



# ---- end imports

TXT_DEFAULTS    = [  "xed",   "gedit ",  "l3afpad",  "leafpad"   "nvim", "vim", "nano", "xedit", ]

print( " -----------------------------------------------------------------")
print( TXT_DEFAULTS )

#-------------------------------

def  open_app_with_file( string_arg_list, file_name ):
    """
    what it says, read
    os_services.open_app_with_file( string_arg_list, file_name )

    string_arg_list     list of strings -- the command and any
                                    arguments needed to launch the app.
                                    file_name is appended as the last
                                    argument.  Popen does not go through a
                                    shell, so no quoting and no desktop
                                    file "@@ ... @@" file-forwarding
                                    markers are needed here
    file_name                      path to the file to open

    example -- Pinta via its flatpak install, whose desktop launcher is

        Exec=/usr/bin/flatpak run --branch=stable --arch=x86_64 --command=pinta --file-forwarding com.github.PintaProject.Pinta @@ %F @@

        PINTA_CMD   = [
            "/usr/bin/flatpak", "run",
            "--branch=stable",
            "--arch=x86_64",
            "--command=pinta",
            "com.github.PintaProject.Pinta",
            ]
        open_app_with_file( PINTA_CMD, "/path/to/file.jpg" )
    """
    a_cmd       = string_arg_list + [ file_name ]
    a_proc      = Popen( a_cmd )

    return a_proc


# ------------------------
class OSCall(  ):

    """
    try to call os based on attempts with different utilities
    in different operating systems
    command_list   =  could get from parameters or

    text_editors            =  [ "xed", "gedit",  "leafpad", "mousepad", ]
    command_list            = text_editors

    import os_services
    self.os_txt_call        = os_services.OSCall( text_editors )

    later

    self.os_txt_call.os_call( cmd )  # cmd is usually filename


    """
    #------------------------
    def __init__(self, command_list = None, ):
        """
        command list is the list of utilities to try, a list of strings
        command_aux: like command list but may be a list, a single string, or none, see code
        command_list
            see add_command
        """
        if command_list is None:
            # not clear we need this
            command_list    = []
            # cannot assume what type of command could add this ??

        self.command_list = []
        self.add_command( command_list )

    # ----------------------------------------------
    def add_command( self, more_command_list, append = True ):
        """
        add a command at the beginning and re init the list
        call internally at init or externally ( parameters ) to add to list
        args
            more_command_list
                None                -- use some defaults at least for now
                string              -- add as a command
                list of strings     -- add the list
        """
        #rint( f"adding {more_command_list}")
        if more_command_list is None:
            self.command_list        = more_command_list     # [   r"D:\apps\Notepad++\notepad++.exe", r"gedit", r"xed", r"leafpad"   ]   # or init from parameters or put best guess first

        else:
            if type( more_command_list ) ==  str:
                more_command_list  = [ more_command_list ]
            # else we expect a list

        if append:
            self.command_list =  self.command_list + more_command_list
        else:
            self.command_list = more_command_list + self.command_list
        self.ix_command          = -1
        self.working_command     = None
        #rint( f"xxxxx list now{self.command_list}")

    # ----------------------------------------------
    def default_for_txt( self, append = True  ):
        """
        a default list for txt files

        """
        self.command_list = []
        self.add_command( TXT_DEFAULTS, append  )

    # ----------------------------------------------
    def get_next_command( self,  ):
        """
        what it says
        None if cannot find one ( at end of list )
        """
        self.ix_command += 1
        if         self.ix_command >= len( self.command_list ):
            ret =  None
        else:
            ret =         self.command_list[ self.ix_command ]
        #rint( f"command = { self.ix_command} {ret} ", flush = True )
        return ret

    # ----------------------------------------------
    def os_call( self, cmd_arg,  ):
        """
        make an os call trying various utilities until one works
        perhaps call open
        """
        while True:   # will exit when it works or run out of editors
            a_command    = self.working_command
            if  a_command is None:
                a_command  = self.get_next_command( )

            if a_command is None:   # still
                msg = f"Run out of editors to try >{a_command}< >{cmd_arg}<"
                #cls.logger.error( msg )
                raise RuntimeError( msg )
                #break  # think we are already done
            try:
                if cmd_arg is None:
                    proc = Popen( [ a_command,  ] )
                else:
                    proc = Popen( [ a_command, cmd_arg ] )
                self.working_command  = a_command
                break  # do not get here if exception
            except Exception as excpt:
                pass     # this should let us loop
#                 cls.logger.error( "os_open_logfile exception trying to use >" + str( cls.parameters.ex_editor ) + "< to open file >" + str( cls.parameters.pylogging_fn ) +
#                                  "< Exception " + str( excpt ) )





# ---- eof