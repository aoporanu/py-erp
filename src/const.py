import os
from tkinter import N, W, S, E

import PIL.Image
import PIL.ImageTk

ICON = os.path.normpath("database_4.ico")
color = "#333333"
SEL_COLOR = "#273f5c"
FOREGROUND = "#cecece"
saveico = os.path.normpath("data/floppy_disk_blue.png")
NEW_ICO = os.path.normpath("data/new_file.png")
NEW_USER_GROUP = os.path.normpath(
    "/home/adyopo/Projects/py-erp/data/user_group_new.png"
)
SETTINGS_ICO = os.path.normpath("/home/adyopo/Projects/py-erp/data/settings_ico2.png")
NEW_DOC = os.path.normpath("/home/adyopo/Projects/py-erp/data/new_doc.png")
NEXT_ICO = os.path.normpath("/home/adyopo/Projects/py-erp/data/next.png")
SEARCH_ICO = os.path.normpath("/home/adyopo/Projects/py-erp/data/search.png")
VIEW_REFRESH_ICO = os.path.normpath(
    "/home/adyopo/Projects/py-erp/data/view_refresh.png"
)
EDIT_ADD = os.path.normpath("/home/adyopo/Projects/py-erp/data/edit_add.png")
tmp4 = PIL.Image.open(EDIT_ADD).resize((25, 25), PIL.Image.ANTIALIAS)
ncico = PIL.Image.open(NEW_USER_GROUP).resize((32, 32), PIL.Image.ANTIALIAS)
ADD_TO_CART = os.path.normpath("/home/adyopo/Projects/py-erp/data/cart_add.png")
tmp = PIL.Image.open(ADD_TO_CART).resize((25, 25), PIL.Image.ANTIALIAS)
REMOVE_FROM_CART = os.path.normpath("/home/adyopo/Projects/py-erp/data/cart_remove.png")
tmp2 = PIL.Image.open(REMOVE_FROM_CART).resize((25, 25), PIL.Image.ANTIALIAS)
genico = PIL.Image.open(NEW_DOC).resize((32, 32), PIL.Image.ANTIALIAS)
EDIT_ADD = os.path.normpath("/home/adyopo/Projects/py-erp/data/edit_add.png")
tmp4 = PIL.Image.open(EDIT_ADD).resize((25, 25), PIL.Image.ANTIALIAS)
tmp6 = PIL.Image.open(SEARCH_ICO).resize((20, 20), PIL.Image.ANTIALIAS)
tmp7 = PIL.Image.open(VIEW_REFRESH_ICO).resize((20, 20), PIL.Image.ANTIALIAS)
tmp_modify = PIL.Image.open(SETTINGS_ICO).resize((20, 20), PIL.Image.ANTIALIAS)
tmp_extra = PIL.Image.open(SETTINGS_ICO).resize((20, 20), PIL.Image.ANTIALIAS)
sty = N + W + S + E


def cmp(a, b):
    return (a > b) - (a < b)
