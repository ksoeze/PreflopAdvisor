#!/usr/bin/env python3

import tkinter as tk
from configparser import ConfigParser
from card_selector import CardSelector
from tree_selector import TreeSelector
from position_selector import PositionSelector
from outputframe import OutputFrame


class MainWindow:
    def __init__(self, root):
        self.root = root

        self.configs = ConfigParser()
        self.configs.read("../config.ini")

        self.root.title("Preflop Advisor based on Monker")

        self.input_frame = tk.Frame(root)
        self.output_frame = tk.Frame(root)

        self.card_selector_position_frame = tk.Frame(self.input_frame)

        self.card_selector = CardSelector(
            self.card_selector_position_frame, self.configs["CardSelector"], self.update_output_frame)
        self.tree_selector = TreeSelector(
            self.input_frame, self.configs["TreeSelector"], self.configs["TreeInfos"], self.update_output_frame
        )
        self.position_selector = PositionSelector(
            self.card_selector_position_frame, self.configs["PositionSelector"], self.update_output_frame
        )
        self.output = OutputFrame(
            self.output_frame, self.configs["Output"], self.configs["TreeReader"])

        self.grid_frames()

    def grid_frames(self):
        self.input_frame.grid(row=0, column=0)
        self.output_frame.grid(row=0, column=1, padx=100)

        self.card_selector_position_frame.grid(row=0, column=0, sticky='W')
        self.tree_selector.grid(row=1, column=0, columnspan=2)

        self.card_selector.grid(row=0, column=0)
        self.position_selector.grid(row=0, column=1, sticky="S")

    def update_output_frame(self):
        tree_infos = self.tree_selector.get_tree_infos()
        # change active positions and get position after that (otherwise inactive position can be selected)
        position = self.position_selector.get_position()
        hand = self.card_selector.get_hand()

        self.output.update_output_frame(hand, position, tree_infos)


if (__name__ == '__main__'):
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()
