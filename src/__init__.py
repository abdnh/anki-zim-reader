import sys

if "pytest" not in sys.modules and "anki" in sys.modules:
    from . import main
