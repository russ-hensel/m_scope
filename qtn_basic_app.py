#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---- tof
"""
A universal app that works on PyQt5 or PyQt6 using QtPy
"""

# ---- imports
import sys
# We import from qtpy instead of PyQt5 or PyQt6
# This requires: pip install qtpy
from qtpy.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget

class MainWindow( QMainWindow ):
    def __init__(self):
        """Build the main window """
        super().__init__()

        self.setWindowTitle( "Universal Qt App" )
        self.setFixedSize(300, 100)

        # Create central widget
        a_central_widget    = QWidget()
        self.setCentralWidget( a_central_widget )

        # Set up layout
        a_layout        = QVBoxLayout()
        a_central_widget.setLayout( a_layout )

        # ---- QLineEdit
        self.line_edit = QLineEdit()
        a_layout.addWidget( self.line_edit )

        # ---- QPushButton
        self.button = QPushButton( "Click Me" )
        self.button.clicked.connect(self.on_button_click)
        a_layout.addWidget( self.button )

    def on_button_click(self):
        print("Button Clicked!")
        self.line_edit.setText("Working on " + QApplication.instance().arguments()[0])

if __name__ == '__main__':
    app         = QApplication( sys.argv )
    window      = MainWindow()
    window.show()

    # QtPy handles the exec_() vs exec() difference automatically
    app.exec()

# ---- eof