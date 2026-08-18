#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


    does it work?? how relaed to combo_sync_2 and combo_sync_qt  this stuff
    has worked but currently a mess
    should be a demo in qt5_by_example but even that is not clear
    is there a combo_sync  module


combo boxes synced across 2 levels

that is index
for second level is
just the current level for the 0 ddl

but allow 2 seperate instances of second  1 ddl  1a and 1 b

level 0   runs on a list of choices

level 1a and b runs on the index from level 0


"""
# ---- tof
# ------------------ QT


# ---- imports
# ----QtWidgets

from PyQt5.QtWidgets import (
    QAction,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QMenu,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QWidget,
    )





#------------------------------------------
class ComboSync2(  ):
    """
    creation of synchronized combo boxes

        it creates
    """
    #----------- init -----------

    def __init__(self, dup = False ):
        """
        See class doc
        """
        # key is index from level 0
        self.values_dict    = {}   # key is an index tuple

        # creates these three  -- 0 is index level
        self.ddl_0          = None    # level 0 ddl, controls both of otthers
        self.ddl_1a         = None    # synced to ddl_0
        self.ddl_1b         = None    # also synced to ddl_0 indipendent of ddl1a

        self.dup            = dup        # duplicate _1
        self.ignore_change  = True  # what it says search


        # was/did I create list here
        self.ddl_widgets    = []
        self._build_dlls()

    #--------------------------------------
    def _build_dlls(self,  ):
        """
        create the actual widgets
        will be placed by the caller
        """
        widget              = QComboBox()
        self.ddl_0          = widget
        widget.setEditable( True )
        self.ddl_widgets.append( widget )

        widget              = QComboBox()
        self.ddl_1a          = widget
        widget.setEditable( True )
        self.ddl_widgets.append( widget )

        widget              = QComboBox()
        self.ddl_1b          = widget
        widget.setEditable( True )
        self.ddl_widgets.append( widget )


    # ---------------------------------------
    def clear_values(self,    ):
        """
        what it says
        """
        self.values_dict    = {}

    # ---------------------------------------
    def set_values(self, index_tuple, values  ):
        """
        what it says
        """
        self.values_dict[ index_tuple ] = values

    # ---------------------------------------
    def add_value(self, index_tuple, i_value  ):
        """
        what it says
        add a i_value to the approprite list
        another way to construct a list
        i_value is a string
        """
        values   = self.values_dict.get( index_tuple, [] )

        values.append( i_value )
        self.values_dict[ index_tuple ] = values

    # ---------------------------------------
    def load_ddls(self,  ):
        """
        load with values -- only 0 needs loading rest are done on change
        """
        self.ignore_change  = True
        values              = self.values_dict[   ( -1, )   ]  # no prior index
        widget              = self.ddl_0
        widget.clear()
        widget.addItems( values )
        widget.setCurrentIndex( 0 )

        # # check dict for indices for all...
        # for ix in range( 0, len( values )):
        #     index_tuple  = ( ix, )
        #     values_2     = self.values_dict.get( index_tuple, None )
        #     if values_2 is None:
        #         msg    = f"index is missing for level {index_tuple = }"
        #         print( msg )
        #         1/0
        # self.ddl_1.addItems( self.values_dict[   ( 0, )   ] )
        # if self.ddl_1b:
        #     self.ddl_1b.addItems( self.values_dict[   ( 0, )   ] )
        self.ignore_change  = False
        self.ddl_0_index_changed( )
        #self.ddl_0.currentIndexChanged.connect( self.ddl_0_index_changed)
        self.ddl_0.currentIndexChanged.connect( lambda: self.ddl_0_index_changed() )

    def ddl_0_index_changed( self,   ):
        """
        when user clicks to change dll0 or at load of ddl
        """
        print( f"ComboSync2 dll_0_index_changed  ")
        index    = self.ddl_0.currentIndex()
        print( f"dll_0_index_changed {index} {self.ignore_change = } ")
        if self.ignore_change:
            return

        index_tuple    = ( index, "a" )
        widget         = self.ddl_1a
        widget.clear()
        widget.addItems( self.values_dict[   index_tuple   ] )
        widget.setCurrentIndex( 0 )

        index_tuple    = ( index, "b" )
        widget         = self.ddl_1b
        widget.clear()
        widget.addItems( self.values_dict[   index_tuple   ] )
        widget.setCurrentIndex( 0 )

        # if self.ddl_1b is not None:
        #     widget        =  self.ddl_1b
        #     widget.clear()
        #     widget.addItems( self.values_dict[ ( index, ) ] )
        #     widget.setCurrentIndex( 0 )


    # ----------------------------------
    def get_3_args( self ):
        """
        !! looks ok but too many trailing blanks ?? and possibly leading ??
        what it says, read
        see call in build_command
        clears out the # if present ( comment )
        Returns
            tuple/list of the contents of 3 drop downs stripped of comments
            would like to apply substitutions

        """
        ret    = []
        for i_widget in self.ddl_widgets:  # change to list comp ??
            data    = i_widget.currentText()
            splits  = data.split("#")
            data    = f"{splits[0].strip()} "   # leave only 1 trailing space
            ret.append( data )

        return ret    # tuple of 3 arg values

# ---- eof ---------------------


