#!/usr/bin/env python3

from configparser import ConfigParser
from preflop_advisor.hand_convert_helper import convert_hand
from collections import OrderedDict

import logging
import os.path

CACHE = OrderedDict()

class ActionProcessor():
    def __init__(self, position_list, tree_infos, configs):
        self.configs = configs  # just saving total info dictionaries for later
        self.tree_infos = tree_infos

        self.position_list = position_list
        self.valid_actions = configs["ValidActions"].replace(
            " ", "").split(",")
        self.valid_raise_sizes = configs["RaiseSizeList"].replace(
            " ", "").split(",")
        self.path = tree_infos["folder"]
        #self.cache = OrderedDict()
        self.cache_size = int(self.configs["CacheSize"])

    def get_action_sequence(self, action_list):
        # action list contains all "active" actions of players as tuples (position, action)
        # actions inbetween are asumed to be folds

        full_action_list = []
        start_index = 0
        position_already_folded = []

        for action in action_list:
            for index in range(len(self.position_list)):
                position_index = (
                    index + start_index) % len(self.position_list)
                position = self.position_list[position_index]
                if position != action[0]:
                    if position not in position_already_folded:
                        full_action_list.append((position, "Fold"))
                        position_already_folded.append(position)
                else:
                    full_action_list.append((position, action[1]))
                    start_index = position_index + 1
                    break
        return full_action_list

    def get_results(self, hand, action_before_list, position):
        if position not in self.position_list:
            logging.error(
                "{} is not a valid Position for the selected Tree".format(position))
            return []
        hand = convert_hand(hand)
        results = []

        for item in self.valid_actions:
            action_sequence = action_before_list + [(position, item)]
            full_action_sequence = self.get_action_sequence(action_sequence)
            full_action_sequence = self.find_valid_raise_sizes(
                full_action_sequence)
            if self.test_action_sequence(full_action_sequence):
                if self.cache_size == 0:
                    result = self.read_hand(hand, full_action_sequence)
                else:
                    result = self.read_hand_with_cache(hand,full_action_sequence)
                results.append(result)

        return results

    def find_valid_raise_sizes(self, full_action_sequence):
        new_action_sequence = []
        for action in full_action_sequence:
            if action[1] != "Raise":
                new_action_sequence.append(action)
            else:
                for raise_size in self.valid_raise_sizes:
                    if self.test_action_sequence(new_action_sequence + [(action[0], raise_size)]):
                        new_action_sequence.append((action[0], raise_size))
                        break  # TODO this fails if we dont find any valid raise size?

        if len(full_action_sequence) != len(new_action_sequence):
            if full_action_sequence[-1][1] == "Raise" and "All_In" in [action[1] for action in new_action_sequence]:
                # we have all in but trying to find reraise action
                # duno but just adding action anyway so we get empty result?
                # print("Adding Invalid raise action to see what happens")
                new_action_sequence.append(
                    (full_action_sequence[-1][0], self.valid_raise_sizes[-1]))
            else:
                logging.warning(
                    "Something went wrong with finding valid RAISE sizes...TAKE A LOOK")
                logging.warning(
                    "Action Sequence: {}".format(full_action_sequence))
                logging.warning(
                    "New Action Sequence: {}".format(new_action_sequence)
                )
        return new_action_sequence

    def test_action_sequence(self, action_sequence):
        filename = os.path.join(self.path, self.get_filename(action_sequence))
        return os.path.isfile(filename)
    
    def read_file_into_hash(self,filename):
        hand_info_hash = {}
        with open(filename, "r") as f:
            lines = f.readlines()
            for i in range(0, len(lines), 2):  # assuming every hand is followed by its info line
                hand = lines[i].strip()
                info = lines[i + 1].strip()
                hand_info_hash[hand] = info
        return hand_info_hash


    def read_hand(self, hand, action_sequence):
        info_line = ""
        filename = os.path.join(self.path, self.get_filename(action_sequence))
        try:
            with open(filename, "r") as f:
                for line in f:
                    if hand + "\n" in line and len(line) < 12: # newline added to distinguish between 2345 and (2345)
                        info_line = f.readline()
                        break
        except EnvironmentError:
            logging.error("Could not find File: {}".format(filename))
            logging.error("ActionSequence is: {}").format(action_sequence)
            return ["", 0, 0]
        logging.debug("Info Line: {} in file: {}".format(info_line, filename))
        if info_line == "":
            logging.error(
                "Could not find Hand: {} in File: {}".format(hand, filename))
            return ["", 0, 0]
        infos = info_line.split(";")
        frequency = float(infos[0])
        ev = float(infos[1])
        last_action = action_sequence[-1][1]
        return [last_action, self.beautify_freq(frequency), self.beautify_ev(ev)]
    
    def read_hand_with_cache(self, hand, action_sequence):
        filename = os.path.join(self.path, self.get_filename(action_sequence))
        try:
            # Check if file data is already in memory
            if filename not in CACHE:
                if len(CACHE) >= self.cache_size:
                    CACHE.popitem(last=False)
                CACHE[filename] = self.read_file_into_hash(filename)
            
            CACHE.move_to_end(filename)

            hand_info = CACHE[filename].get(hand)
            if not hand_info:
                logging.error("Could not find Hand: {} in File: {}".format(hand, filename))
                return ["", 0, 0]

            infos = hand_info.split(";")
            frequency = float(infos[0])
            ev = float(infos[1])
            last_action = action_sequence[-1][1]
            return [last_action, self.beautify_freq(frequency), self.beautify_ev(ev)]

        except EnvironmentError:
            logging.error("Could not find File: {}".format(filename))
            logging.error("ActionSequence is: {}").format(action_sequence)
            return ["", 0, 0]

    def beautify_ev(self, ev):
        return ev

    def beautify_freq(self, freq):
        return freq

    def get_filename(self, action_sequence):
        filename = ""
        for position, action in action_sequence:
            filename = filename + "." + self.configs[action]
        filename = filename[1:]
        filename += self.configs["Ending"]
        return filename


def test():
    config = ConfigParser()
    config.read("config.ini")
    config = config["TreeReader"]
    tree = {"Path": "/home/johann/monker/ranges/Omaha/6-way/100bb/"}
    position_list = ["UTG", "MP", "CO", "BU", "SB", "BB"]
    action_sequence = ActionProcessor(position_list, tree, config)
    action_list = [("CO", "Raise"), ("BU", "Raise")]
    hand = "AhKs4h3s"
    result = action_sequence.get_results(hand, action_list, "SB")
    for item in result:
        print(item)


if (__name__ == '__main__'):
    test()
