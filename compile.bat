rd /s /q dist
pyinstaller main.py --onefile --noconsole
xcopy data dist\data\