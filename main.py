
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFilter, ImageTk
import os

# 1.load image to be water marked

file_path = os.getcwd()

# 1.load image to be water marked
# image_backround = Image.open("backround.png")
# 2.load water mark image
# image_water_mark = Image.open("water_mark.png")

# 3 mix images

# image_backround = image_backround.copy()
# image_backround.paste(image_water_mark)
# image_backround.save("edited.png", quality=100)

# image_backround.show()


# 4. Create Tkinter window and open the image on the backround image on
# thewindow

background_loaded = False
water_mark_path_loaded = False
background_path_loaded = False
# opens the image to be water marked


def open_file():
    # global canvas
    global background_loaded
    global display_image
    global background_path_loaded
    file_name = filedialog.askopenfile().name
    background_path_loaded = file_name
    print("this", file_name)
    pilImage = Image.open(file_name)
    width, height = pilImage.size
    display_image = ImageTk.PhotoImage(pilImage)
    # canvas.config(width=width, height=height)
    # width = round(width/2)
    # height = round(height/2)
    print(width, height)
    canvas.delete("all")
    canvas.config(width=width, height=height)
    canvas.create_image((0, 0), image=display_image, anchor="nw")
    # canvas.itemconfigure(show_image, height=height,
    # width=width, image=display_image)
    background_loaded = True

# opens the water mark
# Only file path is used


def get_water_mark():
    global water_mark_path_loaded
    file_name = filedialog.askopenfile().name
    water_mark_path_loaded = file_name
    return file_name


# water_marks the image


window = tk.Tk()
canvas = tk.Canvas(window, height=1200, width=1200)
# image_pillow = Image.open("./girl.webp")
# image_pillow = ImageTk.PhotoImage(image_pillow)
# image_to_config = image_pillow
# show_image = canvas.create_image((600, 600), image=image_to_config)
canvas.pack()


def get_coordinates(event):
    canvas.itemconfigure(tag, text='({x}, {y})'.format(x=event.x, y=event.y))
    # print(event.x, event.y)


def getorigin(eventorigin):

    global x, y
    x = eventorigin.x
    y = eventorigin.y
    if background_loaded:
        print(x, y)


def getorigin2(eventorigin):
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

        # mix images
        width, height = image_water_mark.size
        # get the center of the picture
        width = round(width / 2)
        height = round(height / 2)

        image_backround = image_backround.copy()
        image_backround.paste(image_water_mark, (x - width, y - height))
        image_backround.save("edited.png", quality=100)

        # ----------------
        display_image = ImageTk.PhotoImage(image_backround)
    # canvas.config(width=width, height=height)
    # width = round(width/2)
    # height = round(height/2)
        width, height = image_backround.size
        print(width, height)
        canvas.delete("all")
        canvas.config(width=width, height=height)
        canvas.create_image((0, 0), image=display_image, anchor="nw")
    # canvas.itemconfigure(show_image, height=height,
    # width=width, image=display_image)

        # print("pöö")


canvas.bind("<Button 1>", getorigin)
canvas.bind("<Button 3>", getorigin2)


canvas.bind('<Motion>', get_coordinates)
# handle <Alt>+<Tab> switches between windows
canvas.bind('<Enter>', get_coordinates)
tag = canvas.create_text(10, 10, text='', anchor='nw')


greeting = tk.Label(text="Hello, Tkinter")
greeting.pack()

open_file_button = tk.Button(
    master=window, text="Open file", command=open_file)

open_water_mark = tk.Button(
    master=window, text="Open water mark", command=get_water_mark)
open_file_button.pack()
open_water_mark.pack()


window.mainloop()
