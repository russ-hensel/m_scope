#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

# ---- tof
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

import string_util
from functools import partial

#------------------------------------------
class ComboSync3(  ):
    """
    creation of synchronized combo boxes
    here 3 levels
        lower levels change higher levels
    """
    #----------- init -----------

    def __init__(self, dup = False ):
        """
        See class doc
        """

        # key is index from level 0
        self.values_dict        = {}   # key is an index tuple
        self.dup                = dup        # duplicate _1 may want to implement??
        self.ddl_widgets        = []
        # may be using disconnect instead     disconnect
        self.ignore_change_1    = True  # what it says search -- during setup
        self.ignore_change_2    = True
            # also consider disconnet
        self._build_ddls()

    def _build_ddls(self,  ):
        """
        what it says, read dll is dropdownlist or QComboBox
        """
        widget              = QComboBox()
        self.ddl_0          = widget
        widget.setEditable( True )
        #rint( f"a_combo_sync.ddl_0 {id(self.ddl_0)  = }")
        self.ddl_widgets.append( widget )

        widget              = QComboBox()
        self.ddl_1          = widget
        widget.setEditable( True )
        self.ddl_widgets.append( widget )

        widget              = QComboBox()
        self.ddl_2          = widget
        widget.setEditable( True )
        self.ddl_widgets.append( widget )

        # if self.dup:

        #     widget              = QComboBox()
        #     self.ddl_1b         = widget

    def set_values(self, index_tuple, values  ):
        """
        what it says
        """
        self.values_dict[ index_tuple ] = values

    def load_ddls(self,  ):
        """
        load with values
        """
        # # consider alternative
        # self.ignore_change_1    = True  # what it says search -- during setup
        # self.ignore_change_2    = True

        print( "load_ddls do we need next ??")
        # try:
        #     self.ddl_0.currentIndexChanged.disconnect()
        # except:
        #     pass

        # try:
        #     self.ddl_1.currentIndexChanged.disconnect()
        # except:
        #     pass

        # print( "load_ddls beware disconnects ")

        values     = self.values_dict[   ( -1, )   ]  # no prior index
        widget     = self.ddl_0

        widget.addItems( values )

        # check dict for indices for all...
        for ix in range( 0, len( values )):
            index_tuple  = ( ix, )
            values_1     = self.values_dict.get( index_tuple, None )
            if values_1 is None:
                msg    = f"index is missing for level {index_tuple = }"
                print( msg )
                1/0

        self.ddl_1.addItems( self.values_dict[   ( 0, )   ] )

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

        self.ddl_2.addItems( self.values_dict[   ( 0, 0 )   ] )
        # if self.ddl_1b:
        #     self.ddl_1b.addItems( self.values_dict[   ( ix, )   ] )
            #   dll_0_index_changed
        # seem not to be woeking try alternatives
        # self.ddl_0.currentIndexChanged.connect( lambda: self.ddl_0_index_changed  )
        # self.ddl_1.currentIndexChanged.connect( lambda: self.ddl_1_index_changed  )

        # this works while above does not seem to so use this
        self.ddl_0.currentIndexChanged.connect( self.ddl_0_index_changed  )
        self.ddl_1.currentIndexChanged.connect( self.ddl_1_index_changed  )

        #rint( "connects should be set")

        #ddl_0_index_changed
    def ddl_0_index_changed( self,   ):
        """
        try
        self.ddl_0.currentIndexChanged.disconnect()
        """
        print( "ddl_0_index_changed")
        # try:
        #     self.ddl_1.currentIndexChanged.disconnect()
                # opposite of connect why
        # except:
        #     pass

        #print( f"dll_0_index_changed  ")
        index    = self.ddl_0.currentIndex()
        print( f"dll_0_index_changed {index}")

        index_tuple    = ( index, )

        print( f"dll_0_index_changed {index}")
        index_tuple    = ( index, )
        widget         = self.ddl_1
        widget.clear()
        widget.addItems( self.values_dict[ ( index, ) ] )
        widget.setCurrentIndex( 0 )

        self.ddl_1.currentIndexChanged.connect( lambda: self.ddl_1_index_changed() )

        self.ddl_1_index_changed()

    def ddl_1_index_changed( self,   ):
        """

        """
        print( "ddl_1_index_changed")
        index_0         = self.ddl_0.currentIndex()
        index_1         = self.ddl_1.currentIndex()
        index_tuple     = ( index_0, index_1 )
        print( f"dll_1_index_changed {index_tuple}")
        #values_2     = self.values_dict.get( index_tuple_2, None )

        widget          = self.ddl_2
        widget.clear()
        widget.addItems( self.values_dict[   index_tuple  ] )
        widget.setCurrentIndex( 0 )

    # ----------------------------------
    def get_3_args( self, remove_cmnt  = False  ):
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
            if remove_cmnt:
                splits  = data.split("#")
                data    = f"{splits[0].strip()} "   # leave only 1 trailing space
            ret.append( data )

        return ret    # list


    def __str__(self ):
        a_str   = ""
        a_str   = ">>>>>>>>>>* ComboSync3 *<<<<<<<<<<<<"
        a_str   = string_util.to_columns( a_str, ["ddl_0",
                                           f"{self.ddl_0}" ] )
        a_str   = string_util.to_columns( a_str, ["ddl_1",
                                           f"{self.ddl_1}" ] )
        a_str   = string_util.to_columns( a_str, ["ddl_2",
                                           f"{self.ddl_2}" ] )
        a_str   = string_util.to_columns( a_str, ["ddl_widgets",
                                           f"{self.ddl_widgets}" ] )
        a_str   = string_util.to_columns( a_str, ["dup",
                                           f"{self.dup}" ] )
        a_str   = string_util.to_columns( a_str, ["values_dict",
                                           f"{self.values_dict}" ] )
        a_str   = string_util.to_columns( a_str, ["ddl_0_index_changed",
                                           f"{self.ddl_0_index_changed}" ] )
        return a_str

# ---- bof