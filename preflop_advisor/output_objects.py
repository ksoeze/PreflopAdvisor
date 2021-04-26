10#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from configparser import ConfigParser

INFO_FONT = ("Helvetica", 15)
RESULT_FONT = ("Helvetica", 10)


class TableEntry(tk.Frame):
    def __init__(self, root, width, height):
        tk.Frame.__init__(self, root)
        self.config(height=height, width=width)
        self.grid_propagate(False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.info_text = tk.StringVar()
        self.left_results = tk.StringVar()
        self.right_results = tk.StringVar()
        self.label = tk.Label(
            self, textvariable=self.info_text, font=INFO_FONT)
        self.label.grid(row=0, column=0)
        self.label_left = tk.Label(
            self, textvariable=self.left_results, font=RESULT_FONT)
        self.label_left.grid(
            row=0, column=0)
        self.label_right = tk.Label(
            self, textvariable=self.right_results, font=RESULT_FONT)
        self.label_right.grid(
            row=0, column=1)

    def set_description_label(self, text=""):
        self.info_text.set(text)
        self.label.grid()

    def set_result_label(self, results):
        if len(results) == 1:
            self.right_results.set(self.convert_result_to_str(results[0]))
            if int(results[0][1]) > 50:
                self.label_right.config(background="linen")
        elif len(results) == 2:
            self.left_results.set(self.convert_result_to_str(results[0]))
            if int(results[0][1]) > 50:
                self.label_left.config(background="linen")
            self.right_results.set(self.convert_result_to_str(results[1]))
            if int(results[1][1]) > 50:
                self.label_right.config(background="linen")

        self.label_left.grid(row=0, column=0, sticky="we", padx=1)
        self.label_right.grid(row=0, column=1, sticky="we", padx=1)

        return

    def convert_result_to_str(self, result):
        s = "\n"
        return s.join(result)

    def clear_entry(self):
        self.label.grid_forget()
        self.label_left.grid_forget()
        self.label_right.grid_forget()

        self.info_text.set("")
        self.left_results.set("")
        self.right_results.set("")

        default_bg = self.label.cget('bg')
        self.label_right.config(background=default_bg)
        self.label_left.config(background=default_bg)
        # self.label.config(background="#40E0D0")


def test(root):
    configs = ConfigParser()
    configs.read("../config.ini")
    settings = configs["Output"]
    # for c in range(12):
    #     for r in range(10):
    #         #entry_frame = ttk.Frame(root, height=100, width=100)
    #         # entry_frame.grid_propagate(False)
    #         data_entry = DataEntry(root, settings, " ", "100", "+123")
    #         data_entry.grid(row=r, column=c)
    #         w = ttk.Separator(data_entry).grid(row=0, column=1)
    #         q = ttk.Separator(data_entry, orient=tk.HORIZONTAL).grid(
    #             row=1, column=0)

    table_entry = TableEntry(root, 100, 100)
    # table_entry.grid_propagate(False)
    table_entry.clear_entry()
    table_entry.set_description_label(("Helvetica", "15"), "UTG")
    table_entry.grid(row=2, column=0)
    ttk.Separator(root).grid(row=1, column=0,
                             columnspan=5, sticky="ew")
    ttk.Separator(root, orient=tk.VERTICAL).grid(
        row=0, column=1, rowspan=3, sticky="sn")
    table_entry1 = TableEntry(root, 100, 100)
    table_entry1.clear_entry()
    table_entry1.set_result_label([[" ", "100", "+23"]])
    table_entry1.grid(row=2, column=2)
    # table_entry1.set_description_label(("Helvetica", "15"), "UTG")
    ttk.Separator(root, orient=tk.VERTICAL).grid(
        row=0, column=3, rowspan=3, sticky="sn")
    table_entry2 = TableEntry(root, 100, 100)
    table_entry2.clear_entry()
    table_entry2.set_result_label(
        [["Flatt ", "100", "+23"], ["3 bet ", "150", "+23"]])
    table_entry2.grid(row=2, column=4)

    table_entry3 = TableEntry(root, 100, 100)
    table_entry3.clear_entry()
    table_entry3.set_description_label(("Helvetica", "15"), "UTG")
    table_entry3.grid(row=0, column=4)

    table_entry4 = TableEntry(root, 100, 100)
    table_entry4.clear_entry()
    table_entry4.set_result_label([["Raise", "100", "+23"]])
    table_entry4.grid(row=3, column=4)


if (__name__ == '__main__'):
    root = tk.Tk()
    test(root)
    root.mainloop()
