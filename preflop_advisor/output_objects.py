#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from configparser import ConfigParser


class DataEntry(tk.Frame):
    def __init__(self, root, settings, description="", freq="-", ev="-"):
        # super().__init__(root)
        tk.Frame.__init__(self, root)
        # self.root = root
        self.fontsize = settings["FontSize"]
        self.font = settings["Font"]
        self.height = int(settings["Height"])
        self.background = settings["Background"]
        self.width = int(settings["Width"]) if int(settings["Width"]) >= \
            max(len(description), len(freq), len(ev)) else max(len(description), len(freq), len(ev))

        self.label = tk.Label(self,
                              text=description + "\n" +
                              freq + "\n" + "(" + ev + ")",
                              font=(self.font, self.fontsize),
                              height=self.height,
                              width=self.width,
                              bg=self.background)
        self.label.grid(row=0, column=0)


class TableEntry(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        #self.config(height=height, width=width)
        # self.grid_propagate(False)
        self.label = None
        self.label_left = None
        self.label_right = None

    def set_description_label(self, font, text=""):
        self.delete_previous_content()
        self.label = tk.Label(self,
                              text=text,
                              font=font)
        self.label.grid(row=0, column=0)

    def set_single_data_label(self, data_entry):
        self.delete_previous_content()
        self.label = data_entry
        # self.label.pack()
        self.label.grid(row=0, column=0)

    def set_double_data_label(self, data_left, data_right):
        self.delete_previous_content()
        self.label_left = data_left
        self.label_right = data_right
        self.label_left.grid(row=0, column=0)
        self.label_right.grid(row=0, column=1)

    def delete_previous_content(self):
        if self.label:
            self.label.destroy()
        if self.label_left:
            self.label_left.destroy()
        if self.label_right:
            self.label_right.destroy()


def test(root):
    configs = ConfigParser()
    configs.read("config.ini")
    settings = configs["DataEntry"]
    # for c in range(12):
    #     for r in range(10):
    #         #entry_frame = ttk.Frame(root, height=100, width=100)
    #         # entry_frame.grid_propagate(False)
    #         data_entry = DataEntry(root, settings, " ", "100", "+123")
    #         data_entry.grid(row=r, column=c)
    #         w = ttk.Separator(data_entry).grid(row=0, column=1)
    #         q = ttk.Separator(data_entry, orient=tk.HORIZONTAL).grid(
    #             row=1, column=0)

    table_entry = TableEntry(root, 200, 200)
    # table_entry.grid_propagate(False)
    table_entry.set_description_label(("Helvetica", "15"), "UTG")
    table_entry.grid(row=2, column=0)
    ttk.Separator(root).grid(row=1, column=0, columnspan=5, sticky="ew")
    ttk.Separator(root, orient=tk.VERTICAL).grid(
        row=0, column=1, rowspan=3, sticky="sn")
    table_entry1 = TableEntry(root, 200, 200)
    data_entry = DataEntry(table_entry1, settings, " ", "100", "+123")
    table_entry1.set_single_data_label(data_entry)
    table_entry1.grid(row=2, column=2)
    #table_entry1.set_description_label(("Helvetica", "15"), "UTG")
    ttk.Separator(root, orient=tk.VERTICAL).grid(
        row=0, column=3, rowspan=3, sticky="sn")
    table_entry2 = TableEntry(root, 200, 200)
    data_entry_left = DataEntry(table_entry2, settings, " ", "100", "+123")
    data_entry_right = DataEntry(table_entry2, settings, " ", "100", "+123")
    table_entry2.set_double_data_label(data_entry_left, data_entry_right)
    table_entry2.grid(row=2, column=4)

    table_entry3 = TableEntry(root, 200, 200)
    # table_entry.grid_propagate(False)
    table_entry3.set_description_label(("Helvetica", "15"), "UTG")
    table_entry3.grid(row=0, column=4)

    table_entry4 = TableEntry(root, 200, 200)
    # table_entry.grid_propagate(False)
    data_entry = DataEntry(table_entry4, settings, " ", "100", "+123")
    table_entry4.set_single_data_label(data_entry)
    table_entry4.grid(row=3, column=4)


if (__name__ == '__main__'):
    root = tk.Tk()
    test(root)
    root.mainloop()
