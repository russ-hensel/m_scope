"""
qt_compat.py — Full PyQt5 / PyQt6 compatibility layer.

Covers:
- Class moves
- Enum changes
- exec differences
- QSqlTableModel, QComboBox, QHeaderView, etc.
"""
# ---- tof
import sys

# --- Import PyQt6 if available, else PyQt5 ---
try:
    import PyQt6 as PyQt
    from PyQt6 import QtCore, QtGui, QtWidgets, QtSql, QtPrintSupport
    from PyQt6.QtWidgets import QApplication, QWidget
    qt_version = 6
except ImportError:
    import PyQt5 as PyQt
    from   PyQt5 import QtCore, QtGui, QtWidgets, QtSql, QtPrintSupport
    from   PyQt5.QtWidgets import QApplication, QWidget
    qt_version = 5

# --- Inject PyQt namespaces for universal import ---
sys.modules["PyQt"]           = PyQt
sys.modules["PyQt.QtCore"]    = QtCore
sys.modules["PyQt.QtGui"]     = QtGui
sys.modules["PyQt.QtWidgets"] = QtWidgets
sys.modules["PyQt.QtSql"]     = QtSql
sys.modules["PyQt.QtPrintSupport"] = QtPrintSupport

# --- QApplication exec method ---
exec_app = QApplication.exec if qt_version == 6 else QApplication.exec_

# --- Qt reference ---
Qt = QtCore.Qt

# --- Alignment flags ---
AlignCenter     = Qt.AlignmentFlag.AlignCenter if qt_version == 6 else Qt.AlignCenter
AlignLeft       = Qt.AlignmentFlag.AlignLeft   if qt_version == 6 else Qt.AlignLeft
AlignRight      = Qt.AlignmentFlag.AlignRight  if qt_version == 6 else Qt.AlignRight
AlignTop        = Qt.AlignmentFlag.AlignTop         if qt_version == 6 else Qt.AlignTop
AlignBottom     = Qt.AlignmentFlag.AlignBottom      if qt_version == 6 else Qt.AlignBottom
AlignVCenter    = Qt.AlignmentFlag.AlignVCenter     if qt_version == 6 else Qt.AlignVCenter
    # from qt_compat import AlignCenter, AlignLeft, AlignRight, AlignTop, AlignBottom, AlignVCenter

# --- Orientation ---
Horizontal = Qt.Orientation.Horizontal if qt_version == 6 else Qt.Horizontal
Vertical   = Qt.Orientation.Vertical   if qt_version == 6 else Qt.Vertical
    # from qt_compat import Horizontal, Vertical

from PyQt.QtWidgets import QMessageBox
ActionRole    = QMessageBox.ButtonRole.ActionRole     if qt_version == 6 else QMessageBox.ActionRole
    # from qt_compat import ActionRole


from PyQt.QtWidgets import QSizePolicy

QSizePolicy_Expanding = QSizePolicy.Policy.Expanding if qt_version == 6 else QSizePolicy.Expanding
QSizePolicy_Minimum   = QSizePolicy.Policy.Minimum   if qt_version == 6 else QSizePolicy.Minimum
QSizePolicy_Fixed     = QSizePolicy.Policy.Fixed     if qt_version == 6 else QSizePolicy.Fixed
QSizePolicy_Preferred = QSizePolicy.Policy.Preferred if qt_version == 6 else QSizePolicy.Preferred

# from qt_compat import QSizePolicy_Expanding, QSizePolicy_Minimum, QSizePolicy_Fixed, QSizePolicy_Preferred

if qt_version == 6:
    from PyQt6.QtWidgets import QFileDialog
    ExistingFiles = QFileDialog.FileMode.ExistingFiles
    ExistingFile = QFileDialog.FileMode.ExistingFile
    AnyFile = QFileDialog.FileMode.AnyFile
    Directory = QFileDialog.FileMode.Directory
    from PyQt6.QtWidgets import  QCheckBox

