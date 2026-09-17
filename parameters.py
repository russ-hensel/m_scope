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
import string_utils


# ---- local imports

#import in_spect_env

global PARAMETERS

PARAMETERS   = None


# ========================================
class ScopeSetups( ):
    """
    a collection of scope setups for this run of the program

    """
    # -------
    def __init__( self, ):
        """

        """
        # it is really the name we want unique
        self.camera_setups      = set( )

    # -------
    def add_setup( self, camera_setup, ):
        """

        """
        camera_setups   = self.camera_setups
        #no_setups       = len( camera_setups )
        camera_setups.add( camera_setup )

    # -------
    def get_setup_dict( self,   ):
        """
        consider a sort
        """
        setup_dict      = {}  # dict comp ??
        camera_setups   = self.camera_setups

        for i_setup in camera_setups:
            setup_dict[ i_setup.setup_id ]  = i_setup

        return setup_dict

# ========================================
class ScopeSetup( ):
    """
    this is just a struct, I like it as a class
    gives an id to c  the scope and its usb sensor
    and then a list of configs for this setup

    a_setup = SetupConfig( setup_id      = "Setup id",
                               scope_name       = "Watson",
                               camera_name      = "users name for camera",
                               camera_usb_name  = "USB CAMERA...."
                               usb_format       = "1920x1080  Jpeg  30 fps"
                               scope_mag        = "objective",
                                   # or the objective
                               reticle_file     = "base reticle name",
                               reticle_scale    =  1.2 )

    ------------------------

    """

    def __init__( self, *,
                 setup_id,
                 scope_name,
                 camera_name,
                 camera_usb_name,
                 usb_format,
                 scope_mag,
                 reticle_file,
                 reticle_scale   ):
        """
        usual init
        """
        self.setup_id           = setup_id
        self.scope_name         = scope_name
        self.camera_name        = camera_name
        self.camera_usb_name    = camera_usb_name
        self.usb_format         = usb_format
        self.scope_mag          = scope_mag

       # self.interface_id       = interface_id
        self.reticle_file       = reticle_file
        self.reticle_scale      = reticle_scale

        # reticle_config_set = set()

        # if reticle_config
        #    reticle_config_set.add( reticle_config )

    #--------------------------
    def __str__( self ):
        """
        universal __str__
        """
        return string_utils.obj_to_str( self )

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
        #self.mode_millhouse()

        # --- add on for testing, use as desired edit mode for your needs
        #self.plus_test_mode()mode_dev_debug

    # ---- ---->> Methods: one for each mode
    # -------
    def new_user_mode( self ):
        """
        a mode for the new user, pretty much empty,
        a new user may experiment here.
        """
        self.mode               = "mode new_user"

    # -------
    def mode_dev_debug( self ):
        """
        for dev and debug, mostly for rsh
        now for kingholmer
        """
        self.mode               = "mode_dev_debug"

         # # ---- output
         # self.output_dir         = "./output"   #
         # self.photo_dir          = "./output"   #
         # self.reticle_dir        = "./misc"   #
         # self.reticle_dict        =  { "4x":   "4x_reticle.png",
         #                               "10x":  "10x_reticle.png"
         #                             }

        # good for kingholmer
        self.qt_width           = 1400
        self.qt_height          = 80    # 700 most of win height
        self.qt_xpos            = 10
        self.qt_ypos            = 10

         # # ---- output
         # self.output_dir         = "./output"   #
         # self.photo_dir          = "./output"   #
         # self.reticle_dir        = "./misc"   #
         # self.reticle_dict        =  { "4x":   "4x_reticle.png",
         #                               "10x":  "10x_reticle.png"
         #                             }

        # ---- output
        self.output_dir         = "/home/russ/global_sync/photo_temp"
        self.output_dir         = "./temp_photo"
        self.output_dir         = "./photos"

        self.photo_dir          = self.output_dir

    # -------
    def mode_millhouse( self ):
        """
        for dev and debug, mostly for rsh
        """
        self.mode               = "mode_millhouse"

         # # ---- output
         # self.output_dir         = "./output"   #
         # self.photo_dir          = "./output"   #
         # self.reticle_dir        = "./misc"   #
         # self.reticle_dict        =  { "4x":   "4x_reticle.png",
         #                               "10x":  "10x_reticle.png"
         #                             }

        # good for kingholmer
        self.qt_width           = 1500
        self.qt_height          = 600    # 700 most of win height
        self.qt_xpos            = 10
        self.qt_ypos            = 10

        # ---- output
        self.output_dir         = "/home/russ/sync_with_bulldog/global_sync/photo_temp"   #
        self.photo_dir          = self.output_dir

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

        # ---- .... icon
        self.icon               = r"./images/icon_red.png"    # icon for running app
        self.icon               = r"./icons/icons/binocular.png"
        self.scope_icon               = r"./misc/puzzle_16x16.png"
        self.view_icon               = r"./misc/binocular.png"

        self.text_editor        = "gedit"
        self.text_editor        = "xed"

        # ---- debug
        self.debug_flag         = True

        # ---- scope setups...............
        scope_setups           = ScopeSetups( )



        # ----  a_setup with prefix >from write_reticle<
        a_setup = ScopeSetup(
                               setup_id         = "russ on millhouse 4x",

                               scope_name       = "AO Russ",
                               scope_mag        = "4x",
                               camera_name      = "sv eyepeice",

                               camera_usb_name  = "SVBONY SV105C: SVBONY SV105C",
                               usb_format       = "1920x1080  Jpeg  30 fps",
                               reticle_file     = "/home/russ/sync_with_bulldog/_projects/m_scope/reticles/10x_reticle.png",
                               reticle_scale    =  2.15 )

        scope_setups.add_setup( a_setup )
        # setup end

        # ----  a_setup with prefix >from write_reticle<
        a_setup = ScopeSetup(
                               setup_id         = "russ on millhouse 10x",

                               scope_name       = "AO Russ",
                               scope_mag        = "10x",
                               camera_name      = "sv eyepeice",

                               camera_usb_name  = "SVBONY SV105C: SVBONY SV105C",
                               usb_format       = "1920x1080  Jpeg  30 fps",
                               reticle_file     = "/home/russ/sync_with_bulldog/_projects/m_scope/reticles/10x_reticle.png",
                               reticle_scale    =  6.3 )

        scope_setups.add_setup( a_setup )
        # setup end




        # ----  a_setup
        a_setup = ScopeSetup(
                               setup_id         = "Setup USB CAMERA: 1920x1080",
                                   # you make up a name for these values

                               # next are your names to help you keep track
                               scope_name       = "Watson 1",
                               scope_mag        = "4x ",
                               camera_name      = "sv eyepeice 1",

                               # next must match the parameters the usb interface emits
                               camera_usb_name  = "USB CAMERA: USB CAMERA",
                               usb_format       = "1920x1080  Jpeg  30 fps",

                               # these are up to you
                               reticle_file     = "10_cricles.png",
                                   # must be a file in ./reticles
                               reticle_scale    =  2.0     )

        scope_setups.add_setup( a_setup )

        # ----  a_setup
        a_setup = ScopeSetup(
                               setup_id         = "Setup USB CAMERA: 1280x720 ",

                               scope_name       = "Watson 300",
                               scope_mag        = "10x",
                               camera_name      = "sv eyepeice 300",

                               camera_usb_name  = "USB CAMERA: USB CAMERA",  #USB CAMERA: USB CAMERA
                               usb_format       = '1280x720  Jpeg  30 fps',
                               reticle_file     = "10x_reticle.png",
                               reticle_scale    =   .5    )

        scope_setups.add_setup( a_setup )
        # setup end
        # ----  a_setup with prefix >from write_reticle<
        a_setup = ScopeSetup(
                               setup_id         = "from wite_setup",

                               scope_name       = "weston",
                               scope_mag        = "1/10",
                               camera_name      = "built in ",

                               camera_usb_name  = "USB CAMERA: USB CAMERA",
                               usb_format       = "1920x1080  Jpeg  30 fps",
                               reticle_file     = "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/m_scope/reticles/10x_reticle.png",
                               reticle_scale    =  1.0 )

        scope_setups.add_setup( a_setup )
        # setup end


        # ----  a_setup with prefix >from write_reticle<
        a_setup = ScopeSetup(
                               setup_id         = "sunday test",

                               scope_name       = "test3",
                               scope_mag        = "test3 1/10",
                               camera_name      = "test3 built in ",

                               camera_usb_name  = "USB CAMERA: USB CAMERA",
                               usb_format       = "320x240  Jpeg  30 fps",
                               reticle_file     = "/mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/m_scope/reticles/10x_reticle.png",
                               reticle_scale    =  1.6 )

        scope_setups.add_setup( a_setup )
        # setup end



        # ---- cameras setup end
        self.scope_setups       = scope_setups

        #setup_dict[ a_setup.setup_id ]   =  a_setup

        # self.valid_cameras     = {}
        # self.valid_cameras[ "Camera 1 High Rez": ( "" , "" )]


        # setup_dict     = {"AO Lab scope": ( "AO similar to 1036A " "SvBony Telescope EyePeice  SV105 or SV106" )}
        #      # id then explain 2 parts
        #      # need to link to configs
        # config_dict     =   {"AO Standard Config": ( "interface id" "scope mag" "list of recicules" )}
        #                                             # CAMERA

        # reticle_dict    =   { "reticule_id": "filename" {scale}}


        # ---- reticle  overlay  defaults

        self.overlay_opacity    = 30

        self.blend_type         = "" # may need to move some enums
        self.blink_on           = False  # !! False = True = blink
        self.auto_load_snap     = True   # load the last snap
        self.overlay_on_snap    = True   # switch to the overlay tab

        # ---- output
        self.output_dir         = "./output"   #
        self.photo_dir          = "./output"   #
        #self.reticle_dir        = "./misc"   #
        self.reticle_dir        = "./reticles"       # !! in process

        # next now auto from reticle_dict, chang back ??
        self.default_ovelay     = "./misc/red_black_cross_2.jpg"  # file_name

        # ---- logging
        self.pylogging_fn           = f"{self.output_dir}/app.py_log"   # file name for the python logging

        self.log_mode               = "w"    # "a" append "w" truncate and write

        self.logging_level          = logging.DEBUG         # may be very verbose
        #self.logging_level          = logging.INFO
        #self.logging_level      = logging.INFO

        self.logger_id              = "m_scope"         # id of app in logging file

        self.default_fn_functon     = None


        # ---- file names -- but not db
        # control button for editing the readme file
        self.readme_fn      = "readme_rsh.txt"   # or None to suppress in gui
            # a readme file accessable from the main menu

        # or anything else ( will try to shell out may or may not work )
        self.help_fn        =  "./docs/help.txt"   #  >>. this is the path to our main .py file self.py_path + "/" +

        self.help_path      =  "./docs"
        self.help_path      =  "/mnt/WIN_D/russ/0000/python00/python3/_projects/qt5_by_example/docs/"
            # path leading to all docs and help



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
        pass

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


        a_str   = self.to_columns( a_str, ["output_dir",
                                           f"{self.output_dir}" ] )


        a_str   = self.to_columns( a_str, ["photo_dir",
                                           f"{self.photo_dir}" ] )



        a_str   = self.to_columns( a_str, ["our_os",
                                           f"{self.our_os}" ] )



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


        return a_str


# ---- eof


