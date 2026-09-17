#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 18:35:25 2026

@author: russ
"""

# ---- tof

# --------------------
if __name__ == "__main__":
    import main   # noqa  stops auto removal by pycln
# --------------------

# ---- imports
from qtpy.QtCore import QAbstractListModel, QModelIndex, Qt


NUMBER_DICT     = {
                    1   : "one",
                    2   : "two",
                    3   : "three",
                    4   : "four",
                    5   : "five",
                  }


# --------------------------------------------------
class DictListModel( QAbstractListModel ):
    """
    dict_list_model.DictListModel( a_dict = )
    this stores the data, but does not keep current
    selection info

    the data is a dict:  key -> value
        the key   is shown as user data ( KEY_ROLE )
        the value is what the combo box displays

    row order is dict insertion order, python 3.7+ guarantees it
    self._keys is just a row -> key lookup so we do not rebuild
    a key list on every call to data()
    """
    # -----------------------
    def __init__( self, a_dict = None, parent = None ):
        super().__init__( parent )

        self.KEY_ROLE       = Qt.UserRole
        self.VALUE_ROLE     = Qt.UserRole + 1

        if a_dict is None:
            a_dict          = NUMBER_DICT

        self._original_dict = dict( a_dict )   # for reset_dict()
        self._dict          = dict( a_dict )
        self._keys          = list( self._dict.keys() )

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

        # For combo rendering, always provide the string value.
        if role in ( Qt.DisplayRole, Qt.EditRole ):
            return value

        # Always provide the key as user data.
        if role == self.KEY_ROLE:
            return key

        if role == self.VALUE_ROLE:
            return value

        if role == Qt.ToolTipRole:
            if col == 0:
                return f"key={key}"
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

    # ---- set and reset the whole dict

    # -----------------------
    def set_dict( self, a_dict ):
        """
        replace all the data with a new dict

        this is a model reset, every view attached to the model
        throws away what it knew, including a QComboBox current
        index.  save/restore the key yourself if you care.
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


# ---- eof ---------------------------


