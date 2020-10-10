call client_venv\Scripts\activate
call py -m PyInstaller --noconfirm --onefile --windowed --icon "web/bot_icon.ico" --add-data "web/;web/" "main.py"