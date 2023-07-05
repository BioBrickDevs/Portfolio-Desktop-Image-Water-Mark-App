import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFilter, ImageTk
import os

file_path = os.getcwd()
background_loaded = False
water_mark_path_loaded = False
background_path_loaded = False


def open_image_to_be_water_marked():
    global background_loaded
    global display_image
    global background_path_loaded
    try:
        file_name = filedialog.askopenfile().name
        background_path_loaded = file_name
        pilImage = Image.open(file_name)
        width, height = pilImage.size
        display_image = ImageTk.PhotoImage(pilImage)
        canvas.delete("all")
        canvas.config(width=width, height=height)
        canvas.create_image((0, 0), image=display_image, anchor="nw")
        background_loaded = True
    except AttributeError:
        pass


def get_water_mark():
    global water_mark_path_loaded
    try:
        file_name = filedialog.askopenfile().name
        water_mark_path_loaded = file_name
    except AttributeError:
        pass


def get_coordinates(event):
    canvas.itemconfigure(tag, text='({x}, {y})'.format(x=event.x, y=event.y))


def get_cordinates(eventorigin):
    global x, y
    x = eventorigin.x
    y = eventorigin.y


def water_mark_the_image(eventorigin):
    global water_mark_path_loaded
    global background_path_loaded
    global x, y
    global display_image
    x = eventorigin.x
    y = eventorigin.y
    if background_loaded and water_mark_path_loaded:
        # get image paths and paste water mark to backround and display
        image_backround = Image.open(background_path_loaded)
        image_water_mark = Image.open(water_mark_path_loaded)
        width, height = image_water_mark.size
        # get the center of the picture
        width = round(width / 2)
        height = round(height / 2)
        # mix images
        image_backround = image_backround.copy()
        image_backround.paste(image_water_mark, (x - width, y - height))
        image_backround.save("edited.png", quality=100)

        # ----------------
        display_image = ImageTk.PhotoImage(image_backround)
        width, height = image_backround.size
        canvas.delete("all")
        canvas.config(width=width, height=height)
        canvas.create_image((0, 0), image=display_image, anchor="nw")


def save_file():
    if background_loaded and water_mark_path_loaded:
        try:
            file_name = filedialog.asksaveasfile().name
            image = Image.open("edited.png")
            image.save(file_name)
        except AttributeError:
            print("No file.")


window = tk.Tk()
window.title("Water mark Application")
canvas = tk.Canvas(window, height=1200, width=1200)
canvas.pack()
canvas.bind("<Button 1>", get_cordinates)  # left mouse button gets cordinates
# right mouse button gets cordinates
canvas.bind("<Button 3>", water_mark_the_image)
canvas.bind('<Motion>', get_coordinates)  # mouse movement gets cordinates
# handle <Alt>+<Tab> switches between windows
canvas.bind('<Enter>', get_coordinates)
tag = canvas.create_text(10, 10, text='', anchor='nw')
greeting = tk.Label(
    text="""First open image to be water marked. Then open the water mark
    and stamp the water mark with right mouse button.""")
greeting.pack()

open_file_button = tk.Button(
    master=window, text="Open image to be water marked",
    command=open_image_to_be_water_marked)

open_water_mark = tk.Button(
    master=window, text="Open water mark", command=get_water_mark)

save_water_mark = tk.Button(master=window, text="Save", command=save_file)
open_file_button.pack()
open_water_mark.pack()
save_water_mark.pack()
window.mainloop()
