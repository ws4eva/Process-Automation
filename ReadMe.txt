# Process automation Python executable

- What it does:
This is a Python script to scan through layers of folder directories to find files in a specific format from local PCs then copy to a dedicated archive directory. Files are renamed in the format of [SN]_[Rig ID]_Summary_[Timestamp].csv

The executable will run from the background and re-scan every X hours as specified in the config file.
To automatically start the application on Windows PC, add it on Task Scheduler with System startup option.

Build command:
pyinstaller -w --onefile --icon=logo.ico --add-data "version_info.ini;." FT_Result_uploader.py 
