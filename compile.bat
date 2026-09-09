set "TCL_LIBRARY="
set "TK_LIBRARY="

rem %1 is the folder of the pyinstaller
%1/pyinstaller main.py --exclude-module pkg_resources --onefile --noconsole --icon=icons\vampire.ico
:
:: kopie dist/main.exe c:/bin/The_count.exe
