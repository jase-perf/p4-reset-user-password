#!/bin/zsh
pyinstaller --onefile -i "./images/bulk_creator_icon.icns" -n "P4 Bulk Creator" --distpath ./bin ./app/main.py