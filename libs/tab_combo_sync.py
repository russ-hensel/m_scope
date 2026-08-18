#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ---- tof
"""
from:
/mnt/WIN_D/Russ/0000/python00/python3/_examples/python_book_code/book_pyqt5_src/basic/widgets_list.py
  widgets_list.py

KEY_WORDS:      comboBox sync ddl syncronized list custom
CLASS_NAME:     ComboSyncTab
WIDGETS:        ComboSync3  ComboSync2
STATUS:         runs_correctly_5_10      demo_complete_2_10   !! review_key_words   !! review_help_0_10
TAB_TITLE:      ComboSync


"""

# --------------------
if __name__ == "__main__":
    #----- run the full app
    import main_qt
    #main.main()
# --------------------


import inspect
import subprocess
import sys
import time
from datetime import datetime
from functools import partial
from subprocess import PIPE, STDOUT, Popen, run

import wat
from PyQt5 import QtGui
from PyQt5.QtCore import (QDate,
                          QDateTime,
                          QModelIndex,
                          QSize,
                          Qt,
                          QTime,
                          QTimer)
from PyQt5.QtGui import QColor, QPalette, QTextCursor, QTextDocument
# sql
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
# widgets biger
# widgets -- small
# layouts
from PyQt5.QtWidgets import (QAction,
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDateEdit,
                             QDateTimeEdit,
                             QDial,
                             QDoubleSpinBox,
                             QFontComboBox,
                             QGridLayout,
                             QGroupBox,
                             QHBoxLayout,
                             QLabel,
                             QLCDNumber,
                             QLineEdit,
                             QListWidget,
                             QListWidgetItem,
                             QMainWindow,
                             QMenu,
                             QMessageBox,
                             QProgressBar,
                             QPushButton,
                             QRadioButton,
                             QSizePolicy,
                             QSlider,
                             QSpinBox,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QTimeEdit,
                             QVBoxLayout,
                             QWidget)

import parameters
#import qt_widgets
import utils_for_tabs as uft
import wat_inspector
import tab_base
#from   functools       import partial


#import ex_helpers
#import gui_qt_ext

import combo_sync_2
import combo_sync_3


# ---- end imports

print_func_header   = uft.print_func_header

