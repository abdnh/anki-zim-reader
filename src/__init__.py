import sys
from pathlib import Path

if sys.argv[1] == "serve":
    from .server import serve_file

    serve_file(Path(sys.argv[2]))
elif "pytest" not in sys.modules:
    from . import main
