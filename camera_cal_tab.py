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
import logging




from qtpy.QtWidgets import ( QComboBox,
                             QWidget,
                             QFileDialog,
                             QFrame,
                             QHBoxLayout,
                             QLabel,
                             QPushButton,
                             QVBoxLayout,
                             )

from qtpy.QtCore import ( Qt )
from qtpy.QtGui  import ( QPixmap )


from    camera_capture_widget import CameraCaptureWidget
import  parameters
from    app_global import AppGlobal
# import  dict_list_model

# ---- constants


basedir         = os.path.dirname( os.path.abspath( __file__ ) )

DEFAULT_OUTPUT  = "./output"        # only if parameters is not up, see _start_save_dir
CAMERA_SUB_DIR  = "camera"
THUMB_WIDTH     = 160


#----------------------------
class CameraCalTab( QWidget ):
    def __init__( self, ):
        """
        the usual
        """
        super().__init__()
        layout    = QVBoxLayout( self )
        self.build_gui( layout )

    #----------------------------
    def build_gui( self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QHBoxLayout(   )
        main_layout.addLayout( layout )

        #self._build_device_row( layout )

        # ---- status line
        # ---- "Snap Photo"
        a_widget            = QPushButton( "Snap Cal. Photo" )
        a_widget.clicked.connect( self.on_snap_still )
        self.snap_button    = a_widget
        layout.addWidget( a_widget )

        a_widget            = QLabel( "no camera" )
        self.status_widget  = a_widget
        layout.addWidget( a_widget )

        #self._build_camera_buttons( layout )

        layout              = QHBoxLayout( )
        main_layout.addLayout( layout )

        a_widget            = QLabel( "Camera/Sensor" )
        layout.addWidget( a_widget )

        a_widget            = QComboBox(   )
        self.device_combo   = a_widget
        a_widget.setMinimumWidth( 240 )
        a_widget.currentIndexChanged.connect( self.on_device_combo_changed )
        layout.addWidget( a_widget )

        a_widget            = QLabel( "Format" )
        layout.addWidget( a_widget )

        a_widget            = QComboBox( )
        self.sensor_widget  = a_widget
        a_widget.setMinimumWidth( 220 )
        a_widget.currentIndexChanged.connect( self.on_sensor_widget_changed )
        layout.addWidget( a_widget )


        # ---- preview + last still, side by side
        view_layout         = QHBoxLayout(   )
        main_layout.addLayout( view_layout )

        # ---- Camera Capture
        # preview -- the combos and buttons that work it are built here and
        # drive it through its api, it answers through its signals
        a_widget            = CameraCaptureWidget(   )
        self.camera_widget  = a_widget
        a_widget.status_message_signal.connect( self.append_msg )
        a_widget.status_text_signal.connect( self.on_status_text )
        a_widget.image_saved_signal.connect( self.on_image_saved )
        a_widget.video_saved_signal.connect( self.on_video_saved )
        a_widget.still_image_signal.connect( self.on_still_image )
        a_widget.camera_list_signal.connect( self.on_camera_list )
        a_widget.format_list_signal.connect( self.on_format_list )
        a_widget.ready_for_capture_signal.connect( self.on_ready_for_capture )
        a_widget.recording_signal.connect( self.on_recording_changed )

        view_layout.addWidget( a_widget, 1 )

        self._build_thumb_column( view_layout )

        # ---- the widget emitted its first camera_list_signal in its own
        # __init__, before any of the connects above, so fill the combos once
        # by hand.  after this the signals keep them up to date
        self.on_camera_list( self.camera_widget.camera_descriptions(),
                             self.camera_widget.device_ix() )

        self.on_format_list( self.camera_widget.format_descriptions(),
                             self.camera_widget.format_ix() )

        self.on_ready_for_capture( self.camera_widget.is_ready_for_capture() )

        # ---- where the files go.  the ONE thing the widget does not decide,
        # because it is an application question, not a camera question
        dir_layout          = QHBoxLayout(   )
        layout.addLayout( dir_layout )

        self.save_dir_widget = None
        # a_widget            = QLabel( "Save to: ( not set yet )" )
        # self.save_dir_widget = a_widget
        # dir_layout.addWidget( a_widget )

        # a_widget            = QPushButton( "Change..." )
        # a_widget.clicked.connect( self.on_change_save_dir )
        # dir_layout.addWidget( a_widget )

        # a_widget            = QPushButton( "Default" )
        # a_widget.clicked.connect( self.on_default_save_dir )
        # dir_layout.addWidget( a_widget )

        dir_layout.addStretch( 1 )

    # ---- the camera controls, all of them this tab's ------------------------

    # -------------------------------------
    def _build_device_rowxxx( self, layout ):
        """
        what it says -- pick a camera, pick a format, start, stop.  the combos
        are filled from the widget, see on_camera_list / on_format_list
        """
        parameters          = AppGlobal.parameters
        controller          = AppGlobal.controller

        device_layout       = QHBoxLayout(   )
        layout.addLayout( device_layout )

        # # ---- setup dict
        # a_widget            = QComboBox(   )
        # a_widget.setMinimumWidth( 220 )

        # values               = AppGlobal.parameters.setup_dict.keys()
        # a_widget.addItems( values )
        # #self.format_combo   = a_widget
        # device_layout.addWidget( a_widget )

        # # ---- setup id
        # a_widget            = QLabel( "Setup IDxx" )
        # device_layout.addWidget( a_widget )

        # # a_widget                = QLineEdit( "Setup id" )
        # # self.setup_id_widget    = a_widget
        # # device_layout.addWidget( a_widget, stretch = 2 )

        # scope_dict              = parameters.scope_setups.get_setup_dict()
        # widget                  = cb_dict.CQComboBoxDict( scope_dict, display_keys = True )
        # self.setup_id_widget    = widget
        # widget.currentIndexChanged.connect( self.setup_id_widget_changed )
        # widget.set_current_key( list(scope_dict.keys())[ 0 ] )
        # device_layout.addWidget( widget, stretch = 2 )

        # # ---- camera name
        # a_widget                = QLabel( "Camera Name:" )
        # device_layout.addWidget( a_widget )

        # a_widget                = QLineEdit( "a_camera_name" )
        # self.camera_name_widget = a_widget
        # device_layout.addWidget( a_widget, )   #stretch = 2 )

        # a_widget            = QLabel( "Camera/Sensor" )
        # device_layout.addWidget( a_widget )

        # a_widget            = QComboBox(   )
        # a_widget.setMinimumWidth( 240 )
        # a_widget.currentIndexChanged.connect( self.on_device_combo_changed )
        # self.device_combo   = a_widget   # phase out
        # self.device_widget  = a_widget
        # device_layout.addWidget( a_widget )

        # a_widget            = QLabel( "USB Format" )
        # device_layout.addWidget( a_widget )

        # a_widget            = QComboBox(   )
        # a_widget.setMinimumWidth( 220 )
        # a_widget.currentIndexChanged.connect( self.on_sensor_widget_changed )
        # #self.format_combo   = a_widget
        # self.sensor_widget   = a_widget
        # device_layout.addWidget( a_widget )



        # a_widget            = QLabel( "Objective:" )
        # device_layout.addWidget( a_widget )

        # a_widget                = QLineEdit( "objective" )
        # self.objective_widget   = a_widget
        # device_layout.addWidget( a_widget, ) # stretch = 2 )



        # a_widget            = QPushButton( "Write setup" )
        # a_widget.clicked.connect( controller.write_setup_config )
        # device_layout.addWidget( a_widget )

        # a_widget            = QPushButton( "Stop" )
        # a_widget.clicked.connect( self.on_stop_camera )
        # device_layout.addWidget( a_widget )

        device_layout.addStretch( 1 )

    # -------------------------------------
    def _build_thumb_column( self, layout ):
        """
        what it says -- the last still, beside the preview.  the widget hands
        over a QImage and this decides how big to show it, see on_still_image
        """
        thumb_layout        = QVBoxLayout(   )
        layout.addLayout( thumb_layout )

        a_widget            = QLabel( "last still" )
        thumb_layout.addWidget( a_widget )

        a_widget            = QLabel( "( none yet )" )
        a_widget.setFrameShape( QFrame.Shape.Box )
        a_widget.setAlignment( Qt.AlignmentFlag.AlignCenter )
        a_widget.setMinimumWidth( THUMB_WIDTH )
        self.thumb_widget   = a_widget
        thumb_layout.addWidget( a_widget )

        thumb_layout.addStretch( 1 )

    # -------------------------------------
    def _build_camera_buttonsxxx( self, layout ):
        """
        what it says -- snap and record.  the enabled state is not this tab's
        guess, it follows ready_for_capture_signal and recording_signal
        """
        button_layout       = QHBoxLayout(   )
        layout.addLayout( button_layout )

        # ---- "Snap Photo"
        a_widget            = QPushButton( "Snap Photo" )
        a_widget.clicked.connect( self.on_snap_still )
        self.snap_button    = a_widget
        button_layout.addWidget( a_widget )

        # a_widget            = QPushButton( "Record Video" )
        # a_widget.clicked.connect( self.on_record_video )
        # self.record_button  = a_widget
        # button_layout.addWidget( a_widget )

        # a_widget            = QPushButton( "Stop Record" )
        # a_widget.clicked.connect( self.on_stop_record )
        # a_widget.setEnabled( False )
        # self.stop_record_button = a_widget
        # button_layout.addWidget( a_widget )

        button_layout.addStretch( 1 )

    # -------------------------------------
    def setup_id_widget_changed( self,   ):
        """
        setup has changed so apply it
        """
        a_setup     = self.setup_id_widget.current_value()
        print( a_setup )

        AppGlobal.controller.setup( a_setup )

    # ---- controls -> widget ------------------------------------------------

    # -------------------------------------
    def on_device_combo_changed( self, ix ):
        """
        what it says -- the widget ignores an index it is already on, so a
        combo re-fill does not restart the camera
        """
        self.camera_widget.set_device_ix( ix )

    # -------------------------------------
    def on_sensor_widget_changed( self, ix ):
        """ what it says """
        self.camera_widget.set_format_ix( ix )
        self.update_camera_id()

    # -------------------------------------
    def on_start_camera( self, ):
        """ what it says """
        self.camera_widget.start_camera()

    # -------------------------------------
    def on_stop_camera( self, ):
        """
        what it says
        """
        self.camera_widget.stop_camera()

    # -------------------------------------
    def update_camera_id( self, ):
        """
        what it says
            does not make sense to me
            name is odd
            should we find then use index
        """
        format_text    = self.sensor_widget.currentText()
        #self.camera_id_widget.setText( format_text )
        #self.device_combo.setText( format_text )

    # -------------------------------------
    def on_snap_still( self, ):
        """
        what it says
            call to do the snap
        """
        controller    = AppGlobal.controller
        controller.on_snap_still_cal( )


    # -------------------------------------
    def save_snap( self, fn_no_ext ):
        """
        what it says
            from controller
            a lot like on_snap_still_old

        """
        camera_widget  = self.camera_widget

        if camera_widget.camera is None:
            self._say( "no camera running -- click Start" )
            1/0
            return

        if not camera_widget.image_capture.isReadyForCapture():
            msg     = ( "camera not ready for capture yet -- try again in a moment" )
            print( msg )
            return

        parameters   = AppGlobal.parameters
        output_dir   = parameters.output_dir

        controller   = AppGlobal.controller

        file_name    = controller.get_file_name( fn_no_ext, ".jpg" )

        # self._say( f"capture {capture_id} asked for: {file_name}" )  zz
        camera_widget.snap_still( file_name )

        # may continue in self.on_image_saved ??

    # -------------------------------------
    def on_snap_still_old( self, ):
        """
        what it says
            call to do the snap
        """
        camera_widget  = self.camera_widget

        if camera_widget.camera is None:
            self._say( "no camera running -- click Start" )
            1/0
            return

        if not camera_widget.image_capture.isReadyForCapture():
            msg     = ( "camera not ready for capture yet -- try again in a moment" )
            print( msg )
            return

        parameters   = AppGlobal.parameters
        output_dir   = parameters.output_dir

        controller   = AppGlobal.controller

        try:
            fn_no_ext         = controller.get_fn_no_ext()
        except ValueError:
            return

        file_name    = controller.get_file_name( fn_no_ext, "_p.jpg" )


        # self._say( f"capture {capture_id} asked for: {file_name}" )  zz
        camera_widget.snap_still( file_name )

        # may continue in self.on_image_saved

    # -------------------------------------
    def on_record_video( self, ):
        """ what it says """
        self.camera_widget.record_video()

    # -------------------------------------
    def on_stop_record( self, ):
        """ what it says """
        self.camera_widget.stop_record()

    # ---- widget -> controls ------------------------------------------------

    # -------------------------------------
    def on_camera_list( self, a_list, ix ):
        """
        read it -- the cameras changed, or this is the first fill.  signals are
        blocked while the combo is loaded or setCurrentIndex would run back
        into the widget and restart a camera that is already right
            build device_combo list
        """
        self.device_combo.blockSignals( True )
        self.device_combo.clear()
        self.device_combo.addItems( a_list )
        self.device_combo.setCurrentIndex( ix )
        self.device_combo.blockSignals( False )

    # -------------------------------------
    def on_format_list( self, a_list, ix ):
        """
        what it says -- as on_camera_list, for the format combo
        """
        msg      = ( f"on_format_list() {a_list}" )
        logging.debug( msg )

        self.sensor_widget.blockSignals( True )
        self.sensor_widget.clear()
        self.sensor_widget.addItems( a_list )
        self.sensor_widget.setCurrentIndex( ix )
        self.sensor_widget.blockSignals( False )

    # -------------------------------------
    def on_status_text( self, msg ):
        """
        what it says -- one line of current state
        """
        self.status_widget.setText( msg )

    # -------------------------------------
    def on_still_image( self, a_image ):
        """
        what it says -- a QImage, in hand before the file is written, so the
        thumbnail can go up right away
        """
        a_pixmap            = QPixmap.fromImage( a_image )
        a_pixmap            = a_pixmap.scaledToWidth( THUMB_WIDTH,
                                                      Qt.TransformationMode.SmoothTransformation )
        self.thumb_widget.setPixmap( a_pixmap )

    # -------------------------------------
    def on_ready_for_capture( self, is_ready ):
        """ what it says -- no point offering a snap the backend would drop """
        self.snap_button.setEnabled( is_ready )

    # -------------------------------------
    def on_recording_changed( self, is_recording ):
        """ what it says """
        self.record_button.setEnabled( not is_recording )
        self.stop_record_button.setEnabled( is_recording )

    # -------------------------------------
    def append_msg( self, msg ):
        """
        what it says -- this tab has no msg box of its own, so the widget's
        chatter goes to the console.  the status LINE is not written here, it
        belongs to on_status_text, or the two would fight over it

        !! _apply_save_dir has always called this and it did not exist, so
        "Change..." and "Default" died with an AttributeError.  now they work
        """
        print( msg )

    # ---- where files go ----------------------------------------------------

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
    def get_last_snap_fn( self, ):
        """
        what it says
        """
        fn   = self.camera_widget.last_file
        return fn

    # -------------------------------------
    def on_change_save_dir( self, ):
        """
        what it says
        """
        a_dir               = QFileDialog.getExistingDirectory( self, "Save captures to",
                                                                self.camera_widget.save_dir() )
        if not a_dir:
            return

        self._apply_save_dir( a_dir )

    # -------------------------------------
    def on_default_save_dir( self, ):
        """
        what it says -- back to the one from parameters
        """
        self._apply_save_dir( self._start_save_dir() )

    # ---- perhaps signals from the widget  ------------------------------------------

    # -------------------------------------
    def on_image_saved( self, file_name ):
        """
        what it says -- the widget already said "saved: ..." through
        status_message_signal, this is the hook for anything the APPLICATION
        wants to do with a new still.  nothing yet

        ?? add it to a gallery, or to the project's db, or show it in the
           image overlay tab as a base image ?
        """
        print( "on_image_saved" )
        if AppGlobal.parameters.auto_load_snap:
            AppGlobal.controller.overlay_tab.load_base_from_last_snap(   )

        controller      = AppGlobal.controller
        tab_widget      = controller.tab_widget
        widget          = controller.overlay_tab

        tab_widget.setCurrentWidget( widget )

    # -------------------------------------
    def on_video_saved( self, file_name ):
        """
        what it says -- as on_image_saved, for recordings

        ?? hand it to tab_vlc_qt_widget to play back ?
        """
        pass

    # -------------------------------------
    def set_widget_usb_format_name( self, name ):
        """
        return
                throw except if fails

        self.sensor_widget  = a_widget
        a_widget.currentIndexChanged.connect( self.on_sensor_widget_changed )
                zz

        """
        widget      = self.sensor_widget
        ix          =  widget.findText( name )
        if ix >= 0:
            widget.setCurrentIndex( ix )
        else:
            raise Exception( "set_widget_usb_format_name failed" )

    # -------------------------------------
    def set_widget_device_combo_name( self, name ):
        """
        return
                throw except if fails

        self.sensor_widget  = a_widget

                zz
        """
        widget      = self.device_combo
        ix          =  widget.findText( name )
        if ix >= 0:
            widget.setCurrentIndex( ix )
        else:
            raise Exception( "set_widget_device_combo_name failed" )





# ---- eof ---------------------------


