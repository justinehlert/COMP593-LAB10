"""
Description:
  Graphical user interface that displays the official artwork for a
  user-specified Pokemon, which can be set as the desktop background image.

Usage:
  python poke_image_viewer.py
"""
from tkinter import *
from tkinter import ttk
import tkinter as tk
import os
import ctypes
import image_lib
import poke_api

# Get the script and images directory
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, 'images')
icon_url = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png'

# TODO: Create the images directory if it does not exist

try:
    os.mkdir(images_dir)
except FileExistsError:
    print("Image dir already exists")

def download_icon(icon_url, name):
    """Downloads the Pokeball icon image and saves
    in the image cache

    Args:
      icon_url (str): URL of the icon
      name (str): Name of the file to be saved as

    Returns:
      (str): The path to the saved file
    
    """

    imageData = image_lib.download_image(icon_url)
    imageDir = os.path.join(images_dir, name)
    image_lib.save_image_file(imageData, imageDir)
    return imageDir

icon_dir = download_icon(icon_url, 'poke-ball.png')

pokemon_list = poke_api.get_pokemon_list('10')
poke_api.download_artwork(pokemon_list, images_dir)

# Create the main window
root = Tk()
root.title("Pokemon Viewer")

# TODO: Set the icon
app_id = 'COMP593.PokemonImageViewer'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

icon = tk.PhotoImage(file=icon_dir)
root.iconphoto(False, icon)


# TODO: Create frames

root.rowconfigure(0, weight=100)
root.rowconfigure(1, weight=50)
root.rowconfigure(2, weight=60)

frm_top = ttk.Frame(root)
frm_top.grid(row=0, column=0, columnspan=1, sticky=NSEW)

frm_mid = ttk.Frame(root)
frm_mid.grid(row=1, column=0, columnspan=1, sticky=NSEW)

frm_btm = ttk.Frame(root)
frm_btm.grid(row=2, column=0, columnspan=1, sticky=NSEW)

# TODO: Populate frames with widgets and define event handler functions

def handle_poke_sel(event):
    
    sel_pkm_index = cbox_img_sel.current()
    icon['file'] =  os.path.join(images_dir, image_list[sel_pkm_index])
    return

def set_desktop():
    sel_pkm_index = cbox_img_sel.current()
    icon = os.path.join(images_dir, image_list[sel_pkm_index])
    image_lib.set_desktop_background_image(image_path=icon)
    return

lbl_image = ttk.Label(frm_top, image=icon)
lbl_image.grid(padx=10,pady=10)

image_list = []
for file in os.listdir(images_dir):
    full_path = os.path.join(images_dir, file)
    if os.path.isfile(full_path):
      image_list.append(file)
    
cbox_img_sel = ttk.Combobox(frm_mid, values=image_list, state='readonly')
cbox_img_sel.grid(row=0,column=0)
cbox_img_sel.bind('<<ComboboxSelected>>', handle_poke_sel)

set_desktop_btn = ttk.Button(frm_btm, text="Set Desktop", command=set_desktop)
set_desktop_btn.grid(row=0,column=0)


root.mainloop()