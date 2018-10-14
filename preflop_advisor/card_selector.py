#!/usr/bin/env python3

import tkinter as tk
#import tkinter.ttk as ttk
from configparser import ConfigParser

NUM_ROWS = 13
NUM_COLUMNS = 4
RANK_DIC = {0: "A", 1: "K", 2: "Q", 3: "J", 4: "T", 5: "9",
            6: "8", 7: "7", 8: "6", 9: "5", 10: "4", 11: "3", 12: "2"}
SUIT_DIC = {0: "h", 1: "c", 2: "s", 3: "d"}
SUIT_SIGN_DIC = {0: "\u2665", 1: "\u2663", 2: "\u2660", 3: "\u2666"}
SUIT_COLORS = {"h": "red", "d": "blue",
               "c": "green", "s": "black"}
BUTTON_FONT = ("Helvetica", "11")


class CardSelector(tk.Frame):
    def __init__(self, root, card_selector_settings, update_output):
        tk.Frame.__init__(self, root)
        self.update_output = update_output
        self.num_cards = int(card_selector_settings["NumCards"])
        self.color_dict = SUIT_COLORS
        self.button_height = int(card_selector_settings["ButtonHeight"])
        self.button_width = int(card_selector_settings["ButtonWidth"])
        self.button_pad = int(card_selector_settings["ButtonPad"])
        self.background = card_selector_settings["Background"]
        self.background_pressed = card_selector_settings["BackgroundPressed"]

        self.button_list = [[self.create_button(r, c) for r in range(
            NUM_ROWS)] for c in range(NUM_COLUMNS)]

        self.selected_cards = []
        self.selection_counter = 0

    def create_button(self, row, column):
        button = tk.Button(
            self, text=RANK_DIC[row] + SUIT_SIGN_DIC[column],
            command=self.on_button_clicked(row, column))
        button.config(background=self.background,
                      foreground=SUIT_COLORS[SUIT_DIC[column]],
                      height=self.button_height,
                      width=self.button_width,
                      font=BUTTON_FONT,
                      padx=self.button_pad, pady=self.button_pad)
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
        if len(self.selected_cards) >= self.num_cards:
            for item in self.selected_cards:
                self.deselect_button(item)
            self.selected_cards = []
        self.selected_cards.append(button_index)
        self.select_button(button_index)
        if len(self.selected_cards) == self.num_cards:
            self.new_hand()
        return

    def select_button(self, button_index):
        button = self.button_list[button_index[1]][button_index[0]]
        button.config(
            relief="sunken",
            background=self.background_pressed,
            foreground=SUIT_COLORS[SUIT_DIC[button_index[1]]])

    def deselect_button(self, button_index):
        button = self.button_list[button_index[1]][button_index[0]]
        button.config(
            relief="raised",
            background=self.background,
            foreground=SUIT_COLORS[SUIT_DIC[button_index[1]]])

    def new_hand(self):
        self.update_output()

    def get_hand(self):
        hand = ""
        for card in self.selected_cards:
            hand += RANK_DIC[card[0]]
            hand += SUIT_DIC[card[1]]
        return hand

    def set_num_cards(self, num_cards):
        if num_cards == 4:
            self.num_cards = 4
        if num_cards == 2:
            self.num_cards = 2
        return  # only 2 or 4 cards are valid...ignore rest


def test(root):
    configs = ConfigParser()
    configs.read("../config.ini")
    card_selector_settings = configs["CardSelector"]
    update_output = print("Cards")
    card_selector = CardSelector(
        root, card_selector_settings, update_output).grid(column=0, row=0)


if (__name__ == '__main__'):
    root = tk.Tk()
    test(root)
    root.mainloop()
