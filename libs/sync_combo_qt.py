# -*- coding: utf-8 -*-

# ---- tof
"""

Purpose:
    part of my ( rsh ) library of reusable code
    a library module for multiple applications
    sometimes included with applications but not used
        as this make my source code management easier.

        my examples do not refer to this and it may be
        either old or perahps new all is unclear

for a gui element, a drop down list ddl or combo box
    cascading for three levels, 0, 1, 2
    with synchronization between them.
"""


# ---- begin pyqt from import_qt.py
# ---- QtGui
from PyQt5.QtGui import (
    QIcon,
    QIntValidator,
    QStandardItem,
    QStandardItemModel,
        )

# ---- QtCore
from PyQt5.QtCore  import  (
    QAbstractTableModel,
    QDate,
    QModelIndex,
    QTimer,
    Qt,
    pyqtSlot,
    )

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

# ----QtWidgets big
from PyQt5.QtWidgets import (
    QActionGroup,
    QApplication,
    QDockWidget,
    QFrame,
    QMainWindow,
    QMdiArea,
    QMdiSubWindow,
    QTabWidget,
    QTableView,
    QToolBar,
    )

# ----QtWidgets layouts
from PyQt5.QtWidgets import (
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    )

# ----QtWidgets Boxs, Dialogs
from PyQt5.QtWidgets import (
    QFileDialog,
    QInputDialog,
    QMessageBox,
    )

# ---- QtSql
from PyQt5.QtSql import (
    QSqlDatabase,
    QSqlDriver,
    QSqlError,
    QSqlField,
    QSqlQuery,
    QSqlQueryModel,
    QSqlRecord,
    QSqlRelation,
    QSqlRelationalDelegate,
    QSqlRelationalTableModel,
    QSqlTableModel,
    )

# ---- end imports

#import sys
# import tkinter as Tk
# from   tkinter import ttk


# --------------- helper functions -----------------------
#------------------------------------------
def dict_merge( dict_1, dict_2 ):
    """
    what it says, read
    just can merge 2 -- is used ... works?
    """
    if dict_1 is None:
        if dict_2 is None:
            # or return None
            return_val = None
        else:
            # or
            return_val = dict_2

    else:
        if dict_2 is None:
            # or return
            return_val = dict_2
        else:
            return_val = { **dict_1 , **dict_2}

    #rint( f"dict_merg return_value = >return_val<")
    return return_val

