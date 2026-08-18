# -*- coding: utf-8 -*-
# ---- tof
""""
Purpose:
    object inspector based on wat
    but running in a qt window


Status:
    draft but useful
    also see help
    some todos

        improve layout
        clean code

    ...

References:

wat-inspector · PyPI
https://pypi.org/project/wat-inspector/

GitHub - igrek51/wat: Deep inspection of Python objects
https://github.com/igrek51/wat

WAT Inspector - Nuclear
https://nuclear-py.readthedocs.io/en/master/inspect/

You can call wat.modifiers / foo with the following modifiers:

    .short or .s to hide the attributes (variables and methods inside the object)
    .dunder to display dunder attributes (starting with __)
    .code to reveal the source code of a function, method, or class
    .long to show non-abbreviated values and docstrings
    .nodocs to hide documentation for functions and classes
    .caller to show how and where the inspection was called (works in files, not REPL)
    .all to include all available information
    .ret to return the inspected object
    .str to return the output string instead of printing it
    .gray to disable colorful output in the console



"""

# ---- imports

import adjust_path

import dis
import inspect
import io
import pprint
import subprocess
import sys
import traceback
from functools import partial
from pprint import pprint as pp
from subprocess import PIPE, STDOUT, Popen, run

import info_about


#print( f"{info_about.INFO_ABOUT =}")



FIF       = info_about.INFO_ABOUT.find_info_for



import wat
from PyQt5 import QtGui
from PyQt5.QtCore import QDate, QDateTime, QModelIndex, Qt, QTimer
from PyQt5.QtGui import QTextCursor, QTextDocument
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
                             QDialog,
                             QGridLayout,
                             QGroupBox,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QListWidget,
                             QListWidgetItem,
                             QMainWindow,
                             QMenu,
                             QMessageBox,
                             QPushButton,
                             QRadioButton,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

import info_about


# ---- module instances

a_wat_inspector         = None
go                      = None    # dialog.setup_go
display_wat             = None
testing                 = True


# ---- a few parameters for you

try:
    import parameters
    my_parameters = parameters.Parameters()

except:
    my_parameters = None

if my_parameters is None:

    TEXT_EDITOR    = "gedit"

else:
    TEXT_EDITOR    = my_parameters.text_editor


# -----------------------
def get_traceback_list( msg = "get_traceback_list", print_it = True ):
    """
    get_traceback_list()

    """
    stop_text = "main.py"

    #stop_text  File "/mnt/WIN_D/Russ/0000/python00/python3/_projects/rshlib/debug_util.py", line 171, in call_tbl

    keep = True
    short_list  = [">>>>>>>>>>>>>see what inspector instead get_traceback_list<<<<<<<<<<<<<<<<<<<<<<"]
    for i_item in reversed( traceback.format_stack() ):

        if keep:
            short_list.append( i_item )

            if stop_text in i_item:
                print( "stop ---------------------------------------")
                keep = False
    short_list.append( msg )
    short_list.append( ">>>>>>>>>>>>>get_traceback_list<<<<<<<<<<<<<<<<<<<<<<" )

    short_list    = list( reversed( short_list ) )
    if print_it:
        for i_item in short_list:
            print( i_item )

    return short_list

