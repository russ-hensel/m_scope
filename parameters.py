# -*- coding: utf-8 -*-
# ---- tof

"""
    parameters    for  pyqt by example
    parameters.PARAMETERS.

"""
# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln
# --------------------

import logging
import sys

# ---- local imports

#import in_spect_env

global PARAMETERS


PARAMETERS   = None

# ========================================
class Parameters( ):
    """
    manages parameter values: use it like an ini file but it is code
    """
    # -------
    def choose_mode( self ):
        """
        typically choose one mode
            and if you wish add the plus_test_mode
            if you comment all out all modes you get the default mode which should
            run, but perhaps not in the way you want
        """
        self.new_user_mode()
        self.mode_dev_debug()
        #self.mode_ram_disk_db()
        #self.mode_russ_on_theprof()
        #self.new_user_mode()
        #self.mode_disk_db()
        #self.millhouse_1_mode()

        # two of my computers
        #self.mode_millhouse_mint()
        #self.mode_theprof_mint()
        #self.russ_1_mode()

        # --- add on for testing, use as desired edit mode for your needs
        #self.plus_test_mode()

    # ---- ---->> Methods: one for each mode
    # -------
    def new_user_mode( self ):
        """
        a mode for the new user, pretty much empty,
        a new user may experiment here.
        """
        self.mode               = "mode new_user"
        self.auto_run           = True

        # ---- min_complete
        self.min_complete       = 20  # minimum value for HOW_COMPLETE


    # -------
    def mode_dc_on_linux_mint( self ):
        """

        """
        self.mode               = "mode_dc_on_linux_mint"


    # -------
    def mode_ram_disk_db( self ):
        """
        run for debugging when you want the db on a fast disk

        /tmp/ramdisk/new_user.db
        """
        self.mode               = "mode_ram_disk_db"
        # expose tabs that are not ready
        self.min_complete       = 6 # minimum value for HOW_COMPLETE

        # ---- search and default
        self.default_search     = "progress"
        self.do_search_on_init  = True

        # ---- database there are 2 ........
        # ---- for sample database
        self.db_type            = "QSQLITE"
        self.db_file_name        = "/tmp/ramdisk/qt_sql.db"

        # ---- for qt tabs
        self.tab_db_type         = "QSQLITE"
        self.tab_db_file_name    = "/tmp/ramdisk/tab.db"

    # -------
    def mode_disk_db( self ):
        """
        run for debugging when you want the db on a disk
        startup is really slow -- minutes
        """
        self.mode               = "mode_disk_db"
        # expose tabs that are not ready
        self.min_complete    = 0  # minimum value for HOW_COMPLETE

        # ---- search and default
        self.default_search     = "progress"
        self.do_search_on_init  = True

        # ---- database there are 2 ........
        # ---- for sample database
        self.db_type            = "QSQLITE"
        self.db_file_name        = "./misc/qt_sql.db"

        # ---- for qt tabs
        self.tab_db_type         = "QSQLITE"
        self.tab_db_file_name    = "./misc/tab.db"

    # -------
    def mode_dev_debug( self ):
        """
        for dev and debug, mostly for rsh
        """
        self.mode               = "mode_dev_debug"
        # expose tabs that are not ready
        self.min_complete    = 0  # minimum value for HOW_COMPLETE

        self.note_default_text  = "note_default_text"

        # ---- search and default

        self.default_search     = ""
        self.do_search_on_init  = True

        # self.default_search     = "qq"
        # self.do_search_on_init  = True

        # good for kingholmer
        self.qt_width           = 1500
        self.qt_height          = 600    # 700 most of win height
        self.qt_xpos            = 10
        self.qt_ypos            = 10

        #self.dir_for_tabs.append(  "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/qt_tabs"  )
        #self.dir_for_tabs.append(  "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/stuffdb/pyqt_tabs" )
        #self.dir_for_tabs.append( "./tabs/experiments" )

    # -------
    def running_on_tweaks(self,  ):
        """
        this is only for things other than the os typically for
        the computer name or hardware info

        !! would we like to get the window size or number or monitors

        not a mode, a tweak to other modes , see documentation
        you need to customize this for your own computers, what you may
            find here are customization's for russ and his computers
        use running on tweaks as a more sophisticated
            version of os_tweaks and computer name tweaks which
        may replace them
        this is computer name tweaks code,
            !! find run_on on which uses os or put computer name under this
            import in_spect_env
            in_spect_env.InSpectEnv.value
        """
        return
        # computer_id    =   in_spect_env.InSpectEnv.computer_id

        # print( f"Parameters running_on_tweaks {computer_id = }")
        # print( f"Parameters {  in_spect_env.InSpectEnv.__str__()  } ")  #ok
        # print( "------------------------------")
        # print( f"{ str(in_spect_env.InSpectEnv)   } ")       # ng

        # if computer_id == "smithers":
        #     self.win_geometry       = '1450x700+20+20'      # width x height position
        #     self.ex_aleditor          =  r"D:\apps\Notepad++\notepad++.exe"
        #     self.db_file_name       =  "smithers_db.db"

        # # ---- bulldog
        # elif computer_id == "bulldog":
        #     self.ex_editor          =  r"gedit"
        #     self.db_file_name       =  "bulldog_db.db"


        # elif computer_id == "millhouse":
        #     self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
        #     #self.win_geometry   = '1300x600+20+20'
        #     self.db_file_name       =  "millhouse_db.db"

        # ---- 'millhouse-mint'
        if computer_id == 'millhouse-mint':
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"

            # ---- for sample database
            self.db_type            = "QSQLITE"
                # the type of database, so far we only support sqllite

            self.db_file_name        = ":memory:"     #  = "sample.db"   =  ":memory:"
            #self.db_file_name        = "./qt_sql.db"    #  real files are very slow

            # ---- for qt tabs
            self.tab_db_type         = "QSQLITE"
            self.tab_db_file_name    = ":memory:"

            #self.dir_for_tabs       = [ "./",  ]

            self.dir_for_tabs.append(  "/home/russ/sync_with_fattony/python3/_projects/stuffdb/qt_tabs"  )

        if computer_id == 'kingholmer':

            self.qt_width           = 1500
            self.qt_height          = 600    # 700 most of win height
            self.qt_xpos            = 10
            self.qt_ypos            = 10

        # # ---- theprof
        # elif computer_id == "theprof":
        #     self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
        #     self.db_file_name       =  "the_prof_db.db"


        # else:
        #     print( f"In parameters: no special settings for computer_id {computer_id}" )
        #     if self.running_on.os_is_win:
        #         self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
        #     else:
        #         self.ex_editor          =  r"leafpad"    # Linux raspberry pi maybe

    # -------
    def os_tweaks( self ):
        """
        this is an subroutine to tweak the default settings of "default_mode"
        for particular operating systems
        you may need to mess with this based on your os setup
        """
        our_os           = sys.platform
        self.our_os      = our_os
             #testing if our_os == "linux" or our_os == "linux2"  "darwin"  "win32"

        if our_os == "win32":
            self.os_win = True     # the OS is windows any version
        else:
            self.os_win = False    # the OS is not windows

        if  self.os_win:
            self.text_editor        = "notepad"

        else:
            pass
            # print( "os_tweaks for not windows " )

    # ------->> default mode, always call
    def mode_default( self ):
        """
        sets up pretty much all settings
        documents the meaning of the modes
        call first, then override as necessary
        good chance these settings will at least let the app run
        """
        self.mode              = "mode_default"
            # name your config, it will show in app title
            # may be changed later in parameter init


        # ---- appearance size--

        # control initial size and position with:
        self.qt_width           = 1200
        self.qt_height          = 500
        self.qt_xpos            = 10
        self.qt_ypos            = 10

        # self.wat_qt_width       = 1000
        # self.wat_qt_height      = 400
        # self.wat_qt_xpos        = 10
        # self.wat_qt_ypos        = 10


        # self.minimun_useful    =  10
        # ---- .... icon
        self.icon               = r"./images/icon_red.png"    # icon for running app
        self.icon               = r"./icons/icons/binocular.png"
        self.icon               = r"./misc/computer.ico"

        self.text_editor        = "gedit"
        self.text_editor        = "xed"

        # ---- overlay  defaults
        self.default_ovelay     = "./misc/red_black_cross_2.jpg"  # file_name
        self.overlay_opacity    = 30

        self.blend_type         = "" # may need to move some enums
        self.blink_on           = False  # !! False = True = blink
        self.auto_load_snap     = True   # load the last snap
        self.overlay_on_snap    = True   # switch to the overlay tab

        # ---- output
        self.output_dir         = "./output"   # file name for the python logging

        # ---- logging
        self.pylogging_fn       = f"{self.output_dir}/app.py_log"   # file name for the python logging

        self.log_mode               = "w"    # "a" append "w" truncate and write


        self.logging_level      = logging.DEBUG         # may be very verbose
        self.logging_level      = logging.INFO
        #self.logging_level      = logging.INFO

        self.logger_id          = "qt_ex"         # id of app in logging file

        self.default_fn_functon   = None




        # self.breakpoint_ok      = True  # enable breakpoin button

        # self.auto_run           = True

        # # ---- database there are 2
        # self.db_type            = "QSQLITE"
        #     # the type of database, so far we only support sqllite

        # # ---- .... for sample database
        # self.db_file_name        = "/tmp/ramdisk/qt_sql.db"
        # self.db_file_name        = ":memory:"     #  = "sample.db"   =  ":memory:"
        # #self.db_file_name        = "./qt_sql.db"    #  real files are very slow

        # # ---- .... for qt tabs
        # self.tab_db_type         = "QSQLITE"
        # self.tab_db_file_name    = "/tmp/ramdisk/tab.db"
        # self.tab_db_file_name    = "./tab.db"
        # self.tab_db_file_name    = ":memory:"

        # ---- file names -- but not db
        # control button for editing the readme file
        self.readme_fn      = "readme_rsh.txt"   # or None to suppress in gui
            # a readme file accessable from the main menu

        # or anything else ( will try to shell out may or may not work )
        self.help_fn        =  "./docs/help.txt"   #  >>. this is the path to our main .py file self.py_path + "/" +

        self.help_path      =  "./docs"
        self.help_path      =  "/mnt/WIN_D/russ/0000/python00/python3/_projects/qt5_by_example/docs/"
            # path leading to all docs and help

        # # ---- dir_for_tabs:  the app will look for tabs in these directories
        # self.dir_for_tabs       = [ "./",  ]
        # self.dir_for_tabs       = [    ]
        # #self.dir_for_tabs       = [ "/mnt/WIN_D/russ/0000/python00/python3/_projects/stuffdb/qt_tabs" ]
        # #may need to be on path sys.path.insert( 1, f"{src_root}/_projects/stuffdb/qt_tabs" )
        # self.dir_for_tabs.append( "./tabs/basic_widgets" )
        # self.dir_for_tabs.append( "./tabs/sql_widgets" )
        # self.dir_for_tabs.append( "./tabs/book_fitz" ) #  book_fitz
        # self.dir_for_tabs.append( "./tabs/more" )
        # self.dir_for_tabs.append( "./tabs/real_python" )
        # self.dir_for_tabs.append( "./tabs/layouts" )

        # # ---- min_complete
        # self.min_complete    = 10  # minimum value for HOW_COMPLETE

        # # ---- search and default
        # self.default_search     = ""
        # self.do_search_on_init  = False
        #     # do search right away, typically if default_search != ""

    # -------
    def __init__( self, ):
        """
        Init for instance, usually not modified, except perhaps debug stuff
        ( if any )... but use plus_test_mode()
        may be down in listing because it should not be messed with.
        """
        self.mode_default()
        self.os_tweaks()
        self.running_on_tweaks()
        self.choose_mode()

        # next lets you use  parameters.PARAMETERS as a global
        global PARAMETERS

        if not PARAMETERS:
            print( "creating global parameters.PARAMETERS")
            PARAMETERS    = self

        else:
            print( "__init__ probably an error")

        #rint( self ) # for debugging

    # -------
    def __init_2__( self, ):
        """
        replacable function
            self.__init_2__ = self.test_init_2
        this is called late in init of app to give access to parts created
        after parameters
        """

        print( "__init_2__   an error ??")

    # -------
    def test_init_2( self, ):
        """
        use to replacabl function
            self.__init_2__ = self.test_init_2
        beware circular imports
        """
        # from    app_global import AppGlobal
        # controller                  = AppGlobal.controller
        import m_scope

        # self.default_fn_functon     =  m_scope.gen_fn_stem
        # print( self.default_fn_functon( "file_prefix" ) )

    # ---------------------
    def to_columns( self, current_str, item_list, format_list = [ "{: <30}", "{:<30}" ], indent = "    "  ):
        """
        for __str__  probably always default format_list
        """
        #rint ( f"item_list {item_list}.............................................................. " )
        line_out  = ""
        for i_item, i_format in zip( item_list, format_list ):
            a_col  = i_format.format( i_item )
            line_out   = f"{indent}{line_out}{a_col}"
        ret_str  = f"{current_str}\n{line_out}"
        return ret_str

    # -----------------------------------
    def __str__( self,   ):
        """
        sometimes it is hard to see where values have come out this may help if printed.
        not complete, add as needed -- compare across applications and code above
        """
        # new_indented    = "\n    "   # but it nice to have some whitespace to see ...

        a_str   = ""
        a_str   = ">>>>>>>>>>* Parameters *<<<<<<<<<<<<"

        a_str   = self.to_columns( a_str, ["mode",
                                           f"{self.mode}" ] )

        a_str   = self.to_columns( a_str, ["our_os",
                                           f"{self.our_os}" ] )

        a_str   = self.to_columns( a_str, ["db_type",
                                           f"{self.db_type}" ] )

        a_str   = self.to_columns( a_str, ["db_file_name",
                                           f"{self.db_file_name}" ] )


        a_str   = self.to_columns( a_str, ["tab_db_type",
                                           f"{self.tab_db_type}" ] )
        a_str   = self.to_columns( a_str, [ "tab_db_file_name",
                                            f"{self.tab_db_file_name}" ] )

        a_str   = self.to_columns( a_str, ["help_fn",
                                           f"{self.help_fn}" ] )
        a_str   = self.to_columns( a_str, ["help_path",
                                           f"{self.help_path}" ] )
        a_str   = self.to_columns( a_str, ["icon",
                                           f"{self.icon}" ] )

        a_str   = self.to_columns( a_str, ["logger_id",
                                           f"{self.logger_id}" ] )

        a_str   = self.to_columns( a_str, ["logging_level",
                                           f"{self.logging_level}" ] )

        a_str   = self.to_columns( a_str, ["pylogging_fn",
                                                  f"{self.pylogging_fn}" ] )

        a_str   = self.to_columns( a_str, [ "log_mode",
                                                  f"{self.log_mode}" ] )

        a_str   = self.to_columns( a_str, ["minimun_useful",
                                           f"{self.minimun_useful}" ] )

        a_str   = self.to_columns( a_str, ["breakpoint_ok",
                                           f"{self.breakpoint_ok}" ] )

        a_str   = self.to_columns( a_str, ["pylogging_fn",
                                           f"{self.pylogging_fn}" ] )

        a_str   = self.to_columns( a_str, ["qt_height",
                                           f"{self.qt_height}" ] )
        a_str   = self.to_columns( a_str, ["qt_width",
                                           f"{self.qt_width}" ] )
        a_str   = self.to_columns( a_str, ["qt_xpos",
                                           f"{self.qt_xpos}" ] )
        a_str   = self.to_columns( a_str, ["qt_ypos",
                                           f"{self.qt_ypos}" ] )
        a_str   = self.to_columns( a_str, ["readme_fn",
                                           f"{self.readme_fn}" ] )
        a_str   = self.to_columns( a_str, ["text_editor",
                                           f"{self.text_editor}" ] )
        a_str   = self.to_columns( a_str, ["wat_qt_height",
                                           f"{self.wat_qt_height}" ] )
        a_str   = self.to_columns( a_str, ["wat_qt_width",
                                           f"{self.wat_qt_width}" ] )
        a_str   = self.to_columns( a_str, ["wat_qt_xpos",
                                           f"{self.wat_qt_xpos}" ] )
        a_str   = self.to_columns( a_str, ["wat_qt_ypos",
                                           f"{self.wat_qt_ypos}" ] )
        a_str   = self.to_columns( a_str, ["self.dir_for_tabs",
                                           f"{self.dir_for_tabs}" ] )

        return a_str


# ---- eof