else:
    from PyQt5.QtWidgets import QFileDialog
    ExistingFiles = QFileDialog.ExistingFiles
    ExistingFile = QFileDialog.ExistingFile
    AnyFile = QFileDialog.AnyFile
    Directory = QFileDialog.Directory
    from PyQt5.QtWidgets import QFileDialog
    from PyQt5.QtWidgets import QCheckBox


    # from qt_compat import QFileDialog, ExistingFiles, ExistingFile, AnyFile, Directory
    # from qt_compat import QCheckBox

if qt_version == 6:
    KeepAspectRatioByExpanding = Qt.AspectRatioMode.KeepAspectRatioByExpanding
else:
    KeepAspectRatioByExpanding = Qt.KeepAspectRatioByExpanding


from PyQt.QtCore import QItemSelectionModel

# if qt_version == 6:
#     Select = QItemSelectionModel.SelectionFlag.Select
#     Rows = QItemSelectionModel.SelectionFlag.Rows
# else:
#     Select = QItemSelectionModel.Select
#     Rows = QItemSelectionModel.Rows

if qt_version == 6:
    Select         = QItemSelectionModel.SelectionFlag.Select
    Deselect       = QItemSelectionModel.SelectionFlag.Deselect
    Toggle         = QItemSelectionModel.SelectionFlag.Toggle
    ClearAndSelect = QItemSelectionModel.SelectionFlag.ClearAndSelect
    Rows           = QItemSelectionModel.SelectionFlag.Rows
    Columns        = QItemSelectionModel.SelectionFlag.Columns
    Current        = QItemSelectionModel.SelectionFlag.Current
else:
    Select         = QItemSelectionModel.Select
    Deselect       = QItemSelectionModel.Deselect
    Toggle         = QItemSelectionModel.Toggle
    ClearAndSelect = QItemSelectionModel.ClearAndSelect
    Rows           = QItemSelectionModel.Rows
    Columns        = QItemSelectionModel.Columns
    Current        = QItemSelectionModel.Current


    # from qt_compat import  Select, Rows # and there are more




# --- ItemDataRole normalizations ---
DisplayRole       = Qt.ItemDataRole.DisplayRole       if qt_version == 6 else Qt.DisplayRole
EditRole          = Qt.ItemDataRole.EditRole          if qt_version == 6 else Qt.EditRole
CheckStateRole    = Qt.ItemDataRole.CheckStateRole    if qt_version == 6 else Qt.CheckStateRole
ToolTipRole       = Qt.ItemDataRole.ToolTipRole       if qt_version == 6 else Qt.ToolTipRole
StatusTipRole     = Qt.ItemDataRole.StatusTipRole     if qt_version == 6 else Qt.StatusTipRole
DecorationRole    = Qt.ItemDataRole.DecorationRole    if qt_version == 6 else Qt.DecorationRole
TextAlignmentRole = Qt.ItemDataRole.TextAlignmentRole if qt_version == 6 else Qt.TextAlignmentRole

# --- WindowState ---
WindowNoState    = Qt.WindowState.WindowNoState    if qt_version == 6 else Qt.WindowNoState
WindowMinimized  = Qt.WindowState.WindowMinimized  if qt_version == 6 else Qt.WindowMinimized
WindowMaximized  = Qt.WindowState.WindowMaximized  if qt_version == 6 else Qt.WindowMaximized
WindowFullScreen = Qt.WindowState.WindowFullScreen if qt_version == 6 else Qt.WindowFullScreen
WindowActive     = Qt.WindowState.WindowActive     if qt_version == 6 else Qt.WindowActive

# --- QComboBox.InsertPolicy ---
from PyQt.QtWidgets import QComboBox
InsertAtTop         = QComboBox.InsertPolicy.InsertAtTop         if qt_version == 6 else QComboBox.InsertAtTop
InsertAtCurrent     = QComboBox.InsertPolicy.InsertAtCurrent     if qt_version == 6 else QComboBox.InsertAtCurrent
InsertAtBottom      = QComboBox.InsertPolicy.InsertAtBottom      if qt_version == 6 else QComboBox.InsertAtBottom
InsertAfterCurrent  = QComboBox.InsertPolicy.InsertAfterCurrent  if qt_version == 6 else QComboBox.InsertAfterCurrent
InsertBeforeCurrent = QComboBox.InsertPolicy.InsertBeforeCurrent if qt_version == 6 else QComboBox.InsertBeforeCurrent
NoInsert            = QComboBox.InsertPolicy.NoInsert            if qt_version == 6 else QComboBox.NoInsert