# ------------------------------------
class WatWindow( QDialog  ):
    """
    window for the wat inspector
    """
    # ------------------------------------------
    def __init__(self,  app,  parent = None ):
        """
        the usual
        """
        super().__init__( parent )

        self._build_gui()

        msg   = "Wat inspector"
        self.setWindowTitle( msg  )

        self.last_get_wat_str_obj   = None

        if my_parameters is None:
            qt_xpos             = 50
            qt_ypos             = 50
            qt_width            = 1200
            qt_height           = 600

        else:
            qt_xpos             = my_parameters.wat_qt_xpos
            qt_ypos             = my_parameters.wat_qt_ypos
            qt_width            = my_parameters.wat_qt_width
            qt_height           = my_parameters.wat_qt_height

        self.setGeometry(  qt_xpos,
                           qt_ypos ,
                           qt_width,
                           qt_height  )

        self.last_position = 0

    # ------------------------------------------
    def _build_gui( self, ):
        """
        what it says, read?
        """
        # self._build_menu() some issues here

        layout          = QVBoxLayout( self )
        self.layout     = layout

        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout )

        # ---- msg_label
        widget          = QLabel( "msg goes here " )
        self.msg_label  = widget
        row_layout.addWidget( widget,  )

        # ----
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout )

        widget        = QPushButton( "Where" )
        widget.clicked.connect(  self.do_where_am_i )
        row_layout.addWidget( widget,   )

        # ---- Cust Inspect
        widget          = QPushButton( "Cust Inspect" )
        widget.clicked.connect(         self.do_info_about )
        row_layout.addWidget( widget,   )

        # ---- Cust Inspect
        widget          = QPushButton( "Get Super" )
        widget.clicked.connect(         self.do_get_super )
        row_layout.addWidget( widget,   )

        # ---- Obj Help
        widget          = QPushButton( "Obj Help" )
        widget.clicked.connect(         self.do_type_help )
        row_layout.addWidget( widget,   )

        # ---- Obj Help
        widget          = QPushButton( "Obj Source" )
        widget.clicked.connect(         self.get_source_code )
        row_layout.addWidget( widget,   )

        # ---- eval
        widget          = QPushButton( "Eval" )
        widget.clicked.connect(         self.do_eval )
        row_layout.addWidget( widget,   )

        widget              =  QLineEdit( " 1 + 1 " )
        self.eval_widget    = widget
        row_layout.addWidget( widget,   )

        row_layout      = QHBoxLayout()
        layout.addLayout( row_layout )

        widget              = QLabel( "Locals" )
        row_layout.addWidget( widget,   )

        widget              = QLabel( "Globals" )
        row_layout.addWidget( widget,   )

        # ----new row
        row_layout      = QHBoxLayout(   )
        layout.addLayout( row_layout )

        widget              = QListWidget(    )
        self.local_widget   = widget
        #widget.setGeometry( 50, 50, 200, 200 )
        widget.itemClicked.connect( self.do_inspect_clicked_local )
        row_layout.addWidget( widget,   )

        # ---- globals
        widget              = QListWidget(    )
        self.global_widget  = widget
        #widget.setGeometry( 50, 50, 200, 200 )
        widget.itemClicked.connect( self.do_inspect_clicked_global )
        row_layout.addWidget( widget,   )

        row_layout      = QHBoxLayout()
        layout.addLayout( row_layout )

        # ---- text edit
        widget           = QTextEdit()
        self.text_edit      = widget
        row_layout.addWidget( widget,   )

        # ---- bottom and buttons
        button_layout           = QHBoxLayout()
        layout.addLayout( button_layout,    )

        widget                  = QLineEdit()
        self.line_edit          = widget
        widget.setPlaceholderText("Enter search text")
        button_layout.addWidget( widget, )

        # Buttons
        widget                  = QPushButton("Down")
        self.down_button        = widget
        widget.clicked.connect(self.search_down)
        button_layout.addWidget( widget,   )

        widget           = QPushButton("Up")
        self.up_button   = widget
        widget.clicked.connect(self.search_up)
        button_layout.addWidget( widget,   )

        button_layout           = QHBoxLayout()
        layout.addLayout( button_layout,     )

        # ---- next bottom layout
        button_layout           = QHBoxLayout()
        layout.addLayout( button_layout,      )
        chat = """
        In a QComboBox, there isn't a direct signal equivalent to returnPressed like in QLineEdit. However, you can achieve similar behavior depending on what you're trying to accomplish:

    Detect when the user presses Enter while editing the text
    If your QComboBox is editable, you can use the lineEdit() method to access the embedded QLineEdit and connect its returnPressed signal.
    combo_box = QComboBox()
combo_box.setEditable(True)
widget.lineEdit().returnPressed.connect(your_function)


"""
        # ---- Filters
        widget                  = QComboBox()
        self.filter_widget      = widget
        widget.setEditable( True )
        widget.lineEdit().returnPressed.connect( self.filter ) # setEditable first
        #widget.setPlaceholderText( "Enter filter text" )
        button_layout.addWidget( widget, )

        values    =  [ "def", "class"]
        for value in values:
            #item = QListWidgetItem( value )
            widget.addItem( value )

        widget                  = QPushButton("Filter Beginning of Line")
        #self.down_button        = widget
        widget.clicked.connect( self.filter )
        button_layout.addWidget( widget,   )

        # ---- next bottom layout
        button_layout           = QHBoxLayout()
        layout.addLayout( button_layout,    )

        # ---- QListWidget
        widget                  = QComboBox(    )
        self.filter_widget_sil  = widget
        widget.setEditable( True )
        widget.lineEdit().returnPressed.connect( self.filter_sil )
        #widget.setGeometry( 50, 50, 200, 200 )
        # widget.setPlaceholderText( "Enter filter text" )
        button_layout.addWidget( widget, )

        values    =  [ "height",
                       "width",
                       "size",
                       "action",
                       "event",
                       "index",
                       "count"
                      ]
        for value in values:
            #item = QListWidgetItem( value )
            widget.addItem( value )

        # ---- "Filter SIL"
        widget                  = QPushButton("Filter Somewhere in Line")
        #self.down_button        = widget
        widget.clicked.connect( self.filter_sil )
        button_layout.addWidget( widget,   )

        # ---- another button layout
        button_layout           = QHBoxLayout()
        layout.addLayout( button_layout,     )

        a_widget                = QPushButton("Append to File")
        self.save_button        = a_widget
        a_widget.clicked.connect(         self.write_file )
        button_layout.addWidget( a_widget )

        a_widget                = QPushButton("Edit File")
        self.save_button        = a_widget
        a_widget.clicked.connect(         self.edit_file )
        button_layout.addWidget( a_widget )

        a_widget                = QPushButton("Help")
        self.save_button        = a_widget
        a_widget.clicked.connect(         self.open_general_help )
        button_layout.addWidget( a_widget )

        a_widget                = QPushButton("OK")
        self.save_button        = a_widget
        a_widget.clicked.connect(   self.do_ok )
        button_layout.addWidget( a_widget )

    # ------------------------------------
    def _build_menu( self,  ):
        """
        what it say
            may not be able to have a menu bar on this type of widget
        """
        menubar         = self.menuBar()
        self.menubar    = menubar

        # a_menu.addSeparator()

        # ---- Help
        menu_help       = menubar.addMenu( "Help" )

        action          = QAction( "README.md...", self )
        connect_to      = partial( self.open_txt_file, "README.md" )
        action.triggered.connect( connect_to )
        menu_help.addAction( action )

        action          = QAction( "General Help...", self )
        connect_to      = partial( self.open_txt_file, "watt_inspector_help.txt" )
        action.triggered.connect( connect_to )
        menu_help.addAction( action )

        action          = QAction( "Developer Notes...", self )
        connect_to      = partial( self.open_txt_file, "readme_rsh.txt" )
        action.triggered.connect( connect_to )
        menu_help.addAction( action )

    #-------
    def open_general_help( self,   ):
        """
        what it says read:
        """
        doc_name           = "watt_inspector_help.txt"
        ex_editor          = TEXT_EDITOR
        proc               = subprocess.Popen( [ ex_editor, doc_name ] )

    # ------------------------------------------
    def do_eval( self,    ):
        """
        what it says, read?
        """
        do_wat      = True
        code        = self.eval_widget.text()
        try:
            result   = eval( code, self.globals, self.locals )

        except Exception as an_except:
            msg     = f"a_except         >>{an_except}<<  type  >>{type( an_except)}<<"
            print( msg )

            msg     = f"an_except.args   >>{an_except.args}<<"
            print( msg )

            s_trace = traceback.format_exc()
            msg     = f"format-exc       >>{s_trace}<<"
            print( msg )

            result   = "got exception "
            do_wat   = False

        if do_wat:
            main_text   = self.get_wat_str(  result )
            title        = f"Eval -> {code}"

        else:
            title       = f"Eval -> {code}"
            main_text   = s_trace

        self.display_text( title = title, main_text = main_text )

    # ------------------------------------------
    def do_info_about( self ):
        """
        what it says
        """
        #main_text   = self.info_about.get_info( self.last_get_wat_str_obj , msg = "what about it " )
        main_text   = FIF( self.last_get_wat_str_obj, msg = "what about it " )

        self.display_text( title = "info_about", main_text = main_text )

    # ------------------------------------------
    def get_source_code( self, ):
        """
        It does not work for built-in functions, classes, or objects defined interactively.
        Dynamic Objects: If the object is dynamically created
        (e.g., using exec or lambda), inspect.getsource() might not work.
        """
        # or consider ( or both? )
        self.get_source_code_eval()
        return

        # --- return above ?
        try:
            # Retrieve the source code of the object
            obj_type     = type( self.last_get_wat_str_obj )
            source_code  = inspect.getsource( obj_type )

        except Exception as e:
            source_code  =   f"Could not retrieve source { obj_type = } code due to exception {e = }"

        self.display_text( title = "Source Code", main_text = source_code )

    # ------------------------------------------
    def get_source_code_eval( self, ):
        """
        suggested by chat that it might work were direct code fails,
        seems a bit dubious
        """
        try:
            # Retrieve the source code of the object
            obj_type     = type( self.last_get_wat_str_obj )
            code         = "inspect.getsource( obj_type ) "
            source_code  = eval( code, globals(), locals() )

        except Exception as e:
            source_code  =   f"Could not retrieve source { obj_type = } code due to exception {e = }"

        self.display_text( title = "Source Code", main_text = source_code )

    # ------------------------------------------
    def do_type_help( self ):
        """
        get help for the obect
        """
        help_text     = self.get_help_as_string( self.last_get_wat_str_obj )

        self.display_text( title = "Object Help", main_text = help_text )

    # ------------------------------------------
    def do_get_super( self ):
        """
        get superclasses
        print([cls.__name__ for cls in C.__mro__])
        # Output: ['C', 'B', 'A', 'object']

        class A:
            pass

        class B(A):
            pass

        class C(B):
            pass

        # List all superclasses of C
        print(C.__mro__)
        # Output: (<class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>)

        """
        # List all superclasses of C
        super_text   = inspect.getmro( type( self.last_get_wat_str_obj )  )
        super_text   = [ str( i_line ) for i_line in super_text ]
        super_text   = "\n".join( super_text )

        # Output: (<class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>)

        self.display_text( title = "Super Classes", main_text = super_text )

    # ------------------------------------------
    def get_help_as_string( self, obj ):
        """
        what it says
        """
        obj_type = type(obj)

        try:
            # Capture the help output
            help_output    = io.StringIO()
            sys.stdout     = help_output  # Redirect stdout to capture help()
            help( obj_type )
            help_text      = help_output.getvalue()
        except:
            pass
            help_text   = "Sorry we got an exception "
        finally:
            sys.stdout = sys.__stdout__

        return help_text

    # ------------------------------------------
    def do_test( self ):
        """
        """
        main_text   = self.info_about.get_info( self.last_get_wat_str_obj , msg = "what about it " )

        self.display_text( title = "info_about", main_text = main_text )

    # ------------------------------------------
    def do_where_am_i( self ):
        """
        """
        print(f"where_am_i   {''}")
        widget              = self.text_edit
        widget.clear()
        debug               = get_traceback_list()
        main_text           = "\n".join( get_traceback_list() )
        title               = "Where in the code are you:"

        self.display_text( title = title, main_text= main_text )

    # ------------------------------------------
    def setup_go(   self,
                    *,

                    a_locals       = None,
                    a_globals      = None,
                    msg            = "no message" ):
        """
        what it says.
        """
        #rint( f"setup_go with {msg = } " )

        self.msg_label.setText( msg )
        self.setup( None,  a_locals, a_globals   )
        #self.do_inspect( inspect_me )
        self.show()
        # print( "next app exec can we see if already running?")
        # self.app.exec_()
        # print( "after  app exec can we see if already running?")

    # ------------------------------------------
    def setup( self, inspect_me = None,  a_locals = None,  a_globals = None ):
        """
        what it says.
        """
        a_locals             =  {a_key: a_value for a_key, a_value in sorted(
                                 a_locals.items(),  key = lambda item: item[0]) }

        a_globals            =  {a_key: a_value for a_key, a_value in sorted(
                                 a_globals.items(), key = lambda item: item[0]) }

        self.locals          = a_locals
        self.globals         = a_globals

        if a_locals:
            widget      = self.local_widget
            widget.clear()
            values      = [ i_key for i_key in a_locals.keys() ]
            for value in values:
                item = QListWidgetItem( value )
                widget.addItem( item )
                index_to_select = 0
                widget.setCurrentRow( index_to_select )

        if a_globals:
            widget      = self.global_widget
            widget.clear()
            values      = [ i_key for i_key in a_globals.keys() ]

            for value in values:
                item = QListWidgetItem( value )
                widget.addItem( item )
                index_to_select = 0
                widget.setCurrentRow(index_to_select)

    # ------------------------------------------
    def do_inspect_clicked_global( self, item  ):
        """
        what it says
        """
        widget              = self.global_widget
        # row                 = widget.row( item )

        text               = item.text()
        i_object           = self.globals[ text ]

        title         = f"Global -> {text}"
        main_text     = self.get_wat_str( i_object )
        self.display_text( title = title, main_text = main_text )

    # ------------------------------------------
    def do_inspect_clicked_local( self, item  ):
        """
        what it says.
        """
        widget              = self.local_widget
        row = widget.row( item )

        text               = item.text()
        i_object           = self.locals[ text ]

        title         = f"Local -> {text}"
        main_text     = self.get_wat_str( i_object )
        self.display_text( title = title, main_text = main_text )

    # ---------------------
    def filter_sil( self ):
        """
        filter the lines based on text at start:
            ignore blank space
            case insensitive
        """
        #print( self.filter_widget_sil.currentText() )

        filter_text = self.filter_widget_sil.currentText().casefold()
        all_text    = self.text_edit.toPlainText()
        splits      = all_text.split( "\n" )

        new_lines   = []

        for i_split in splits:
            i_test    = i_split.strip()
            if  filter_text   in  i_test.casefold():
                new_lines.append( i_split )

        #rint( new_lines )
        new_text       = "\n".join( new_lines )
        self.display_text( f"Results filtered on {filter_text}", new_text )

    # ---------------------
    def filter( self ):
        """
        filter the lines based on text at start:
            ignore blank space
            case insensitive
        """
        filter_text = self.filter_widget.currentText().casefold()
        all_text    = self.text_edit.toPlainText()
        splits      = all_text.split( "\n" )

        new_lines   = []

        for i_split in splits:
            i_test    = i_split.strip()
            if i_test.casefold().startswith( filter_text ):
                new_lines.append( i_split )

        #rint( new_lines )
        new_text       = "\n".join( new_lines )
        self.display_text( f"Results filtered on {filter_text}", new_text )

    #  --------
    def copy_all_text( self, text_edit ):
        """
        what it says
            copy into clipboard
        """
        # Save current cursor position
        cursor = text_edit.textCursor()
        original_position = cursor.position()

        text_edit.selectAll()
        text_edit.copy()   # goed to clipboard
        all_text = self.text_edit.toPlainText()

        # Restore cursor
        cursor.setPosition(original_position)
        text_edit.setTextCursor(cursor)
        return  all_text

    # ------------------------------------------
    def write_file( self,   ):
        """
        read it
        !! add the message and some seperation .. other stuff ?
        """
        my_text    = self.copy_all_text( self.text_edit )

        file_name  = "./wat_inspector_out.txt"
        with open( file_name, 'a') as a_file:    # a will append so file should be deleted time to time "w" will be for write no append ?
            a_file.write( my_text)     # f"{i_line}\n" )

    # ------------------------------------------
    def edit_file( self,   ):
        """
        read it
        """
        file_name           = "./wat_inspector_out.txt"
        ex_editor           = TEXT_EDITOR
        proc                = subprocess.Popen( [ ex_editor, file_name ] )

    # ------------------------------------------
    def inspect_object( self, an_object  ):
        """
        what it says, read?
        output result to text_edit widget
        """
        #rint( "inspect_object >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        #print( f"i_object { self.inspect_me = }   {type( self.inspect_me ) = }")
        widget              = self.text_edit
        widget.clear()
        #self.inspect_me     = inspect_me
        ex_text             = self.get_wat_str( an_object )
        cursor              = widget.textCursor()

        ex_text    = f"inspect_object { '' }: \n {ex_text}"
        cursor.insertText( ex_text )

        cursor.movePosition(QTextCursor.Start)   # .End
        widget.setTextCursor(cursor)

    # --------------------------
    def get_wat_str( self,  obj, options_dict = None ):
        """
        get the string from wat
        """
        msg      = wat( obj, str = True, gray = True )

        self.last_get_wat_str_obj  = obj

        return msg

    def display_text( self, title = "no_title_fix", main_text = "this_sis_the_main_text" ):
        """
        what it says, read
            leave cursor at top
        """
        full_text           = f"{title}\n\n{main_text}"

        widget              = self.text_edit
        widget.clear()
        #self.inspect_me     = inspect_me

        cursor              = widget.textCursor()

        cursor.insertText( full_text )

        cursor.movePosition(QTextCursor.Start)   # or .End
        widget.setTextCursor( cursor )

    # ---------------------
    def search_down(self):
        """
        search for text
            case insensitive
        """
        search_text = self.line_edit.text()
        if search_text:
            cursor = self.text_edit.textCursor()
            cursor.setPosition( self.last_position )
            found = self.text_edit.find(search_text)

            if found:
                self.last_position = self.text_edit.textCursor().position()
            else:
                # Reset position if end is reached and no match
                self.last_position = 0

    # ---------------------
    def search_up(self):
        search_text = self.line_edit.text()
        if search_text:
            cursor = self.text_edit.textCursor()
            cursor.setPosition( self.last_position )
            # Use QTextDocument.FindBackward for backward search
            found = self.text_edit.find(search_text, QTextDocument.FindBackward)

            if found:
                self.last_position = self.text_edit.textCursor().position()
            else:
                # Reset position if start is reached and no match
                self.last_position = self.text_edit.document().characterCount()

    #-------
    def open_txt_file( self, file_name  ):
        """
        what it says
        """
        proc               = subprocess.Popen( [ TEXT_EDITOR, file_name ] )

    def do_ok( self ):
        """
        close out window
        """
        self.accept()

