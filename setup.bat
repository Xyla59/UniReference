@echo off
pyinstaller --noconfirm --onedir --console --add-data "C:/Users/xande/OneDrive/Documents/UniReference/inputFiles;inputFiles/" --add-data "C:/Users/xande/OneDrive/Documents/UniReference/outputFiles;outputFiles/" "C:/Users/xande/OneDrive/Documents/UniReference/UniReference.py"