CustomContextMenu = Qt.ContextMenuPolicy.CustomContextMenu if qt_version == 6 else Qt.CustomContextMenu
PreventContextMenu = Qt.ContextMenuPolicy.PreventContextMenu if qt_version == 6 else Qt.PreventContextMenu
DefaultContextMenu = Qt.ContextMenuPolicy.DefaultContextMenu if qt_version == 6 else Qt.DefaultContextMenu

    # from qt_compat import CustomContextMenu, PreventContextMenu, DefaultContextMenu
# Key_Return = Qt.Key.Key_Return if qt_version == 6 else Qt.Key_Return
# Key_Enter  = Qt.Key.Key_Enter  if qt_version == 6 else Qt.Key_Enter
# Key_Escape = Qt.Key.Key_Escape if qt_version == 6 else Qt.Key_Escape


if qt_version == 6:
    AscendingOrder  = Qt.SortOrder.AscendingOrder
    DescendingOrder = Qt.SortOrder.DescendingOrder
else:
    AscendingOrder  = Qt.AscendingOrder
    DescendingOrder = Qt.DescendingOrder
    # from qt_compat import AscendingOrder, DescendingOrder




if qt_version == 6:
    # Keys
    Key_Tab = Qt.Key.Key_Tab
    Key_Enter = Qt.Key.Key_Enter
    Key_Return = Qt.Key.Key_Return
    Key_F = Qt.Key.Key_F
    Key_Backtab = Qt.Key.Key_Backtab

    # Modifiers
    ShiftModifier   = Qt.KeyboardModifier.ShiftModifier
    ControlModifier = Qt.KeyboardModifier.ControlModifier
else:
    # Keys
    Key_Tab = Qt.Key_Tab
    Key_Enter = Qt.Key_Enter
    Key_Return = Qt.Key_Return
    Key_F = Qt.Key_F
    Key_Backtab = Qt.Key_Backtab
    # Modifiers
    ShiftModifier   = Qt.ShiftModifier
    ControlModifier = Qt.ControlModifier


# Add others as needed

# WindowType flags
Window_SubWindow           = Qt.WindowType.SubWindow           if qt_version == 6 else Qt.SubWindow
Window_SystemMenuHint      = Qt.WindowType.WindowSystemMenuHint if qt_version == 6 else Qt.WindowSystemMenuHint
Window_CloseButtonHint     = Qt.WindowType.WindowCloseButtonHint if qt_version == 6 else Qt.WindowCloseButtonHint
Window_MinimizeButtonHint  = Qt.WindowType.WindowMinimizeButtonHint if qt_version == 6 else Qt.WindowMinimizeButtonHint
Window_MaximizeButtonHint  = Qt.WindowType.WindowMaximizeButtonHint if qt_version == 6 else Qt.WindowMaximizeButtonHint





# QTextCursor move flags
from PyQt.QtGui import QTextCursor   # same in 5 and 6
# from qt_compat import QTextCursor


MoveStart      = QTextCursor.MoveOperation.Start    if qt_version == 6 else QTextCursor.Start
MoveEnd        = QTextCursor.MoveOperation.End      if qt_version == 6 else QTextCursor.End
MoveWordLeft   = QTextCursor.MoveOperation.WordLeft if qt_version == 6 else QTextCursor.WordLeft
MoveWordRight  = QTextCursor.MoveOperation.WordRight if qt_version == 6 else QTextCursor.WordRight
MoveUp         = QTextCursor.MoveOperation.Up       if qt_version == 6 else QTextCursor.Up
MoveDown       = QTextCursor.MoveOperation.Down     if qt_version == 6 else QTextCursor.Down
MoveLeft       = QTextCursor.MoveOperation.Left     if qt_version == 6 else QTextCursor.Left
MoveRight      = QTextCursor.MoveOperation.Right    if qt_version == 6 else QTextCursor.Right