# ------------------------------------
class WatInspector(   ):
    """
    main class for the inspector basically to create the window
    """
    # ------------------------------------------
    def __init__(self,  app,  parent = None ):
        """

        """
        global    display_wat
        global    app_for_wat
        global    go
        global    a_wat_inspector

        a_wat_inspector      = self
        go                   = self.create_window

        self.last_get_wat_str_obj  = None

        self.app            = app

        self.wat_window     = None    # not sure which kind to use
        self.parent         = parent  # parent may be a function use parent_window
        self.parent_window  = parent

    # --------------------------
    def create_window( self,  *,

                              a_locals   = None,
                              a_globals  = None,
                              msg        = None ):

        """ """




        self.window    = WatWindow( self.app )  # is necessary ??
        # self.window.show( )
        self.window.setup_go(
                                a_locals   = a_locals,
                                a_globals  = a_globals,
                                msg        = msg, )

        self.app.exec_()

# -----------------
def run_display_wat():
    """
    example run/sanity test
    """
    app         = QApplication(  [] )  # Create the QApplication instance

    a_wat_inspector  = WatInspector( app  )

    a_local_list    = [ 1,2,3,5 ]

    a_wat_inspector.create_window(

              a_locals   = locals(),
              a_globals  = globals(),
              msg        = "my message" )




# --------------------
if __name__ == "__main__":
    #----- for running examples
    run_display_wat()



"""

Scratch text:


-


"""

# ---- eof






