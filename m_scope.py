#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
m_scope  PyQt6 using QtPy
"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln
# --------------------


import sys
import os
from   pathlib import Path
from   functools import partial

import logging
import time
from datetime import datetime

from qtpy import QtGui
from qtpy.QtGui import QAction, QPainter



from qtpy.QtCore import ( QDate )

from qtpy.QtWidgets import ( QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget,
                             QHBoxLayout,
                             QDateEdit,
                             QDialog,
                             QMessageBox,
                             QTabWidget,
                             QLabel,
                             QPushButton,
                             QVBoxLayout,
                             )


# ---- local imports

import  parameters
#import  image_overlay_view

import  overlay_tab
import  camera_cal_tab
import  camera_user_tab


import  note_tab
from    app_global import AppGlobal
import  utils
import  show_parameters
import  cq_combo_box_dict as cb_dict
import  write_config

basedir         = os.path.dirname( os.path.abspath( __file__ ) )

BLINK_MS        = 500

# what the blend combo offers.  Difference is the one that earns its keep for
# alignment: identical pixels come out black, so a misregistration lights up
COMPOSITION_MODES = [ ( "Normal ( over )", QPainter.CompositionMode.CompositionMode_SourceOver ),
                      ( "Difference",      QPainter.CompositionMode.CompositionMode_Difference ),
                      ( "Multiply",        QPainter.CompositionMode.CompositionMode_Multiply ),
                      ( "Screen",          QPainter.CompositionMode.CompositionMode_Screen ),
                      ( "Overlay",         QPainter.CompositionMode.CompositionMode_Overlay ),
                      ( "Darken",          QPainter.CompositionMode.CompositionMode_Darken ),
                      ( "Lighten",         QPainter.CompositionMode.CompositionMode_Lighten ),
                      ]

IMAGE_FILTER    = ( "Images (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.webp);;All files (*)" )


__VERSION__     = "ver_06 - 2026 09 13.02"



