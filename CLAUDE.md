# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`m_scope` is a PyQt desktop app for microscope work: a camera tab (live capture / stills),
an overlay tab (align a reticle or second image over a base image, with blend modes and
blink comparison), and a notes tab (item code + date drive the saved file-name stem).

Written against **QtPy**, so it runs on either PyQt5 or PyQt6. Never import `PyQt5` or
`PyQt6` directly — always `from qtpy...`.

## Running

    python main.py

`main.py` is the launcher: it imports `adjust_path`, `chdir`s to the script directory, then
calls `m_scope.main()`. The `chdir` matters — relative paths like `./misc/...` in
`parameters.py` and the window icon assume the project directory is cwd.

Ask which virtualenv is in use before running or asserting anything about the environment;
see `.claude/skills/run-m-scope/SKILL.md` for the venvs available and their Qt bindings.

## Imports come from outside this directory

`adjust_path.py` inserts a list of sibling project directories into `sys.path`. Several
modules imported by name here are **not** in this directory:

| import | actually lives in |
|---|---|
| `camera_capture_widget` | `../pyqt_by_example/tabs/more/` |
| `image_overlay_view`    | `../pyqt_by_example/` |
| `gui_qt_ext`            | `../rshlib/rshlib_qt/` |
| `app_global_abc`        | `../rshlib/app_services/` |

Those files are outside the project — read them to understand behavior, but do not edit
them unless asked.

When an import fails, suspect `adjust_path.py` before suspecting the code. It derives
`src_root` by looking for `/pyqt_by_example` in cwd, which is never present when running
m_scope, so it always takes the hostname fallback — and this machine (`KingHomer`) is not
in that table, so `src_root` lands on `/mnt/WIN_D/russ/0000/python00/python3`, which does
not exist here. Every `f"{src_root}/..."` insert is therefore dead. The app works only
because of the six hardcoded `/mnt/8ball1/...` inserts further down the file. If a
sibling-project import breaks, add or fix a hardcoded insert there.

## Module conventions

- Every module opens with

      if __name__ == "__main__":
          import main   # noqa  stops auto removal by pycln

  so that running any single file in Spyder launches the whole app. Keep this block when
  adding a module; the `# noqa` comment stops pycln from stripping the import.
- `AppGlobal` (`app_global.py`) is a class-level namespace, never instantiated — its
  `__init__` deliberately raises. `MainWindow.__init__` populates `AppGlobal.controller`
  and `AppGlobal.parameters`; other modules read them via `from app_global import AppGlobal`.
- `parameters.py` is an ini-file-as-code. `Parameters.choose_mode()` calls one or more
  `mode_*` methods; switching configuration means commenting lines in and out there, not
  editing an external config file.
- `# ---- name` comments are Spyder outline markers. Preserve them, and add them for new
  sections.

## Do not edit

- `old/ver00/`, `old/ver01/` — frozen snapshots of earlier versions.
- `m_scope_old.py` — superseded by `m_scope.py`, kept for reference.
- `russ_util/` — general-purpose shell utilities, not part of this app.
- `qtn_basic_app.py` — a minimal QtPy template kept as a reference example.

Stills written by the app land in the project root as `still_<timestamp>.jpg`, and `output/`
is a scratch directory; neither is source.

## Environment gotchas

- The shell exports `QT_API=pyqt5`. Under a PyQt6-only venv, qtpy warns
  `Selected binding 'pyqt5' could not be found; falling back to 'pyqt6'` and then works.
  Set `QT_API=pyqt6` for that venv rather than treating the warning as a bug.
- `russ_util/spy_py_13_qt_6.sh` activates `py_13_qt6`, which does not exist — the real
  directory is `py3_13_qt6`.

There are no tests, no lint config, and no package manifest. Do not add them unasked.
