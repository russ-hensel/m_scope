#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 18:22:46 2026

@author: russ
"""

# ---- tof

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main   # noqa  stops auto removal by pycln
# --------------------




# ---- imports

from   functools import partial
from   pathlib   import Path

from qtpy import QtGui


from qtpy.QtWidgets import ( QComboBox,
                             QDoubleSpinBox,
                             QFileDialog,
                             QLineEdit,
                             QWidget,
                             QApplication,
                             QHBoxLayout,
                             QDialog,
                             QTextEdit,
                             QVBoxLayout,
                             QTabWidget,
                             QGroupBox,
                             QRadioButton,
                             QLabel,
                             QPushButton,
                             QSlider,
                             QSpinBox,
                             QVBoxLayout,
                             )

from qtpy.QtCore import ( Qt, QTimer )
from qtpy.QtGui  import ( QPainter )

# ---- imports local

import  image_overlay_view
from    app_global import AppGlobal



# ---- constants
RESULT_CANCEL   = 0
RESULT_OK       = 1
RESULT_SKIP     = 2

# ----------------------------
class ConfigWriter( QDialog ):
    """
    write out te config
    """
    def __init__( self, parent, controller ):
        """
        the usual
        """
        #breakpoint()
        super().__init__( parent )

        self.controller = controller
        layout          = QVBoxLayout( self )
        self.build_gui( layout )
        self.setWindowTitle( "Create a Setup" )
        self.preview()

    # -----------------------
    def build_gui( self, parent_layout ):
        """
        """
        row_layout      = QHBoxLayout()
        parent_layout.addLayout( row_layout )

        widget                  = QLineEdit( "new setup name here " )
        self.seup_name_widget   = widget
        parent_layout.addWidget( widget )

        widget          = QPushButton( "Create" )
        #self.ok_button  = widget
        widget.setDefault( True )       # the return key presses this one
        widget.clicked.connect( self.preview )
        row_layout.addWidget( widget )

        widget          = QPushButton( "Ok" )
        #self.ok_button  = widget
        #widget.setDefault( True )       # the return key presses this one
        widget.clicked.connect( self.on_ok )
        row_layout.addWidget( widget )

        widget      = QPushButton( "Cancel" )
        widget.clicked.connect( self.on_cancel )
        row_layout.addWidget( widget )

        #widget         = QLabel( "proposed setup" )

        widget          =  QTextEdit()
        self.msg_widget = widget
        widget.setMinimumWidth(600)
        widget.setMinimumHeight(600)
        parent_layout.addWidget( widget )

    # -----------------------
    def on_ok( self ):
        """
        write out and return
        """
        print( "write it here" )

        self.finish( RESULT_OK )

    # -----------------------
    def on_skipxxx( self ):
        """
        close with the skip code, no validation
        """
        self.finish( RESULT_SKIP )

    # -----------------------
    def on_cancel( self ):
        """
        close with the cancel code,
        """
        self.finish( RESULT_CANCEL )

    # -----------------------
    def finish( self, result_code ):
        """
        remember the code and close, done() is what ends exec()
        """
        self.result_code    = result_code
        self.done( result_code )

    #------------------------------------
    def preview( self, ):
        """
        """
        a_string     = self.make_setup_str()
        text_edit    = self.msg_widget
        text_edit.clear()
        text_edit.append( a_string )

        text_edit.ensureCursorVisible()
        QApplication.clipboard().setText( text_edit.toPlainText() )


    #------------------------------------
    def make_setup_str( self, ):
        """
        """

        controller          = self.controller

        setup_id            = "get from user" # self.controller.setup_id_widget.currentText()
        setup_id            = self.seup_name_widget.text()

        scope_name          = self.controller.get_widget_mscope_name( )
        scope_mag           = self.controller.get_widget_objective_name()

        camera_name         = self.controller.get_widget_camera_name()

        # camera_name         = a_camera_cal_tab.camera_name_widget.text()

        camera_usb_name     = self.controller.get_widget_csensor_name()
        usb_format          = self.controller.get_widget_usb_format_name()
        scale               = controller.overlay_tab.scale_widget.value()
        reticle_fn          = self.controller.get_reticle()   # "tbd"   #a_overlay_tab.reticle_fn_widget.text()
        objective           = self.controller.get_widget_objective_name()
        #  scope_mag            = objective  # so not used

       # format_text         = a_camera_cal_tab.sensor_widget.currentText()

       # self.controller.camera_id_widget.setText( format_text )
        #camera_id_text      = a_camera_cal_tab.camera_id_widget.text()

        # msg     = f"{camera_id_text} --> {format_text}"
        # print( msg )

        msg        = f"""
        # ----  a_setup
        a_setup = ScopeSetup(
                               setup_id         = "{setup_id}",  # edit is safe

                               scope_name       = "{scope_name}", # edit is safe
                               scope_mag        = "{objective}",  # edit is safe
                               camera_name      = "{camera_name}", # edit is safe

                               camera_usb_name  = "{camera_usb_name}", # need exact match
                               usb_format       = "{usb_format}",      # need exact match
                               reticle_file     = "{reticle_fn}",      # critical for calibration
                               reticle_scale    =  {scale} )           # critical for calibration

        scope_setups.add_setup( a_setup )
        # setup end

                        """

        return msg

# ---- eof





