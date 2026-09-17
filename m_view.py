#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
m_scope  PyQt6 using QtPy
"""

# # --------------------
# if __name__ == "__main__":
#     #----- run the full app
#     #import main   # noqa  stops auto removal by pycln

#     main()
# # --------------------

import sys
import os
from   pathlib import Path
from   functools import partial
import logging
import time
from   datetime import datetime

from   qtpy import QtGui


from qtpy.QtWidgets import ( QApplication, QMainWindow,  QWidget, QAction, QPainter,
                             QFileDialog,
                             QHBoxLayout,
                             QDialog,
                             QMessageBox,
                             QLabel,
                             QPushButton,
                             QVBoxLayout,
                             )




# ---- local imports

import  parameters
#import  image_overlay_view


import  gui_qt_ext
from    app_global import AppGlobal
import  utils
import  show_parameters

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


__VERSION__     = "ver_06 - 2026 09 13.01"



# -------------------------------
class MainWindow( QMainWindow ):
    def __init__( self ):
        """
        Build the main window
        """
        super().__init__()
           # breakpoint()

        #self.setWindowTitle( "M Scope" )

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

        #app_logging.init()

        self.app_name           = "m_view"

        self.setup_ok           = False
            # when applying a setup


        self.last_dir           = basedir  # for browse not sure good idea here
        self.current_fn_stem    = ""



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
        self.setWindowTitle( f"M View  {__VERSION__}" )
        self.build_menu( )

        icon    = QtGui.QIcon( my_parameters.view_icon )
        self.setWindowIcon( icon )

        central_widget          = QWidget()
        self.setCentralWidget(central_widget)

        central_widget_layout   =  QVBoxLayout( central_widget )

        # --- out main layout
        layout          = QVBoxLayout(   )
        central_widget_layout.addLayout( layout )



        # ----   rows
        self.build_device_row( layout )
        #self.build_thing_row( layout )
        #self.build_action_row( layout )




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

        # # -----
        # widget                      =  QLineEdit(  )
        # self.microscope_widget      = widget
        # # keys                        = my_parameters.scope_dict.keys()
        # # #widget.currentIndexChanged.connect( self.microscope_widget_index_changed )
        # # #widget.clicked.connect( self.test2    )
        # # widget.addItems( keys )
        # row_layout.addWidget( widget, )

        # # ---- objective  self.scope_mag          = scope_mag
        # a_widget            = QLabel( "Objective:" )
        # row_layout.addWidget( a_widget )

        # a_widget                = QLineEdit( "objective" )
        # self.objective_widget   = a_widget
        # row_layout.addWidget( a_widget, ) # stretch = 2 )

        # # ---- objective  self.scope_mag          = scope_mag
        # a_widget            = QLabel( "Mode:not set" )
        # self.mode_widget        = a_widget
        # row_layout.addWidget( a_widget )

        # # a_widget                = QLineEdit( "what mode " )
        # # self.mode_widget        = a_widget
        # # row_layout.addWidget( a_widget, ) # stretch = 2 )

        # row_layout.addStretch( 1 )


        # a_widget            = QPushButton( "Write setup" )
        # a_widget.clicked.connect( self.write_setup_config )
        # row_layout.addWidget( a_widget )

    # -------------------------------------
    def build_device_row( self, layout ):
        """
        what it says -- pick a camera, pick a format, start, stop.  the combos
        are filled from the widget, see on_camera_list / on_format_list
        """
        row_layout          = QVBoxLayout(   )
        layout.addLayout( row_layout )


        widget            = QPushButton( "Load File..." )
        widget.clicked.connect( self.on_load_file )
        #self.load_reticle_widget = widget
        row_layout.addWidget( widget )



        # # ---- setup dict
        # a_widget            = QComboBox(   )
        # a_widget.setMinimumWidth( 220 )

        # values               = AppGlobal.parameters.setup_dict.keys()
        # a_widget.addItems( values )
        # #self.format_combo   = a_widget
        # device_layout.addWidget( a_widget )


        # ---- QLabel for jpg
        widget              = QLabel( "a_jpg" )
        self.jpg_widget     = widget
        widget.setMinimumSize( 500, 500 )     # width, height
        # widget.setMaximumSize(400, 300)
        row_layout.addWidget( widget )



        # ---- message area
        widget                  = gui_qt_ext.MessageArea()
        self.message_area       = widget
        #widget.clicked.connect( self.load    )
        row_layout.addWidget( widget, )





        #row_layout.addStretch( 1 )



    #----------------------------------------------------------------------
    def build_menu( self ):
        """
        what it says, read
        """
        # Create the menu bar
        menubar   = self.menuBar()
        #menu_bar.Append(menu_1, "tx_menu_1")
        # menu_bar.Append(menu_2, "tx_menu_2")

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

        if len( sys.argv ) == 0:
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

    #----------------------------------------------------------------------
    def menu_open_txt_file( self, event, file_name ):
        """
        use partial ??
        partial_function   = self.menu_open_txt_file
        partial_function   = value_from_hundreds = partial(         partial_function   = , units = 2, tens = 1 )
        partial_function = partial( self.menu_open_txt_file, file_name = "parameters.py" )
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
    def on_load_file( self, ):
        """
        what it says
        """
        my_parameters       = AppGlobal.parameters
        a_dir               = my_parameters.reticle_dir

        file_name, _        = QFileDialog.getOpenFileName( self, "Overlay image ( the top one )",
                                                           a_dir,
                                                           IMAGE_FILTER )

        if not file_name:
            return

        # self.last_dir       = os.path.dirname( file_name )

        # self.load_overlay( file_name )  #

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

        my_parameters   = AppGlobal.parameters
        output_dir      = my_parameters.output_dir

        fn_no_ext       = f"{output_dir}/{file_stem}"
            # all but ext

        return fn_no_ext

    # ---- get set enable !! could make widget names properties ?? ============================


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



    # ---- experiments -------------------------------------
    def test_something( self,  ):
        """


        """

        #self.get_setup_from_file( file_name)

# -------------------------------------
def main(): # do not remove
    app         = QApplication( sys.argv )
    window      = MainWindow()
    window.show()

    # QtPy handles the exec_() vs exec() difference automatically
    app.exec()

# for tests, move
if __name__ == '__main__':
    main()
# ---- eof
