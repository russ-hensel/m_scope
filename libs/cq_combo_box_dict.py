#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 19:31:14 2026

@author: claude, russ edit
"""

# ---- tof

# # --------------------
# if __name__ == "__main__":
#     import main   # noqa  stops auto removal by pycln
# # --------------------



"""
vib coded for pyqt by example where it has a tab, this is copied out
but should be linked in to replace inline code !!


2.  the model lives inside a QComboBox subclass, CQComboBoxDict.
    The caller never touches setModel(), never converts a key to a
    row, and never has to remember to save the selected key across
    a set_dict().  Compare:

        # tab_q_combo_box_dict.py, model outside the widget
        keys = self.save_keys()
        self.dict_model.set_dict( BIG_DICT )
        self.restore_keys( keys )

        # here, model inside the widget
        self.combo_box.set_dict( BIG_DICT )

    The price is that the model is no longer shareable.  In
    tab_q_combo_box_dict.py both combo boxes ran off one model,
    here each CQComboBoxDict has its own, which is why mutate_2
    changes one combo box and leaves the other alone.
"""



# ---- imports


from qtpy.QtCore import QAbstractListModel, QModelIndex, Qt
from qtpy.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

# ---- imports local -- then constants

# ---- the dicts we play with

NUMBER_DICT     = {
                    1   : "one",
                    2   : "two",
                    3   : "three",
                    4   : "four",
                    5   : "five",
                  }

COLOR_DICT      = {
                    1   : "red",
                    2   : "green",
                    3   : "blue",
                  }

BIG_DICT        = {
                    1   : "uno",
                    2   : "dos",
                    3   : "tres",
                    4   : "cuatro",
                    5   : "cinco",
                    6   : "seis",
                    7   : "siete",
                    8   : "ocho",
                  }


# --------------------------------------------------
class DictKeyListModel( QAbstractListModel ):
    """
    this stores the data, but does not keep current
    selection info

    the data is a dict:  key -> value

    display_keys True    the drop down shows str( key )
    display_keys False   the drop down shows the value

    either way KEY_ROLE gives the key and VALUE_ROLE the value,
    so what is displayed and what you read back are independent

    row order is dict insertion order, python 3.7+ guarantees it
    self._keys is just a row -> key lookup so we do not rebuild
    a key list on every call to data()
    """
    # -----------------------
    def __init__( self, a_dict = None, display_keys = True, parent = None ):
        super().__init__( parent )

        self.KEY_ROLE       = Qt.UserRole
        self.VALUE_ROLE     = Qt.UserRole + 1

        if a_dict is None:
            a_dict          = NUMBER_DICT

        self._original_dict = dict( a_dict )   # for reset_dict()
        self._dict          = dict( a_dict )
        self._keys          = list( self._dict.keys() )
        self._display_keys  = display_keys

    # -----------------------
    def rowCount( self, parent = QModelIndex() ):
        if parent.isValid():
            return 0
        return len( self._keys )

    # -----------------------
    def columnCount( self, parent = QModelIndex() ):
        if parent.isValid():
            return 0
        return 2

    # -----------------------
    def data( self, index, role = Qt.DisplayRole ):
        if not index.isValid():
            return None

        row     = index.row()
        col     = index.column()
        if row < 0 or row >= len( self._keys ):
            return None

        key     = self._keys[ row ]
        value   = self._dict[ key ]

        # the display, key or value depending on the flag
        # str() because a key may be an int and a view wants text
        if role in ( Qt.DisplayRole, Qt.EditRole ):
            if self._display_keys:
                return str( key )
            return value

        # both are always available, whatever is on display
        if role == self.KEY_ROLE:
            return key

        if role == self.VALUE_ROLE:
            return value

        if role == Qt.ToolTipRole:
            if col == 0:
                return f"key={key}  value={value}"
            if col == 1:
                return f"value={value}"

        return None

    # -----------------------
    def headerData( self, section, orientation, role = Qt.DisplayRole ):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == 0:
                return "key"
            if section == 1:
                return "value"
        return None

    # ---- what gets displayed

    # -----------------------
    def set_display_keys( self, display_keys ):
        """
        show keys or show values

        only the DisplayRole changes, no row comes or goes, so this
        is a dataChanged over every row and NOT a model reset --
        which is why the combo box keeps its selection
        """
        if display_keys == self._display_keys:
            return

        self._display_keys  = display_keys

        last_row    = len( self._keys ) - 1
        if last_row < 0:
            return

        self.dataChanged.emit( self.index( 0, 0 ),
                               self.index( last_row, 0 ) )

    # -----------------------
    def get_display_keys( self ):
        return self._display_keys

    # ---- set and reset the whole dict

    # -----------------------
    def set_dict( self, a_dict ):
        """
        replace all the data with a new dict

        this is a model reset, every view attached to the model
        throws away what it knew, including a QComboBox current
        index.  CQComboBoxDict.set_dict() puts the selection back.
        """
        self.beginResetModel()
        self._dict      = dict( a_dict )
        self._keys      = list( self._dict.keys() )
        self.endResetModel()

    # -----------------------
    def reset_dict( self ):
        """
        put back the dict the model was built with
        """
        self.set_dict( self._original_dict )

    # -----------------------
    def get_dict( self ):
        """
        a copy, so a caller cannot edit around our back
        """
        return dict( self._dict )

    # ---- smaller changes, no full reset

    # -----------------------
    def set_item( self, key, value ):
        """
        add a key at the end, or change the value of a key
        we already have -- like dict[ key ] = value
        """
        if key in self._dict:
            self._dict[ key ]   = value
            row                 = self.row_for_key( key )
            index               = self.index( row, 0 )
            self.dataChanged.emit( index, index )
            return

        insert_row  = len( self._keys )
        self.beginInsertRows( QModelIndex(), insert_row, insert_row )
        self._dict[ key ]   = value
        self._keys.append( key )
        self.endInsertRows()

    # -----------------------
    def remove_key( self, key ):
        """
        drop one key, returns True if there was one to drop
        """
        row     = self.row_for_key( key )
        if row < 0:
            return False

        self.beginRemoveRows( QModelIndex(), row, row )
        del self._dict[ key ]
        del self._keys[ row ]
        self.endRemoveRows()
        return True

    # ---- lookups

    # -----------------------
    def row_for_key( self, target_key ):
        """
        -1 when we do not have the key, which is also what
        QComboBox.setCurrentIndex() wants for "nothing selected"
        """
        for ix, i_key in enumerate( self._keys ):
            if i_key == target_key:
                return ix
        return -1

    # -----------------------
    def key_for_row( self, row ):
        if row < 0 or row >= len( self._keys ):
            return None
        return self._keys[ row ]


# --------------------------------------------------
class CQComboBoxDict( QComboBox ):
    """
    a QComboBox that builds and owns its own DictKeyListModel

    the whole api is in keys and dicts, rows never leave this class

        combo   = CQComboBoxDict( NUMBER_DICT )
        combo.set_current_key( 3 )
        combo.set_dict( COLOR_DICT )    # selection kept if key survives
        combo.current_key()             # 3
        combo.current_value()           # "blue"

    the model is reachable as combo.dict_model if you need the raw
    thing, but you should not need it
    """
    # -----------------------
    def __init__( self, a_dict = None, display_keys = True, parent = None ):
        super().__init__( parent )

        self.dict_model     = DictKeyListModel( a_dict,
                                                display_keys = display_keys,
                                                parent       = self )
        self.setModel( self.dict_model )
        # With QAbstractListModel descendants, use column 0 for combo stability.
        self.setModelColumn( 0 )
        self.setSizeAdjustPolicy( QComboBox.AdjustToContents )
        self.setMaxVisibleItems( 10 )
        self.setMinimumWidth( 320 )
        self.setMinimumHeight( 32 )
        self.view().setMinimumWidth( 320 )
        self.view().setMinimumHeight( 120 )

    # ---- selection, in keys not rows

    # -----------------------
    def current_key( self ):
        """
        None when nothing is selected, empty model for instance
        """
        return self.currentData( self.dict_model.KEY_ROLE )

    # -----------------------
    def current_value( self ):
        """
        the value even when the key is what is on display
        """
        return self.currentData( self.dict_model.VALUE_ROLE )

    # -----------------------
    def set_current_key( self, key ):
        """
        select the row holding key, returns True if we found it
        a key we do not have leaves the combo box with nothing
        selected, index -1
        """
        row     = self.dict_model.row_for_key( key )
        self.setCurrentIndex( row )
        return row >= 0

    # ---- the dict, pass through to the model

    # -----------------------
    def set_dict( self, a_dict, keep_key = True ):
        """
        new data for the combo box

        keep_key True   remember the selected key over the model
                        reset and select it again if the new dict
                        still has it
        keep_key False  take what the reset leaves us, row 0

        this is the reason for the subclass, the caller does not
        have to remember to do the save and restore
        """
        old_key     = self.current_key()

        self.dict_model.set_dict( a_dict )

        if keep_key and ( old_key is not None ):
            self.set_current_key( old_key )

    # -----------------------
    def reset_dict( self, keep_key = True ):
        """
        put back the dict we were built with
        """
        old_key     = self.current_key()

        self.dict_model.reset_dict()

        if keep_key and ( old_key is not None ):
            self.set_current_key( old_key )

    # -----------------------
    def get_dict( self ):
        return self.dict_model.get_dict()

    # -----------------------
    def set_item( self, key, value ):
        """
        no selection juggling needed, an insert or a dataChanged
        does not disturb the current row
        """
        self.dict_model.set_item( key, value )

    # -----------------------
    def remove_key( self, key ):
        return self.dict_model.remove_key( key )

    # ---- display

    # -----------------------
    def set_display_keys( self, display_keys ):
        """
        show the keys in the drop down, or the values
        """
        self.dict_model.set_display_keys( display_keys )

    # -----------------------
    def get_display_keys( self ):
        return self.dict_model.get_display_keys()

    # -----------------------
    def toggle_display_keys( self ):
        """
        handy for a button, returns the new setting
        """
        display_keys    = not self.dict_model.get_display_keys()
        self.set_display_keys( display_keys )
        return display_keys



# ---- eof ---------------------------


