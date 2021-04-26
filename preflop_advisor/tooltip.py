#!/usr/bin/env python3

import tkinter as tk
from PIL import ImageTk, Image


class CreateToolTip(object):
    '''
    create a tooltip for a given widget
    '''

    def __init__(self, widget, text='widget info', pic=False):
        self.widget = widget
        self.text = text
        self.pic = pic
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 50  # 25
        y += self.widget.winfo_rooty() + 60  # 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        if not self.pic:
            label = tk.Label(self.tw, text=self.text, justify='left',
                             background='yellow', relief='solid', borderwidth=1,
                             font=("courier", "8", "normal"))
            label.pack(ipadx=1)
        else:
            load = Image.open(self.text)
            load = load.resize((800, 450)) #change to default sizing
            render = ImageTk.PhotoImage(load)
            img = tk.Label(self.tw, image=render)
            img.image = render
            img.pack(ipadx=1)
    def close(self, event=None):
        if self.tw:
            self.tw.destroy()


# testing ...
if (__name__ == '__main__'):
    root = tk.Tk()
    btn1 = tk.Button(root, text="button 1")
    btn1.pack(padx=10, pady=5)
    button1_ttp = CreateToolTip(btn1, "mouse is over button 1")
    btn2 = tk.Button(root, text="button 2")
    btn2.pack(padx=10, pady=5)
    button2_ttp = CreateToolTip(btn2, "mouse is over button 2")
    root.mainloop()
