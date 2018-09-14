#!/usr/bin/env python3

from configparser import ConfigParser
import logging
from preflop_advisor.tree_reader_helpers import ActionProcessor
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

        self.hand = hand  
        self.position = None if position not in self.full_position_list else position

        self.configs = configs
        self.tree_infos = tree_infos

        self.action_processor = ActionProcessor(
            self.position_list, self.tree_infos, configs)

        self.results = []

    def init_position_list(self, num_players, positions):
        self.position_list = positions
        self.position_list = self.position_list[0:num_players]
        self.position_list.reverse()

    def fill_default_results(self):
        row = []
        row.append({"isInfo": True, "Text": "X"})
        row.append({"isInfo": True, "Text": "FI"})
        for position in self.position_list:
            row.append({"isInfo": True, "Text": "vs " + position})
        self.results.append(row)

        for row_pos in self.position_list:
            row = [{"isInfo": True, "Text": row_pos}]
            if row_pos != "BB":
                row.append(
                    {"isInfo": False, "Results": self.action_processor.get_results(self.hand, [], row_pos)})
            else:
                row.append(
                    {"isInfo": False, "Results": self.action_processor.get_results(self.hand, [("SB", "Call")], row_pos)})

            for column_pos in self.position_list:
                row.append(
                    {"isInfo": False, "Results": self.get_vs_first_in(
                        row_pos, column_pos)}
                )
            self.results.append(row)

    def get_results(self):
        self.results = []
        if self.position:
            self.fill_position_results()
        else:
            self.fill_default_results()
        return self.results

    def fill_position_results(self):

        # Info Line
        pos = self.position
        row = []
        row.append({"isInfo": True, "Text": pos})
        for position in self.position_list:
            row.append({"isInfo": True, "Text": "vs " + position})
        self.results.append(row)

        # RFI Line (without infos)
        if pos != "BB":
            row = [{"isInfo": False, "Results": self.action_processor.get_results(self.hand, [], pos)}]
        else:
            row = [{"isInfo": False, "Results": self.action_processor.get_results(self.hand, [("SB", "Call")], pos)}]

        for column_pos in self.position_list:
            row.append(
                {"isInfo": False, "Results": self.get_vs_first_in(
                    pos, column_pos)}           
            )
        self.results.append(row)

        # SB special infos because of limp
        if pos == "SB":
            row = [{"isInfo": True, "Text": "after Limp"}]
            for column_pos in self.position_list:
                if column_pos == "BB":
                    row.append(
                        {"isInfo": False, "Results": self.action_processor.get_results(self.hand, [("SB", "Call"),("BB", "Raise")],pos)})
                else:
                    row.append({"isInfo": False, "Results": []} )
            self.results.append(row)

        # squeeze line
        row = [{"isInfo": True, "Text": "squeeze"}]
        for column_pos in self.position_list:
            row.append(
                {"isInfo":False, "Results": self.get_squeeze(pos,column_pos)}
            )
        self.results.append(row)  
            
        # vs 4bet
        row = [{"isInfo": True, "Text": "vs 4bet"}]
        for column_pos in self.position_list:
            row.append(
                {"isInfo":False, "Results": self.get_vs_4bet(pos,column_pos)}
            )
        self.results.append(row)

         # vs squeeze
        row = [{"isInfo": True, "Text": "vs squeeze"}]
        for column_pos in self.position_list:
            row.append(
                {"isInfo":False, "Results": self.get_vs_squeeze(pos,column_pos)}
            )
        self.results.append(row)       
        
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

    def get_vs_4bet(self, position, reraise_position):
        pos_index = self.position_list.index(position)
        if position == reraise_position or pos_index == 0: # both same position or utg spot where there is no possible face 4bet
            return []
        if pos_index > self.position_list.index(reraise_position):
            # we 3bet and face a 4bet from the opener:
            results = self.action_processor.get_results(
                self.hand, [(reraise_position,"Raise"),(position,"Raise"),(reraise_position,"Raise")], position
            )
        else:
            # we face cold4bet after the position before us opens and we 3bet:
            opener=self.position_list[pos_index - 1]
            results = self.action_processor.get_results(
                self.hand, [(opener,"Raise"),(position, "Raise"),(reraise_position,"Raise")], position
            )
        return results
    
    def get_vs_squeeze(self,position,squeeze_position):
        pos_index = self.position_list.index(position)
        squeeze_index = self.position_list.index(squeeze_position)

        if squeeze_index <= pos_index + 1: # squeezer must be after opener + at least one coldcall in between
            return []
        
        results = self.action_processor.get_results(
                self.hand, [(position,"Raise"),(self.position_list[pos_index+1],"Call"),(squeeze_position,"Raise")], position
            )
        return results

    def get_squeeze(self,position,rfi_position):
        pos_index = self.position_list.index(position)
        rfi_index = self.position_list.index(rfi_position)

        if pos_index <= rfi_index + 1: # we have to have at least one player in between rfi and coldcaller
            return []
        
        results = self.action_processor.get_results(
                self.hand, [(rfi_position,"Raise"),(self.position_list[rfi_index+1],"Call")], position
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
