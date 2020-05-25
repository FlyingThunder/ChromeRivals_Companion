import sys
import PyQt5
import requests
import datetime
from cx_Freeze import setup, Executable


build_exe_options = {
    "packages": ["sys", "requests", "datetime"],
    "includes": ["Output"]
}

base = None
if sys.platform == "win32":
	base = "Win32GUI"

setup(  name = "CRComp",
        version = "0.1",
        description = "ChromeRivals Companion App",
        options = {"build_exe": build_exe_options},
        executables = [Executable("QT MainWindow Test.py", base=base)])