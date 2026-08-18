#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 08:48:38 2025

@author: grok draft

this is in test take a look with qt5 by example



"""
import sys
from    PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QCheckBox, QPushButton, QDialogButtonBox
    )
from PyQt5.QtCore import Qt

class ConfirmDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Action")
        self.resize(300, 150)

        # Main layout
        layout = QVBoxLayout(self)

        # Message label
        label = QLabel("Do you really want to perform this action?")
        label.setWordWrap(True)
        layout.addWidget(label)

        # Checkbox option
        self.dont_ask_checkbox = QCheckBox("Don't ask me again")
        layout.addWidget(self.dont_ask_checkbox)

        # Spacer
        layout.addStretch()

        # Button layout
        button_layout = QHBoxLayout()

        # Custom "View Log" button (doesn't close dialog)
        view_log_btn = QPushButton("View Log")
        view_log_btn.clicked.connect(self.on_view_log)
        button_layout.addWidget(view_log_btn)

        # Standard buttons using QDialogButtonBox (easier management)
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)   # OK -> accept()
        buttons.rejected.connect(self.reject)   # Cancel -> reject()

        # Rename OK to "Proceed"
        buttons.button(QDialogButtonBox.Ok).setText("Proceed")

        button_layout.addWidget(buttons)
        layout.addLayout(button_layout)

    def on_view_log(self):
        # This action does NOT close the dialog
        print("User clicked 'View Log' – opening log viewer...")
        # Here you could open a log window, file, etc.
        # For demo, we'll just show a message in console
        # self.some_log_viewer.show()  # example

    # Convenience methods to get results
    def dont_ask_again(self):
        return self.dont_ask_checkbox.isChecked()

    @staticmethod
    def get_confirmation(parent=None):
        dialog = ConfirmDialog(parent)
        result = dialog.exec_()  # Shows modal dialog
        return (
            result == QDialog.Accepted,   # True if Proceed clicked
            dialog.dont_ask_again()       # Checkbox state
        )

# -----------------------------
# Usage example
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    proceed, dont_ask = ConfirmDialog.get_confirmation()

    if proceed:
        print("User chose to proceed.")
        if dont_ask:
            print("User doesn't want to be asked again.")
        # ... perform the action ...
    else:
        print("User canceled.")

    sys.exit(app.exec_())
