#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# ---- tof
"""
/mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib/rshlib_qt/text_edit_ext.py
Created on Fri Jan 10 16:32:00 2025
text edit extensions

        features to add

            have it created the edit need method
                 for it and change the inti
                 _obj   = TextEditExt( parameters )
                  self.text_edit = TextEditExt.build_text_edit()

                  then build other stuff

            block indent and out-dent

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

text_edit_ext.    ( )


"""
# ---- imports

import os
#from   subprocess import Popen
from collections import defaultdict

# ---- Qt

from qt_compat import QApplication, QAction, exec_app, qt_version
from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox

from PyQt import QtCore
from PyQt.QtGui import QIntValidator, QStandardItem, QStandardItemModel, QTextCursor
from PyQt.QtCore import QDate, QModelIndex, Qt, QTimer, pyqtSlot
from PyQt.QtGui import  QTextDocument

#from PyQt.QtGui import ( QAction, QActionGroup, )

from PyQt.QtWidgets import (
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDateEdit,
                             QDockWidget,
                             QFileDialog,
                             QFrame,
                             QGridLayout,
                             QHBoxLayout,
                             QInputDialog,
                             QLabel,
                             QLineEdit,
                             QListWidget,
                             QMainWindow,
                             QMdiArea,
                             QMdiSubWindow,
                             QMenu,
                             QMessageBox,
                             QPushButton,
                             QSpinBox,
                             QTableView,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)

import webbrowser
import logging

import platform
import subprocess
import string_utils


# ---- local imports
from app_global import AppGlobal
import exec_qt      #

STUFF_DB            = None  # may be monkey patched in
                            # this wold be the app
                            # STUFF_DB.main_window may be what you want
                            # go_active_sub_window_func

logger              = logging.getLogger( )
LOG_LEVEL           = 10   # higher is more

MARKER              = ">>"
EXEC_RUNNER         = None  # setup below
# TEXT_EXT            = None
SCAN_LINES          = 100

TEXT_EDIT_EXT       = None

# # !! delete
# KEY_DICT    = { "sys":      "system",
#                 "system":    "system",
#                 "subsys":    "sub_system",
#                 "name": "name",
#                 "id": "id",

#                 }
#does order matter
REPLACE_LIST    = [ ( "*>url ",   ">>url " ),   # note deliberate space
                    ( "*>url0 ",  ">>url " ),
                    ( "*>shell ",  ">>shell " ),
                    ]


