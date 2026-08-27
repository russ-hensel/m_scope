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
from   functools import partial

from qtpy import QtGui


from qtpy.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget

from qtpy.QtWidgets import ( QComboBox,
                             QDoubleSpinBox,
                             QFileDialog,
                             QHBoxLayout,
                             QTabWidget,
                             QLabel,
                             QPushButton,
                             QSlider,
                             QSpinBox,
                             QVBoxLayout,
                             )

from qtpy.QtCore import ( Qt, QTimer )
from qtpy.QtGui  import ( QPainter )

# ---- imports local
import  parameters
import  image_overlay_view
from    app_global import AppGlobal



# ---- constants

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




# ----------------------------
class OverlayTab( QWidget  ):
    def __init__( self,  ):
        """
        the usual
        """
        #breakpoint()
        super().__init__()
        layout          = QVBoxLayout( self )
        self.build_gui_widgets( layout )

        self.last_dir   = "./misc"   # ! from parameters
        #self.last_dir       = os.path.dirname( file_name )

        parameters      = AppGlobal.parameters
        self.overlay_view.set_overlay_image( parameters.default_ovelay )

        self.on_opacity_changed( AppGlobal.parameters.overlay_opacity )

    #----------------------------
    def build_gui_widgets( self, main_layout ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        parameters          = AppGlobal.parameters

        layout              = QVBoxLayout(   )
        main_layout.addLayout( layout )

        # ---- load layout
        load_layout         = QHBoxLayout(   )
        layout.addLayout( load_layout )


        # ---- load photo
        a_widget            = QPushButton( "Load Photo..." )
        a_widget.clicked.connect( self.on_load_base )
        load_layout.addWidget( a_widget )

        # ---- "Load last snap..."
        a_widget            = QPushButton( "Load last Photo" )
        a_widget.clicked.connect( self.load_base_from_last_snap )
        load_layout.addWidget( a_widget )


        #self.reticle_disptach = {}
        for key, value in parameters.reticle_dict.items():
            a_widget            = QPushButton( key )
            file_name           = (parameters.reticle_dir + "/" + value ).replace( "//", "/" )
            foo                 = partial( self.load_overlay, file_name )
            a_widget.clicked.connect( foo )
            load_layout.addWidget( a_widget )


        a_widget            = QPushButton( "Load Reticle..." )
        a_widget.clicked.connect( self.on_load_overlay )
        load_layout.addWidget( a_widget )

        a_widget            = QPushButton( "Load Test Images" )
        a_widget.clicked.connect( self._load_demo_images )
        load_layout.addWidget( a_widget )

        load_layout.addStretch( 1 )

        a_widget            = QPushButton( "Save..." )
        a_widget.clicked.connect( self.on_save_result )
        load_layout.addWidget( a_widget )

        # ----  ImageOverlayView
        a_widget            = image_overlay_view.ImageOverlayView(   )
        a_widget.setMinimumHeight( 320 )
        a_widget.overlay_changed.connect( self.on_overlay_changed )
        self.overlay_view   = a_widget
        layout.addWidget( a_widget, 1 )

        # ---- position / rotation / scale row.  these show what the mouse is
        # doing and can also drive it, which is the only way to get an exact
        # offset back after finding it once
        pos_layout          = QHBoxLayout(   )
        layout.addLayout( pos_layout )

        a_widget            = QLabel( "X" )
        pos_layout.addWidget( a_widget )

        a_widget            = QSpinBox(   )
        a_widget.setRange( -10000, 10000 )
        a_widget.valueChanged.connect( self.on_offset_spin_changed )
        self.x_spin         = a_widget
        pos_layout.addWidget( a_widget )

        a_widget            = QLabel( "Y" )
        pos_layout.addWidget( a_widget )

        a_widget            = QSpinBox(   )
        a_widget.setRange( -10000, 10000 )
        a_widget.valueChanged.connect( self.on_offset_spin_changed )
        self.y_spin         = a_widget
        pos_layout.addWidget( a_widget )

        a_widget            = QLabel( "Rotation" )
        pos_layout.addWidget( a_widget )

        a_widget            = QDoubleSpinBox(   )
        a_widget.setRange( -360.0, 360.0 )
        a_widget.setSingleStep( 0.5 )
        a_widget.setDecimals( 2 )
        a_widget.setSuffix( " deg" )
        a_widget.valueChanged.connect( self.on_rotation_spin_changed )
        self.rotation_spin  = a_widget
        pos_layout.addWidget( a_widget )

        # ---- Scale
        a_widget            = QLabel( "Scale" )
        pos_layout.addWidget( a_widget )

        a_widget            = QDoubleSpinBox(   )
        a_widget.setRange( 0.05, 20.0 )
        a_widget.setSingleStep( 0.05 )
        a_widget.setDecimals( 3 )
        a_widget.setValue( 1.0 )
        a_widget.valueChanged.connect( self.on_scale_spin_changed )
        self.scale_spin     = a_widget
        pos_layout.addWidget( a_widget )

        # ---- reset
        a_widget            = QPushButton( "Reset" )
        a_widget.clicked.connect( self.on_reset_overlay )
        pos_layout.addWidget( a_widget )

        pos_layout.addStretch( 1 )

        # ---- look row: opacity, blend mode, blink, and the view's own zoom
        look_layout         = QHBoxLayout(   )
        layout.addLayout( look_layout )

        # ---- Opacity
        a_widget            = QLabel( "Opacity" )
        look_layout.addWidget( a_widget )

        a_widget            = QSlider( Qt.Orientation.Horizontal )
        a_widget.setRange( 0, 100 )
        #a_widget.setValue( 100 )
        a_widget.setValue( AppGlobal.parameters.overlay_opacity )  # may be too late or early
        a_widget.setMaximumWidth( 160 )
        a_widget.valueChanged.connect( self.on_opacity_changed )
        self.opacity_slider = a_widget
        look_layout.addWidget( a_widget )

        a_widget            = QLabel( "Blend" )
        look_layout.addWidget( a_widget )

        a_widget            = QComboBox(   )
        for i_name, i_mode in COMPOSITION_MODES:
            a_widget.addItem( i_name )
        a_widget.currentIndexChanged.connect( self.on_blend_changed )
        self.blend_combo    = a_widget
        look_layout.addWidget( a_widget )

        # ---- blink: the eye catches a shift far better than it judges a
        # steady overlay, so flick the top image on and off
        a_widget            = QPushButton( "Blink" )
        a_widget.setCheckable( True )
        a_widget.toggled.connect( self.on_blink_toggled )
        self.blink_button   = a_widget
        look_layout.addWidget( a_widget )

        blink_timer         = QTimer( self )
        blink_timer.setInterval( BLINK_MS )
        blink_timer.timeout.connect( self._blink_tick )
        self.blink_timer    = blink_timer

        look_layout.addStretch( 1 )

        # ---- view zoom.  NOT the overlay scale above -- this one only
        # changes how big it looks, it is never part of what gets saved
        a_widget            = QLabel( "View" )
        look_layout.addWidget( a_widget )

        a_widget            = QPushButton( "Fit" )
        a_widget.clicked.connect( self.on_fit )
        look_layout.addWidget( a_widget )

        a_widget            = QPushButton( "1:1" )
        a_widget.clicked.connect( self.overlay_view.zoom_reset )
        look_layout.addWidget( a_widget )

        a_widget            = QPushButton( "-" )
        a_widget.setMaximumWidth( 32 )
        a_widget.clicked.connect( self.overlay_view.zoom_out )
        look_layout.addWidget( a_widget )

        a_widget            = QPushButton( "+" )
        a_widget.setMaximumWidth( 32 )
        a_widget.clicked.connect( self.overlay_view.zoom_in )
        look_layout.addWidget( a_widget )

        # ---- buttons
        button_layout       = QHBoxLayout(   )
        layout.addLayout( button_layout )

    # ---- loading -----------------------------------------------------------

    # -------------------------------------
    def _load_demo_images( self, ):
        """
        read it -- images made in code, so the tab shows something the moment
        it opens with no files to hunt for.  the overlay has a hole punched in
        it, which is what you look through
        """
        base, overlay       = image_overlay_view.make_demo_pixmaps()

        self.overlay_view.set_base_image( base )
        self.overlay_view.set_overlay_image( overlay )
        self.overlay_view.fit_to_view()

        msg                 = ( "demo images loaded -- drag the red ring about, "
                                "arrow keys nudge it a pixel ( shift for ten ), "
                                "the wheel zooms the view" )
        print( msg )

    # -------------------------------------
    def on_load_base( self, ):
        """ what it says """
        file_name, _        = QFileDialog.getOpenFileName( self, "Base image ( the bottom one )",
                                                           self.last_dir, IMAGE_FILTER )
        if not file_name:
            return

        self.last_dir       = os.path.dirname( file_name )

        if self.overlay_view.set_base_image( file_name ):
            self.overlay_view.fit_to_view()
            print( f"base image: {file_name}" )
        else:
            print( f"could not load {file_name}" )

    # -------------------------------------
    def load_base_from_last_snap( self, file_name = None ):
        """ what it says

        file_name sometims late to camera tab, pass it but pass with care
        """
        if not file_name:
            camera_tab      = AppGlobal.controller.camera_tab
            file_name       = camera_tab.get_last_snap_fn()

        if not file_name:  # sort of left over should not happen
            return

        if self.overlay_view.set_base_image( file_name ):
            self.overlay_view.fit_to_view()
            print( f"base image: {file_name}" )

        else:
            print( f"could not load {file_name}" )

    # -------------------------------------
    def on_load_overlay( self, ):
        """
        what it says -- and a word in the msg box if the image has no alpha,
        since "nothing shows through" is otherwise a puzzling result
        """
        file_name, _        = QFileDialog.getOpenFileName( self, "Overlay image ( the top one )",
                                                           self.last_dir, IMAGE_FILTER )
        if not file_name:
            return

        self.load_overlay( file_name )

        self.last_dir       = os.path.dirname( file_name )

        if not self.overlay_view.set_overlay_image( file_name ):
            print( f"could not load {file_name}" )
            return

        print( f"overlay image: {file_name}" )

        a_pixmap            = self.overlay_view.overlay_item.pixmap()
        if not a_pixmap.hasAlphaChannel():
            msg                 = ( "note: that image has no alpha channel, so nothing will show "
                                    "through it -- use the opacity slider or a blend mode instead" )
            print( msg )


    # -------------------------------------
    def load_overlay( self, file_name ):
        """
        what it says -- and a word in the msg box if the image has no alpha,
        since "nothing shows through" is otherwise a puzzling result
        """
        if not self.overlay_view.set_overlay_image( file_name ):
            print( f"could not load {file_name}" )
            return

        print( f"overlay image: {file_name}" )

        a_pixmap            = self.overlay_view.overlay_item.pixmap()
        if not a_pixmap.hasAlphaChannel():
            msg                 = ( "note: that image has no alpha channel, so nothing will show "
                                    "through it -- use the opacity slider or a blend mode instead" )
            print( msg )

    # -------------------------------------
    def on_save_result( self, ):
        """
        read it -- saved at the size of the base image, not at the size it
        happens to look on screen, so the view zoom makes no difference to it
        """
        if not self.overlay_view.has_images():
            print( "nothing to save -- load a base and an overlay first" )
            return

        file_name, _        = QFileDialog.getSaveFileName( self, "Save the composite",
                                                           os.path.join( self.last_dir, "overlay_result.png" ),
                                                           IMAGE_FILTER )
        if not file_name:
            return

        self.last_dir       = os.path.dirname( file_name )

        is_ok               = self.overlay_view.save_result( file_name )

        if is_ok:
            a_image             = self.overlay_view.render_to_image()
            msg                 = ( f"saved {a_image.width()}x{a_image.height()} to {file_name}" )
            print( msg )
        else:
            print( f"save FAILED to {file_name}" )

    # -------------------------------------
    def save_file( self, file_name ):
        """

        """
        if not self.overlay_view.has_images():
            print( "nothing to save -- load a base and an overlay first" )
            return

        # not sure about this
        self.last_dir       = os.path.dirname( file_name )

        is_ok               = self.overlay_view.save_result( file_name )

        if is_ok:
            a_image         = self.overlay_view.render_to_image()
            msg             = ( f"saved {a_image.width()}x{a_image.height()} to {file_name}" )
            print( msg )
        else:
            print( f"save FAILED to {file_name}" )


    # ---- the controls ------------------------------------------------------

    # -------------------------------------
    def on_overlay_changed( self, x, y, rotation, scale ):
        """
        read it -- the view telling us the overlay moved, most often because
        of a mouse drag.  every spin box has its signals blocked while it is
        filled in, or setValue would fire valueChanged, which would drive the
        view, which would emit again -- round and round
        """
        for i_widget, i_value in ( ( self.x_spin,        int( round( x ) ) ),
                                   ( self.y_spin,        int( round( y ) ) ),
                                   ( self.rotation_spin, rotation ),
                                   ( self.scale_spin,    scale ), ):
            i_widget.blockSignals( True )
            i_widget.setValue( i_value )
            i_widget.blockSignals( False )

    # -------------------------------------
    def on_offset_spin_changed( self, value ):
        """
        what it says -- value is unused, both spin boxes are read together
        """
        self.overlay_view.set_overlay_offset( self.x_spin.value(), self.y_spin.value() )

    # -------------------------------------
    def on_rotation_spin_changed( self, value ):
        """ what it says """
        self.overlay_view.set_overlay_rotation( value )

    # -------------------------------------
    def on_scale_spin_changed( self, value ):
        """
        what it says -- the overlay's own scale, part of the saved result.
        the Fit / 1:1 / +- buttons are the other kind of scale, view zoom
        """
        self.overlay_view.set_overlay_scale( value )

    # -------------------------------------
    def on_opacity_changed( self, value ):
        """ what it says -- slider is 0..100, the view wants 0.0..1.0 """
        self.overlay_view.set_overlay_opacity( value / 100.0 )

    # -------------------------------------
    def on_blend_changed( self, ix ):
        """ what it says """
        if ix < 0 or ix >= len( COMPOSITION_MODES ):
            return

        a_name, a_mode      = COMPOSITION_MODES[ ix ]
        self.overlay_view.set_composition_mode( a_mode )
        print( f"blend mode: {a_name}" )

    # -------------------------------------
    def on_blink_toggled( self, is_checked ):
        """ what it says """
        if is_checked:
            self.blink_timer.start()
        else:
            self.blink_timer.stop()
            self.overlay_view.set_overlay_visible( True )

    # -------------------------------------
    def _blink_tick( self, ):
        """ what it says -- flip the overlay on and off """
        self.overlay_view.set_overlay_visible( not self.overlay_view.is_overlay_visible() )

    # -------------------------------------
    def on_reset_overlay( self, ):
        """ what it says -- corner on corner, no rotation, no scale """
        self.overlay_view.reset_overlay()
        print( "overlay reset" )

    # -------------------------------------
    def on_fit( self, ):
        """ what it says """
        self.overlay_view.fit_to_view()




# ---- eof ---------------------------


