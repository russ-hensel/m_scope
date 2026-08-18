#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
needs import and
call to init

import app_logging
app_logging.init( )

my_logging   = app_logging.APP_LOGGING
my_logging.what(0)

sets up glogal lobbing

depends on parmetes being set up first
        and appGlobal


"""

import logging
import sys
import traceback



from qt_compat import QApplication, QAction, exec_app, qt_version
from PyQt.QtWidgets import QMainWindow, QToolBar, QMessageBox

#from PyQt.QtGui import ( QAction, QActionGroup, )

from PyQt.QtWidgets import (
                             QApplication,
                             QButtonGroup,
                             QCheckBox,
                             QComboBox,
                             QDataWidgetMapper,
                             QDateEdit,
                             QDialog,
                             QDockWidget,
                             QFileDialog,
                             QFrame,
                             QGraphicsPixmapItem,
                             QGraphicsScene,
                             QGraphicsView,
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
                             QSizePolicy,
                             QSpacerItem,
                             QSpinBox,
                             QTableView,
                             QTableWidget,
                             QTableWidgetItem,
                             QTabWidget,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)


# ---- local imports
from app_global import AppGlobal

#import app_globals

# breakpoint()

# ---- end imports
#global APP_LOGGING
APP_LOGGING     = None

#-------------------------------

# this is a mess as code is in flux

PARAMETERS      = None


# ---- ----------------
class DialogAddToLog( QDialog ):
    """
    deep seek did draft
    app_logging.DialogAddToLog
    """
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data  # Mutable object to store input and output data
        self.initUI()

    #-----------------------------
    def initUI( self,    ):
        """ data is a mutuable dict """
        self.setWindowTitle("Remark for Log ")
        self.setGeometry( 300, 300, 600,  100 )   # * * width * height

        layout          = QVBoxLayout()

        #------------
        label           = QLabel("Remark:")
        layout.addWidget(label)

        # # Line Edit for input
        # self.line_edit  = QLineEdit(self)

        # editable combobos for input
        widget          = QComboBox()
        self.combo_box  = widget
        self.line_edit  = widget
        widget.setEditable( True )

        # may want in future
        #widget.lineEdit().returnPressed.connect( self.conbo_return )

        widget.addItem('Select from List')
        widget.addItem('Add a record')
        widget.addItem('Update a record')
        widget.addItem('Press Save')

        widget.setEditable( True )   # if is edited then value does not match index

        # check dict for a default
        if "default_value" in self.data:
            self.combo_box.lineEdit().setText(self.data["default_value"])
        layout.addWidget( widget )

        # ---- buttons
        row_layout          = QHBoxLayout()
        layout.addLayout( row_layout )

        widget = QPushButton("OK", self)
        widget.clicked.connect( self.on_ok )
        row_layout.addWidget(widget)

        widget = QPushButton("Cancel", self)
        widget.clicked.connect( self.on_cancel )
        row_layout.addWidget(widget)

        self.setLayout(layout)


    def on_ok(self):
        # Store the input data in the mutable object
        self.data["return_value"] = self.combo_box.currentText() #      .text()

        self.accept()  # Close the dialog and return QDialog.Accepted

    def on_cancel(self):
        self.reject()

# ---- ----------------
class AppLogging( ):

    def __init__(self ):
        """ """
        global PARAMETERS
        if PARAMETERS is None:
            try:

                PARAMETERS      = AppGlobal.parameters

            except:
                pass


        if PARAMETERS is None:
            try:
                from app_globals import PARAMETERS

                PARAMETERS

            except:
                pass


        if not PARAMETERS:
            1/0    # set up parameters first


        global APP_LOGGING

        APP_LOGGING = self

        self.config_logger( )

    # def init():
    #     """for stuffdb? """

    # ------------------------------
    def config_logger(self):
        """
        Configure the Python logger to allow logging from other modules.
        """
        # PARAMETERS      = app_globals.PARAMETERS

        log_file_name   = PARAMETERS.pylogging_fn  # File to log messages
        log_mode        = PARAMETERS.log_mode
        log_level       = PARAMETERS.logging_level

        try:
            # Configure the ROOT LOGGER (so other modules can use it)
            root_logger = logging.getLogger()  # Get root logger
            root_logger.setLevel( log_level )

            # Remove existing handlers to prevent duplicates
            if root_logger.hasHandlers():
                root_logger.handlers.clear()

            # Create file handler (overwrites or appends based on mode)
            file_handler = logging.FileHandler(log_file_name, mode = log_mode )
            file_handler.setLevel( log_level )
            file_handler.setFormatter(logging.Formatter(
                           '%(asctime)s - %(levelname)s - %(message)s'))

            # Create console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel( log_level )
            console_handler.setFormatter(logging.Formatter(
                          '%(asctime)s - %(levelname)s - %(message)s'))

            # Add handlers to root logger
            root_logger.addHandler(file_handler)
            root_logger.addHandler(console_handler)

        except Exception as e:
            print("Exception occurred setting up logger:")
            traceback.print_exc()

        logger          = logging.getLogger( )
        AppGlobal.set_logger( logger )
        self.logger      = logger

        # Example log from the root logger
        logging.critical("Root logger is set up. Modules can now log using logging.getLogger().")
        logging.info("config_logger call was: logging.info")

        # # Example logs and test
        # self.logger.critical("config_logger call was logger.critical()")
        # self.logger.critical(f"config_logger {log_file_name = } ")
        # self.logger.log(22, "config_logger This is a 22 message from my_logger.")
        # self.logger.debug("config_logger call was: logging.debug")
        # self.logger.info("config_logger call was: logging.info")


    # def test_logingr(self):
    #     """ """
    #     pass

    # ----------------------------------------------
    def os_open_log_file( self,  ):
        """
        have function since want flush

        """
        self.log_file_handler.flush()  # Manually flushing

        AppGlobal.os_open_txt_file( self.parameters.pylogging_fn )

    # ------------------------------------------
    def close_logger( self, ):
        """
        not tested after other changes
        """
        logger  = AppGlobal.logger
        for a_handler in logger.handlers:
            a_handler.close()

# ------------------------
def add_to_log(   ):
    """
    add a messge from user to the log

    app_logging.add_to_log()
    """

    # Mutable object to pass data to and from the dialog
    data = {"default_value": "Add to log ... "}

    # Create and show the dialog
    dialog = DialogAddToLog ( data, )
    result = dialog.exec()

    # Check if the dialog was accepted or rejected
    if result == QDialog.Accepted:
        msg     = f"{data['return_value']}"
        #QMessageBox.information(self, "Result", msg )
        print( msg )
        logging.error( F"USER_MSG: {msg}" )
    1/0   # to test exception management
    # else:
    #     msg     = "Dialog was canceled"
    #     #QMessageBox.information(self, "Result",  msg )
    #     print( msg )


# def  init( ):
#     global APP_LOGGING
#     if not APP_LOGGING:
#         APP_LOGGING = AppLogging( )

# def  init( ):
#     global APP_LOGGING
#     if not APP_LOGGING:
#         APP_LOGGING = AppLogging( )



# ---- eof