KeepAnchor     = QTextCursor.MoveMode.KeepAnchor    if qt_version == 6 else QTextCursor.KeepAnchor


ItemIsSelectable = Qt.ItemFlag.ItemIsSelectable if qt_version == 6 else Qt.ItemIsSelectable
ItemIsEnabled    = Qt.ItemFlag.ItemIsEnabled    if qt_version == 6 else Qt.ItemIsEnabled
ItemIsEditable   = Qt.ItemFlag.ItemIsEditable   if qt_version == 6 else Qt.ItemIsEditable
ItemIsDragEnabled= Qt.ItemFlag.ItemIsDragEnabled if qt_version == 6 else Qt.ItemIsDragEnabled
ItemIsDropEnabled= Qt.ItemFlag.ItemIsDropEnabled if qt_version == 6 else Qt.ItemIsDropEnabled

ScrollBarAlwaysOn  = Qt.ScrollBarPolicy.ScrollBarAlwaysOn  if qt_version == 6 else Qt.ScrollBarAlwaysOn
ScrollBarAlwaysOff = Qt.ScrollBarPolicy.ScrollBarAlwaysOff if qt_version == 6 else Qt.ScrollBarAlwaysOff
ScrollBarAsNeeded  = Qt.ScrollBarPolicy.ScrollBarAsNeeded  if qt_version == 6 else Qt.ScrollBarAsNeeded

from PyQt.QtGui     import QPainter
from PyQt.QtWidgets import QGraphicsView

# Normalize constants for PyQt6 vs PyQt5
RenderHint_Antialiasing            = QPainter.RenderHint.Antialiasing          if qt_version == 6 else QPainter.Antialiasing
RenderHint_SmoothPixmapTransform   = QPainter.RenderHint.SmoothPixmapTransform if qt_version == 6 else QPainter.SmoothPixmapTransform

AnchorUnderMouse = QGraphicsView.ViewportAnchor.AnchorUnderMouse if qt_version == 6 else QGraphicsView.AnchorUnderMouse

from PyQt.QtWidgets import QAbstractItemView, QTableView

if qt_version == 6:
    NoEditTriggers = QAbstractItemView.EditTrigger.NoEditTriggers
else:
    NoEditTriggers = QTableView.NoEditTriggers

# from qt_compat import NoEditTriggers

# this is a bit differen approach -- is it a mess from earlier?
if qt_version == 6:
    from PyQt6.QtWidgets import QDialogButtonBox
    CQDialogButtonBox = QDialogButtonBox.StandardButton
else:
    from PyQt5.QtWidgets import QDialogButtonBox
    CQDialogButtonBox = QDialogButtonBox




# --- QSqlTableModel EditStrategy ---
from PyQt.QtSql import QSqlTableModel
OnManualSubmit = (
    QSqlTableModel.EditStrategy.OnManualSubmit
    if qt_version == 6 else QSqlTableModel.OnManualSubmit
)
OnRowChange = (
    QSqlTableModel.EditStrategy.OnRowChange
    if qt_version == 6 else QSqlTableModel.OnRowChange
)
OnFieldChange = (
    QSqlTableModel.EditStrategy.OnFieldChange
    if qt_version == 6 else QSqlTableModel.OnFieldChange
)

    # from qt_compat import OnManualSubmit, OnRowChange, OnFieldChange
#------------------------------
if qt_version == 6:
    from PyQt6.QtSql import QSqlRelationalTableModel
    RModel_OnManualSubmit = QSqlRelationalTableModel.EditStrategy.OnManualSubmit
    RModel_OnFieldChange = QSqlRelationalTableModel.EditStrategy.OnFieldChange
    RModel_OnRowChange = QSqlRelationalTableModel.EditStrategy.OnRowChange
