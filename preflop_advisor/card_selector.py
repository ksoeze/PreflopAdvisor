#!/usr/bin/env python3

import tkinter as tk
# from tkinter import ttk
from configparser import ConfigParser

NUM_ROWS = 13
NUM_COLUMNS = 4
RANK_DIC = {0: "A", 1: "K", 2: "Q", 3: "J", 4: "T", 5: "9",
            6: "8", 7: "7", 8: "6", 9: "5", 10: "4", 11: "3", 12: "2"}
SUIT_DIC = {0: "h", 1: "c", 2: "s", 3: "d"}
SUIT_SIGN_DIC = {0: "\u2665", 1: "\u2663", 2: "\u2660", 3: "\u2666"}
SUIT_COLORS = {"h": "red2", "d": "SteelBlue1",
               "c": "SpringGreen2", "s": "gray50"}
SELECTED_SUIT_COLORS = {"h": "red4", "d": "SteelBlue4",
                        "c": "SpringGreen4", "s": "gray30"}


class CardSelector(tk.Frame):
    def __init__(self, root, card_selector_settings, update_output):
        #self.root = root
        tk.Frame.__init__(self, root)
        self.update_output = update_output
        self.num_cards = int(card_selector_settings["NumCards"])
        #self.timeout = int(card_selector_settings["TimeOut"])
        self.color_dict = SUIT_COLORS
        self.button_height = int(card_selector_settings["ButtonHeight"])
        self.button_width = int(card_selector_settings["ButtonWidth"])
        self.button_pad = int(card_selector_settings["ButtonPad"])
        #self.button_size = card_selector_settings["ButtonSize"]
        #self.button_style = card_selector_settings["ButtonStyle"]

        self.button_list = [[self.create_button(r, c) for r in range(
            NUM_ROWS)] for c in range(NUM_COLUMNS)]

        self.current_hand = []
        self.selected_cards = []
        self.selection_counter = 0
        self.time_last_click = 0

    def create_button(self, row, column):
        button = tk.Button(
            self, text=RANK_DIC[row] + SUIT_SIGN_DIC[column], command=self.on_button_clicked(row, column))
        button.config(background=self.color_dict[SUIT_DIC[column]], height=self.button_height,
                      width=self.button_width, padx=self.button_pad, pady=self.button_pad)
        button.grid(row=row, column=column)
        return button

    def on_button_clicked(self, row, column):
        def event_handler():
            self.process_button_clicked(row, column)
        return event_handler

    def process_button_clicked(self, row, column):
        button_index = [row, column]
        if button_index in self.selected_cards:
            self.deselect_button(button_index)
            self.selected_cards.remove(button_index)
            self.selection_counter -= 1
            return
        if len(self.selected_cards) == self.num_cards:
            for item in self.selected_cards:
                self.deselect_button(item)
            self.selected_cards = []
        self.selected_cards.append(button_index)
        self.select_button(button_index)
        # self.selection_counter+=1
        # if selection_counter == num_cards:
        #     self.selection_counter = 0
        #     self.new_hand()
        #     return
        if len(self.selected_cards) == self.num_cards:
            # print(time.time() - self.time_last_click)
            # if time.time() - self.time_last_click > self.timeout:
            #     self.time_last_click = time.time()
            self.new_hand()
        return

    def select_button(self, button_index):
        button = self.button_list[button_index[1]][button_index[0]]
        button.config(
            relief="sunken", background=SELECTED_SUIT_COLORS[SUIT_DIC[button_index[1]]])

    def deselect_button(self, button_index):
        button = self.button_list[button_index[1]][button_index[0]]
        button.config(relief="raised",
                      background=SUIT_COLORS[SUIT_DIC[button_index[1]]])

    def new_hand(self):
        self.update_output()

    def get_hand(self):
        hand = ""
        for card in self.selected_cards:
            hand += RANK_DIC[card[0]]
            hand += SUIT_DIC[card[1]]
        return hand


def test(root):
    configs = ConfigParser()
    configs.read("config.ini")
    card_selector_settings = configs["CardSelector"]
    card_selector = CardSelector(root, card_selector_settings)


if (__name__ == '__main__'):
    root = tk.Tk()
    test(root)
    root.mainloop()
