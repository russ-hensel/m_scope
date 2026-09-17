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
import os


from qtpy.QtWidgets import QVBoxLayout, QWidget

from qtpy.QtWidgets import ( QFileDialog,
                             QVBoxLayout,
                             )


import  gui_qt_ext
#import  custom_widgets as cw

from    app_global import AppGlobal
# ---- constants

basedir         = os.path.dirname( os.path.abspath( __file__ ) )

DEFAULT_OUTPUT  = "./output"        # only if parameters is not up, see _start_save_dir
CAMERA_SUB_DIR  = "camera"

# ---------------------------------------
class NoteTab( QWidget ):
    def __init__( self, ):
        """
        the usual
        """
        super().__init__()
        layout    = QVBoxLayout( self )

        self.gui( layout )

    # -------------------------------
    def gui( self, layout ):
        """
        what it says -- build the gui
        """
        controller      = AppGlobal.controller
        parameters      = AppGlobal.parameters
        my_layout       = layout

        # ---- message area
        widget                  = gui_qt_ext.MessageArea()
        self.message_area       = widget
        widget.setMinimumHeight( 100 )
        #widget.clicked.connect( self.load    )
        my_layout.addWidget( widget, )

    # -------------------------------
    def microscope_widget_index_changed( self, microscope_widget_index_changed, ):
        """
        setup for a change in microscope, change reticle s
            use a combo that  uses a dict, is it one of the models
        """
        parameters      = AppGlobal.parameters
        widget          = self.microscope_widget
        ix              = widget.currentIndex()
        keys            = list( parameters.scope_dict.keys() )
        key             = keys[ix]  # same as current test
        value           = parameters.scope_dict[ key ]
        msg             = f"{key = } {value = }"
        print( msg )

    # -------------------------------
    def display_string( self, text ):
        """
        display_string
        """
        self.message_area.display_string( text )

    # # -------------------------------------
    # def save_text_file( self, file_stem ):
    #     """
    #     this will apply .txt and save
    #         !! use pathlib
    #     """
    #     parameters  = AppGlobal.parameters

    #     file_name   = f"{parameters.output_dir}{file_stem}.txt"
        the_text    = self.message_area.get_plain_text()

        with open(  file_name, 'w' ) as a_file:

            # for i_line in a_list:
            #     a_file.write( f"{i_line}\n" )  # note addition of \n
            a_file.write( the_text )


    # -------------------------------------
    def save_file( self, file_name ):
        """
        overwrite
        """
        the_text    = self.message_area.get_plain_text()

        with open(  file_name, 'w' ) as a_file:
            a_file.write( the_text )


    # -------------------------------------
    def use_camera( self,   ):
        """

        """
        controller      = AppGlobal.controller
        tab_widget      = controller.tab_widget
        widget          = controller.camera_tab

        try:
            index           = tab_widget.indexOf( widget )

        except:
            return

        tab_widget.removeTab( index )
        widget.deleteLater()

    # -------------------------------------
    def explore_camera( self,   ):
        """

        """
        controller      = AppGlobal.controller
        tab_widget      = controller.tab_widget
        widget          = controller.camera_tab

        try:
            index           = tab_widget.indexOf( widget )

        except:
            return

        tab_widget.removeTab( index )
        widget.deleteLater()


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