class TextEditExt( ):
    """
    is this obsolete seems to be overlap with custom widgets extenions see mixin
    About this class.....
    self.text_edit_ext_obj         = text_edit_ext.TextEditExt( AppGlobal.parameters, entry_widget)
    """
    #----------- init -----------
    def __init__( self, parameters, text_edit ):
        """
        Usual init see class doc string
        """
        # this is the constructor run when you create
        # like  app = AppClass( 55 )
        self.parameters       = parameters
        self.text_edit        = text_edit
        self.shell_ext        = ShellExe()  # or change to run by import
        self.prior_text       = ""
        self.last_position    = 0
        self.idle_exe         = IdleExe()
        self.search_line_edit  = None    # set later

        msg   = ( "------------------------ monkey_patch_here reexamine this--------------------------" )
        logging.error( msg )

        text_edit.text_edit_ext_obj  = self
            # create on first use?
        global    TEXT_EDIT_EXT
        if TEXT_EDIT_EXT is None:
            TEXT_EDIT_EXT = self
        else:
            msg   = ( f"second instance of TextEditExt created move all methods in this object ?  {1  = }  ")
            logging.error( msg )

        self.set_custom_context_menu( text_edit )

    #----------------------------
    def foo( self ):
            # Example function to be called from context menu
            msg   = ("Foo action triggered!")
            print( msg )


    # ------------------------------------------
    def set_search_line_edit(self, search_line_edit ):
        """

        """
        self.search_line_edit  = search_line_edit


    # ------------------------------------------
    def get_snippet_ddl_values(self):
        """
        get the list of drop-down value from the
        parameter templates

        """
        values              = []
        text_templates      = self.parameters.text_snippets
        for i_key, i_value in text_templates.items( ):
            values.append( i_key )

        return values

    # ---------------------------------
    def get_template_by_key( self, key ):
        """
        what it says
            when a drop-down needs a text item

        """
        text_templates      = self.parameters.text_snippets
        text                = text_templates[ key ]

        return text

    # ---------------------------------
    def build_up_template_widgets( self,   ):
        """
        what it says
            perhaps we should change to create
            and even return its button ??
            ddl_widget,  ddl_button_widget  =    self.txt_....build_up_template_widgets
        """
        #self.text_edit_ext_obj.set_up_widget( widget )
        # ---- combo
        widget              = QComboBox()
        self.ddl_widget     = widget
        #self.text_edit_ext_obj.set_up_widget( widget )
        values              = self.get_snippet_ddl_values()
        widget.addItems( values )
        widget.setCurrentIndex( 0 )
        widget.setMinimumWidth( 200 )

        # # these work but in some case seem only to work with a lambda
        # widget.currentIndexChanged.connect( self.combo_currentIndexChanged )
        # widget.currentTextChanged.connect(  self.combo_currentTextChanged  )
        #widget.currentTextChanged.connect(self.current_text_changed)

        # ---- button
        label                   = "Paste Snippet"
        widget                  = QPushButton( label )
        self.ddl_button_widget  = widget
        #connect_to         = functools.partial( text_edit_ext.qt_exec, entry_widget )
        connect_to         = self.paste_snippet
        widget.clicked.connect( connect_to )

        return ( self.ddl_widget, self.ddl_button_widget )

    #-----------------------------------
    def paste_snippet( self, ):
        """
        what it says
        """
        key    = self.ddl_widget.currentText( )
        text   = self.get_template_by_key( key )
        #rint( "this is the text we need to paste")
        #rint( text )
        self.insert_text_at_cursor( text )

    #-----------------------------------
    def smart_paste_clipboard( self, ):
        """
        what it says

        consider strip out tabs....
        detect line contentns and prefix with >> ...
        string_utils.begins_with_url( a_string )

        may want to make more advanced, look at file extension
        .txt  .py????

        /home/russ/anaconda.sh

         ~/russ/anaconda.sh

    Google Calendar - June 2025
    https://calendar.google.com/calendar/u/0/r


        """
        text            = QApplication.clipboard().text( )
        splits          = text.split( "\n" )
        new_lines       = []

        for i_line in splits:
            ii_line      = i_line

            if string_utils.begins_with_url( i_line ):
                ii_line  = f">>url {i_line}"

            elif string_utils.begins_with_file_name( i_line ):
                ii_line  = f">>shell {i_line}"

            new_lines.append( ii_line )

        # !! integrate the next if a multiline
        #new_lines.append( "the end")
        new_text = "\n".join( new_lines )

        self.insert_text_at_cursor( new_text )
        self.insert_text_at_cursor( "" )       # extra line at end

    #-----------------------------------
    def paste_clipboard( self, ):
        """
        what it says
        """
        text    = QApplication.clipboard().text( )
        self.insert_text_at_cursor( text )

    # ------------------------
    def insert_text_at_cursor( self, text ):
        """
        insert text at the cursor position
        """
        text_edit       = self.text_edit
        cursor          = text_edit.textCursor()
        cursor.insertText( text )


    def run_shell( self, code_lines ):
        """ """
        # self.shell_ext        = ShellExe()

        self.shell_ext.run_code_lines( code_lines )

    def cache_current( self ):
        """
        save contents of the text in one level deep buffer
        probably trigger before select or add
        this code would go
        """
        text_edit   = self.text_edit
        cursor      = text_edit.textCursor()  # Save the current cursor position

        self.prior_text     = text_edit.toPlainText()  # Get all text as a string

        text_edit.setTextCursor(cursor)

    def paste_cache( self ):
        """
        save contents of the text in one level deep buffer
        """
        self.insert_text_at_cursor( self.prior_text )
        pass # debug

    # ---------------------
    def search_down( self, search_line_edit ):
        """
        search for text see search up
            case insensitive
        """
        text_edit   = self.text_edit
        search_text = search_line_edit.text()
        if search_text:
            cursor = text_edit.textCursor()
            cursor.setPosition( self.last_position )
            found = text_edit.find( search_text )

            if found:
                self.last_position = text_edit.textCursor().position()
                text_edit.ensureCursorVisible()  # Scroll to the found text

            else:
                # grok code
                self.last_position = 0
                cursor.setPosition(self.last_position)
                text_edit.setTextCursor(cursor)
                text_edit.ensureCursorVisible()  # Optional: Scroll to top if reset

    # ---------------------
    def search_up( self, search_line_edit ):
        """case insensitive
        for an text edit search for a string
        the line_edit contains the string that is the target
        direction of search is up
        case insensitive
        may need to protect against trying to start beyond end !!
        as user may have deleted some text

        """
        text_edit   = self.text_edit
        search_text = search_line_edit.text()
        if search_text:
            cursor = text_edit.textCursor()
            cursor.setPosition( self.last_position )

            found = text_edit.find( search_text, QTextDocument.FindBackward )

            if found:
                self.last_position = text_edit.textCursor().position()
                text_edit.ensureCursorVisible()  # Scroll to the found text

            else:
                self.last_position = text_edit.document().characterCount()
                cursor.setPosition( self.last_position )
                text_edit.setTextCursor(cursor)
                text_edit.ensureCursorVisible()  # Optional: Scroll to top if reset

    #----------------------------
    def set_custom_context_menu( self, widget ):
        """
        what it says
        """
        widget.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
        widget.customContextMenuRequested.connect( self.show_context_menu )
        self.context_widget   = widget # for later use in menu

    # ---------------------------------------
    def show_context_menu( self, pos ):
        """
        from chat, refactor please !!
        !! needs extension

        """
        widget      = self.context_widget
        menu        = QMenu( widget )

        # Add standard actions
        undo_action = menu.addAction("Undo")
        undo_action.triggered.connect(widget.undo)
        menu.addSeparator()

        cut_action = menu.addAction("Cut")
        cut_action.triggered.connect(widget.cut)

        copy_action = menu.addAction("Copy")
        copy_action.triggered.connect(widget.copy)

        paste_action = menu.addAction("Paste")
        paste_action.triggered.connect(widget.paste)
        #menu.addSeparator()

        # ---- "Smart Paste"
        foo_action = menu.addAction("Smart Paste")
        foo_action.triggered.connect(self.smart_paste_clipboard )
        menu.addSeparator()

        # ---- "Strip Sel"
        foo_action = menu.addAction("Strip Sel")
        foo_action.triggered.connect( self.strip_lines_in_selection)
        #menu.addSeparator()

        # ---- "RStrip Sel"
        foo_action = menu.addAction("RStrip Sel")
        foo_action.triggered.connect( self.strip_eol_lines_in_selection )
        #menu.addSeparator()

        # ---- ""Update Markup""
        foo_action = menu.addAction("Update Markup")
        foo_action.triggered.connect( self.update_markup )
        menu.addSeparator()

        # ---- "Open Urls"
        foo_action = menu.addAction("Open Urls")
        foo_action.triggered.connect( self.goto_urls_in_selection )
        menu.addSeparator()


        select_all_action = menu.addAction("Select All")
        select_all_action.triggered.connect(widget.selectAll)

        # ---- >>   go
        menu_action = menu.addAction(">>   go ...")
        menu_action.triggered.connect( self.cmd_exec )
        menu.addSeparator()


        # Enable/disable actions based on context
        cursor = widget.textCursor()
        has_selection   = cursor.hasSelection()
        can_undo        = widget.document().isUndoAvailable()
        can_paste       = QApplication.clipboard().text() != ""

        undo_action.setEnabled(can_undo)
        cut_action.setEnabled(has_selection)
        copy_action.setEnabled(has_selection)
        paste_action.setEnabled(can_paste)
        foo_action.setEnabled(can_paste)

        # Show the context menu
        menu.exec_(widget.mapToGlobal(pos))

    # ----------------------------------
    def parse_search_partxxxx( self, criteria, part ):
        """

        still needs error check
        """
        splits    = part.split( "=" )
        key       = (splits[0].strip()).lower()
        value     = splits[1].strip()
        # may need type conversion when get to dates
        key       = KEY_DICT[key]
        criteria[key] = value


    # ----------------------------------
    def parse_search_stuffdbxxxx( self, a_string ):
        """
        >>search jeoe sue   /sys=python /subsys=qt
        change to a dict

        cirteria = {key_words: "joe" "sue" }

        """
        criteria    = defaultdict( None )
        parts       = a_string.split( "/" )
        key_words   = parts[0].strip()
        criteria[ "key_words" ] = key_words

        for i_part in parts[ 1: ]:
            try:
                self.parse_search_part( criteria, i_part  )
            except ValueError as error:
                # Access the error message
                error_message = str(error)
                msg  = (f"Parse >>search Caught an error: {error_message}")
                msg_box             = QMessageBox()
                msg_box.setIcon( QMessageBox.Information )
                msg_box.setText( msg )
                msg_box.setWindowTitle( "Sorry that is a No Go " )
                msg_box.setStandardButtons( QMessageBox.Ok )

        print( criteria )

        return criteria

    #------------------------------------
    def search_stuffdbxxxx(self, cmd, args ):
        """
        first just for window we are in then others later
        """

        criteria    = self.parse_search_stuffdb( args )

        # if command is search need to search window w

        STUFF_DB.main_window.search_me( criteria )  # cmd_args rest of line


    #------------------------------------
    def strip_eol_lines_in_selection(self, ):
        """

            The processed text (also replaces the selection in the widget)
        """
        text_edit       = self.text_edit
        # Get the selected text
        cursor          = text_edit.textCursor()
        selected_text   = cursor.selectedText()

        # Check if there's any selected text
        if not selected_text:
            return None

        # Split into lines and strip each line
        # Note: QTextEdit uses Unicode paragraph separators (U+2029) for line breaks in selectedText()
        lines           = selected_text.split('\u2029')
        stripped_lines  = [line.rstrip() for line in lines]

        processed_text = '\n'.join(stripped_lines)

        cursor.insertText(processed_text)
        return processed_text # for no good reason ??

    #------------------------------------
    def goto_urls_in_selection(self, ):
        """
        what it says

        and/or look in clipboard utils
        """
        text_edit       = self.text_edit
        # Get the selected text
        cursor          = text_edit.textCursor()
        selected_text   = cursor.selectedText()

        if not selected_text:
            return None

        lines           = selected_text.split('\u2029')
        stripped_lines  = [line.strip() for line in lines]
        for i_line in stripped_lines:
            i_line.replace( ">>url", "") # what about caps -- do better
            i_line.strip( )
            if string_utils.begins_with_url( i_line ):
                splits = i_line.split( " " )
                i_line = splits[0]
                webbrowser.open( i_line, new = 0, autoraise = True )

    #------------------------------------
    def strip_lines_in_selection(self, ):
        """
        Remove whitespace both end of lines

        Originally Claude says
            Gets selected text from a QTextEdit, strips leading and trailing spaces from each line,
            and replaces the original selection with the processed text.


        Returns:
            The processed text (also replaces the selection in the widget)
        """
        text_edit       = self.text_edit
        # Get the selected text
        cursor          = text_edit.textCursor()
        selected_text   = cursor.selectedText()

        if not selected_text:
            return None

        # Split into lines and strip each line
        # Note: QTextEdit uses Unicode paragraph separators (U+2029) for line breaks in selectedText()
        lines           = selected_text.split('\u2029')
        stripped_lines  = [line.strip() for line in lines]

        # Join the lines back together
        processed_text = '\n'.join(stripped_lines)

        # Replace the selected text with the processed text
        cursor.insertText(processed_text)

        return processed_text


    def do_line_replacements( self, line ):
        """

        may want to strip eol while at it
        """
        print( "do_line_replacements {line =}" )
        #breakpoint()
        for old, new in REPLACE_LIST:
                line   = line.replace( old, new )

        return line

    #------------------------------------
    def update_markup(self, ):
        """
        update from old stuff markup to new markup
        """
        text_edit       = self.text_edit
        # Get the selected text
        cursor          = text_edit.textCursor()
        selected_text   = cursor.selectedText()

        # Check if there's any selected text
        if not selected_text:
            return None

        # Split into lines and strip each line
        # Note: QTextEdit uses Unicode paragraph separators (U+2029) for line breaks in selectedText()
        lines           = selected_text.split('\u2029')
        updated_lines  = [self.do_line_replacements(line) for line in lines]

        processed_text = '\n'.join(updated_lines)

        # Replace the selected text with the processed text
        cursor.insertText( processed_text )

        return processed_text


    # ------------------------
    def ctrl_f_find ( self   ):
        """

        """
        selected_text   = self.capture_selected_text()
        text_edit       = self.text_edit
        search_line_edit.setTtext( selected_text  )




    def capture_selected_text(self):
        """Capture the currently highlighted (selected) text
        is this worth a function
        """
        cursor = self.text_edit.textCursor()
        selected_text = cursor.selectedText()

        if selected_text:
            print(f"Captured highlighted text: '{selected_text}'")
            # Call your function with the captured text
            #self.foo(selected_text)
        else:
            print("No text is currently highlighted/selected")

        return selected_text

    # ------------------------
    def cmd_exec( self   ):
        """
        execute command parsed out of text

        !! change to use marker
        py
        sh
        url
        shell
        text
        idle
        copy

        """
        text_edit        = self.text_edit
        # ---- do some parsing
        code_lines       = get_snippet_lines( text_edit  )
        debug_msg        = ( code_lines )
        logging.debug( debug_msg )

        code_lines       = undent_lines(code_lines)
        splits           = code_lines[0].split()
        splits_1         = code_lines[0].split( " ", 1 )
        if len( splits_1 ) > 1:
            arg_1 = splits_1[1].strip()   # ?? follow by remove of nl

        if len( splits) == 0:
            return

        if splits[0] == ">>":
            splits = splits[1:]        # toss the >>

        if splits[0].startswith( ">>" ):
            splits[0]  = splits[0][ 2: ]  # again toss the >>

        cmd         = splits[0].lower()
        cmd_args    = splits[ 1:]

        debug_msg   = ( f"cmd_exec {cmd = } \n {cmd_args = }")
        logging.log( LOG_LEVEL,  debug_msg, )

        # ---- py
        if   cmd == "py":
            code    = "\n".join( code_lines[ 1:] )  # title in line 0 !!
            msg     = " ".join( cmd_args )
            if msg == "":
                msg  = "execute some python code"
            #rint( code )
            global   EXEC_RUNNER
            if EXEC_RUNNER is None:
                EXEC_RUNNER      = exec_qt.ExecRunner( AppGlobal.q_app  )

            EXEC_RUNNER.create_window(
                        code       = code,
                        a_locals   = locals(),
                        a_globals  = globals(),
                        msg        = msg,
                        autorun    = True )

        elif cmd == "copy":
            #rint( "you need to implement >>idle")
            QApplication.clipboard().setText( " ".join( cmd_args )   )

        # ---- snippet  !! missing from docs ??
        elif cmd == "snippet":
            #rint( "you need to implement >>idle")
            # QApplication.clipboard().setText( " ".join( cmd_args )   )
            code    = "\n".join( code_lines[ 1:] )  # title in line 0 !!
            msg     = " ".join( cmd_args )

            QApplication.clipboard().setText( code   )

        # ---- idle and idle file
        elif cmd == "idle":   # want a one line and may line
            msg     = ( "  >>idle in process ................................")
            logging.debug( msg, )

            self.idle_exe.idle_on_temp_file( code_lines )

        elif cmd == "idle_file":   # want a one line and may line
            file_name     = cmd_args[0]
            self.idle_exe.idle_file( file_name  )
            pass  # debug

        # ---- text
        elif cmd == "text":
            file_name     = cmd_args[0]
            AppGlobal.os_open_txt_file( file_name )

        elif cmd == "url":
            filename     = cmd_args[0]
            webbrowser.open( filename, new = 0, autoraise = True )

        # ---- bash
        elif cmd == "bash":
            #rint( f"you need to implement >>shell {code_lines}")
            TEXT_EDIT_EXT.run_shell( code_lines )

        # ---- shell
        elif cmd == "shell":
            #file_name     = cmd_args[0]  # older change to next t
            file_name     = arg_1
            shell_file( file_name )
    \
        # ---- search  !! should not have in this object move to stuff db
        # as a plugin of some source
        elif cmd.startswith( "search" ):
            # msg   = ( "implementing >>search")
            # logging.debug( msg )
            #breakpoint( )
            if  STUFF_DB  is None:
                msg   = ( f"cannot do search as {STUFF_DB  = }  ")
                logging.error( msg )
                # !! put up dialog
                return

            else:
                AppGlobal.mdi_management.do_db_search( cmd,  cmd_args )


            #     # msg   = ( f"you need to implement >>search {STUFF_DB  = }  ")
            #     # logging.debug( msg )
            #     new_args =  []  # drop after #
            #     for i_arg in cmd_args:
            #         if i_arg.startswith( "#" ):
            #             break
            #         new_args.append( i_arg )
            #         key_words   = " ".join( new_args )
            #     self.search_stuffdb( cmd,do_db_search
            # " ".join( new_args ))
            #     #STUFF_DB.main_window.search_me( " ".join( new_args ) )  # cmd_args rest of line
            # # = None  # may be monkey patched in
            # #                     # this wold be the app
            # #                     # STUFF_DB.main_window may be what you want
            # #                     # go_active_sub_window_func


        elif cmd == "xxx":
            pass

        else:
            msg   = ( f"{cmd = } \n {cmd_args = }" )
            logging.error( msg )
        # next case based on command cmd