else:
    from PyQt5.QtSql import QSqlRelationalTableModel

    # Qt5 - EditStrategy enum is directly accessible
    RModel_OnManualSubmit = QSqlRelationalTableModel.OnManualSubmit
    RModel_OnFieldChange = QSqlRelationalTableModel.OnFieldChange
    RModel_OnRowChange = QSqlRelationalTableModel.OnRowChange

# from qt_compat import RModel_OnManualSubmit, RModel_OnFieldChange, RModel_OnRowChange



# --- QHeaderView ResizeMode ---
from PyQt.QtWidgets import QHeaderView
HeaderInteractive = QHeaderView.ResizeMode.Interactive if qt_version == 6 else QHeaderView.Interactive
HeaderStretch     = QHeaderView.ResizeMode.Stretch    if qt_version == 6 else QHeaderView.Stretch
HeaderFixed       = QHeaderView.ResizeMode.Fixed      if qt_version == 6 else QHeaderView.Fixed

# --- QTableView SelectionBehavior ---
from PyQt.QtWidgets import QTableView
SelectRows      = QTableView.SelectionBehavior.SelectRows      if qt_version == 6 else QTableView.SelectRows
SelectColumns   = QTableView.SelectionBehavior.SelectColumns   if qt_version == 6 else QTableView.SelectColumns
SelectItems     = QTableView.SelectionBehavior.SelectItems     if qt_version == 6 else QTableView.SelectItems
ExtendedSelection = (
    QTableView.SelectionMode.ExtendedSelection if qt_version == 6 else QTableView.ExtendedSelection )

    # from qt_compat import SelectRows, SelectItems,ExtendedSelection


# --- Moved classes helper ---
def _compat_class(gui_cls, widgets_cls):
    try:
        return getattr(QtGui, gui_cls)
    except AttributeError:
        return getattr(QtWidgets, widgets_cls)

QAction        = _compat_class("QAction", "QAction")
QActionGroup   = _compat_class("QActionGroup", "QActionGroup")
QShortcut      = _compat_class("QShortcut", "QShortcut")
QKeySequence   = _compat_class("QKeySequence", "QKeySequence")
QTextCursor    = _compat_class("QTextCursor", "QTextCursor")

# --- Convenience helpers ---
def set_icon_visible_in_menu(action, visible=True):
    if qt_version == 5:
        action.setIconVisibleInMenu(visible)

def make_action(text, icon=None, parent=None, shortcut=None, triggered=None):
    act = QAction(text, parent)
    if icon:
        act.setIcon(icon)
    if shortcut:
        act.setShortcut(shortcut)
    if triggered:
        act.triggered.connect(triggered)
    set_icon_visible_in_menu(act, True)
    return act

# --- Common widgets ---
QMainWindow = QtWidgets.QMainWindow
QToolBar    = QtWidgets.QToolBar
QLabel      = QtWidgets.QLabel
QMessageBox = QtWidgets.QMessageBox

# --- Exported names ---
__all__ = [
    "PyQt", "qt_version", "Qt",
    "QApplication", "QWidget", "QMainWindow", "QToolBar", "QLabel", "QMessageBox",
    "QAction", "QActionGroup", "QShortcut", "QKeySequence", "QTextCursor",
    "exec_app",
    "DisplayRole", "EditRole", "CheckStateRole", "ToolTipRole", "StatusTipRole",
    "DecorationRole", "TextAlignmentRole",
    "AlignCenter", "AlignLeft", "AlignRight", "AlignTop", "AlignBottom",
    "Horizontal", "Vertical",
    "WindowNoState", "WindowMinimized", "WindowMaximized",
    "WindowFullScreen", "WindowActive",
    "InsertAtTop", "InsertAtCurrent", "InsertAtBottom",
    "InsertAfterCurrent", "InsertBeforeCurrent", "NoInsert",
    "OnManualSubmit", "OnRowChange", "OnFieldChange",
    "HeaderInteractive", "HeaderStretch", "HeaderFixed",
    "set_icon_visible_in_menu", "make_action",
    "SelectRows", "SelectColumns", "SelectItems",

]


# ---- eof