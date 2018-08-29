#!/usr/bin/env python3

from configparser import ConfigParser
from hand_convert_helper import convert_hand

import logging
import os.path


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
                result = self.read_hand(hand, full_action_sequence)
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
            logging.error(
                "Something went wrong with finding valid RAISE sizes...TAKE A LOOK")
            logging.error(
                "Action Sequence: {}".format(full_action_sequence))
            logging.error(
                "New Action Sequence: {}".format(new_action_sequence)
            )
        return new_action_sequence

    def test_action_sequence(self, action_sequence):
        filename = os.path.join(self.path, self.get_filename(action_sequence))
        return os.path.isfile(filename)

    def read_hand(self, hand, action_sequence):
        info_line = ""
        filename = os.path.join(self.path, self.get_filename(action_sequence))
        try:
            with open(filename, "r") as f:
                for line in f:
                    if hand in line and len(line) < 10:
                        info_line = f.readline()
                        break
        except EnvironmentError:
            logging.error("Could not find File: {}".format(filename))
            logging.error("ActionSequence is: {}").format(action_sequence)
            return [0, 0]
        logging.debug("Info Line: {} in file: {}".format(info_line, filename))
        if info_line == "":
            logging.error(
                "Could not find Hand: {} in File: {}".format(hand, filename))
            return [0, 0]
        infos = info_line.split(";")
        frequency = float(infos[0])
        ev = float(infos[1])
        last_action = action_sequence[-1][1]
        return [last_action, self.beautify_freq(frequency), self.beautify_ev(ev)]

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