class ShellExe( object ):
    """
    for executing shell commands that begin as a list
    this may need refactoring
    based on cmd_assist perhaps should go back there
    should be a singleton for now built by TextEditExt
    """
    #----------- init -----------
    def __init__(self,   ):
        pass

    #---------------------------
    def run_code_lines( self, code_lines, ):
        """ """

        code_lines_new     = [i_code_line.strip()
                               for i_code_line in code_lines
                                   if i_code_line.strip() != "" ]

        #rint( f"run_code_lines in shellext    >>shell {code_lines_new =}")
        # line one == 0 is a comment add echo in front and quote
        code_lines_new[ 0 ]    = f"echo '{code_lines_new[ 0 ]}'   "

        #rint( f"run_code_lines in shellext    >>shell {code_lines_new =}")
        code_lines_new      = self.add_echo( code_lines_new )
        debug_msg    = ( f""""run_code_lines in shellext    >>shell {code_lines_new =}""")
        logging.log( LOG_LEVEL,  debug_msg, )

        cmd_str     = ";".join( code_lines_new )
        cmd_str     = f"""gnome-terminal -- bash -c "{cmd_str}; echo 'exec bash' ;exec bash" """

        debug_msg   = ( f"about to os.system {cmd_str = }" )
        logging.log( LOG_LEVEL,  debug_msg, )

        result = os.system( cmd_str  )
        #rint( f"result = os.system >>{result}<<\n\n")

    # ----------------------------------
    def add_echo(self, code_lines ):
        """
        add echo commands except to echo commands
        and for now remove comments from the command part

        """
        new_list      = []
        for i_item in code_lines:
            if i_item.startswith( "echo" ):
                new_list.append( i_item )
            else:
                new_list.append( f"echo '{i_item}'")
                # now look for command part comment
                splits     = i_item.split( "#" )
                i_item     = splits[0]     # combine lines for clean
                new_list.append( i_item )

        return new_list

    # ----------------------------------
    def build_command_1_2xxx( self, add_echo = True, add_newline = False ):
        """
        from command_0 suck dry and delete
        build command from arg1 and arg2
        self.build_command_1_2
        ex:
        return self.build_command_1_2( add_echo = add_echo, add_newline = add_newline )

        ! need a 0 1 2 version and a generalized one see commands 3 for vert which seems to do it
        """
        print( "build_command_1_2" )
        args        = self.get_ddl_args()

        cmd_prefix  = self.build_prefix()

        cmd_list    = cmd_prefix + [ f"{args[1]} {args[2]}",
                                     "exec bash",
                                     ]

        if add_echo:
            cmd_list    = self.build_echo( cmd_list )

        if add_newline:
            cmd_str     = "\n".join( cmd_list )   # may still want to strip exec bash  !!

        else:
            cmd_str     = ";".join( cmd_list )
            cmd_str     = f'gnome-terminal -- bash -c "{cmd_str}"'

        #rint( cmd_str )
        #rint( cmd_list )

        return cmd_str

