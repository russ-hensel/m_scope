#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purpose:


    part of my ( rsh ) library of reusable code
    a library module for multiple applications
    sometimes included with applications but not used
        as this make my source code management easier.

    Test:  see sub dir and programs where used like
        web_search

        Search:
            PlaceInGrid

Various classes to extend qt functionality
     browsers
     message frames


master in rsh_lib, gui_qt_ext

us sys path for development, then copy over file and edit for git hub

sys.path.append( "../rshlib" )
import gui_ext

AppGlobal is needed to run this,
look for links
        .parameters
        .logger
gui_qt_ext.

saved a compat version but convert this to qtpy


TEST
      /mnt/8ball1/first6_root/russ/0000/python00/python3/_projects/rshlib/rshlib_qt/test/test_gui_qt_ext.py

"""
# ---- tof


# ---- imports

from   qtpy  import QtGui
from   qtpy.QtCore import ( QDateTime,  Qt,    )


from qtpy.QtGui  import ( QCursor,
                          QTextCursor,
                          QTextDocument,
                          QAction, )

from qtpy.QtGui import QColor, QBrush
#import PyQt.QtWidgets as qtw    #  qt widgets avoid so much import below


from qtpy.QtWidgets import (
                            QApplication, QMessageBox,
                            QGridLayout,   QVBoxLayout,       QGroupBox,  QPushButton,
                            QWidget,      QLabel,     QLineEdit,  QFileDialog,
                            QCheckBox,
                            QStyledItemDelegate,

                            QTextEdit,

                             )


QCursor  =  QtGui.QCursor



import string_utils

from   app_global import AppGlobal
# for above to work need to have an AppGlobal in the dir
# where app was started, or provide another in this dir
# seems to work

import logging

logger          = logging.getLogger( )


# for custom logging level at module
LOG_LEVEL   = 5   # higher is more
NOGO        =  "That is a No Go"


# ----- style sheets  gui_qt_ext.LINE_EDIT_READ_ONLY

LINE_EDIT_READ_ONLY = (
    "QLineEdit { "
     "   background-color: #ececec; "
     "   border: 1px solid #cccccc; "
     "   border-radius: 4px; "
     "   padding: 4px; "
    " } "
      )
#  see stufdb for color by name

#---------------------
def bring_to_top( root_frame  ):
    """
    What it says, read code
    gui_ttk_ext.bring_to_top( root )
    """
    #rint( f"bring_to_top() {__name__}"  )

    # ---- ---- method one, did not work ?
    # self.root.attributes('-topmost', 1)
    # self.root.attributes('-topmost', 0)  # else it will stay on top as a pain

    # method 2
    root_frame.iconify()
    root_frame.update()
    root_frame.deiconify()

#---------------------
def minimize_gui( root_frame ):
    """
    What it says, read code
    gui.ttk_ext.minimize_gui( root )
    root frame is QMainWindow
    """
    root_frame.showMinimized()
    #rint( f"bring_to_top() {__name__}"  )
    # method 2
    #root_frame.iconify()
    #.showMinimized()
    #root_frame.update()
    #root_frame.deiconify()

#---------------------
def maximize_gui( root_frame  ):
    """
    What it says, read code
    gui.ttk_ext.minimize_gui( root )
    root_frame may be central_widget or its parent or....
    """
    root_frame.showMaximized()
    #rint( f"bring_to_top() {__name__}"  )
    # method 2
    #root_frame.iconify()
    #.showMinimized()
    #root_frame.update()
    #root_frame.deiconify()

#---------------------
def move_under_mouse( widget ):
    """
    widget right now expected to be a window
    perhaps this can be generalized
    """
    mouse_pos = QCursor.pos()
    widget.move( mouse_pos )

    widget.show()

#---------------------
class SizedMessageBoxxxx( QMessageBox ):
    def __init__(self, *args, fixed_width=500, fixed_height=300, custom_show_event, **kwargs):
        super().__init__(*args, **kwargs)
        self.fixed_size = (fixed_width, fixed_height)
        self.custom_show_event   = custom_show_event

    def showEvent(self, event):
        super().showEvent(event)
        self.custom_show_event( self, event )
            # this is injected or replaceable function
            # self twice since it is not in class


    # or a null function ( pass ) may be as effective
    def resizeEvent(self, event):
        pass    # i do not have the rectangle
        # super().resizeEvent(event)
        # if self._rect:
        #     self.resize(self._rect.size())

#---------------------
def custom_show_event( widget_self, event, rectangle,  ):
    """
    adjust with partial then pass to above
    """
    # widget_self.resize( widget_self.fixed_size )          # or self.setFixedSize(...)
    # Optional: center on screen or parent
    widget_self.setGeometry( rectangle  )

    # if widget_self.parent():
    #     widget_self.move( widget_self.parent().geometry().center() - widget_self.rect().center())
    # else:
    #     screen = QApplication.primaryScreen().geometry()
    #     widget_self.move(
    #         (screen.width() - self.width()) // 2,
    #         (screen.height() - self.height()) // 2
    #   )


#---------------------
def color_toolbar_action( toolbar, action, bg_color, text_color):
    """
    from claud
    Apply colors to a specific toolbar action

    Args:
        toolbar: QToolBar containing the action
        action: QAction to color
        bg_color: Background color (hex string)
        text_color: Text color (hex string)

    gui_qt_ext.color_toolbar_action( toolbar, action, bg_color = "#FF5555", text_color = "#FFFFFF" )
                make/find some constans for these
                color_toolbar_action(toolbar, action1, "#FF5555", "#FFFFFF")  # Red background
                color_toolbar_action(toolbar, action2, "#55FF55", "#000000")  # Green background
                color_toolbar_action(toolbar, action3, "#5555FF", "#FFFFFF")  # Blue background
    """
    if not toolbar or not action:
        print("Error: Invalid toolbar or action")
        return

    # Get the QToolButton widget associated with this action
    widget = toolbar.widgetForAction( action )

    if widget:
        stylesheet = f"""
            QToolButton {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid #888;
                border-radius: 3px;
                padding: 5px;
            }}
            QToolButton:hover {{
                background-color: {lighten_color(bg_color)};
                border: 1px solid #000;
            }}
            QToolButton:pressed {{
                background-color: {darken_color(bg_color)};
            }}
        """
        widget.setStyleSheet(stylesheet)
    #else:
        #rint(f"Warning: Could not find widget for action '{action.text()}'")

#---------------------
def lighten_color( hex_color, factor=1.2):
    """
    Lighten a hex color for hover effect"""
    try:
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r       = min(255, int(r * factor))
        g       = min(255, int(g * factor))
        b       = min(255, int(b * factor))
        return f"#{r:02x}{g:02x}{b:02x}"

    except ( ValueError, IndexError ):
        return hex_color

#---------------------
def darken_color( hex_color, factor=0.8 ):
    """Darken a hex color for pressed effect"""
    try:
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}"
    except ( ValueError, IndexError ):
        return hex_color

#---------------------
def about(  controller  ):
    """
    interfaces with controller and called back from gui
    What it says, read code
            url   =  r"coming soon not at http://www.opencircuits.com/TBD"
        __, mem_msg   = cls.show_process_memory( )
        msg  = f"{cls.controller.app_name}  version:{cls.controller.version} \n
        by Russ Hensel\n  Memory in use {mem_msg} \n
        Check <Help> or \n     {url} \n     for more info."
        messagebox.showinfo( "About", msg,  )
        #   tried ng: width=20  icon = "spark_plug_white.ico"
    gui_qt_ext.about( controller )
    """
    message_box = QMessageBox( controller.gui )
    message_box.setWindowTitle( "About this Application" )

    msg         = ( f"{ controller.app_name}  version:{ controller.app_version}"
                    f"\n  by Russ Hensel"
                    # f"\n  Memory in use {mem_msg} "
                    f"\n  Check <Help> or "
                    f"\n  {controller.app_url} \n"
                   )

    message_box.setText( msg )

    # message_box.setIcon(QMessageBox.Information)
    box_exec  = message_box.exec( )

#-----------------------------------
def error_message_box( error_text ):
    """
    this is simple, plan to extend !!
    Returns:
        None
    if not base_document_tabs.is_delete_ok():
        return
    may want to extend to position color... log
    from base_document_tabs   is_delete_ok
    gui_qt_ext.error_message_box( error_text )   # import gui_qt_ext

    """
    QMessageBox.information( AppGlobal.main_window,
                             NOGO, error_text )

# -----------------------------------
class DateFormatDelegate( QStyledItemDelegate ):
    """for table integer to date formats """

    # -----------------------------------
    def displayText(self, value, locale):

        # Assuming the integer is a Unix timestamp in seconds
        date = QDateTime.fromSecsSinceEpoch(int(value ) )
        return date.toString("yyyy-MM-dd")  # Customize format as needed
        #return super().displayText(value, locale)

# -----------------------------------
class DateTimeFormatDelegate( QStyledItemDelegate ):
    """
    for table integer to datetime formats
    gui_qt_ext.DateTimeFormatDelegate
    """

    # -----------------------------------
    def displayText( self, value, locale ):

        date_time = QDateTime.fromSecsSinceEpoch(int( value ) )

        return date_time.toString( "yyyy-MM-dd hh:mm:ss" )

# -----------------------------------
class ColoredRowDelegate( QStyledItemDelegate ):
    """ """
    def __init__(self, colored_rows = None, parent = None, color = '#FFDDC1'  ):
        """
        colored_rows   = {1, 3}  # Rows to color
        delegate       = gui_qt_ext.ColoredRowDelegate( colored_rows, self )
        view.setItemDelegate( delegate )

        # '#FFDDC1' Light orange background

        when applied can we change it either color or rows ?
             or change and reapply??

        """
        super().__init__( parent )
        self.colored_rows       = colored_rows if colored_rows is not None else set()
        self.highlight_color    = color  # or use as interface -- will it work

    # -----------------------------------
    def initStyleOption(self, option, index):
        """ """
        super().initStyleOption(option, index)

        if index.row() in self.colored_rows:
            option.backgroundBrush = QBrush( QColor( self.highlight_color ) )

        else:
            option.backgroundBrush = QBrush( QColor('#FFFFFF') )  # Default white background

# -----------------------------------
class TableModelDateTimeDelegate( QStyledItemDelegate ):
    """
    for a qabstract table model from grok, slightly modified
    """
    def __init__(self, date_column=0, parent = None):
        super().__init__(parent)
        self.date_column = date_column  # Column index with integer timestamps

    # -----------------------------------
    def displayText(self, value, locale):
        # Convert integer timestamp to datetime string for the specified column
        # if isinstance( value, int ):
        try:
            # works
            value   = int( value )
            dt      = QDateTime.fromSecsSinceEpoch(value)
            return dt.toString("yyyy-MM-dd hh:mm:ss")

            # in a line??  -- think failed
            #dt      = QDateTime.fromSecsSinceEpoch( int( value ) ).toString("yyyy-MM-dd hh:mm:ss")

        except:
            return str(value)  # Fallback if conversion fails

        return str(value)

#---------------------
class PositionMessageBox( QMessageBox ):
    def __init__( self, *args, upper_left,  **kwargs ):
        """
        the message box is opened at a position
        upper_left is a point

        """
        super().__init__(*args, **kwargs)
        self.upper_left           = upper_left

    # ---------
    def showEvent(self, event):
        super().showEvent(event)
        self.move( self.upper_left )


        # Defer geometry until after Qt finishes auto-sizing
        # QTimer.singleShot(0, self._apply_geometry)

    # def resizeEvent(self, event):
    #     super().resizeEvent(event)
    #     self.resize( self.rectangle.size() )

    # def adjustSize(self):
    #     pass

    # def _apply_geometry(self):
    #     print( "_apply_geometry" )
    #     self.setGeometry(self.rectangle)

# -----------------------------------
class CursorContext:
    """
    chat context manager
    gui_qt_ext.CursorContext   # import gui_qt_ext
         replaces base_document_tabs.CursorContext
    use         with CursorContext():
                    ...... code
    """
    # ---------------------------------
    def __enter__(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)

    # ---------------------------------
    def __exit__(self, exc_type, exc_val, exc_tb):
        QApplication.restoreOverrideCursor()

# ---------------------------------
class FileBrowseWidget( QWidget ):
    """
    where already used ??
    gui_qt_ext.FileBrowseWidget

    in stuff db
       /mnt/WIN_D/Russ/0000/python00/python3/_projects/stuffdb/file_browse.py
       but apparently not used instead code in our test

    adding to ./test

    """
    #-----------------------------
    def __init__(self, parent=None, entry_width=None):
        """
        unclear what this is or does is not a widget but
        seems to contain widgets

        for now just see stuff code.

        Args:
            parent (TYPE, optional): DESCRIPTION. Defaults to None.
            entry_width (TYPE, optional): DESCRIPTION. Defaults to None.

        Returns:
            None.

        """
        super().__init__(parent)
        self.setWindowTitle("File Browse Widget")
        self.resize(400, 100)

        if entry_width is None:
            entry_width = 100

        self.label_widget   = QLabel("Get File Name:", self)
        self.label_widget.setGeometry(10, 10, 100, 30)

        self.entry_1 = QLineEdit(self)
        self.entry_1.setGeometry(120, 10, entry_width, 30)

        self.button_2 = QPushButton("Browse...", self)
        self.button_2.setGeometry(240, 10, 80, 30)
        self.button_2.clicked.connect(self.browse)

        self.initialdir     = "./"
        self.title          = "Select file for db"
        self.filetypes      = "All Files (*)"

    #-----------------------------
    def browse(self):
        """
        what it says
        Returns:
            None.

        """
        options  = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setOptions(options)
        file_dialog.setDirectory(    self.initialdir )
        file_dialog.setWindowTitle(  self.title      )
        file_dialog.setNameFilter(   self.filetypes  )

        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            self.set_text(filenames[0])

    #--------------------
    def set_text(self, a_string):
        self.entry_1.setText(a_string)

    def get_text(self):
        return self.entry_1.text()


#---------------------------------
class DirBrowseWidget(QWidget):
    """


    """
    # ---------------------------------
    def __init__(self, parent=None, initialdir=None, browse_title=None):
        super().__init__(parent)
        self.setWindowTitle("Directory Browse Widget")
        self.resize(400, 100)

        self.label_widget = QLabel("Get Directory Name:", self)
        self.label_widget.setGeometry(10, 10, 120, 30)

        self.entry_1 = QLineEdit(self)
        self.entry_1.setGeometry(140, 10, 200, 30)

        self.button_2 = QPushButton("Browse...", self)
        self.button_2.setGeometry(350, 10, 80, 30)
        self.button_2.clicked.connect(self.browse)

        self.initialdir = initialdir if initialdir else "/"
        self.browse_title = browse_title if browse_title else "Select Directory"

    # ---------------------------------
    def browse(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks

        dir_dialog = QFileDialog()
        dir_dialog.setFileMode(QFileDialog.Directory)
        dir_dialog.setOptions(options)
        dir_dialog.setDirectory(self.initialdir)
        dir_dialog.setWindowTitle(self.browse_title)

        if dir_dialog.exec_():
            selected_dir = dir_dialog.selectedFiles()
            self.set_text(selected_dir[0])

    # ---------------------------------
    def set_text(self, a_string):
        self.entry_1.setText(a_string)

    # ---------------------------------
    def get_text(self):
        return self.entry_1.text()

#  --------
class MessageArea( QGroupBox ):
    def __init__( self ):

        """
        widget   =  gui_qt_ext.MessageArea()
    need to add or make new class to be an edit window
         get rid of buttons
         get all text programatically
         make ctrl-c -v work

    add arguments to init
    make buttons optional !!
    make disable always on !!

    message frame used in so many apps

        a_frame            = gui_qt_ext.MessageArea(    )


    # ----------- from web search -------------------------------   gui_qt_ext.MessageArea
    def _make_message_frame( self, parent,  ):
        x""
        make the message frame for user feedback
        x""
        message_widget       = gui_qt_ext.MessageArea()
        self.message_frame   = message_widget
        return message_widget



        self.message_frame = a_frame
        return a_frame

    Interface
         functions
         self.max_lines
         self.msg_text
         self.button_widgets
         do_clear_button()
         print_string()


    """
        #rint( QApplication.instance())
        super().__init__()

        # ---- build gui
        group_placer   = CQGridLayout( )
        self.setLayout( group_placer )

        #group_placer   = PlaceInGrid(  self, by_rows = False )

        copy_button = QPushButton( "Copy Text" )
        copy_button.clicked.connect( lambda: self.copy_text( ))
        group_placer.place( copy_button, rowspan = 1, columnspan = 1 )

        # Create QTextEdit widget
        text_edit = QTextEdit()
        # layout.addWidget(text_edit, 4, 0, 1, 3)  # Row 4, Column 0, RowSpan 1, ColumnSpan 3
        self.text_edit  = text_edit
        group_placer.place( text_edit, rowspan = 8, columnspan = 3 )

        widget = QPushButton( "Delete Text" )
        widget.clicked.connect( lambda: self.delete_text( ))
        widget.setMaximumWidth(150)
        #widget       = delete_button
        group_placer.new_row( )
        group_placer.place( widget, rowspan = 1, columnspan = 1 )

        insert_button = QPushButton("Insert Text")
        insert_button.clicked.connect(lambda: self.insert_text(  "Inserted Text"))
        widget        = insert_button
        group_placer.new_row( )
        group_placer.place( widget, rowspan = 1, columnspan = 1 )

        copy_selected_button = QPushButton("Copy Selected Text")
        copy_selected_button.clicked.connect(lambda: self.copy_selected_text( ))
        widget = copy_selected_button
        # layout.addWidget(copy_selected_button, 6, 0)
        group_placer.new_row( )
        group_placer.place( widget, rowspan = 1, columnspan = 1 )

        widget          = QPushButton("Clear")
        widget.clicked.connect( lambda: self.clear_text( ) )
        group_placer.new_row( )
        group_placer.place( widget, rowspan = 1, columnspan = 1 )

        widget                      = QCheckBox( "Auto Scroll")
        widget.clicked.connect( self.set_auto_scroll )
        self.auto_scroll_widget     = widget
        state                       = True
        self.auto_scroll_widget.setChecked( state )
        self.auto_scroll = state
        group_placer.new_row( )
        group_placer.place( widget, rowspan = 1, columnspan = 1 )

    # ---------------  end of button actions and class


    # ---------------------------------------
    def display_string( self, a_string, update_now = False ):
        """
        !! we may phase out for print_string  or the reverse ??
             make one call the other
        print to message area, with scrolling and
        log if we are configured for it

        parameters.gui_text_log_fn    = False  # "gui_text.log"
                                               # a file name or something false


        parameters.log_gui_text       = False # True or false to log text
        parameters.log_gui_text_level = 10    # logging level for above

        !! add parameter clear_msg = True or false

        """
        #rint(  f"MessageArea.display_string, with a_string = {a_string}")
        # return
        #   try  !!!  QTextEdit.clear()
        cursor = self.text_edit.textCursor()
        # cursor.movePosition( QTextCursor::End )
        cursor.insertText( a_string )

#         #rint( "debug for display_string")
#         if  AppGlobal.parameters.gui_text_log_fn:
#             # for now open close.... later perhaps improve
#             with open( AppGlobal.parameters.gui_text_log_fn, "a"  ) as a_file:
#                 a_file.write( a_string )   # do we need \n check
#                 #rint(   a_string )

#         if  AppGlobal.parameters.log_gui_text:
#             AppGlobal.logger.log( AppGlobal.parameters.log_gui_text_level, a_string, )

#         self.msg_text.insert( tk.END, a_string, )      # this is going wrong, why how
#         try:
#             numlines = int( self.msg_text.index( 'end - 1 line' ).split('.')[0] )
#                 # !! beware int( None ) how could it happen ?? it did this is new
#         except Exception as exception:
#         # Catch the custom exception -- !! to broad except
#             AppGlobal.logger.error( str( exception ) )
#             print( exception )
#             numlines = 0
#         if numlines > self.max_lines:
#             cut  = int( numlines/2  )    # lines to keep/remove
#             self.msg_text.delete( 1.0, str( cut ) + ".0" )
#                 # remove excess text
# #            msg     = "Delete from test area at " + str( cut )
# #            self.logger.info( msg )

#         if self.cb_scroll_var.get():
#             self.msg_text.see( tk.END )

#         if update_now:
#             AppGlobal.gui.root.update()
#             print( "!! self.root not valid here ")

    #  --------
    def print_message(self, text):
        print("Button clicked:", text)

    #--------
    def clear_text( self ):
        self.text_edit.clear()

    #  --------
    def set_auto_scroll( self ):
        """
        really set from check box
        the state you get is the new one
        """
        state           =  self.auto_scroll_widget.isChecked() # after  state has changed
        self.auto_scroll_widget.setChecked( state ) # why it does not change auto

        self.auto_scroll = state

    #-------------
    def get_plain_text(self,  ):
        """
        returns
            text in the text_edit
        """
        text_edit     = self.text_edit
        selected_text = text_edit.toPlainText()
        return selected_text
        #print(  f" copy_text -> {selected_text }" )

    #-------------
    def copy_text(self,  ):
        """
        returns
            mutates clipboard all text in the text_widget into the clipboard
            None
        """
        text_edit     = self.text_edit
        selected_text = text_edit.toPlainText()
        QApplication.clipboard().setText(selected_text)
        #rint(  f" copy_text -> {selected_text }" )

    #-------------------
    def delete_text( self,  ):
        self.text_edit.clear()

    #------------------------------
    def append_text( self, text, add_nl = True ):
        """may include new line """
        text_edit   = self.text_edit
        # self.text_edit.append( text )  adds nl at end
        text_edit.moveCursor( QTextCursor.MoveOperation.End )

        if add_nl:
            text = text + "\n"  # and cr ???
        text_edit.insertPlainText( text )

        if self.auto_scroll:
            text_edit   = self.text_edit
            # cursor      = text_edit.textCursor()
            # cursor.movePosition(cursor.Start)
            # text_edit.setTextCursor(cursor)
            text_edit.ensureCursorVisible()

    #------------------------------
    def insert_text( self,  text ):
        cursor = self.text_edit.textCursor()
        cursor.insertText(text)

    # --------------------------------
    def copy_selected_text( self, ):
        """ """
        selected_text = self.text_edit.textCursor().selectedText()
        QApplication.clipboard().setText(selected_text)
        #rint(  f" copy_selected_text -> {selected_text }" )

# -----------------------------------
class CQGridLayout( QGridLayout ) :
    """
    a custom grid layout from PlaceInGrid but this is a layout
    layout      = gui_qt_ext.CQGridLayout( col_max = 10 )

    --- next two may have been fixed
    indent is not properly handled in all the code
        needs to be anywhere go to next row

    unclear what happens when columnspan will overrun the col_max
    might experiment and offer options

    self.ix_row
    self.ix_col are port of the interface, but how does
    changing them affect last_ix_row

    """
    def __init__( self,   *, col_max = 0, indent = 0   ):
        super().__init__(  )
        self.reset( col_max = col_max, indent = indent  )

    # -----------------------------------
    def reset( self,  *, col_max = 0, indent = 0   ):
        """
        for debug may become more permanent
        grids my have enough internal state that they should
        not be reused
        """
        self.col_max        = col_max  # 0 no max
        self.ix_row         = 0
        self.ix_col         = 0
        self.indent         = indent  # an idea but what idea no implemented
        # for debug
        self.last_ix_row    = None
        self.last_ix_col    = None
        #self.last_stretch = None

        #rint( "CQGridLayout_reset================>", self )

    # -----------------------------------
    def addWidget( self,
               widget,
               ix_row       = None,
               ix_col       = None, *,
               columnspan   = 1,   # implemented
               rowspan      = 1,
               #stretch      = None,
               ):
        """
        to work like QLayouts but do ix_row, ix_col automatically
        this is preliminary
        layout.addWidget( widget, ix_row, ix_col, row_span, col_span )

        rowspan will be passed on but is not accounted for by
        self.ix_row

        """
        if ix_row is None:
            ix_row  = self.ix_row

        if ix_col is None:
            ix_col = self.ix_col

        # check if it fits

        if self.col_max and ( self.ix_col + columnspan  > self.col_max ):
            self.new_row()

        self.last_ix_row     = ix_row
        self.last_ix_col     = ix_col
        self.last_columnspan = columnspan

        # later check for nones and delta
        super().addWidget( widget, self.ix_row, self.ix_col, rowspan, columnspan )
            #  row, column, rowspan, columnspan

        # if columnspan is None: not sure what is default
        #     # make default
        #     columnspan = 1

        # this computes the next -- do we need now we have precheck ?
        self.ix_col    += columnspan
        if self.col_max and ( self.ix_col  >= self.col_max ):
            self.new_row()
            # is self.new_row better here?
            # self.ix_row    += 1
            # self.ix_col    = 0

            debug_msg       = f"addWidget__increment row {self}  "
            logging.log( LOG_LEVEL,  debug_msg, )
        # else:  # for debug
        #     pass
        #     print( self )


    # -----------------------------------
    def addLayout( self,
               layout,
               ix_row       = None,
               ix_col       = None,
               *,
               columnspan   = 1,   # implemented
               rowspan      = 1,
               #stretch      = None,
               ):
        """
        to work like QLayouts but do ix_row, ix_col automatically
        this is preliminary
        layout.addWidget( widget, ix_row, ix_col, row_span, col_span )

        rowspan will be passed on but is not accounted for by
        self.ix_row

        """
        if self.ix_row is None:
            self.ix_row  = 0

        if ix_row is None:
            ix_row  = self.ix_row

        if self.ix_col is None:  # or just in init
            self.ix_col  = 0

        if ix_col is None:
            ix_col = self.ix_col

        # check if it fits

        if self.col_max and ( self.ix_col + columnspan  > self.col_max ):
            self.new_row()

        self.last_ix_row     = ix_row
        self.last_ix_col     = ix_col
        self.last_columnspan = columnspan

        # later check for nones and delta
        super().addLayout( layout, self.ix_row, self.ix_col, ) # rowspan, columnspan )

        # if columnspan is None: not sure what is default
        #     # make default
        #     columnspan = 1

        # this computes the next -- do we need now we have precheck ?
        self.ix_col    += columnspan
        if self.col_max and ( self.ix_col  >= self.col_max ):
            self.new_row()

            debug_msg       = f"addLayout  increment row {self}  "
            logging.log( LOG_LEVEL,  debug_msg, )
        # else:  # for debug
        #     pass
        #     print( self )

    # ------------------------think bad indent-----------
    def place( self,
               a_widget,
               columnspan   = None,
               rowspan      = None,
               sticky       = None
               ):
        """
        for compat with PlaceInGrid so we can phase it out
           widget,
           ix_row       = None,
           ix_col       = None,
           *,
           columnspan   = 1,
           rowspan      = 1,
           #stretch      = None,
        """
        if columnspan is None:
            columnspan = 1

        if rowspan is None:
            rowspan = 1

        self.addWidget( a_widget, columnspan = columnspan, rowspan = rowspan )

    # ----------------------
    def get_add_parm_str( self, ):
        """
        for debugging label controls wit this
        """
        msg       = f"r{self.last_ix_row},c{self.last_ix_col} s{self.last_columnspan}"
        return msg
        #super().addWidget( widget, self.ix_row, self.ix_col )


    # -----------------------------------
    def new_row( self, delta_row = 1, indent = None ):
        """
        start a new row in col 0
        !! also for col
        """
        if indent is None:
            indent = self.indent    # or vise

        else:
            self.indent = indent

        self.ix_row     += delta_row
        self.ix_col      = indent
        debug_msg       =( f"new_row {self.ix_row = }  {self.ix_col = }")
        logging.log( LOG_LEVEL,  debug_msg, )

    #--------------------------
    def __str__( self ):
        """
        universal __str__
        """
        return string_utils.obj_to_str( self )

# -----------------------------------
class PlaceInGrid( ):
    """
    DO NOT USE IN NEW WORK PHASE OUT
    old tk comment, some applies to qt some not
    called sequentially to help layout grids in a row and column format
    columnspan=2, rowspan=2
    add columnspan to place  make it increment in direction we are moving ....??

    to do
    add column span row span -- keep delta ? delta is span in direction, but may need both ?
    add setup for stickyness ??
    tested through my use, works in my apps, but may nt even be used

    placer    = gui_qt_ext.PlaceInGrid( 99,  central_widget = a_widget, by_rows = False )
    placer.place(  a_widget, columnspan = None,   rowspan = None, sticky = None )

    Interface
        tried to use _xxx for non interface functions and var
        debug_id


      gui_qt_ext.PlaceInGrid(  a_widget )

    """
    def __init__( self,  central_widget, a_max = 0, by_rows = True  ):
        """
        and see class doc.... combine
        uses  layout a QGridLayout()
        placer = gui_qt_ext.PlaceInGrid( parent_widget, a_max, by_rows = False)
        Args:
               parent_widget  container for the widgets that this will place
                a_max, may want to change to by name and default to 0 which is unlimited
                by_rows  --- require name ?? default

        """
        self.central_widget = central_widget
        self.layout         = QGridLayout()

        if  isinstance(  central_widget,  QVBoxLayout ):  # should be more here
            self.central_widget.addLayout( self.layout )

        else:
            self.central_widget.setLayout( self.layout )

        #rint( f"PlaceInGrid __init__ central_widget.layout(){ central_widget.layout()} " )
        self.debug_id       = "default_id"  # use as part of interface
        self.max            = a_max
        self.ix_row         = 0
        self.ix_col         = 0     # ix_col   += 1 to move across one
        self.ix_col_max     = 0 # may be used by filler
        self.by_rows        = by_rows
        self.indent         = 0    # interface and set by new_row

        if by_rows:
            1/0   # droped this option
            #self.function =  self._place_down_row_

        else:
            self.function =  self._place_across_col_

    # -----------------------------------
    def addWidget( self,
               a_widget,
               columnspan   = None,
               rowspan      = None,
               sticky       = None
               ):
        """
        to work like QLayouts
        """
        self.place(
               a_widget     = a_widget,
               columnspan   = columnspan,
               rowspan      = rowspan,
               sticky       = sticky
               )

    # -----------------------------------
    def place( self,
               a_widget,
               columnspan   = None,
               rowspan      = None,
               sticky       = None
               ):
        """

        move row or column by delta grid spacing's after pacing control
        what is row span vs delta
        args:
            widget     -> the widget being placed
            columnspan -> the column span               left over from tk not implemented
            rowspan    -> the rowspan                    left over from tk not implemented
            sticky     -> temporary override of sticky via argument   left over from tk not implemented
        """
        if columnspan is None:
            columnspan = 1

        if rowspan is None:
            rowspan    = 1

        #app_global.print_debug( f"row,co = {self.ix_row}, {self.ix_col}" )
        self.function( a_widget,  columnspan = columnspan, rowspan = rowspan, sticky = sticky )

    # -----------------------------------
    def place_filler( self,  stretch   = 1, widget = None  ):
        """
        place a filler widget that will stretch
        filler is layed out in the central_widget layout ?
        need to fix for widget = None
        """
        #rint( f"&&&&&&&&&& place_filler {self}")

        widget          = QWidget()
        widget          = QGroupBox( f"filler {self.debug_id}" )   # just for debugging

        # which of next ??
        ix_col_stretch  = self.ix_col_max + 1
        ix_col_stretch  = self.ix_col + 1

        self.layout.setColumnStretch( ix_col_stretch, stretch )
        #rint( f"-------- end place filler  ----- col >{ix_col_stretch}<  row >{self.ix_row}< ---- {stretch}-----")
        # seems keywords not allowed in addWidget, just by position
        self.layout.addWidget(  widget,
                                self.ix_row,
                                ix_col_stretch ,
        # column_span,       # columnSpan -1, then the widget will extend to the
                            #     bottom and/or right edge, respectively.
        # row_span,          # rowSpan

        #1,    #Alignment or flag  Qt.Alignment()]]])
            # is it a list ? The alignment is specified by alignment .
            #The default alignment is 0, which means that the widget fills the entire cell.
                                )



    # -----------------------------------
#    delta_row_col( delta_row, delta_col )
#    add a span argument
    # -----------------------------------
    def new_column( self, delta = 1,  ):
        """
        start a new column in row 0
        for going down columns not across

        """
        self.ix_row     = 0
        self.ix_col     += delta

    # -----------------------------------
    def new_row( self, delta_row = 1, indent = None ):
        """
        start a new row in col 0
        !! also for col
        """
        if indent is None:
            indent = self.indent    # or vise versa
        else:
            self.indent = indent
        self.ix_row     += delta_row
        self.ix_col      = indent

        # -----------------------------------
    def dwn_and_back( self, delta_row = 1 ):
        """
        just an idea
        for now just us direct manipulation of ix_row, ix_col
        go dwn row and back column
        to set up directly below last placement
        delta_row = 1 !! add this
        set up for next placer, then will need a self.ix_row     -= 1
        """
        self.ix_row     += 1
        self.ix_col     -= 1

    # -----------------------------------
    def set_row( self, row,  ):
        """
        what if beyond max
        """
        self.ix_row = row

    # -----------------------------------
    def set_col( self,  col ):
        """
        what it says, why not just the property

        """
        self.ix_col = col

    # -----------------------------------
    def _place_across_col_( self, a_widget, *, columnspan,  rowspan, sticky, ):
        """
        # layout.addWidget(text_edit, 4, 0, 1, 3)  # Row 4, Column 0, RowSpan 1, ColumnSpan 3
        what it says
        one of the value intended for self.function
        args:
            widget     -> the widget being placed
            columnspan -> the column span
            rowspan    -> the rowspan
            sticky     -> temporary override of sticky via argument
        """
        #rint( f"_place_across_col_ row = {self.ix_row} col = {self.ix_col}"  )
        # defaulting should be done in place
        # if columnspan is None:
        #     columnspan = 1

        # if rowspan is None:
        #     rowspan = 1

        # probably wrong but not using sticky
        if sticky is None:
            self.sticky = sticky

        #rint( f"_place_across_col_ ({self.ix_col}, {self.ix_row})"
        #                               f"columnspan = {columnspan}" )
        #rint( f"for {self.debug_id} placing   {a_widget}  at {self.ix_col}, row {self.ix_row}")
        #	addWidget(QWidget *widget, int stretch = 0, Qt::Alignment alignment = Qt::Alignment())

        self.layout.addWidget( a_widget,
                               self.ix_row,
                               self.ix_col,
                               rowspan,
                               columnspan,
                               )
        # ---- code that may be useful?
        # self.gridLayout.addWidget(textEdit1, 0, 0)
        # self.gridLayout.addWidget(textEdit2, 1, 1)
        # self.gridLayout.addWidget(textEdit3, 0, 1)
        # self.gridLayout.setColumnStretch(0, 1)
        # self.gridLayout.setColumnStretch(1, 3)
        # self.gridLayout.setRowStretch(0, 3)
        # self.gridLayout.setRowStretch(1, 1)



        # self.layout.addWidget( a_widget,
        #                        self.ix_row,
        #                        self.ix_col,
        #                        rowspan,              # streah
        #                        # sticky,  #  Qt.AlignCenter,       # alignment ??    Qt.AlignCenter works but makes a mess
        #                        )

        self.ix_col         += columnspan
        self.ix_col_max      = max( self.ix_col_max, self.ix_col )
        if ( self.max > 0  ) and ( self.ix_col >= self.max ):
            #rint( f"hit max row {self.max}"  )
            self.new_row()

        #rint("_place_across_col_",  self.ix_row, self.ix_col  )
        #rint( f"end placing   self = {self}  ") 2023-08-03 10:18:53

    # -----------------------------------
    def __str__( self,   ):
        """
        what is says, read, for debugging

        """
        a_str = f"/n>>>>>>>>>>* __str__ for PlaceInGrid  debug id =  {self.debug_id} * <<<<<<<<<<<<"
        a_str = f"{a_str}\n   ix_row                 {self.ix_row }"
        a_str = f"{a_str}\n   ix_col                 {self.ix_col }"

        a_str = f"{a_str}\n   ix_col_max             {self.ix_col_max}"

        #a_str = f"{a_str}\n   function               {self.function}"
        # a_str = f"{a_str}\n   xxx        {self.xxx}"
        return a_str


# ---- eof
