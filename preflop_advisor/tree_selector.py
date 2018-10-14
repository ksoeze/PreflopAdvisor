#!/usr/bin/env python3

import tkinter as tk
from configparser import ConfigParser
from preflop_advisor.tooltip import CreateToolTip


class TreeSelector(tk.Frame):
    def __init__(self, root, tree_selector_settings, tree_configs, tree_tooltips, update_output):
        # self.root = root
        tk.Frame.__init__(self, root)
        self.update_output = update_output
        self.num_trees = int(tree_selector_settings["NumTrees"])
        self.button_height = int(tree_selector_settings["ButtonHeight"])
        self.button_width = int(tree_selector_settings["ButtonWidth"])
        self.button_pad = int(tree_selector_settings["ButtonPad"])
        self.fontsize = tree_selector_settings["FontSize"]
        self.font = tree_selector_settings["Font"]
        self.background = tree_selector_settings["Background"]
        self.background_pressed = tree_selector_settings["BackgroundPressed"]
        self.trees = []

        self.process_tree_infos(tree_configs)
        self.button_list = [self.create_button(
            r) for r in range(self.num_trees)]
        
        if tree_selector_settings["ToolTips"] == "YES":
            self.tooltips = [tree_tooltips[i] for i in tree_tooltips]
            self.tooltip_list = self.create_tooltip_list()

        self.current_tree = int(tree_selector_settings["DefaultTree"])
        self.select_button(self.current_tree)

    def process_tree_infos(self, tree_infos):
        for table in tree_infos:
            infos = tree_infos[table].split(",")
            table_dic = {}
            table_dic["plrs"] = int(infos[0])
            table_dic["bb"] = int(infos[1])
            table_dic["game"] = infos[2]
            table_dic["folder"] = infos[3]
            table_dic["infos"] = infos[4]
            self.trees.append(table_dic)

    def create_tooltip_list(self):
        tooltip_list = []
        for tooltip, button in zip(self.tooltips, self.button_list):
            tip = CreateToolTip(button, tooltip)
            tooltip_list.append(tip)
        return tip

    def create_button(self, row):
        text = str(self.trees[row]["plrs"]) + "-max " + \
            str(self.trees[row]["bb"]) + "bb" + " " + \
            self.trees[row]["game"] + " " + self.trees[row]["infos"]
        if len(text) > self.button_width:
            self.button_width = len(text)
        button = tk.Button(
            self, text=text, command=self.on_button_clicked(row))
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
        if row == self.current_tree:
            return
        self.deselect_button(self.current_tree)
        self.current_tree = row
        self.select_button(row)
        self.tree_changed()

    def deselect_button(self, row):
        self.button_list[row].config(relief="raised", bg=self.background)

    def select_button(self, row):
        self.button_list[row].config(
            relief="sunken", bg=self.background_pressed)

    def tree_changed(self):
        self.update_output()

    def get_tree_infos(self):
        return self.trees[self.current_tree]


def test(root):
    configs = ConfigParser()
    configs.read("../config.ini")
    settings = configs["TreeSelector"]
    infos = configs["TreeInfos"]
    action = "do something"
    tree_selector = TreeSelector(
        root, settings, infos, action).grid(row=0, column=0)


if (__name__ == '__main__'):
    root = tk.Tk()
    test(root)
    root.mainloop()