#  --------
class ComboSyncTab( tab_base.TabBase  ) :
    def __init__(self):
        """
        some content from and there may be more
        /mnt/WIN_D/Russ/0000/python00/python3/_projects/rshlib/gui_qt_ext.py
        tab_misc_widgets.py
        """
        super().__init__()


        self.help_file_name    = "combo_sysn_tab.txt"
        self.mutate_dict[0]    = self.mutate_0
        self.mutate_dict[1]    = self.mutate_1
        # self.mutate_dict[2]    = self.mutate_2
        # self.mutate_dict[3]    = self.mutate_3
        # self.mutate_dict[4]    = self.mutate_4

        self._build_gui()

    #-------------------------------------
    def build_sync_combo_2( self ):
        """
        for the sync_combo test/example
        """
        tab_page    = QWidget()
        # Create a QGridLayout
        layout = QGridLayout()
        tab_page.setLayout(layout)

       # # Add buttons to the layout
       # for i, label in enumerate( button_labels ):
       #     button = QPushButton(label)
       #     layout.addWidget(button, i // 3, i % 3)
        dup             = False
        a_combo_sync    = combo_sync_2.ComboSync2( dup = dup )
        self.combo_sync_2 = a_combo_sync

        widget          = QLabel( "filler")
        ix_row          = 0
        ix_col          = 0
        layout.addWidget( widget, ix_row, ix_col )

        ix_row          += 1
        #ix_col          = 0
        widget          = QLabel( "but spacing still messed up")
        layout.addWidget( widget, ix_row, ix_col )

        ix_row          += 1
        #ix_col          = 0
        widget          = QLabel( "next ddl controls other 2")
        layout.addWidget( widget, ix_row, ix_col )

        ix_row          += 1
        #ix_col          = 0
        widget          = a_combo_sync.ddl_0
        layout.addWidget( widget, ix_row, ix_col )

        ix_row          += 1
        #ix_col          = 0
        widget           = a_combo_sync.ddl_1a
        layout.addWidget( widget, ix_row, ix_col )

        widget           = a_combo_sync.ddl_1b
        ix_row           += 1
        ix_col           = 0
        layout.addWidget( widget, ix_row, ix_col )

        widget           = QPushButton( "get_3_args from combos -- get_vals_2")
        widget.clicked.connect( lambda: self.get_vals_2() )
        ix_row           += 1
        ix_col           = 0
        layout.addWidget( widget, ix_row, ix_col )


        # ---- PB build_sync_combo_1_vals_b
        widget = QPushButton("combo_1\nvals_b")
        widget.clicked.connect( self.build_sync_combo_1_vals_b    )
        #button_layout.addWidget( widget,   )
        #ix_row           += 1
        ix_col           += 1
        layout.addWidget( widget, ix_row, ix_col )

        # ---- PB build_sync_combo_1_vals_b
        widget = QPushButton("combo_1\nvals_c")
        widget.clicked.connect( self.build_sync_combo_1_vals_c    )
        #button_layout.addWidget( widget,   )
        #ix_row           += 1
        ix_col           += 1
        layout.addWidget( widget, ix_row, ix_col )

        self.build_sync_combo_1_vals_a()

        return  tab_page


    def _build_gui_widgets(self, main_layout  ):
        """
        the usual, build the gui with the widgets of interest
        and the buttons for examples
        """
        layout              = QVBoxLayout(   )

        main_layout.addLayout( layout )
        button_layout        = QHBoxLayout(   )

        # ---- QLabel
        widget  = QLabel("Qlabel 1")
        layout.addWidget( widget )

        # ---- Create tabs
        self.tab_widget = QTabWidget()   # really the folder for the tabs
                                         # tabs themselves are just Widgets
        layout.addWidget( self.tab_widget   ) # what do the numbers mean

        tab_page_widget    = self.build_sync_combo_2( )
        self.tab_widget.addTab( tab_page_widget, "sync_combo_2"  )

        tab_page_widget    = self.build_sync_combo_3( )
        self.tab_widget.addTab( tab_page_widget, "sync_combo_3"  )

        button_layout      = QHBoxLayout(   )
        layout.addLayout( button_layout )


        widget = QPushButton("mutate\n")
        self.button_ex_1         = widget
        widget.clicked.connect( lambda: self.mutate( ) )
        button_layout.addWidget( widget )

        # ---- PB inspect
        widget = QPushButton("inspect\n")
        widget.clicked.connect( self.inspect    )
        button_layout.addWidget( widget,   )

        # ---- PB breakpoint
        widget = QPushButton("breakpoint\n")
        widget.clicked.connect( self.breakpoint    )
        button_layout.addWidget( widget,   )


    #----------------------
    def build_sync_combo_1_vals_a( self ):
        """
        """
        #self.append_function_msg( "build_sync_combo_1_vals_a" )
        self.combo_sync_2.set_values( (-1, ),       [ "0_index", "1_index" ] )

        self.combo_sync_2.set_values( ( 0, "a" ),   [ "0_index_ddl_a_item_0", "0_index_ddl_a_item_1" ] )
        self.combo_sync_2.set_values( ( 0, "b" ),   [ "0_index_ddl_b_item_0"  , "0_index_ddl_b_item_1" , "0_index_ddl_b_item_2"   ] )

        self.combo_sync_2.set_values( ( 1, "a" ),   [ "1_index_ddl_a_item_0",  "1_index_ddl_a_item_1" ] )
        self.combo_sync_2.set_values( ( 1, "b" ),   [ "1_index_ddl_b_item_0",  "1_index_ddl_b_item_1", "1_index_ddl_b_item_2" ] )

        self.combo_sync_2.load_ddls()


    def build_sync_combo_1_vals_b( self ):
        """
        """
        self.append_function_msg( "build_sync_combo_1_vals_b" )

        self.combo_sync_2.clear_values()

        self.combo_sync_2.set_values( (-1, ),       [ "0", "1" ] )

        self.combo_sync_2.set_values( ( 0, "a" ),   [ "0 a" ] )
        self.combo_sync_2.set_values( ( 0, "b" ),   [ "0 b"  ] )

        self.combo_sync_2.set_values( ( 1, "a" ),   [ "1 a" ] )
        self.combo_sync_2.set_values( ( 1, "b" ),   [ "1 b" ] )

        self.combo_sync_2.load_ddls()


    def build_sync_combo_1_vals_c( self ):
        """
        """
        self.append_function_msg( "build_sync_combo_1_vals_c" )
        self.combo_sync_2.clear_values()

        self.combo_sync_2.add_value( (-1, ), "00" )
        self.combo_sync_2.add_value( (-1, ), "11" )


        #self.combo_sync_2.set_values( (-1, ),       [ "0", "1" ] )

        self.combo_sync_2.set_values( ( 0, "a" ),   [ "0 a" ] )
        self.combo_sync_2.set_values( ( 0, "b" ),   [ "0 b"  ] )

        self.combo_sync_2.set_values( ( 1, "a" ),   [ "1 a" ] )
        self.combo_sync_2.set_values( ( 1, "b" ),   [ "1 b" ] )

        self.combo_sync_2.load_ddls()


    # ---------------------
    def get_vals_2( self, ):
        ""
        ""
        self.append_function_msg( "get_vals_2" )
        args      = self.combo_sync_2.get_3_args()
        self.append_msg( f"get_vals_2 {args = }")

    # ---------------------
    def build_sync_combo_3( self ):
        """
        for the sync_combo test/example
        """
        tab_page            = QWidget()
        # Create a QGridLayout
        layout              = QGridLayout()
        tab_page.setLayout(layout)

        a_combo_sync        = combo_sync_3.ComboSync3( )    # dup = dup
        self.combo_sync_3   = a_combo_sync

        widget     = a_combo_sync.ddl_0
        print( f"a_combo_sync.ddl_0 {id(widget) = }")
        ix_row     = 0
        ix_col     = 0
        layout.addWidget( widget, ix_row, ix_col )

        widget     = a_combo_sync.ddl_1
        ix_row     = 1
        ix_col     = 0
        layout.addWidget( widget, ix_row, ix_col )

        widget     = a_combo_sync.ddl_2
        ix_row     += 1
        ix_col     = 0
        layout.addWidget( widget, ix_row, ix_col )

        widget           = QPushButton( "get_vals_3")
        widget.clicked.connect( lambda: self.get_vals_3() )
        ix_row           += 1
        ix_col           = 0
        layout.addWidget( widget, ix_row, ix_col )

        self.set_vals_combo_sync_3_a(   )

        # ---- PB build_sync_combo_1_vals_b
        widget = QPushButton("not_implemeted")
        #widget.clicked.connect( self.build_sync_combo_1_vals_b    )
        #button_layout.addWidget( widget,   )
        #ix_row           += 1
        ix_col           += 1
        layout.addWidget( widget, ix_row, ix_col )

        # ---- PB build_sync_combo_1_vals_b
        widget = QPushButton("also_not_implemented")
        #widget.clicked.connect( self.build_sync_combo_1_vals_c    )
        #button_layout.addWidget( widget,   )
        #ix_row           += 1
        ix_col           += 1
        layout.addWidget( widget, ix_row, ix_col )

        return  tab_page

    # ---------------------
    def set_vals_combo_sync_3_a( self, ):
        ""
        ""
        # ---------

        # this is almost right  -- could just have the numbers

        # ---- set_values -- do not have 2 many values at a lower level
        self.combo_sync_3.set_values( (-1, ),   [ "0_index", "1_index", ] ) # "1_index_2" ] )

        # second ddl index = value first index in tuple her 0 0r 1
        self.combo_sync_3.set_values( ( 0, ),   [ "0_index/0",  "0_index/1" ] )
        self.combo_sync_3.set_values( ( 1, ),   [ "1_index/0",  "1_index/1", "1_index/2"  ]) #  "2_index_0",  "3_index_1" ] )

        # all for thired ddl forst index the level, second indx choice at pripr level ?
        self.combo_sync_3.set_values( ( 0, 0 ),   [ "0_index/0_index/0", "0_index/0_index/1", "0_index/0_index/2" ] )
        self.combo_sync_3.set_values( ( 0, 1 ),   [ "0_index_1_index/0", "0_index/1_index_1/1" ] )
        #self.combo_sync.set_values( ( 0, 2 ),   [ "a1-c", "a1-c" ] )

        self.combo_sync_3.set_values( ( 1, 0 ),  [ "1_index_0_index_0/0", "1_index/0_index/1" ] )

        self.combo_sync_3.set_values( ( 1, 1 ),  [ "1_index/1_index/0", "1_index_1_index/1", "1_index_1_index/2", "1_index/1_index/3" ] )

        self.combo_sync_3.set_values( ( 1, 2 ),  [ "1_index/2_index_0", "1_index_2/1" ] )

        self.combo_sync_3.set_values( ( 1, 3 ),  [ "1_index/3_index/0", "1_index_3/1", "1_index_3/2", "1_index_1_index/3" ] )

        #self.combo_sync.set_values( ( 1, 2 ),   [ "b0", "b1" ] )

        self.combo_sync_3.load_ddls()

    # ---------------------
    def get_vals_3( self, ):
        ""
        ""
        self.append_function_msg( "get_vals_3" )
        args      = self.combo_sync_3.get_3_args()
        self.append_msg( f"get_vals_3 {args = }")


     # --------
    def make_partial_widget_clicked( self, widget):
        """
        """
        from   functools import partial
        a_partial_foo       = partial( self.widget_clicked,  widget = widget )  # will set first arg    # --------

        return a_partial_foo


    # ------------------------------------
    def mutate_0( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_0" )

        msg    = "so far not implemented "
        self.append_msg( msg, clear = False )

    # ------------------------------------
    def mutate_1( self ):
        """
        read it -- mutate the widgets
        """
        self.append_function_msg( "mutate_1" )

        msg    = "so far not implemented "
        self.append_msg( msg, clear = False )




    # ------------------------
    def inspect(self):
        """
        the usual
        """
        self.append_function_msg( "inspect" )

        self_combo_sync_2     = self.combo_sync_2
        self_combo_sync_2_values_dict  = self.combo_sync_2.values_dict

        self_combo_sync_3     = self.combo_sync_3

        self_combo_sync_3_values_dict  = self.combo_sync_3.values_dict
        wat_inspector.go(
             msg            = "see self_widgets_list",
             a_locals       = locals(),
             a_globals      = globals(), )

    # ------------------------
    def breakpoint(self):
        """
        each tab gets its own function so we break in that
        tabs code
        """
        self.append_function_msg( "breakpoint" )

        breakpoint()



# ---- eof








