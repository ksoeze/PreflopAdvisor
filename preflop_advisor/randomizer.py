#!/usr/bin/env python3

import tkinter as tk
from configparser import ConfigParser
from random import randint


class RandomButton(tk.Frame):
    def __init__(self, root, config):
        tk.Frame.__init__(self, root)
        self.button_height = int(config["ButtonHeight"])
        self.button_width = int(config["ButtonWidth"])
        self.button_pad = int(config["ButtonPad"])
        self.fontsize = config["FontSize"]
        self.font = config["Font"]
        self.background = config["Background"]

        self.text_lable = tk.StringVar()
        self.button = self.get_rand_button()

    def get_rand_button(self, init_label="100"):
        button = tk.Button(
            self, textvariable=self.text_lable, command=self.on_button_clicked)
        button.config(height=self.button_height,
                      width=self.button_width,
                      bg=self.background,
                      font=(self.font, self.fontsize),
                      padx=self.button_pad, pady=self.button_pad)
        self.text_lable.set(init_label)
        button.grid(row=0, column=0)
        return button

    def on_button_clicked(self):
        self.text_lable.set(str(randint(0, 100)))


def test(root):
    configs = ConfigParser()
    configs.read("config.ini")
    settings = configs["PositionSelector"]
    rand_button = RandomButton(root, settings)
    rand_button.grid(row=0, column=0)
    return


if (__name__ == '__main__'):
    root = tk.Tk()
    test(root)
    root.mainloop()