#------------------------------------------
class SyncComboQt(  ):
    """
    creation of synchronized combo boxes
    """
    #----------- init -----------
    def __init__(self,  ):
        """
        See class doc
        """
        self._ddl_dict              = {}       # hold drop down contents of

            # need to undeerstand what this is
            # values for the ddl
            #     0 level
            #    all keys are the values for the for ddl_0
        x =    """
                 the values here are a dict for each key with info for ddl_1
                 { a: { aa1: [ "aaa", ]}
                   b:
                   c:

                       }

                  { a: { aa1: [ "aaa", ]}

                   do by index not text

                   ddl_0
                       [ "a", "b", "c" ]
                   ddl_1
             a          [ aa, aaa,]
             b          [ bb  bbb  bbbb ]
             c          [ cc  ccc  cccc, ccccc ]

                    dll_2

            aa          [ AA1   AA2   AA3  AA4 ]
            aaa         [ AAA1  AAA2   AAA3  AAA4 ]

            bb
            bbb
            bbbb

                        n             []
                        n x n         [][]
                        n x n x n     [][][]

                        how to setup, how to check

                        zero just a list
                        []
                        first level
                        {}    key is zero level
                        second level  key is () of first and second --- do on value or index?


            """
                                               # all three levels of the ddl
        self.arg_width              = 50       # ok as interface set prior to make
                                               # or change to set property

        self.ddl_0_widget           = None
        self.ddl_1_widget           = None
        self.ddl_2_widget           = None
        self.ddl_widgets            = None  # order matters
        self.dll_label_texts        = [None, None, None]   # not implemented ??

        # still loops
        self.enbled_change_ok       = None  # for debug
        self.ignore_change_cnt      = 0

    # --------------------------------------------------
    def __str__( self ):
        """
        the usual, read  !! need to be implemented
        """
        line_begin  = "\n    "  # formatting aid

        a_str       =  ""
        a_str       = f"{a_str}\n>>>>>>>>>>* SyncCombo  *<<<<<<<<<<<<"

        a_str       = f"{a_str}{line_begin}_ddl_dict             >{self._ddl_dict}<"
        #is_3d = self.is_3d()
        #----------------------------------+---------------------+-----------------------------
        a_str       = f"{a_str}{line_begin}self.is_3d()          >{self.is_3d()}<"
        return a_str

    # -----------------------------------
    def check( self, print_flag = False ):
        """

        """
        if type( self._ddl_dict ) != dict:
            e_msg = f"self._ddl_dict is not a dict"
            if print_flag:
                print( e_msg )
            is_ok = False
            return( is_ok, e_msg )

        is_3d = self.is_3d()
        if print_flag:
            print( f"is the control 3d {is_3d}" )

        for key, value  in self._ddl_dict.items():
            if print_flag:
                print( key,  value )
            if type( key ) != str:
                e_msg = f"self._ddl_dict key >{key}< is not a string"
                if print_flag:
                    print( e_msg )
                is_ok = False
                return( is_ok, e_msg )

            if type( value ) != dict:
                e_msg = f"self._ddl_dict value >{key}< is not a dict"
                if print_flag:
                    print( e_msg )
                is_ok = False
                return( is_ok, e_msg )

            lower_dict   = value
            if type( lower_dict ) != dict:
                e_msg = f"self._ddl_dict is not a dict"
                if print_flag:
                    print( e_msg )
                is_ok = False
                return( is_ok, e_msg )

            for l_key, l_value  in lower_dict.items():
                if print_flag:
                    print( "    ", l_key,  l_value )
                if type( l_key ) != str:
                    e_msg = f"lower dict for >{key}< own key not a string:\n    it is >{l_key}<"
                    if print_flag:
                        print( e_msg )
                    is_ok = False
                    return( is_ok, e_msg )

                if type( l_value ) != list:
                    e_msg = f"lower dict value for >{key}< is not a list:\n    it is >{l_value}<"
                    if print_flag:
                        print( e_msg )
                    is_ok = False
                    return( is_ok, e_msg )

        return ( True, "seems ok")

    # -----------------------------------
    def load_ddl_0( self, ):
        """
        ddl = drop down list
        what it says, read
        return
            mutates self
        """
        # values    = list( self._ddl_dict.keys() )
        #rint( f"load_ddl_0 values  {values}" )

        # clear the values load the values, then set to the first
        # for i_value in values
        #     self.ddl_0_widget.
        # self.ddl_0_widget.configure( values = values )
        # self.ddl_0_widget.set( values[0] )
        #rint( "check cascade to other ddls working" )


        values    = list( self._ddl_dict.keys() )
        widget    =         self.ddl_0_widget
        widget.clear()       # delete all items from comboBox
        widget.addItems( values )

        self.sync_ddl_0(   )

    # -----------------------------------
    def build_ddls( self, parent  ):
        """
        what it says, read
        call from external routine
        return
            mutates self
        """
        # ---- 0
        widget              = QComboBox()
        self.ddl_0_widget   = widget
        widget.addItem('Zero')
        widget.addItem('One')
        widget.addItem('Two')
        widget.addItem('Three')
        widget.addItem('Four')
        #widget.currentTextChanged.connect(self.current_text_changed)
        widget.setMinimumWidth( 200 )   # pretty much sets width
        widget.setEditable( True )

        foo     = self.conbo_currentIndexChanged
        foo     = lambda: self.conbo_currentIndexChanged()  # really ony one tha works
        foo     = self.zero_arg   # nothing
        #foo     = self.one_arg   # nothing
        #foo     = self.two_arg   # nothing
        #foo     = lambda: self.zero_arg()   # works
        #foo     = lambda: self.one_arg()  # TypeError: SyncComboQt.one_arg() missing 1 required positional argument: 'arg_1'
        # foo     = lambda: self.two_arg()  #  SyncComboQt.two_arg() missing 2 required positional arguments: 'arg_1' and 'arg_2'


        #widget.currentIndexChanged.connect( lambda: self.conbo_currentIndexChanged() )
        # widget.currentIndexChanged[int].connect(  self.conbo_currentIndexChanged  )
        # widget.currentIndexChanged[int].connect(  foo  )
        # a_widget = ttk.Combobox( parent,
        #                          width         = self.arg_width,
        #                          state         = "normal",
        #                          #textvariable  = "self.arg_2_var"
        #                          )
        # a_widget.bind( "<<ComboboxSelected>>", self.sync_ddl_0  )


        #self.ddl_widgets            = [ self.ddl_0_widget, ]

        # ---- 1
        widget              = QComboBox()
        self.ddl_1_widget   = widget
        widget.addItem('One')
        widget.addItem('Two')
        widget.addItem('Three')
        widget.addItem('Four')
        widget.setEditable( True )
        #widget.currentIndexChanged.connect(  self.sync_ddl_0 )
        #widget.currentTextChanged.connect(self.current_text_changed)
        widget.setMinimumWidth( 200 )

        # ---- 2
        widget              = QComboBox()
        self.ddl_2_widget   = widget
        #widget.addItem('One')
        widget.addItem('Two')
        widget.addItem('Three')
        widget.addItem('Four')
        widget.setEditable( True )
        #widget.currentIndexChanged.connect(self.current_index_changed)
        #widget.currentTextChanged.connect(  self.sync_ddl_1 )
        widget.setMinimumWidth( 200 )


        self.ddl_widgets            = [ self.ddl_0_widget,
                                        self.ddl_1_widget,
                                        self.ddl_2_widget,   ]

        self.load_ddl_0( )

        #self.enable_changed( True )  # up to now no command at all

        print( "connects follow" )
        # ---- all connects here
        #self.ddl_0_widget.currentIndexChanged.connect(self.current_text_changed )
        # self.ddl_0_widget.currentIndexChanged.connect( self.sync_ddl_0 )
        # self.ddl_1_widget.currentIndexChanged.connect( self.sync_ddl_1 )
        # nothing for ddl_2

        # self.ddl_0_widget.currentIndexChanged.connect( lambda: self.current_text_changed )
        self.ddl_0_widget.currentIndexChanged.connect( lambda: self.sync_ddl_0() )
        self.ddl_1_widget.currentIndexChanged.connect( lambda: self.sync_ddl_1() )

        print( "connects done" )
        return

    # ----------------------------------
    def is_3d( self,    ):
        """
        return:
            true if 3d ... by seeing if more than one value at top level
        """
        values    = list( self._ddl_dict.keys() )
        #rint( f"is_3d {len( values )}  {values}" )
        return len( values ) > 1

    # ----------------------------------
    def no_fun( self,    ):
        """
        a do nothing function
        """
        print( "call to no_fun")
        pass

    # -------------------------
    def enable_changed( self, enable_ok ):
        """

        """
        self.enbled_change_ok   = enable_ok
        if enable_ok:
            print( "enable_changed True")
            # self.ddl_0_widget.currentTextChanged.connect( self.sync_ddl_0 )
            # self.ddl_1_widget.currentTextChanged.connect( self.sync_ddl_1 )
        else:
            print( "enable_changed False")
            # self.ddl_0_widget.currentTextChanged.connect( self.no_fun )
            # self.ddl_1_widget.currentTextChanged.connect( self.no_fun )

    #     if enable_ok:

    #         self.ddl_1_widget.currentTextChanged.connect( self.sync_ddl_0 )
    #         self.ddl_0_widget.currentTextChanged.connect( self.current_text_changed )
    # # ----------------------------------
    # def get_label_widget( self, n, parent  ):
    #     """

    #     else:
    #         self.ddl_1_widget.currentTextChanged.connect( no_fun )
    #         self.ddl_0_widget.currentTextChanged.connect( no_fun )

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
            data    = i_widget.get()
            splits  = data.split("#")
            data    = f"{splits[0].strip()} "   # leave only 1 trailing space
            ret.append( data )

        return ret    # tuple of 3 arg values

    # ----------------------------------
    def set_label_text( self, lbl_text_0 = None, lbl_text_1 = None, lbl_text_2 = None  ):
        """
        save label text for get label_widget
        """
        self.dll_label_texts  = [ lbl_text_0, lbl_text_1, lbl_text_2 ]

    # -----------------------
    def zero_arg(self, ):
        """

        """
        print( f"zero_arg")

    # -----------------------
    def one_arg(self, arg_1 ):
        """

        """
        print( f"one_arg {arg_1 = }")



    # -----------------------
    def two_arg(self, arg_1, arg_2 ):
        """

        """
        print( f"two_arg {arg_1 = } {arg_2 = }")

    # -----------------------
    def conbo_currentIndexChanged(self, index ):
        """

        """
        print( f"conbo_currentIndexChanged {index}")

    # ----------------------------------
    def sync_ddl_0( self,    ):
        """
        sync when ddl_0 changes
        bind to    from self.arg_1_widget

        ?? this has a fixed widget -- so get rid of event so we can call from elsewhere !!
        arg:
            event -- not used
        """
        print( f"sync_ddl_0 " )

        return

        # if self.ignore_change_cnt:
        #     self.ignore_change_cnt     -= 1
        #     print( "sync_ddl_0 {self.ignore_change_cnt}")
        #     return

        #self.enable_changed( False)

        widget        = self.ddl_0_widget

        #rint( f"a_widget.get() {a_widget.get()}" )

        # some cases might need find index or try.....
        #dict_index     = a_widget.get()
        dict_index     = widget.currentText()

        # now for this widget
        widget         = self.ddl_1_widget

        values         = self._ddl_dict[ dict_index ]
            # what do i get I get a dict of lists, I need all the keys
        values         = list( values.keys( ) )
        widget.clear()       # delete all items from comboBox
        widget.addItems( values )


        #widget     = self.ddl_1_widget

        #rint( f"configure arg_2 with {values}" )
        #self.ddl_1_widget.configure( values = values )



        #rint( f"set value combb_2 {values[0]} type = {type(values[0])}")
        #self.ddl_1_widget.set( values[0] )

        #rint( "sync_ddl_0 need to cascade " )

        #print( "!! need to complete next")


        self.sync_ddl_1( None )

    # ----------------------------------
    def sync_ddl_1( self,    ):
        """
        sync when ddl_1 changes
        since one has changed then 2 values need to change

        """
        print( f"sync_ddl_1  " )

        # need to know the text in widget 0 so can work thru dict

        a_dict          = self._ddl_dict          # perhaps have each dll keep track of its dict?
        widget          = self.ddl_0_widget
        dict_index      = widget.currentText()
        a_dict          = a_dict[ dict_index ]
        values          = a_dict.keys()
        print( values )
        widget          = self.ddl_1_widget
        dict_index      = widget.currentText()


        #values         = dict_0[dict_index]

    # ----------------------------------
    def sync_ddl_1_bak( self,    ):
        """
        sync when ddl_1 changes

        arg:
            event__ -- not used
        """
        print( f"sync_ddl_1  " )
        #self.enable_changed( False)
        # print( "! have not set to 0 element ")
        # self.ignore_change_cnt += 1

        return

        a_widget_0      = self.ddl_0_widget
        dict_index_0    = a_widget_0.currentText()

        a_widget        = self.ddl_1_widget

        #rint( f"sync_ddl_1 a_widget.get() {a_widget.get()}" )

        # some cases might need find index or try.....
        dict_index     = a_widget.currentText()

        # now navigate our self._ddl_dict
        dict_0         = self._ddl_dict[ dict_index_0 ]
            # what do i get I get a dict of lists, I need all the keys
        values         = dict_0[dict_index]
        #rint( f"sync_ddl_1 configure  with {values}" )
        #rint( f"configure arg_2 with {values}" )
        # self.ddl_2_widget.configure( values = values )

        self.ddl_2_widget.clear()       # delete all items from comboBox
        self.ddl_2_widget.addItems( values )

        self.enable_changed( True )

        #rint( f"set value combb_2 {values[0]} type = {type(values[0])}")
         #self.ddl_2_widget.set( values[0] )
# # ----------------------------------------------------
#         widget        = self.ddl_1_widget

#         #rint( f"a_widget.get() {a_widget.get()}" )

#         # some cases might need find index or try.....
#         #dict_index     = a_widget.get()
#         dict_index     = widget.currentText()

#         # now for this widget
#         widget         = self.ddl_2_widget

#         values         = self._ddl_dict[ dict_index ]
#             # what do i get I get a dict of lists, I need all the keys
#         values         = list( values.keys( ) )
#         widget.clear()       # delete all items from comboBox
#         widget.addItems( values )




    # -----------------------------------
    def print_ddl_dict( self,   ):
        """
        what it says, read
        """
        print( self._ddl_dict )

    # -----------------------------------
    def add_to_dict ( self, key_0, key_1, list_2 ):
        """
        what it says, read
        via a mutate
        may actually work ??
        """
        old_value_0   = self._ddl_dict.get( key_0 )  # value for key 0
        if old_value_0  is None:
            self._ddl_dict[ key_0 ] = { key_1: list_2 }
        else:
            # need to merge a value into old_value_0 which is a dict in the self.... ??
            old_value_0[ key_1 ] = list_2

        #self.print_ddl_dict()

        # could return it but it is a mutate caller should know
