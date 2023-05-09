from distutils.core import setup
import py2exe
import sys

# Add any missing modules that need to be included
includes = ["tkinter", "sqlite3", "pillow"]

# Add any data files that need to be included
data_files = ["img.png"]

# Add your top-level modules to the packages list
packages = [
    'calculate_restore_page',
    'db_helper',
    'enums',
    'info_page',
    'interoperational_control_page',
    'main',
    'patient_parameters',
    'select_patient_page',
]

sys.argv.append("py2exe")

setup(
    options={
        "py2exe": {
            "compressed": 1,
            "optimize": 2,
            "includes": includes,
            "packages": packages,
            "bundle_files": 1,
        }
    },
    zipfile=None,
    console=[{"script": "main.py"}],
    data_files=data_files,
)