#-----------------------------
class SetupDialog( QDialog ):
    """
    An example dialog from chat then edited """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_gui()

    #-----------------------------
    def setup_gui(self):
        """
        what it says
        """
        self.setWindowTitle( "Enter Setup Name" )

        # Explicitly set the size (width, height)
        self.resize(400, 250)

        # Optional: Set minimum and maximum sizes
        self.setMinimumSize(300, 200)
        self.setMaximumSize(600, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        widget                  = QLabel("Setup Name:")
        layout.addWidget( widget )

        widget                  = QLineEdit()
        self.setup_name_widget  = widget
        layout.addWidget( widget )

        # Add buttons
        widget            = QPushButton("OK")
        widget.clicked.connect( self.accept )
        layout.addWidget( widget )

        widget             = QPushButton("Cancel")
        widget.clicked.connect( self.reject )
        layout.addWidget(widget)

    #-----------------------------
    def get_name(self):
        """
        Return the entered name
        """
        return self.setup_name_widget.text()

# -------------------------------
class MainWindow( QMainWindow ):
    """
    app mainwindow
    """
    def __init__(self):
        """
        Build the main window
        """
        super().__init__()
           # breakpoint()

        AppGlobal.controller    = self
        my_parameters           = parameters.Parameters()
        self.parameters         = my_parameters

        AppGlobal.parameters    = my_parameters

        # after parameters are set up
        import app_logging
        an_applogging    = app_logging.AppLogging( )
        # app_logging.init()

        qt_xpos             = my_parameters.qt_xpos
        qt_ypos             = my_parameters.qt_ypos
        qt_width            = my_parameters.qt_width
        qt_height           = my_parameters.qt_height

        self.setGeometry(  qt_xpos,
                           qt_ypos ,
                           qt_width,
                           qt_height  )

        self.app_name           = "m_scope"
        self.camera_cal_tab     = None
        self.camera_user_tab    = None
        self.note_tab           = None
        #self.tab_overlay     = None
        self.overlay_tab        = None

        self.setup_ok           = False
            # when applying a setup

        self.mode_edit_setup    = None  # allow edits setup not from parms

        self.last_setup         = None   # from parameters

        self.last_dir           = basedir  # for browse not sure good idea here
        self.current_fn_stem    = ""

        # after parameters are set up
        self.log_prog_info()

        # ---- build_gui
        self.build_gui()

        my_parameters.test_init_2()

    #----------------------------------------------------------------------
    def build_gui( self ):
        """
        what it says, read
        """
        my_parameters     = self.parameters
        self.setWindowTitle( f"M Scope  {__VERSION__}" )
        self.build_menu( )

        # icon    = QtGui.QIcon(  "./misc/broom_edit_2.png" )
        # icon    = QtGui.QIcon(  "./misc/magnifier.png" )
        icon    = QtGui.QIcon( my_parameters.scope_icon )

        self.setWindowIcon( icon )

        central_widget          = QWidget()
        self.setCentralWidget(central_widget)

        central_widget_layout   =  QVBoxLayout( central_widget )

        # --- out main layout
        layout          = QVBoxLayout(   )
        central_widget_layout.addLayout( layout )

        # ----   rows
        self.build_device_row( layout )
        self.build_thing_row( layout )
        self.build_action_row( layout )

        # ---- tabs
        self.tab_widget = QTabWidget()   # really the folder for the tabs
                                         # tabs themselves are just Widgets
        # there is another approach using a style sheet according to chat
        self.tab_widget.setTabsClosable( False )
        #self.tab_widget.tabCloseRequested.connect( self.close_tab )
        # Set custom height for the tabs
        self.tab_widget.setStyleSheet( "QTabBar::tab { height: 30px; }" )

        self.tab_widget.currentChanged.connect( self.on_tab_changed )
        self.tab_widget.tabBarClicked.connect(  self.on_tab_clicked )

        # self.tab_widget.tabCloseRequested.connect( self.on_tab_close_requested )
        # self.tab_widget.setTabsClosable( False )
            # Allows you to enable or disable the close button on tabs.
        self.tab_widget.setMovable( True )

        layout.addWidget( self.tab_widget   )

        # ---- tab notes
        tab                     = note_tab.NoteTab()
        self.note_tab           = tab
        title                   = "Control and Notes"
        self.tab_widget.addTab( tab, title  )

        # ---- tab overlay
        tab                     = overlay_tab.OverlayTab()
        self.overlay_tab        = tab
        title                   = "Reticle - Measure"
        self.tab_widget.addTab( tab, title  )

        self.build_menu()
        self.mode_edit_setup_on( False )

    # -------------------------------------
    def build_device_row( self, layout ):
        """
        what it says -- pick a camera, pick a format, start, stop.  the combos
        are filled from the widget, see on_camera_list / on_format_list
        """
        my_parameters       = AppGlobal.parameters

        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- setup id
        a_widget            = QLabel( "Setup ID valid:" )
        row_layout.addWidget( a_widget )

        scope_dict              = my_parameters.scope_setups.get_setup_dict()
        widget                  = cb_dict.CQComboBoxDict( scope_dict, display_keys = True )
        self.setup_id_widget    = widget
        widget.currentIndexChanged.connect( self.setup_id_widget_changed )
        widget.set_current_key( list(scope_dict.keys())[ 0 ] )
        row_layout.addWidget( widget, stretch = 2 )

        # ---- camera name
        a_widget                = QLabel( "Camera Name:" )
        row_layout.addWidget( a_widget )

        a_widget                = QLineEdit( "a_camera_name" )
        self.camera_name_widget = a_widget
        row_layout.addWidget( a_widget, )   #stretch = 2 )

        # ---- camera sensor
        a_widget            = QLabel( "Camera/Sensor:" )
        row_layout.addWidget( a_widget )

        # a_widget            = QComboBox( )
        a_widget            = QLineEdit( "xxx" )
        self.csensor_widget = a_widget
        a_widget.setMinimumWidth( 240 )
        a_widget.setReadOnly( True )
        #a_widget.currentIndexChanged.connect( self.on_device_combo_changed )
        # self.device_combo   = a_widget   # phase out
        # self.device_widget  = a_widget
        row_layout.addWidget( a_widget )

        # ---- usb format
        a_widget            = QLabel( "USB Format:" )
        row_layout.addWidget( a_widget )

        a_widget                = QLineEdit( )
        self.usb_format_widget  = a_widget
        a_widget.setReadOnly( True )
        a_widget.setMinimumWidth( 220 )
        #a_widget.currentIndexChanged.connect( self.on_sensor_widget_changed )
        #self.format_combo   = a_widget
        row_layout.addWidget( a_widget )

        row_layout.addStretch( 1 )

    # -------------------------------------
    def build_thing_row( self, layout ):
        """
        what it says --
        """
        my_layout       = layout

        row_layout      = QHBoxLayout(   )
        my_layout.addLayout( row_layout, )

        # ---- microscope
        # update on read or snap -- does snap save to a file
        widget                   =  QLabel( "Microscope:" )
        #self.file_stem_widget    = widget
        row_layout.addWidget( widget, )

        # -----
        widget                  = QLineEdit(  )
        self.microscope_widget  = widget
        # keys                        = my_parameters.scope_dict.keys()
        # #widget.currentIndexChanged.connect( self.microscope_widget_index_changed )
        # #widget.clicked.connect( self.test2    )
        # widget.addItems( keys )
        row_layout.addWidget( widget, )

        # ---- objective  self.scope_mag          = scope_mag
        a_widget                = QLabel( "Objective:" )
        row_layout.addWidget( a_widget )

        a_widget                = QLineEdit( "objective" )
        self.objective_widget   = a_widget
        row_layout.addWidget( a_widget, ) # stretch = 2 )

        # ---- mode
        a_widget                = QLabel( "Mode:not set" )
        self.mode_widget        = a_widget
        row_layout.addWidget( a_widget )

        # ---- switch_camera_tab button label in self.switch_camera_tab
        widget                   = QPushButton( "switch_camera_tab"   )
        self.switch_mode_widget  = widget
        widget.clicked.connect( self.switch_camera_tab )
        row_layout.addWidget( widget, )

        row_layout.addStretch( 1 )


    # -------------------------------------
    def build_action_row( self, layout ):
        """
        what it says -- pick a camera, pick a format, start, stop.  the combos
        are filled from the widget, see on_camera_list / on_format_list
        """
        row_layout          = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- write_reticle
        widget          =  QPushButton( "Write Reticle -\nMearurement" )
        widget.clicked.connect( self.write_reticle  )
        row_layout.addWidget( widget, )

        # ---- date
        widget          =  QLabel( "Date Tag:"  )
        row_layout.addWidget( widget, )

        widget                  =  QDateEdit( )
        self.date_code_widget   = widget
        widget.setCalendarPopup( True )
        today                   = QDate.currentDate()
        widget.setDate( today )
        # widget.setMinimumDate(QDate(1900, 1, 1))
        # widget.setMaximumDate(QDate(2100, 12, 31))
        widget.setDisplayFormat( "yyyy_MM_dd" )
        row_layout.addWidget( widget, )

        # ---- item = tag code
        widget          =  QLabel( "Id Tag:"  )
        row_layout.addWidget( widget, )

        # ---- item code widget
        widget                   =  QLineEdit( "temp" )
        self.item_code_widget    = widget
        row_layout.addWidget( widget, )

        # ---- current file stem
        # update on read or snap -- does snap save to a file
        widget                   = QLabel( "file_stem" )
        self.file_stem_widget    = widget
        row_layout.addWidget( widget, )

        row_layout.addStretch( 1 )

    #----------------------------------------------------------------------
    def build_menu( self ):
        """
        what it says, read
        """
        # Create the menu bar
        menubar   = self.menuBar()
        #menu_bar.Append(menu_1, "tx_menu_1")

        # ---- Configuration ............
        a_menu          = menubar.addMenu("Configuration")

        # ---- "Show Parameters"
        open_action     = QAction( "Show Parameters", self )
        connect_to      = self.show_parameters
        open_action.triggered.connect( connect_to )
        a_menu.addAction( open_action )

        #---------------
        open_action     = QAction( "Open Parameters", self )
        # connect_to      = AppGlobal.controller.os_open_parmfile
        # open_action.triggered.connect( connect_to )
        a_menu.addAction( open_action )

        # ---- "Open Log"
        open_action     = QAction( "Open Log", self )
        connect_to      = partial( AppGlobal.os_open_txt_file,
                                             AppGlobal.parameters.pylogging_fn  )
        open_action.triggered.connect( connect_to )
        a_menu.addAction( open_action )

        return

        # #---------------

        menu_1      = menu_bar.addMenu( "Configuration" )


        partial_function = partial( self.menu_open_txt_file, file_name = "parameters.py" )
        action.triggered.connect( partial_function )

        #---- Edit Readme
        action    = menu_1.addAction( "Edit Readme" )
        partial_function = partial( self.menu_open_txt_file, file_name = "readme_rsh.txt" )
        action.triggered.connect( partial_function )


        # ---- Help
        menu_2      = menu_bar.addMenu( "Help" )

        # ----  "Help Info"
        action    = menu_2.addAction( "Help Info" )
        partial_function = partial( self.menu_open_txt_file, file_name = "help.txt"  )
        action.triggered.connect( partial_function )

        #---- Technical Information
        action    = menu_2.addAction( "Technical Information" )
        partial_function = partial( self.menu_open_txt_file, file_name = "technical.txt"  )
        action.triggered.connect( partial_function )

        # help_function    = partial( AppGlobal.os_open_txt_file, "./help/technical.txt" )
        # a_menu.add_command( label   = "Show Technical Information",


    # --------------------------------------------
    def log_prog_info( self,  ):
        """
        record info about the program to the log file
        """
        fll         = AppGlobal.force_log_level
        logger      = logging.getLogger( )
        # logger      = self.logger
        logger.log( fll, "" )
        logger.log( fll, "============================" )
        logger.log( fll, "" )
        title       =   ( f"Application: {self.app_name} in mode {AppGlobal.parameters.mode}"
                          f"and version  {__VERSION__}" )
        logger.log( fll, title )
        logger.log( fll, "" )

        if len( sys.argv ) == 0:   # ??
            logger.info( "no command line arg " )
        else:
            for ix_arg, i_arg in enumerate( sys.argv ):
                msg = f"command line arg + {str( ix_arg ) }  =  { i_arg })"
                logger.log( AppGlobal.force_log_level, msg )

        msg          = f"current directory {os.getcwd()}"
        logger.log( fll, msg  )

        start_ts     = time.time()
        dt_obj       = datetime.utcfromtimestamp( start_ts )
        string_rep   = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        msg          = f"Time now: {string_rep}"
        logger.log( fll, msg )
        # logger_level( "Parameters say log to: " + self.parameters.pylogging_fn )
                         # parameters and controller not available can get fro logger_level

    # -------------------------------------
    def switch_camera_tab( self, ):
        """
        what it says
             we should apply self.last_setup
             as necessary
             will change self.mode_edit_setup
                  enable/disable
                  camera name
                  microscope
                  objective mag
                  ridicule file open


        """
        self.mode_edit_setup_on( not( self.mode_edit_setup ) )

    # -------------------------------------
    def mode_edit_setup_on( self,  on_off_flag ):
        """
        what it says  mode_edit_setup
            when true the setup may be altered then saved
            will change self.mode_edit_setup
            zzt
        """
        if self.mode_edit_setup == on_off_flag:
            return

        self.mode_edit_setup     = on_off_flag

        if on_off_flag:
            tab     = self.add_camera_cal_tab()
            self.mode_widget.setText( "Mode: Create \nCalibration Setup" )
            self.switch_mode_widget.setText( "Change Mode\nto Measure")

        else:
            tab     = self.add_user_camera_tab()
            self.mode_widget.setText( "Mode: Measure \nUsing Setup" )
            self.switch_mode_widget.setText( "Change Mode\nto Calibrate" )
            # !! make sure mode is one in current drop down
            self.setup_id_widget_changed( )

        self.enable_load_reticle_widget( on_off_flag )

        self.enable_scale_widget( on_off_flag )

        self.enable_widget_mscope_name( on_off_flag )
        self.enable_widget_objective_name( on_off_flag )
        self.enable_widget_camera_name( on_off_flag )

        # self.write_setup_widget.setEnabled( on_off_flag )
        # self.tab_widget.setCurrentWidget( tab )

    # -------------------------------------
    def get_camera_tab( self, ):
        """
        camera_tab  = AppGlobal.controller.get_camera_tab()
        """
        if self.camera_user_tab:
            return  self.camera_user_tab

        else:
            return self.camera_cal_tab


    # -------------------------------------
    def delete_tab( self, widget ):
        """
        what it says, should fail silently or perhaps add a return code
        """
        tab_widget      = self.tab_widget

        try:
            index       = tab_widget.indexOf( widget )

        except:
            return

        if index < 0:
            return

        tab_widget.removeTab( index )
        widget.deleteLater()

    # -------------------------------------
    def setup( self, a_setup ):
        """
        what it says
            do the harder ones first
        """
        self.setup_ok   = False
        setup_id        =  a_setup.setup_id
            # not easy, but from the drop down so nothing
        scope_name      =  a_setup.scope_name
            # no just a string
        camera_name     =  a_setup.camera_name
            # easy to apply just a string -- Camera Sensor ?
            # set_device_by_description
        camera_usb_name =  a_setup.camera_usb_name
            # may fail do after camera name
        scope_mag       =  a_setup.scope_mag
            # just a string
        reticle_file    =  a_setup.reticle_file
            # file might not exist
        reticle_scale   =  a_setup.reticle_scale
            # fail only on bad number

        camera_tab      = self.get_camera_tab( )

        camera_widget   = camera_tab.camera_widget
        ix   = camera_widget.set_device_by_description( camera_name )
        print( ix )

    # -------------------------------------
    def add_user_camera_tab( self, ):
        """
        what it says
            add one tab, delete the other
        """
        if self.camera_user_tab:
            return

        self.delete_tab( self.camera_cal_tab  )
        self.camera_cal_tab      = None

        tab                     = camera_user_tab.CameraUserTab()
        self.camera_user_tab    = tab
        title                   = "Specimen Camera"
        self.tab_widget.addTab( tab, title  )

        return tab

    # -------------------------------------
    def add_camera_cal_tab( self, ):
        """
        what it says
        """
        if self.camera_cal_tab:
            return

        self.delete_tab( self.camera_user_tab )
        self.camera_user_tab     = None

        tab                     = camera_cal_tab.CameraCalTab()
        self.camera_cal_tab     = tab
        title                   = "Calibration Camera"
        self.tab_widget.addTab( tab, title  )

        return tab

    #----------------------------------------------------------------------
    def menu_open_txt_file( self, event, file_name ):
        """
        use partial
        partial_function   = self.menu_open_txt_file
        partial_function   = value_from_hundreds = partial(         partial_function   = , units = 2, tens = 1 )
        partial_function = partial( self.menu_open_txt_file, file_name = "parameters.py" )

       Args:
            event (TYPE): DESCRIPTION.

        Returns:
            None.

        """
        #rint( f"menu_open_txt_file event     >{event}<")
        #rint( f"menu_open_txt_file file_name >{file_name}<")
        AppGlobal.os_open_txt_file( file_name )

    # -----------------------
    def show_parameters(self):
        """
        what it says,
        """
        dialog     = show_parameters.DisplayParameters( parent = self )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            pass

    # -------------------------------------
    def write_setup_configxxx( self, ):
        """
        what it says

            self.setup_id           = setup_id
            self.scope_name         = scope_name
            self.camera_name        = camera_name
            self.camera_usb_name    = camera_usb_name
            self.usb_format         = usb_format
            self.scope_mag          = scope_mag

           # self.interface_id       = interface_id
            self.reticle_file       = reticle_file
            self.reticle_scale      = reticle_scale

        """
        dialog      = write_config.ConfigWriter( self,
                                   self,
                                     )

        dialog.exec()       # blocks here until a button closes it
                            # exec() not exec_(), exec_ is gone in PyQt6


        return
        1/0 # -- next code moved to dialog but now using some in add_to_msg
        #= AppGlobal.controller.note_tab # control = note
        if not self.mode_edit_setup:
            msg    = "you are not in create setup mode"
            print( msg )
            return

        a_camera_cal_tab     = self.camera_cal_tab
        a_note_tab           = self.note_tab
        a_overlay_tab        = self.overlay_tab

        setup_id            = "get from user" # self.setup_id_widget.currentText()

        scope_name          = self.get_widget_mscope_name( )

        scope_mag           = self.get_widget_objective_name()

        camera_name         = self.get_widget_camera_name()

        # camera_name         = a_camera_cal_tab.camera_name_widget.text()

        camera_usb_name     = self.get_widget_csensor_name()

        usb_format          = self.get_widget_usb_format_name()

        scale                = a_overlay_tab.scale_widget.value()

        reticle_fn           = self.get_reticle()   # "tbd"   #a_overlay_tab.reticle_fn_widget.text()

        objective            = self.get_widget_objective_name()

       #  scope_mag            = objective  # so not used

       # format_text         = a_camera_cal_tab.sensor_widget.currentText()

       # self.camera_id_widget.setText( format_text )
        #camera_id_text      = a_camera_cal_tab.camera_id_widget.text()

        # msg     = f"{camera_id_text} --> {format_text}"
        # print( msg )

        msg        = f"""
        # ----  a_setup
        a_setup = ScopeSetup(
                               setup_id         = "{setup_id}",

                               scope_name       = "{scope_name}",
                               scope_mag        = "{objective}",
                               camera_name      = "{camera_name}",

                               camera_usb_name  = "{camera_usb_name}",
                               usb_format       = "{usb_format}",
                               reticle_file     = "{reticle_fn}",
                               reticle_scale    =  {scale} )

        scope_setups.add_setup( a_setup )
        # setup end

                        """

        self.note_tab.display_string( "\n")
        self.note_tab.display_string( msg )

    # -------------------------------------
    def setup_id_widget_changed( self, ):
        """
        what it says
        a_widget.currentIndexChanged.connect( self.on_device_combo_changed )

        setup_id_widget_changed

                change the setup items in all of gui

                reticle_fn still has to be set and on each change !!
                camera name

        """
        self.setup_ok   = True
        try:
            debug_msg    = ( "setup_id_widget_changed:" )
            logging.debug( debug_msg )

            a_setup   = self.setup_id_widget.current_value() # value of the dict

            debug_msg    = ( f"setup_id_widget_changed() {str( a_setup ) = }" )
            logging.debug( debug_msg )

            self.last_setup = a_setup

            # ---- mscope_name
            mscope_name     = a_setup.scope_name
            self.set_widget_mscope_name( mscope_name )
            self.enable_widget_mscope_name( False )

            # ---- scope_mag
            name        = a_setup.scope_mag
            self.set_widget_objective_name( name )
            self.enable_widget_objective_name( False )

            # ---- camera name
            camera_name     = a_setup.camera_name  # like brand name not on list
            self.set_widget_camera_name( camera_name )
            self.enable_widget_camera_name( False )

            # ---- camera_usb_name  csensor_name
            name        = a_setup.camera_usb_name
            self.set_widget_csensor_name( name )
            self.enable_widget_csensor_name( False )

            # ---- usb format
            name        = a_setup.usb_format
            self.set_widget_usb_format_name( name )
            self.enable_widget_usb_format_name( False )

            # ----  reticle
            name        = a_setup.reticle_file
            self.set_reticle( name )
            self.enable_reticle_wdiget( False )

            # ---- reticle_scale
            value        = a_setup.reticle_scale
            self.set_scale( value )
            self.enable_scale_widget( False )

        except Exception as an_except:
            self.setup_ok           = False
            error_msg               = str( an_except )
            logging.error( error_msg )

    # -------------------------------
    def add_image_info_to_msg( self, image_fn, prefix  ):
        """
        add image info to the message area
            check in right mode ?
            zz
        """
        if self.mode_edit_setup:
            mode    = "mode = edit_setup"
        else:
            mode    = "mode = user_mode"

        base_fn     = self.get_base_fn( )
        x, y        = self.get_x_y()

        msg         = f"""
        add_image_info_to_msg
        Adding image with prefix >{prefix}< in mode >{mode}<
        image file name   = {image_fn}
        base_file_name    = {base_fn}
        x position        = {x}
        y position        = {y}
                            """

        text_edit    = self.note_tab.message_area.text_edit
        text_edit.append( msg )

    # -------------------------------
    def add_setup_to_msg( self, prefix  ):
        """
        deprecate and remove
        add info to the message area
        check in right mode ?
        this is the setup info -- not quite right for camera
        """
        a_camera_cal_tab    = self.camera_cal_tab
        a_note_tab          = self.note_tab
        a_overlay_tab       = self.overlay_tab

        # in some case may want to parameterize
        #setup_id            = "get from user" #

        if self.mode_edit_setup:
            setup_id            =  self.setup_name_from_dialog()

            if setup_id == "":
                raise Exception   # fix to correct except

        else:
            setup_id            = self.setup_id_widget.currentText()

        scope_name          = self.get_widget_mscope_name( )

        camera_name         = self.get_widget_camera_name()

        # camera_name         = a_camera_cal_tab.camera_name_widget.text()

        camera_usb_name     = self.get_widget_csensor_name()

        usb_format          = self.get_widget_usb_format_name()

        scale                = a_overlay_tab.scale_widget.value()

        reticle_fn           = self.get_reticle()   # "tbd"   #a_overlay_tab.reticle_fn_widget.text()

        objective            = self.get_widget_objective_name()

       # format_text         = a_camera_cal_tab.sensor_widget.currentText()

       # self.camera_id_widget.setText( format_text )
        #camera_id_text      = a_camera_cal_tab.camera_id_widget.text()

        # msg     = f"{camera_id_text} --> {format_text}"
        # print( msg )

        msg        = f"""
        add_setup_to_msg
        # ----  a_setup with prefix >{prefix}<
        a_setup = ScopeSetup(
                               setup_id         = "{setup_id}",

                               scope_name       = "{scope_name}",
                               scope_mag        = "{objective}",
                               camera_name      = "{camera_name}",

                               camera_usb_name  = "{camera_usb_name}",
                               usb_format       = "{usb_format}",
                               reticle_file     = "{reticle_fn}",
                               reticle_scale    =  {scale} )

        scope_setups.add_setup( a_setup )
        # setup end

                        """

        text_edit    = self.note_tab.message_area.text_edit
        text_edit.append( msg )

    # -------------------------------
    def add_to_msg( self, prefix  ):
        """
        deprecate and remove
        add info to the message area
        check in right mode ?
        this is the setup info -- not quite right for camera
        """
        a_camera_cal_tab    = self.camera_cal_tab
        a_note_tab          = self.note_tab
        a_overlay_tab       = self.overlay_tab

        # in some case may want to parameterize
        #setup_id            = "get from user" #
        setup_id            = self.setup_id_widget.currentText()

        scope_name          = self.get_widget_mscope_name( )

        scope_mag           = self.get_widget_objective_name()

        camera_name         = self.get_widget_camera_name()

        # camera_name         = a_camera_cal_tab.camera_name_widget.text()

        camera_usb_name     = self.get_widget_csensor_name()

        usb_format          = self.get_widget_usb_format_name()

        scale                = a_overlay_tab.scale_widget.value()

        reticle_fn           = self.get_reticle()   # "tbd"   #a_overlay_tab.reticle_fn_widget.text()

        objective            = self.get_widget_objective_name()

       #  scope_mag            = objective  # so not used

       # format_text         = a_camera_cal_tab.sensor_widget.currentText()

       # self.camera_id_widget.setText( format_text )
        #camera_id_text      = a_camera_cal_tab.camera_id_widget.text()

        # msg     = f"{camera_id_text} --> {format_text}"
        # print( msg )

        msg        = f"""
        add_to_msg
        # ----  a_setup with prefix >{prefix}<
        a_setup = ScopeSetup(
                               setup_id         = "{setup_id}",

                               scope_name       = "{scope_name}",
                               scope_mag        = "{objective}",
                               camera_name      = "{camera_name}",

                               camera_usb_name  = "{camera_usb_name}",
                               usb_format       = "{usb_format}",
                               reticle_file     = "{reticle_fn}",
                               reticle_scale    =  {scale} )

        scope_setups.add_setup( a_setup )
        # setup end

                        """

        text_edit    = self.note_tab.message_area.text_edit
        text_edit.append( msg )

    # ------------------------------------
    def setup_name_from_dialog( self ):
        """
        What it says

        """
        dialog = SetupDialog()

        if dialog.exec_() == QDialog.Accepted:
            name = dialog.get_name()

        else:
            name    = ""

        print( "name", name )
        return name

    # -------------------------------
    def on_snap_still( self, ):
        """
        this is the user mode
        similar to dual_wwrite whose name may be change soon
            write out the camera photo and the notes
            useful in app
        """
        self.tab_widget.setCurrentWidget( self.note_tab )

        try:
            fn_no_ext       = self.get_fn_no_ext()
                # we get once but use twice

        except ValueError:
            return

        file_name       = self.get_file_name( fn_no_ext, ".txt" )

        tab_note        = self.note_tab
        self.add_image_info_to_msg( file_name, "from on_snap_still_cal" )
        self.add_to_msg( "from on_snap_still" )

        self.save_msg_area_to_file( file_name )

        tab             = self.get_camera_tab( )
        tab.save_snap( fn_no_ext )

    # -------------------------------
    def on_snap_still_cal( self, ):
        """
        this is in the calibrate mode

        """
        self.tab_widget.setCurrentWidget( self.note_tab )

        try:
            fn_no_ext       = self.get_fn_no_ext()
                # we get once but use twice

        except ValueError:
            return

        file_name       = self.get_file_name( fn_no_ext, ".txt" )
        tab_note        = self.note_tab

        self.add_image_info_to_msg( file_name, "from on_snap_still_cal" )
        self.add_to_msg( "from on_snap_still_cal" )

        self.save_msg_area_to_file( file_name )

        tab             = self.get_camera_tab( )
        tab.save_snap( fn_no_ext )

    # -------------------------------
    def write_reticle( self, ):
        """
        write_reticle copy of but change dual_wwrite
            write out the overlay photo and the notes
            how does this differed from other writes and
            calibration
            zz
        """
        try:
            fn_no_ext       = self.get_fn_no_ext()
                # we get once but use twice

        except ValueError:
            return

        # tab_note        = self
        file_name       = self.get_file_name( fn_no_ext, ".txt" )
        tab_note        = self.note_tab
        #note_tab.save_file( file_name )

        file_name       = self.get_file_name( fn_no_ext, ".jpg" )
        a_overlay_tab   = self.overlay_tab
        a_overlay_tab.save_file( file_name )

        self.tab_widget.setCurrentWidget( self.note_tab )

        self.add_image_info_to_msg( file_name, "from write_reticle" )
        self.add_setup_to_msg( "from write_reticle" )

        # tab_note        = self
        file_name       = self.get_file_name( fn_no_ext, ".txt" )
        tab_note        = self.note_tab
        #note_tab.save_file( file_name )
        self.save_msg_area_to_file( file_name )

    # -------------------------------
    def dual_writexxxx( self, ):
        """
        dual_write
            write out the overlay photo and the notes
            this may be absolute, see write+reticle
        """
        self.tab_widget.setCurrentWidget( self.note_tab )
        self.add_to_msg( "from dual_wwrite >> stop using" )

        try:
            fn_no_ext       = self.get_fn_no_ext()
                # we get once but use twice

        except ValueError:
            return

        # tab_note        = self
        file_name       = self.get_file_name( fn_no_ext, ".txt" )
        tab_note        = self.note_tab
        #note_tab.save_file( file_name )
        self.save_msg_area_to_file( file_name )

        file_name       = self.get_file_name( fn_no_ext, ".jpg" )
        a_overlay_tab   = self.overlay_tab
        a_overlay_tab.save_file( file_name )

    # -------------------------------
    def write_note( self, ):
        """
        to write note button
            and see camera_tab.on_snap_still()
            writes a note only, may be useful code but not useful to app
        """
        self.tab_widget.setCurrentWidget( self.note_tab )
        self.add_to_msg( "from write_note"  )

        parameters  = AppGlobal.parameters

        # # fn_stem     = self.get_fn_stem() ??
        # fn_stem     = self.get_fn_no_ext()

        output_dir  = parameters.output_dir

        try:
            stem    = self.get_fn_no_ext()

        except ValueError:
            return

        file_name   = stem + ".txt"

        # path        = Path( output_dir )   # not complete
        # path        = path.resolve( )
        # full_path   = path / file_name
        # file_name   = str( full_path )
        # need to add setup name to the message area

        self.save_msg_area_to_file( file_name )

    # -------------------------------------
    def save_msg_area_to_file( self, file_name ):
        """
        overwrite
        """
        note_tab    = self.note_tab
        the_text    = note_tab.message_area.get_plain_text()

        with open(  file_name, 'w' ) as a_file:
            a_file.write( the_text )

    # -------------------------------------
    def get_fn_no_ext( self, ):
        """
        what it says
            fn_no_ext = controller.get_fn_no_ext()
            this puts a time stamp on it so it is unique
            may use with more than one extension
        """
        #note_tab        = self.note_tab
        item_code       = self.item_code_widget.text()
        # test for not blank
        if not item_code:
            msg_box_msg    = "Please add an Item Code"
            msg_box        = QMessageBox()
            msg_box.setIcon( QMessageBox.Information )
            msg_box.setText(  msg_box_msg  )
            msg_box.setWindowTitle( "We have a Problem" )
            msg_box.setStandardButtons( QMessageBox.Ok )

            ret    = msg_box.exec_( )
            raise ValueError( )

        date_code       = self.date_code_widget.date().toString(  'yyyy_MM_dd' )
        prefix          = f"{date_code}_{item_code}"

        file_stem       = utils.gen_fn_stem( prefix )  # import utils
            # no path to, no ext
        self.file_stem_widget.setText( file_stem )

        parameters   = AppGlobal.parameters
        output_dir   = parameters.output_dir

        fn_no_ext    = f"{output_dir}/{file_stem}"
            # all but ext

        return fn_no_ext

    # ---- get set enable !! could make widget names properties ?? ============================
    # ---- item code
    def get_item_code( self,  ):
        """
        what it says
        """
        value      = self.item_code_widget.text()

        return value

    # -------------------------------------
    def set_item_code( self, value ):
        """
        to the widget
        """
        self.item_code_widget.setText( value  )

        return

    # -------------------------------------
    def enable_widget_item_code( self, enable = True ):
        """
        from the widget
        """
        widget       = self.item_code_widget
        widget.setReadOnly( not enable )

        return

    # ---- mscope_name ...........................
    # -------------------------------------
    def get_note_text( self,  ):
        """
        what it says
        """
        tab        = self.note_tab
        value      = tab.message_area.get_plain_text()

        return value

    # ---------------------
    #         # ---- objective  self.scope_mag          = scope_mag
    #         a_widget            = QLabel( "Objective:" )
    #         row_layout.addWidget( a_widget )

    #         a_widget                = QLineEdit( "objective" )
    #         self.objective_widget   = a_widget

    # ----------------

    # ---- widget_objective
    def get_widget_objective_name( self,  ):
        """
        from the widget
        """
        widget       = self.objective_widget
        value        = widget.text()

        return value

    # -------------------------------------
    def set_widget_objective_name( self, name ):
        """
        from the widget
        """
        widget       = self.objective_widget
        widget.setText( name )

        return

    # -------------------------------------
    def enable_widget_objective_name( self, enable = True ):
        """
        from the widget
        """
        widget       = self.objective_widget
        widget.setReadOnly( not( enable ) )

    # ---- camera_name ................
    def get_widget_camera_name( self,  ):
        """
        from the widget
          self.device_combo
        """
        widget       = self.camera_name_widget
        value        = widget.text()

        return value

    # -------------------------------------
    def set_widget_camera_name( self, camera_name ):
        """

              self.device_combo
        """
        widget       = self.camera_name_widget
        widget.setText( camera_name )

        # if self.mode_edit_setup:
        #     tab          = self.camera_cal_tab
        #     xx =2
        #     # tab.set_widget_usb_format_name( name )
        #     tab.set_widget_device_combo_name( camera_name  )


    # -------------------------------------
    def enable_widget_camera_name( self, enable = True ):
        """
        from the widget
        """
        widget       = self.camera_name_widget
        widget.setReadOnly( not( enable ) )

    # ---- csensor  camera_sensor_name ...................
    # -------------------------------------
    def get_widget_csensor_name( self,  ):
        """
        may depend on mode,

        self.camera_cal_tab

        self.camera_user_tab

        a_widget            = QComboBox(   )
        self.device_combo   = a_widget

        """
        mode         = self.mode_edit_setup
        if mode:
            # setup mode
            tab        = self.camera_cal_tab
            value      = tab.device_combo.currentText()     #  QComboBox
        else:
            widget       = self.csensor_widget
            value        = widget.text()

        return value

    # -------------------------------------
    def set_widget_csensor_name( self, name ):
        """
        from the widget
        """
        widget       = self.csensor_widget
        widget.setText( name )

        if self.mode_edit_setup:
            tab          = self.camera_cal_tab
            # tab.set_widget_usb_format_name( name )
            tab.set_widget_device_combo_name( name  )

    # -------------------------------------
    def enable_widget_csensor_name( self, enable = True ):
        """
        from the widget
        """
        widget       = self.csensor_widget
        widget.setReadOnly( not( enable ) )

    # ---- scale ...................
    # -------------------------------------
    def get_scale( self,  ):
        """
        what it says
        """
        tab          = self.overlay_tab
        widget       = tab.scale_widget
        value        = widget.value()

        return value

    # -------------------------------------
    def set_scale( self, value ):
        """
        what it says
        """
        tab          = self.overlay_tab
        widget       = tab.scale_widget
        widget.setValue( value )

    # -------------------------------------
    def enable_scale_widget( self, enable = True ):
        """
        what it says
            plus reset
        """
        tab          = self.overlay_tab
        widget       = tab.scale_widget
        widget.setReadOnly( not enable )
        #widget.setEnabled( enable  )

        widget       = tab.reset_widget
        widget.setEnabled( enable  )

    # ---- base_fn_widget ...................
    def get_base_fn( self,  ):
        """
        what it says zz base_fn_widget
        """
        tab          = self.overlay_tab
        widget       = tab.base_fn_widget
        value        = widget.text()

        return value

    # -------------------------------------
    def set_base_fnxxx( self, file_name ):
        """
        set the value and load the file
            file_name is in the reticle_dir
        """
        a_dir    = self.parameters.reticle_dir
        fn       = ( a_dir + "/"  + file_name ).replace( "//", "/" )
            # now full file name

        tab          = self.overlay_tab
        msg          = tab.load_overlay( fn ) # loads file set name

        return msg   # msg on a fail else ""

    # -------------------------------------
    def enable_base_fn_wdiget( self, enable = True ):
        """
        this widget is a label so not an edit no read only
        """
        return

    # ---- reticle ...................
    def get_reticle( self,  ):
        """
        what it says zz
        """
        tab          = self.overlay_tab
        widget       = tab.reticle_fn_widget
        value        = widget.text()

        return value

    # -------------------------------------
    def set_reticle( self, file_name ):
        """
        set the value and load the file
            file_name is in the reticle_dir
            !! is this correct
        """
        dir      = self.parameters.reticle_dir
        fn       = ( dir + "/"  + file_name ).replace( "//", "/" )
            # now full file name

        tab          = self.overlay_tab
        msg          = tab.load_overlay( fn ) # loads file set name

        return msg   # msg on a fail else ""

    # -------------------------------------
    def enable_reticle_wdiget( self, enable = True ):
        """
        this widget is a label so not an edit no read only
        """
        return

    # ---- x_y = x and y ...................
    def get_x_y( self,  ):
        """
        what it says zz
        """
        tab          = self.overlay_tab
        widget       = tab.y_spin
        y_value      = widget.value()

        widget       = tab.x_spin
        x_value      = widget.value()

        return x_value, y_value

    # # -------------------------------------
    # def set_x_y( self, file_name ):
    #     """
    #     set the value and load the file
    #         file_name is in the reticle_dir
    #         !! is this correct
    #     """
    #     dir      = self.parameters.reticle_dir
    #     fn       = ( dir + "/"  + file_name ).replace( "//", "/" )
    #         # now full file name

    #     tab          = self.overlay_tab
    #     msg          = tab.load_overlay( fn ) # loads file set name

    #     return msg   # msg on a fail else ""

    # # -------------------------------------
    # def enable_x_y_wdiget( self, enable = True ):
    #     """
    #     this widget is a label so not an edit no read only
    #     """
    #     return

    # ---- mscope_name ...........................
    def get_widget_mscope_name( self,  ):
        """
        what it says
        """
        widget       = self.microscope_widget
        value        = widget.text()

        return value

    # -------------------------------------
    def set_widget_mscope_name( self, camera_name ):
        """
        what it says
        """
        widget       = self.microscope_widget
        widget.setText( camera_name )

    # -------------------------------------
    def enable_widget_mscope_name( self, enable = True ):
        """
        what it says
        """
        widget       = self.microscope_widget
        widget.setReadOnly( not( enable ) )

    # ----  usb format
    def get_widget_usb_format_name( self,  ):
        """
        what it says
        zz

        self.sensor_widget   = QComboBox(   )
        """
        mode         = self.mode_edit_setup
        if mode:
            # setup mode
            tab        = self.camera_cal_tab
            value      = tab.sensor_widget.currentText()     #  QComboBox

        else:
            widget       = self.usb_format_widget
            value        = widget.text()

        return value

    # -------------------------------------
    def set_widget_usb_format_name( self, name ):
        """
        from the widget

           return
               None or exception
        """
        widget       = self.usb_format_widget
        widget.setText( name )

        if   self.mode_edit_setup:
            tab          = self.camera_cal_tab
            tab.set_widget_usb_format_name( name )

    # -------------------------------------
    def enable_widget_usb_format_name( self, enable = True ):
        """
        from the widget
        """
        widget       = self.usb_format_widget
        widget.setReadOnly( not( enable ) )

    # -------------------------------------
    def enable_load_reticle_widget( self, enable = True ):
        """
        from the widget
        """
        tab          = self.overlay_tab
        widget       = tab.load_reticle_widget
        widget.setEnabled( enable )

    # -------------------------------------
    def get_file_name( self, fn_no_ext, ext ):
        """
        put extension on fn_no_ext
            ext    like .txt
            file_name     = controller.get_file_name( fn_no_ext, ext )
        """
        file_name    = fn_no_ext + ext

        path         = Path( file_name )
        path         = path.resolve( )

        file_name    = str( path )

        return file_name

    # -------------------------------------
    def on_tab_changed( self, ):
        """ """
    # -------------------------------------
    def on_tab_clicked( self, ):
        """ """

    # ---- experiments -------------------------------------
    def get_setup_from_file( self, file_name ):
        """
        setup_id         = "get from user",

        """
        setup_id         = utils.get_setup_from_file( file_name )

        return  ""  # ?? is this right

        a_list    = utils.read_file_to_list( file_name )

        for i_line in reversed( a_list ):
            #rint( i_line )
            i_line   = i_line.strip( )
            splits   = i_line.split( "=" )
            if len( splits ) != 2:
                continue

            parm   = splits[ 0 ].strip()
            if parm == "setup_id":
                setup  = splits[1]
                print( f"get_setup_from_file() found setup >{setup}<")
                break

        else:
            setup  = ""

        return setup

    # ---- experiments -------------------------------------
    def test_something( self,  ):
        """

        """

# -------------------------------------
def main(): # do not remove
    app         = QApplication( sys.argv )
    window      = MainWindow()
    window.show()

    # QtPy handles the exec_() vs exec() difference automatically
    app.exec()

# for tests, move
#if __name__ == '__main__':

# ---- eof
