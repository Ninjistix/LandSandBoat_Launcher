@echo off
REM Install required Python packages
py -3 -m pip install psutil

REM Launch the GUI script
start "" pyw launcher_gui.pyw