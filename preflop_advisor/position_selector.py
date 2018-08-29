#!/usr/bin/env python3

import tkinter as tk
# from tkinter import ttk
from configparser import ConfigParser


class PositionSelector(tk.Frame):
    def __init__(self, root, position_config, update_output):
        #self.root = root
        tk.Frame.__init__(self, root)
        self.update_output = update_output
        self.position_list = position_config["PositionList"].split(",")
        self.position_inactive_list = position_config["PositionInactive"].split(
            ",")

        self.button_height = int(position_config["ButtonHeight"])
        self.button_width = int(position_config["ButtonWidth"])
        self.button_pad = int(position_config["ButtonPad"])
        self.fontsize = position_config["FontSize"]
        self.font = position_config["Font"]
        self.background = position_config["Background"]
        self.background_pressed = position_config["BackgroundPressed"]

        self.button_list = [self.create_button(
            row) for row in range(len(self.position_list))]
        self.default_position = int(position_config["DefaultPosition"])
        self.current_position = self.default_position

        for item in self.position_inactive_list:
            self.deactivate_button(self.convert_position_name_to_index(item))
        self.select_button(self.current_position)

    def create_button(self, row):
        button = tk.Button(
            self, text=self.position_list[row], command=self.on_button_clicked(row))
        button.config(height=self.button_height,
                      width=self.button_width,
                      bg=self.background,
                      font=(self.font, self.fontsize), padx=self.button_pad, pady=self.button_pad)
        button.grid(row=row)
        return button

    def on_button_clicked(self, row):
        def event_handler():
            self.process_button_clicked(row)
        return event_handler

    def process_button_clicked(self, row):
        if row == self.current_position:
            return
        self.deselect_button(self.current_position)
        self.current_position = row
        self.select_button(row)
        self.position_changed()

    def deselect_button(self, row):
        self.button_list[row].config(relief="raised", bg=self.background)

    def select_button(self, row):
        self.button_list[row].config(
            relief="sunken", bg=self.background_pressed)

    def position_changed(self):
        self.update_output()

    def get_position(self):
        return self.position_list[self.current_position]

    def set_active_positions(self, active_position_list):
        if self.get_position() not in active_position_list:
            self.current_position = self.default_position
        for position in self.position_list:
            if position in active_position_list:
                self.activate_button(
                    self.convert_position_name_to_index(position))
            else:
                self.deactivate_button(
                    self.convert_position_name_to_index(position))

    def convert_position_name_to_index(self, name):
        return self.position_list.index(name)

    def deactivate_button(self, index):
        self.button_list[index]['state'] = "disabled"

    def activate_button(self, index):
        self.button_list[index]['state'] = "normal"


def test(root):
    configs = ConfigParser()
    configs.read("config.ini")
    settings = configs["PositionSelector"]
    tree_selector = PositionSelector(root, settings)


if (__name__ == '__main__'):
    root = tk.Tk()
    test(root)
    root.mainloop()
