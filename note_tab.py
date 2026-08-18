#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 20:15:48 2026

@author: russ
"""

# ---- tof

# --------------------
if __name__ == "__main__":
    import main   # noqa  stops auto removal by pycln
# --------------------


# ---- imports
import sys
import os



from qtpy import QtGui

from qtpy.QtCore import ( QDate,
                          QDateTime,
                          Qt,
                          QTime)



from qtpy.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget

from qtpy.QtWidgets import ( QComboBox,
                             QDoubleSpinBox,
                             QFileDialog,
                             QHBoxLayout,
                             QTabWidget,
                             QTextEdit,
                             QDateEdit,
                             QLabel,
                             QPushButton,
                             QSlider,
                             QSpinBox,
                             QVBoxLayout,
                             )

from qtpy.QtCore import ( Qt, QTimer )

from qtpy.QtGui  import ( QPainter )


from    camera_capture_widget import CameraCaptureWidget
#import  parameters
#import  image_overlay_view
import  gui_qt_ext
#import  custom_widgets as cw

from    app_global import AppGlobal
# ---- constants


basedir         = os.path.dirname( os.path.abspath( __file__ ) )

DEFAULT_OUTPUT  = "./output"        # only if parameters is not up, see _start_save_dir
CAMERA_SUB_DIR  = "camera"



class NoteTab( QWidget ):
    def __init__( self, ):
        """
        the usual
        """
        super().__init__()
        layout    = QVBoxLayout( self )

        #self.build_gui_widgets( layout )

        # ---- try both
        #self.build_gui_bot( layout )
        self.build_message_area( layout )

    #----------------------------
    def build_gui_widgetsxxx( self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )
        main_layout.addLayout( layout )

        # ---- the widget of interest.  it brings its own device and format
        # combos, its own start/stop, preview, thumbnail, snap and record --
        # everything about cameras.  this tab adds none of that
        a_widget            = CameraCaptureWidget(   )

        a_widget.image_saved_signal.connect( self.on_image_saved )
        a_widget.video_saved_signal.connect( self.on_video_saved )
        self.camera_widget  = a_widget
        layout.addWidget( a_widget, 1 )

        # ---- where the files go.  the ONE thing the widget does not decide,
        # because it is an application question, not a camera question
        dir_layout          = QHBoxLayout(   )
        layout.addLayout( dir_layout )

        a_widget            = QLabel( "Save to: ( not set yet )" )
        self.save_dir_widget = a_widget
        dir_layout.addWidget( a_widget )

        a_widget            = QPushButton( "Change..." )
        a_widget.clicked.connect( self.on_change_save_dir )
        dir_layout.addWidget( a_widget )

        a_widget            = QPushButton( "Default" )
        a_widget.clicked.connect( self.on_default_save_dir )
        dir_layout.addWidget( a_widget )

        dir_layout.addStretch( 1 )

        # # ---- buttons
        # button_layout       = QHBoxLayout(   )
        # layout.addLayout( button_layout )


    # -------------------------------
    def build_message_area( self, layout  ):
        """

        """

        # ---- new layout -- is it even needed
        my_layout       = QVBoxLayout(   )
        layout.addLayout( my_layout, )

        row_layout      = QHBoxLayout(   )
        my_layout.addLayout( row_layout, )

        # ----
        widget          =  QPushButton( "test1" )
        #self.output_edit    = widget
        widget.clicked.connect( self.test1    )
        row_layout.addWidget( widget, )

        # ---- date
        widget                  =  QDateEdit(  )
        self.date_code_widget   = widget
        widget.setCalendarPopup( True )
        today                   = QDate.currentDate()
        widget.setDate( today )
        # widget.setMinimumDate(QDate(1900, 1, 1))
        # widget.setMaximumDate(QDate(2100, 12, 31))
        widget.setDisplayFormat( "yyyy_MM_dd" )
        row_layout.addWidget( widget, )

        # ---- item code
        widget          =  QLabel( "item code ->"  )
        row_layout.addWidget( widget, )

        # ---- item code widget
        widget                   =  QLineEdit(  )
        self.item_code_widget    = widget
        row_layout.addWidget( widget, )

        # ---- current file stem
        # update on read or snap -- does snap save to a file
        widget                   =  QLabel( "file_stem" )
        self.file_stem_widget    = widget
        row_layout.addWidget( widget, )

        # ----
        widget                  =  gui_qt_ext.MessageArea()
        self.message_area       = widget
        #widget.clicked.connect( self.load    )
        my_layout.addWidget( widget, )

    # -------------------------------
    def test1( self, ):
        """
        """
        controller   = AppGlobal.controller
        print( controller.get_fn_stem() )

    # -------------------------------
    def build_gui_bot( self, layout ):
        """
        from other code --- but not my message widget wht
            make the bottom of the gui, mostly the large
            message widget
            layouts
                a vbox for main layout
        """
        # ---- new row
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout, )

        # widget          = QPushButton( "Top" )
        # widget.clicked.connect( self.top )
        # row_layout.addWidget( widget )

        # widget          = QPushButton( "Bottom" )
        # widget.clicked.connect( self.bot )
        # row_layout.addWidget( widget )

        # ---- new row
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout, )

        # ----
        widget          = QTextEdit( "load\nthis should be new row " )
        self.msg_widget = widget
        #widget.clicked.connect( self.load    )
        row_layout.addWidget( widget, )
        self.output_edit    = widget

    # -------------------------------------
    def save_result_file( self, file_stem ):
        """
        this will apply .txt and save
        """

    # -------------------------------------
    def save_image_file( self, file_stem ):
        """
        this will apply .txt and save
        """


    # -------------------------------------
    def save_text_file( self, file_stem ):
        """
        this will apply .txt and save
            !! use pathlib
        """
        parameters  = AppGlobal.parameters

        file_name   = f"{parameters.output_dir}{file_stem}.txt"
        the_text    = self.message_area.get_plain_text()

        with open(  file_name, 'w' ) as a_file:

            # for i_line in a_list:
            #     a_file.write( f"{i_line}\n" )  # note addition of \n
            a_file.write( the_text )



    # -------------------------------------
    def construct_file_name( self,   ):
        """
        get date and item code
        """

    # ---- next probably old junk  ----------------------------------------------------

    # -------------------------------------
    def _start_save_dir( self, ):
        """
        read it -- the app's own output directory, parameters.PARAMETERS.output_dir
        ( "./output" as it stands ), with a camera sub directory under it.

        imported and read lazily rather than at module import time: PARAMETERS
        is built while the app starts, and this module gets imported by the tab
        machinery, so reading it at import time is asking for a None.  the
        fallback keeps the tab usable outside the app, eg in a test harness
        """
        output_dir          = DEFAULT_OUTPUT

        try:
            import parameters
            if parameters.PARAMETERS is not None:
                output_dir          = parameters.PARAMETERS.output_dir
        except Exception:
            pass            # no app around, the default will do

        return os.path.join( output_dir, CAMERA_SUB_DIR )

    # -------------------------------------
    def _apply_save_dir( self, a_dir ):
        """
        what it says -- tell the widget, then say so.  the widget makes the
        directory if it is missing and hands back what it used
        """
        a_dir               = self.camera_widget.set_save_dir( a_dir )

        self.save_dir_widget.setText( f"Save to: {a_dir}" )
        self.append_msg( f"captures will be saved to {os.path.abspath( a_dir )}" )

    # -------------------------------------
    def on_change_save_dir( self, ):
        """ what it says """
        a_dir               = QFileDialog.getExistingDirectory( self, "Save captures to",
                                                                self.camera_widget.save_dir() )
        if not a_dir:
            return

        self._apply_save_dir( a_dir )

    # -------------------------------------
    def on_default_save_dir( self, ):
        """ what it says -- back to the one from parameters """
        self._apply_save_dir( self._start_save_dir() )

    # ---- what the widget tells us ------------------------------------------

    # -------------------------------------
    def on_image_saved( self, file_name ):
        """
        what it says -- the widget already said "saved: ..." through
        status_message_signal, this is the hook for anything the APPLICATION
        wants to do with a new still.  nothing yet

        ?? add it to a gallery, or to the project's db, or show it in the
           image overlay tab as a base image ?
        """
        pass

    # -------------------------------------
    def on_video_saved( self, file_name ):
        """
        what it says -- as on_image_saved, for recordings

        ?? hand it to tab_vlc_qt_widget to play back ?
        """
        pass


# ---- eof ---------------------------


