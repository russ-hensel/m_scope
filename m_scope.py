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


# ---- imports
import sys
import os
from   pathlib import Path
from   functools import partial

from qtpy import QtGui


from qtpy.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget

from qtpy.QtWidgets import ( QComboBox,
                             QDoubleSpinBox,
                             QFileDialog,
                             QHBoxLayout,
                             QMessageBox,
                             QTabWidget,
                             QLabel,
                             QPushButton,
                             QSlider,
                             QSpinBox,
                             QVBoxLayout,
                             )

from qtpy.QtCore import ( Qt, QTimer )
from qtpy.QtGui  import ( QPainter )


from datetime import datetime

import  parameters
#import  image_overlay_view

import  overlay_tab
import  camera_tab
import  note_tab
from    app_global import AppGlobal
import  utils

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


__VERSION__     = "ver_03 - 2026 08 27.01"


# -------------------------------
class MainWindow( QMainWindow ):
    def __init__(self):
        """Build the main window """
        super().__init__()

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

        self.last_dir           = basedir
        self.current_fn_stem    = ""

        # ---- build_gui
        self.setWindowTitle( f"M Scope  {__VERSION__}" )
        self.build_menu( )

        icon    = QtGui.QIcon(  "./misc/broom_edit_2.png" )
        icon    = QtGui.QIcon(  "./misc/magnifier.png" )
        #/  !! move to parameters
        self.setWindowIcon(icon)

        central_widget          = QWidget()
        self.setCentralWidget(central_widget)

        central_widget_layout   =  QVBoxLayout( central_widget )

        # --- out main layout
        layout          = QVBoxLayout(   )
        central_widget_layout.addLayout( layout )

        # ---- Create tabs
        self.tab_widget = QTabWidget()   # really the folder for the tabs
                                         # tabs themselves are just Widgets
        # there is another approach using a style sheet acording to chat
        self.tab_widget.setTabsClosable( False )
        #self.tab_widget.tabCloseRequested.connect( self.close_tab )
        # Set custom height for the tabs
        self.tab_widget.setStyleSheet( "QTabBar::tab { height: 60px; }" )

        self.tab_widget.currentChanged.connect( self.on_tab_changed )
        self.tab_widget.tabBarClicked.connect(  self.on_tab_clicked )

        # self.tab_widget.tabCloseRequested.connect( self.on_tab_close_requested )
        # self.tab_widget.setTabsClosable( False )
            # Allows you to enable or disable the close button on tabs.
        self.tab_widget.setMovable( True )

        layout.addWidget( self.tab_widget   )

        # ---- notes
        tab                     = note_tab.NoteTab()
        self.note_tab           = tab
        title                   = "Control\n and Notes"
        self.tab_widget.addTab( tab, title  )

        tab                     = camera_tab.CameraTab()
        self.camera_tab         = tab
        title                   = "Photo\nSnap"
        self.tab_widget.addTab( tab, title  )

        # ---- tab overlay
        tab                     = overlay_tab.OverlayTab()
        self.tab_overlay        = tab
        title                   = "Overlay\nMeasure"
        self.tab_widget.addTab( tab, title  )

        for key, value in my_parameters.reticle_dict.items():
            file_name           = ( my_parameters.reticle_dir + "/" + value ).replace( "//", "/" )
            foo                 = partial( tab.load_overlay, file_name )
            foo()
            break

        my_parameters.test_init_2()

    # -------------------------------------
    def get_fn_no_ext( self, ):
        """
        what it says
            fn_no_ext = controller.get_fn_no_ext()
        """
        note_tab        = self.note_tab
        item_code       = self.note_tab.item_code_widget.text()
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

        date_code       = self.note_tab.date_code_widget.date().toString(  'yyyy_MM_dd' )
        prefix          = f"{date_code}_{item_code}"

        file_stem       = utils.gen_fn_stem( prefix )  # import utils
            # no path to, no ext
        note_tab.file_stem_widget.setText( file_stem )

        parameters   = AppGlobal.parameters
        output_dir   = parameters.output_dir

        fn_no_ext    = f"{output_dir}/{file_stem}"
            # all but ext

        return fn_no_ext

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


    # #----------------------------
    # def on_button_click(self):
    #     print("Button Clicked!")
    #     self.line_edit.setText("Working on " + QApplication.instance().arguments()[0])


    # -------------------------------------
    def build_menu( self, ):
        """
        what it says
        """
        return

    # -------------------------------------
    def on_tab_changed( self, ):
        """ """
    # -------------------------------------
    def on_tab_clicked( self, ):
        """ """

# -------------------------------------
def main():
    app         = QApplication( sys.argv )
    window      = MainWindow()
    window.show()

    # QtPy handles the exec_() vs exec() difference automatically
    app.exec()

# for tests, move
#if __name__ == '__main__':


# ---- eof



