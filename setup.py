from distutils.core import setup
import py2exe
import sys

# Add any missing modules that need to be included
includes = ["tkinter", "sqlite3"]

# Add any data files that need to be included
data_files = []

sys.argv.append("py2exe")

setup(
    options = {
        "py2exe": {
            "compressed": 1,
            "optimize": 2,
            "includes": includes,
            "bundle_files": 1
        }
    },
    zipfile = None,
    console = [{"script": "main.py"}],
    data_files = data_files
)
