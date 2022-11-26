import sys
from pathlib import Path

if len(sys.argv) > 1:
    from .server import serve_file

    serve_file(Path(sys.argv[1]))
