#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from tree_reader import TreeReader

#from output_objects import TableEntry


class OutputFrame(tk.Frame):
    def __init__(self, root, output_configs, tree_reader_configs):
        tk.Frame.__init__(self, root)
        self.root = root
        self.output_configs = output_configs
        self.tree_reader_configs = tree_reader_configs

        self.info_frame = tk.Frame(root)
        self.general_infos = tk.StringVar()
        self.general_infos_label = tk.Label(
            self.info_frame, textvariable=self.general_infos).grid(row=0, column=0)

        self.update_info_frame(hand="", position="", treeinfo="")

        self.output_frame = tk.Frame(root)

        self.info_frame.grid(row=0, column=0)
        self.output_frame.grid(row=1, column=0)

    def update_info_frame(self, hand, position, treeinfo):
        text = "Hand: " + hand + " Position: " + position + " " + treeinfo
        self.general_infos.set(text)

    def redraw_output_frame(self, hand, position, tree):
        self.update_info_frame(hand, position, "")
        self.output_frame.destroy()

        self.output_frame = tk.Frame(self.root)
        tree_reader = TreeReader(hand, position, tree,
                                 self.tree_reader_configs)
        tree_reader.fill_default_results()

        results = tree_reader.get_results()

        for row in range(len(results)):
            for column in range(len(results[0])):
                field_frame = tk.Frame(self.output_frame)
                self.print_infos(field_frame, results[row][column])
                field_separator_horizontal = ttk.Separator(self.output_frame)
                field_separator_horizontal.grid(
                    row=row * 2, column=0, columnspan=len(results[0]) * 2, sticky="ew")
                field_separator_vertical = ttk.Separator(
                    self.output_frame, orient=tk.VERTICAL)
                field_separator_vertical.grid(
                    row=2, column=2 + column * 2, rowspan=len(results) * 2 + 2, sticky="sn"
                )
                field_frame.grid(row=1 + row * 2, column=1 + column * 2)

        self.output_frame.grid(row=1, column=0)

    def print_infos(self, root, results):
        # print(results)
        if results["isInfo"]:
            tk.Label(root, text=results["Text"]).grid(column=0, row=0)
        else:
            for column in range(len(results["Results"])):
                frame = tk.Frame(root)
                self.print_result(frame, results["Results"][column])
                frame.grid(row=0, column=column)

    def print_result(self, root, result):
        text = "{0} \n {1:.0f} \n ({2:.02f})".format(
            result[0], result[1] * 100, result[2] / 2000)
        tk.Label(root, text=text).pack()


def test(root):
    configs = ConfigParser()
    configs.read("../config.ini")
    output_configs = configs["Output"]
    tree_configs = configs["TreeReader"]

    output_frame = OutputFrame(root, output_configs, tree_configs)
    tree = {"Path": "/home/johann/monker/ranges/Omaha/6-way/100bb/", "NumPlayers": 6}
    output_frame.redraw_output_frame("AsKhTs9h", "X", tree)

    print(output_frame.general_infos.get())


if (__name__ == '__main__'):
    root = tk.Tk()
    test(root)
    root.mainloop()
