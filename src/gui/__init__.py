from __future__ import annotations

from typing import Callable

from aqt.qt import pyqtBoundSignal, pyqtSignal


# Copied from Anki and used to fix typing issues in older versions we support
# TODO: drop this in the future
def qconnect(signal: Callable | pyqtSignal | pyqtBoundSignal, func: Callable) -> None:
    """Helper to work around type checking not working with signal.connect(func)."""
    signal.connect(func)  # type: ignore