class IdleExe( ):
    """
    for executing shell commands that begin as a list
    this may need refactoring
    based on cmd_assist perhaps should go back there
    should be a singleton for now built by TextEditExt
    """
    def __init__( self ):
        """ """
        self.venv               = "py_12_misc"  # !! change to parameter
        self.file_name_temp_py  = "temp_py.py"
        self.file_name_temp_sh  = "temp_sh.sh"

    #--------
    def write_file_py( self, code_lines, file_name = None ):
        """ """
        file_name    = self.file_name_temp_py

        with open( file_name, 'w' ) as a_file:
                # wa will append so file should be deleted time to time w will overwrite
            a_file.writelines(f"{line}\n" if not line.endswith("\n") else line for line in code_lines )

    #--------
    def write_file_sh( self, sh_lines, file_name = None ):
        """ """
        file_name    = self.file_name_temp_sh

        with open( file_name, 'w' ) as a_file:    # wa will append so file should be deleted time to time w will overwrite
            a_file.writelines(f"{line}\n" if not line.endswith("\n") else line for line in sh_lines )


    def idle_on_temp_file( self, code_lines ):
        """ """
        code_lines[0]   =  f"# -- {code_lines[0]}"
        self.write_file_py( code_lines, )
        sh_lines        = [ f"conda activate {self.venv}", f"idle  {self.file_name_temp_py}" ]
        self.write_file_sh( sh_lines )

        #subprocess.run(  ["bash", self.file_name_temp_sh ] )
        #    # blocking
        subprocess.Popen(["bash", self.file_name_temp_sh] )
            # non blocking --- see help


    def idle_file( self, file_name ):
        """
        open idle in a conda venv for file_name

        think links to idle_file   filename
        """

        sh_lines        = [ f"conda activate {self.venv}", f"idle  {file_name}" ]
        self.write_file_sh( sh_lines )

        # next seems to be blocking
        #subprocess.run(["bash", self.file_name_temp_sh ])

        # should be non blocking
        subprocess.Popen([ "bash", self.file_name_temp_sh])


        # next is wrong because we need the environment set up
        #subprocess.run([ "idle", file_name ])

