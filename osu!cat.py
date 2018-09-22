from tkinter import Tk, Label
import PIL.ImageTk
import PIL.Image
from keyboard import is_pressed
from win32gui import GetCursorPos
from math import sqrt
from time import sleep


def close_window():
    root.withdraw()
    global LOOP
    LOOP = False


root = Tk()
root.resizable(width=False, height=False)
root.title('osu!cat v1.0.0')
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

print('Bongo Cat Live Cam v1.0.0')
print('----------------------------------------------------------------------------------------------------------------------')
print('Disclaimer: There is a high probability you will experience som bugs or that the program will now work at all.\n'
      'This program will also most likely not work on resolutions where the height is bigger than the width, it will most\n'
      'likely use much of your cpu and there is no support for custom ingame resolutions. You have been warned.')
print('----------------------------------------------------------------------------------------------------------------------')
print('Before you can use this program you need to configure key 1, key 2 and tablet/mouse')
while True:
    k1 = input('Key 1: ')
    k2 = input('Key 2: ')
    if len(k1) == 1 and len(k2) == 1:
        break
    else:
        print('Keys can only be 1 character long')

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

print('All done! To reconfigure, just close and relaunch the application')

open_img = PIL.Image.open("cat/{0}/Hand A.png".format(cursor_device))
base_img = PIL.ImageTk.PhotoImage(open_img)
hit1_img = PIL.Image.open("cat/KeyTapHand.png")
hit2_img = PIL.Image.open("cat/KeyTapHand2.png")

#l_xyf = StringVar()  # Label string for x and y cursor position + current base frame

image_label = Label(root, image=base_img) # ,textvariable=l_xyf, compound=CENTER)
image_label.image = base_img
image_label.pack()

f = 'A'
last_hit = 0
LOOP = True
while LOOP:
    k1_p = is_pressed(k1)
    k2_p = is_pressed(k2)
    x, y = GetCursorPos()
    f = find_frame(x, y, f)

    n_open_img = PIL.Image.open("cat/{0}/Hand {1}.png".format(cursor_device, f))

    if k1_p or k2_p:

        final_hit_img = hit1_img

        if last_hit == 0:

            if k1_p:

                final_hit_img = hit1_img
                last_hit = 1

            elif k2_p:

                final_hit_img = hit2_img
                last_hit = 0

        elif last_hit == 1:

            if k2_p:

                final_hit_img = hit2_img
                last_hit = 0

            elif k1_p:

                final_hit_img = hit1_img
                last_hit = 1

        test_var = PIL.Image.alpha_composite(n_open_img, final_hit_img)
        n_base_img = PIL.ImageTk.PhotoImage(test_var)
    else:
        n_base_img = PIL.ImageTk.PhotoImage(n_open_img)

    image_label.configure(image=n_base_img)
    image_label.image = n_base_img

    #l_xyf.set('x: ' + str(x) + ' ' + 'y: ' + str(y) + ' ' + 'frame: ' + f)  # Updates x, y and frame values
    root.update()
    sleep(0.005)
