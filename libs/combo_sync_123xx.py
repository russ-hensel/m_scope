#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
combo boxes synced across 2 levels

that is index
for second level is
just the current level for the 0 ddl

but allow 2 seperate instances of second  1 ddl  1a and 1 b

level 0   runs on a list of choices

level 1a and b runs on the index from level 0


"""
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
class ComboSync3(  ):
    """
    creation of synchronized combo boxes
    """
    #----------- init -----------

    def __init__(self, dup = False ):
        """
        See class doc
        """

        # key is index from level 0
        self.values_dict    = {}   # key is an index tuple
        self.dup            = dup        # duplicate _1 may want to implement??
        self.dll_widgets    = []

        self._build_dlls()

    def _build_dlls(self,  ):
        """
        what it says, read dll is dropdownlist or QComboBox
        """
        widget              = QComboBox()
        self.dll_0          = widget
        self.dll_widgets.append( widget )

        widget              = QComboBox()
        self.dll_1          = widget
        self.dll_widgets.append( widget )

        widget              = QComboBox()
        self.dll_2          = widget
        self.dll_widgets.append( widget )

        # if self.dup:

        #     widget              = QComboBox()
        #     self.dll_1b         = widget

    def set_values(self, index_tuple, values  ):
        """
        what it says
        """
        self.values_dict[ index_tuple ] = values

    def load_dlls(self,  ):
        """
        load with values
        """
        try:
            self.dll_0.currentIndexChanged.disconnect()
        except:
            pass

        try:
            self.dll_1.currentIndexChanged.disconnect()
        except:
            pass

        values     = self.values_dict[   ( -1, )   ]  # no prior index
        widget     = self.dll_0

        widget.addItems( values )

        # check dict for indices for all...
        for ix in range( 0, len( values )):
            index_tuple  = ( ix, )
            values_1     = self.values_dict.get( index_tuple, None )
            if values_1 is None:
                msg    = f"index is missing for level {index_tuple = }"
                print( msg )
                1/0

        self.dll_1.addItems( self.values_dict[   ( 0, )   ] )

        for ix in range( 0, len( values )):
            index_0      = ix
            index_tuple  = ( ix, )
            values_1     = self.values_dict.get( index_tuple, None )

            for iy  in range( 0, len ( values_1 ) ):
                index_tuple_2  = ( ix, iy )
                print( index_tuple_2 )
                values_2     = self.values_dict.get( index_tuple_2, None )
                if values_2 is None:
                    msg    = f"index is missing for level {index_tuple_2 = }"
                    print( msg )
                    1/0

        self.dll_2.addItems( self.values_dict[   ( 0, 0 )   ] )
        # if self.dll_1b:
        #     self.dll_1b.addItems( self.values_dict[   ( ix, )   ] )

        self.dll_0.currentIndexChanged.connect( lambda: self.dll_0_index_changed() )
        self.dll_1.currentIndexChanged.connect( lambda: self.dll_1_index_changed() )


    def dll_0_index_changed( self,   ):
        """
        try
        self.dll_0.currentIndexChanged.disconnect()
        """
        try:
            self.dll_1.currentIndexChanged.disconnect()
        except:
            pass

        #print( f"dll_0_index_changed  ")
        index    = self.dll_0.currentIndex()
        print( f"dll_0_index_changed {index}")

        index_tuple    = ( index, )

        print( f"dll_0_index_changed {index}")
        index_tuple    = ( index, )
        widget         = self.dll_1
        widget.clear()
        widget.addItems( self.values_dict[ ( index, ) ] )
        widget.setCurrentIndex( 0 )

        self.dll_1.currentIndexChanged.connect( lambda: self.dll_1_index_changed() )

        self.dll_1_index_changed()

    def dll_1_index_changed( self,   ):
        """

        """
        index_0         = self.dll_0.currentIndex()
        index_1         = self.dll_1.currentIndex()
        index_tuple     = ( index_0, index_1 )
        print( f"dll_1_index_changed {index_tuple}")
        #values_2     = self.values_dict.get( index_tuple_2, None )

        widget          = self.dll_2
        widget.clear()
        widget.addItems( self.values_dict[   index_tuple  ] )
        widget.setCurrentIndex( 0 )

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