# ------------------------
def get_snippet_lines( text_edit, do_undent = True  ):
    """
    title is line 0
    often for code
    assume cursor in the body
    but there is a built in find function

    # ---- top of text
    >beginmarker    anything else on line

    >>py this is a title
    print( 1 )
    for ix in range( 10, 15 ):
        print( ix )

    >beginmarker    anything else on line

    # ---- end  of text

    start scanning up:
        stop if hit begin marker or top ( or blank lines?

    now scan down and collect lines ( rstripped, no spaces no \n )

        stop if  n_blank lines
        marker
        or end of text
    """
    lines                   = []
    cursor                  = text_edit.textCursor()
    consective_blank_lines  = 0
    original_position       = cursor.position()
    cursor.movePosition( cursor.StartOfLine )
    prior_start_of_line     = cursor.position()

    # ---- upward scan
    for ix in range( SCAN_LINES ):

        cursor.movePosition( QTextCursor.StartOfLine )
        cursor.movePosition(cursor.EndOfLine, cursor.KeepAnchor )
        selected_text = cursor.selectedText()

        selected_text   = selected_text.rstrip()
        if   selected_text == "":
            consective_blank_lines  += 1

        else:
            consective_blank_lines  = 0

        if selected_text.strip().lower().startswith( MARKER ):
            #rint( f"hit the top of marked text {ix =}")
            break # leave curor at begin of marker line

        # lines.append( selected_text  )

        cursor.movePosition( cursor.Up )
        cursor.movePosition( QTextCursor.StartOfLine )
        position       = cursor.position()
        if position == prior_start_of_line:
            debug_msg = ( f"is error !! hit the top of all text {ix =}")
            logging.log( LOG_LEVEL,  debug_msg, )
            break
        else:
            prior_start_of_line  = position

    # now at top of text
    #rint( f"found the top of  text {ix =}")

    # ---- start down collecting lines
    consective_blank_lines  = 0
    on_top_line             = True
    for ix in range( SCAN_LINES ):
        cursor.movePosition( cursor.EndOfLine, cursor.KeepAnchor )
        selected_text   = cursor.selectedText()
        selected_text   = selected_text.rstrip()

        if   selected_text == "":
            consective_blank_lines  += 1

        else:
             consective_blank_lines  = 0

        if consective_blank_lines  > 3:
            #msg = f"scan down blank line limit {consective_blank_lines}"
            #rint( msg )
            break

        # hot on firs line down
        if not on_top_line and selected_text.strip().lower().startswith( MARKER ):
            #rint( f"hit the next line of marked text {ix =}")
            break # leave curor at begin of marker line
        else:
            on_top_line = False

        lines.append( selected_text  )

        # Move to the start of the next line 2 steps
        cursor.movePosition(cursor.Down)
        cursor.movePosition(QTextCursor.StartOfLine)
        position       = cursor.position()

        if position == prior_start_of_line:
            #rint( f"hit the end of text {ix =} ")
            break

        else:
            prior_start_of_line  = position

    if do_undent:
        lines   = undent_lines( lines )

    return lines

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
    text_edit.copy()   # goes to clipboard
    all_text = self.text_edit.toPlainText()

    # Restore cursor
    cursor.setPosition(original_position)
    text_edit.setTextCursor(cursor)
    return  all_text

