from tkinter import Tk, Label
import PIL.ImageTk
import PIL.Image
from keyboard import is_pressed
from win32gui import GetCursorPos
from math import sqrt
from time import sleep
from sys import exit

version = 'v1.2.0'

start = False
drag = False
drag_id = ''

def close_window():
    root.withdraw()
    exit() # Ensures python window exits

def resize():
    window_x = root.winfo_width()
    window_y = root.winfo_height()
    if window_x > window_y:
        root.geometry('{0}x{0}'.format(window_x))
    elif window_y > window_x:
        root.geometry('{0}x{0}'.format(window_y))

def dragging(event):
    global drag_id
    global drag
    if drag_id == '':
        pass
    else:
        root.after_cancel(drag_id)
        drag = True
    drag_id = root.after(100, stop_drag)

def stop_drag():
    global drag_id
    global drag
    drag = False
    drag_id = ''

root = Tk()
root.resizable(width=True, height=True)
root.geometry('640x640')
root.maxsize(width=640, height=640) # Max size is the original image size
root.minsize(width=124, height=124)
root.title('osu!cat ' + version)
root.protocol('WM_DELETE_WINDOW', close_window)

screen_x = root.winfo_screenwidth()
screen_y = root.winfo_screenheight()
add = (screen_x - screen_y)/2

x_1 = add + screen_y/6
x_2 = x_1 + screen_y/3
x_3 = x_2 + screen_y/3
y_1 = screen_y/6
y_2 = y_1 + screen_y/3
y_3 = y_2 + screen_y/3
ix_1 = screen_y/3 + add
ix_2 = ix_1 + screen_y/3
iy_1 = screen_y/3
iy_2 = iy_1 + screen_y/3

d_bias = screen_x/8


frame_points = {'A': (x_1, y_1),
                'B': (x_2, y_1),
                'C': (x_3, y_1),
                'D': (x_1, y_2),
                'E': (x_2, y_2),
                'F': (x_3, y_2),
                'G': (x_1, y_3),
                'H': (x_2, y_3),
                'I': (x_3, y_3),
                'IA': (ix_1, iy_1),
                'IB': (ix_2, iy_1),
                'IC': (ix_1, iy_2),
                'ID': (ix_2, iy_2)}

def find_distance(cx, cy, px, py):  # Calculates the distance from the cursor position to a point
    d = sqrt((px-cx)**2 + (py-cy)**2)  # Euclidean metric
    return d

def find_frame(cx, cy, f):

    best_d = [10000, 'NaN']
    for key, value in frame_points.items():

        d = find_distance(cx, cy, value[0], value[1])

        if key == f:
            d -= d_bias

        if d < best_d[0]:
            best_d[0] = d
            best_d[1] = key

    return best_d[1]

print('Bongo Cat Live Cam ' + version)
print('----------------------------------------------------------------------------------------------------------------------')
print('Disclaimer: There is a high probability you will experience some bugs or that the program will now work at all.\n'
      'This program will also most likely not work on resolutions where the height is bigger than the width and there\n'
      'is no support for custom ingame resolutions or sensitivities. You have been warned.')
print('----------------------------------------------------------------------------------------------------------------------')
print('Before you can use this program you need to configure some things')
while True:
    k1 = input('Key 1: ')
    k2 = input('Key 2: ')
    arrowKeys = ["up", "down", "left", "right"]
    if len(k1) == 0 or k1 in arrowKeys and len(k2) == 0 or k2 in arrowKeys:
        break;
    else:
        print('Keys can only be 1 character long, or arrow keys such as \'up\', \'right\', \'left\', or \'down\'')

print('(Type 0 for tablet and 1 for mouse)')
while True:
    i_type = input('Tablet or mouse: ')
    if i_type == '0':
        cursor_device = 'tablet'
        break
    elif i_type == '1':
        cursor_device = 'mouse'
        break
    else:
        print('Invalid input')

print('(Type 0 for no and 1 for yes)')
while True:
    i_type = input('Use chroma key green background?: ')
    if i_type == '0':
        background = 'standard'
        start = True
        break
    elif i_type == '1':
        background = 'green'
        start = True
        break
    else:
        print('Invalid input')

print('All done! To reconfigure, just close and relaunch the application')
print('Note: When re-sizing, hit k1 or k2 to reload the image!')


#preload all images
hit_images = {
    1: PIL.Image.open("cat/KeyTapHand1.png"),
    2: PIL.Image.open("cat/KeyTapHand2.png")
}

cursor_images = {}
for key in frame_points.keys():
    cursor_images[key] = PIL.Image.open("cat/{0}/{1}/Hand {2}.png".format(cursor_device, background, key))

default_img = PIL.ImageTk.PhotoImage(cursor_images['A'])
image_label = Label(root, image=default_img)
image_label.image = default_img
image_label.pack()

f = 'A'
f_prev = f
w_size = root.winfo_width, root.winfo_height
w_size_prev = w_size
k1_p_prev = False
k2_p_prev = False
first_iteration = True
force_update = True
last_hit = 1

def iterate():
    global f, f_prev, k1_p_prev, k2_p_prev, last_hit, drag, w_size_prev, w_size, first_iteration, force_update
    if drag:
        root.after(5, iterate)
        return

    k1_p = is_pressed(k1)
    k2_p = is_pressed(k2)
    x, y = GetCursorPos()
    f = find_frame(x, y, f)

    base_img = cursor_images[f]

    def forceUpdate():
        base_img = cursor_images[f].resize((root.winfo_width(), root.winfo_height()), PIL.Image.ANTIALIAS)
        n_base_img = PIL.ImageTk.PhotoImage(base_img)
        image_label.configure(image=n_base_img)
        image_label.image = n_base_img
        root.update()

    if first_iteration:
        first_iteration = False
        forceUpdate()
        root.after(0, iterate)
        return

    resize()

    if f == f_prev and k1_p == k1_p_prev and k2_p == k2_p_prev:
        root.after(5, iterate)
        return

    if k1_p or k2_p:
        force_update = True
        if (k1_p and not k1_p_prev) or (not k2_p and k2_p_prev):
            final_hit = 1
        elif (k2_p and not k2_p_prev) or (not k1_p and k1_p_prev):
            final_hit = 2
        else:
            final_hit = last_hit

        last_hit = final_hit
        final_hit_img = hit_images[final_hit]
        composite_image = PIL.Image.alpha_composite(base_img, final_hit_img)
        composite_image.thumbnail((root.winfo_width(), root.winfo_height()), PIL.Image.ANTIALIAS)
        n_base_img = PIL.ImageTk.PhotoImage(composite_image)
    else:
        base_img = base_img.resize((root.winfo_width(), root.winfo_height()), PIL.Image.ANTIALIAS)
        n_base_img = PIL.ImageTk.PhotoImage(base_img)

    f_prev = f
    k1_p_prev = k1_p
    k2_p_prev = k2_p

    image_label.configure(image=n_base_img)
    image_label.image = n_base_img
    root.update()
    root.after(5, iterate)

if start:
    root.bind('<Configure>', dragging)
    root.after(0, iterate)
    root.mainloop()
