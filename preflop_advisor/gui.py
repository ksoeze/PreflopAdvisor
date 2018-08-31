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
            self.card_selector_position_frame,
            self.configs["CardSelector"],
            self.update_output_frame)
        self.tree_selector = TreeSelector(
            self.input_frame,
            self.configs["TreeSelector"],
            self.configs["TreeInfos"],
            self.update_output_frame)
        self.position_selector = PositionSelector(
            self.card_selector_position_frame,
            self.configs["PositionSelector"],
            self.update_output_frame)
        self.output = OutputFrame(
            self.output_frame,
            self.configs["Output"],
            self.configs["TreeReader"])

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
        game = tree_infos["game"]

        # change active positions and get position after that (otherwise inactive position can be selected)
        self.update_card_and_position_selector(tree_infos)

        position = self.position_selector.get_position()
        hand = self.card_selector.get_hand()

        if len(hand) == 4 and game== "NL" or len(hand) == 8 and game in ["PLO","PLO8"]:
            self.output.update_output_frame(hand, position, tree_infos)
            
    def update_card_and_position_selector(self,tree_infos):
        # select 4 or 2 cards in card_selector depending on game
        # update possible position buttons based on tree
        num_players=tree_infos["plrs"]
        game = tree_infos["game"]

        if game in ["PLO", "PLO8"]:
            self.card_selector.set_num_cards(4)
        elif game in ["NL"]:
            self.card_selector.set_num_cards(2)
            
        self.position_selector.update_active_positions(num_players)    

if (__name__ == '__main__'):
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()