# ------------------------
def undent_lines( lines ):
    """
    delete leading spaces ( as per code )
    then return as a multiline string  that is a list of strings
        lines   is a list of lines


    """
    new_lines            = []
    if len( lines ) == 0:
        return new_lines

    num_leading_spaces   = len( lines[0] ) - len( lines[0].lstrip(' ') )
    #rint( f"{num_leading_spaces = }")
    leading_spaces       = " " * num_leading_spaces

    for i_line in lines:
        if i_line.startswith( leading_spaces ):
            i_line   = i_line[ num_leading_spaces : ]
        new_lines.append( i_line )

    return new_lines

# ------------------------
def qt_exec( text_edit ):
    """
    execute in a qt window from code in text_edit
    this is like the wat inspector but is not it
    >>

    """
    code_lines      = get_snippet_lines( text_edit  )
    debug_msg       = ( code_lines )
    logging.log( LOG_LEVEL,  debug_msg, )
    code_lines       = undent_lines(code_lines)
    #rint( f"{code_lines = }")
    code    = "\n".join( code_lines[ 1:] )  # title in line 0 !!
    #rint( code )
    global   EXEC_RUNNER
    if EXEC_RUNNER is None:
        EXEC_RUNNER      = exec_qt.ExecRunner( AppGlobal.q_app  )

    EXEC_RUNNER.create_window(
                code       = code,
                a_locals   = locals(),
                a_globals  = globals(),
                msg        = "my code message" )


def shell_file( file_name ):
    """ """
    if platform.system() == 'Windows':
        os.startfile(file_name)
    elif platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', file_name))
    else:  # Linux
        subprocess.call(('xdg-open', file_name ) )

# Usage

# # ------------------------
# def cmd_exec( text_edit ):
#     """
#     execute command parsed out of text


#     """/mnt/WIN_D/russ/0000/python00/python3/_projects/rshlib/rshlib_qt/text_edit_ext.py

# ---- eof
