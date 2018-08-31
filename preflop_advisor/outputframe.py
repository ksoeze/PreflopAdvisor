#!/usr/bin/env python3

import tkinter as tk
import tkinter.ttk as ttk
from tree_reader import TreeReader
from output_objects import TableEntry

# from output_objects import TableEntry

RESULT_ROWS = 7
RESULT_COLUMNS = 8
RESULT_HEIGHT = 80
RESULT_WIDTH = 150

INFO_FONT = ("Helvetica", 16)


class OutputFrame(tk.Frame):
    def __init__(self, root, output_configs, tree_reader_configs):
        tk.Frame.__init__(self, root)
        self.root = root
        self.output_configs = output_configs
        self.tree_reader_configs = tree_reader_configs

        self.info_frame = tk.Frame(root)
        self.general_infos = tk.StringVar()
        self.general_infos_label = tk.Label(
            self.info_frame,
            textvariable=self.general_infos,
            font=INFO_FONT).grid(row=0, column=0)

        self.update_info_frame(hand="", position="", treeinfo="")

        self.output_frame = tk.Frame(root)

        self.table_entries = [[None for columns in range(
            RESULT_COLUMNS)] for row in range(RESULT_ROWS)]
        self.create_result_grid()

        self.info_frame.grid(row=0, column=0, pady=30)
        self.output_frame.grid(row=1, column=0)

    def update_info_frame(self, hand, position, treeinfo):
        text = "Hand: " + hand + "   Position: " + position + "   " + treeinfo
        self.general_infos.set(text)

    def update_output_frame(self, hand, position, tree):
        tree_infos = "{}-max {}bb {} {}".format(tree["plrs"],tree["bb"],tree["game"],tree["infos"]) 
        self.update_info_frame(hand, position, tree_infos)
        tree_reader = TreeReader(hand, position, tree,
                                 self.tree_reader_configs)
        #tree_reader.fill_default_results()
        results = tree_reader.get_results()

        for row in range(RESULT_ROWS):
            for column in range(RESULT_COLUMNS):
                self.table_entries[row][column].clear_entry()

        for row in range(len(results)):
            for column in range(len(results[0])):
                if results[row][column]["isInfo"]:
                    self.table_entries[row][column].set_description_label(
                        results[row][column]["Text"])
                else:
                    self.table_entries[row][column].set_result_label(
                        self.preprocess_results(results[row][column]["Results"]))

    def create_result_grid(self):
        for row in range(RESULT_ROWS):
            for column in range(RESULT_COLUMNS):
                table_entry = TableEntry(
                    self.output_frame, RESULT_WIDTH, RESULT_HEIGHT)
                # table_entry.clear_entry()
                # table_entry.set_description_label("TEST")
                self.table_entries[row][column] = table_entry
                field_separator_horizontal = ttk.Separator(self.output_frame)
                field_separator_horizontal.grid(
                    row=1 + row * 2, column=0, columnspan=RESULT_COLUMNS * 2 + 2, sticky="ew")
                field_separator_vertical = ttk.Separator(
                    self.output_frame, orient=tk.VERTICAL)
                field_separator_vertical.grid(
                    row=0, column=1 + column * 2, rowspan=RESULT_ROWS * 2 + 2, sticky="sn"
                )
                table_entry.grid(row=0 + row * 2, column=0 + column * 2)

    def preprocess_results(self, results):
        if len(results) == 0:
            return []

        
        fold_ev = results[0][2] if self.output_configs["AdjustFoldEV"] == "yes" else 0
        results = results[1:]

        if len(results) == 0:
            return []

        new_entry1 = [results[0][0], "{0:.0f}".format(
            results[0][1] * 100), "{0:.02f}".format((results[0][2] - fold_ev) / 2000)]
        if len(results) == 2:
            new_entry2 = [results[1][0], "{0:.0f}".format(
                results[1][1] * 100), "{0:.02f}".format((results[1][2] - fold_ev) / 2000)]
            return [new_entry1, new_entry2]
        return [new_entry1]

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
