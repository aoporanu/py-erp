import os

import PIL.Image
import PIL.ImageTk

ICON = os.path.normpath('database_4.ico')
color = '#333333'
SEL_COLOR = '#273f5c'
FOREGROUND = "#cecece"
saveico = os.path.normpath('data/floppy_disk_blue.png')
NEW_ICO = os.path.normpath('data/new_file.png')
NEW_USER_GROUP = os.path.normpath('data/user_group_new.png')
SETTINGS_ICO = os.path.normpath('data/settings_ico2.png')
NEW_DOC = os.path.normpath('data/new_doc.png')
NEXT_ICO = os.path.normpath('data/next.png')
SEARCH_ICO = os.path.normpath('data/search.png')
VIEW_REFRESH_ICO = os.path.normpath('data/view_refresh.png')
SYMBOL_REMOVE = os.path.normpath('data/symbol_remove.png')
tmp5 = PIL.Image.open(SYMBOL_REMOVE).resize((25, 25), PIL.Image.ANTIALIAS)
EDIT_ADD = os.path.normpath('data/edit_add.png')
tmp4 = PIL.Image.open(EDIT_ADD).resize((25, 25), PIL.Image.ANTIALIAS)