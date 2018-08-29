#!/usr/bin/env python3

from configparser import ConfigParser
import logging
from tree_reader_helpers import ActionProcessor
import cProfile

# Result Data Structure Keys:
# IS_INFO = "isInfo"
# RESULTS = "Results"
# TEXT = "Text"
# RFI_DIC = {"Raise100": "R100", "AllIn": "AllIn"}


class TreeReader():
    def __init__(self, hand, position, tree_infos, configs):

        self.full_position_list = configs["Positions"].split(",")
        self.position_list = []
        self.num_players = tree_infos["plrs"]
        self.init_position_list(self.num_players, self.full_position_list)

        #self.num_players = int(tree_infos["NumPlayers"])
        #self.stacksize = int(tree_infos["Stack"])
        #self.game = tree_infos["Game"]

        self.hand = hand  # self.convert_hand(hand)
        self.position = None if position not in self.full_position_list else position

        self.configs = configs
        self.tree_infos = tree_infos
        #self.raise_size_list = configs["RaiseSizeList"].split(",")
        #self.default_fold = "Fold"
        #self.default_call = "Call"
        #self.default_raise = "Raise100"

        self.action_processor = ActionProcessor(
            self.position_list, self.tree_infos, configs)

        self.results = []

    def init_position_list(self, num_players, positions):
        self.position_list = positions
        self.position_list = self.position_list[0:num_players]
        self.position_list.reverse()

    def fill_default_results(self):
        self.results = []
        row = []
        row.append({"isInfo": True, "Text": "X"})
        row.append({"isInfo": True, "Text": "FI"})
        for position in self.position_list:
            row.append({"isInfo": True, "Text": position})
        self.results.append(row)

        for row_pos in self.position_list:
            row = [{"isInfo": True, "Text": row_pos}]
            row.append(
                {"isInfo": False, "Results": self.action_processor.get_results(self.hand, [], row_pos)})
            for column_pos in self.position_list:
                row.append(
                    {"isInfo": False, "Results": self.get_vs_first_in(
                        row_pos, column_pos)}
                )
            self.results.append(row)

    def get_results(self):
        return self.results

    def fill_position_results(self, position):
        # TODO
        return

    def get_vs_first_in(self, position, fi_position):
        if position == fi_position:
            return []
        if self.position_list.index(position) > self.position_list.index(fi_position):
            # we face an open
            results = self.action_processor.get_results(
                self.hand, [(fi_position, "Raise")], position)
        else:
            # we face a 3bet after an open (could include sb limp -> bb raises?!)
            results = self.action_processor.get_results(
                self.hand, [(position, "Raise"),
                            (fi_position, "Raise")], position
            )
        return results


def test():
    config = ConfigParser()
    config.read("config.ini")
    config = config["TreeReader"]
    tree = {"Path": "/home/johann/monker/ranges/Omaha/6-way/100bb/", "NumPlayers": 6}
    position_list = ["UTG", "MP", "CO", "BU", "SB", "BB"]
    hand = "AhKs4h3s"
    tree_reader = TreeReader(hand, "X", tree, config)
    tree_reader.fill_default_results()

    for row in tree_reader.results:
        print("---------------------------------------------------------------------------")
        for field in row:
            print(field)


if (__name__ == '__main__'):
    cProfile.run('test()')
