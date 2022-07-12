from preflop_advisor.tree_reader_helpers import ActionProcessor
from preflop_advisor.tree_reader import  TreeReader
from configparser import ConfigParser
from preflop_advisor.hand_convert_helper import convert_hand

import os
import itertools
import pickle

RANKS = list("AKQJT98765432")
SUITS = list("cdhs")
CARDS = list(rank + suit for suit in SUITS for rank in RANKS)

WEIGHTS={}

def get_total_weight(filename):
    total_weight = 0
    try:
        with open(filename, "r") as f:
            for line in f:
                if ";" not in line:
                    hand=line[:-1]
                    if hand not in WEIGHTS:
                        ranks=hand.replace("(","")
                        ranks=ranks.replace(")","")
                        if len(ranks) == 4:
                            all_suits=itertools.product(SUITS,repeat=4)
                            all_combos = [sorted([ranks[0]+i[0],ranks[1]+i[1],ranks[2]+i[2],ranks[3]+i[3]]) for i in all_suits]
                            all_combos.sort()
                            all_combos= list(all_combos for all_combos,_ in itertools.groupby(all_combos))
                            all_combos = [''.join(i) for i in all_combos if len(set(i))==4]
                        elif len(ranks) == 5:
                            all_suits=itertools.product(SUITS,repeat=5)
                            all_combos = [sorted([ranks[0]+i[0],ranks[1]+i[1],ranks[2]+i[2],ranks[3]+i[3],ranks[4]+i[4]]) for i in all_suits]
                            all_combos.sort()
                            all_combos= list(all_combos for all_combos,_ in itertools.groupby(all_combos))
                            all_combos = [''.join(i) for i in all_combos if len(set(i))==5]
                        weight_adjust=0
                        for combo in all_combos:
                            if convert_hand(combo)+ "\n" in line:
                                weight_adjust+=1
                        WEIGHTS[hand]=weight_adjust
                    else:
                        weight_adjust=WEIGHTS[hand]
                    info_line=f.readline()
                    total_weight+=float(info_line.split(";")[0])*weight_adjust
        return total_weight
    except EnvironmentError:
        logging.error("Could not find File: {}".format(filename))
        return total_weight

def get_frequencies(action_before_list,position,position_list,tree_infos,configs):
    action_processor=ActionProcessor(
            position_list, tree_infos, configs)
    valid_actions = configs["ValidActions"].replace(
            " ", "").split(",")
    valid_raise_sizes = configs["RaiseSizeList"].replace(
            " ", "").split(",")
    #full_action_before_list=action_processor.get_action_sequence(action_before_list)
    
    weights=[]
    for item in valid_actions:
        action_sequence = action_before_list + [(position, item)]
        full_action_sequence = action_processor.get_action_sequence(action_sequence)
        full_action_sequence = action_processor.find_valid_raise_sizes(full_action_sequence)
        if action_processor.test_action_sequence(full_action_sequence):
            full_filename=os.path.join(action_processor.path, action_processor.get_filename(full_action_sequence))
            weights.append(get_total_weight(full_filename))
    full_weight=sum(weights)
    frequencies=[i/full_weight*100 for i in weights]
    return frequencies

def get_vs_first_in(row_pos,column_pos,position_list,tree_infos,configs):
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

def get_default_frequencies(position_list,tree_infos,configs):
    results=[]
    row = []
    row.append("X")
    row.append("FI")
    for position in position_list:
        row.append("vs " + position)
    results.append(row)

    for row_pos in position_list:
        row = [row_pos]
        if row_pos != "BB":
            row.append(get_frequencies([], row_pos,position_list,tree_infos,configs))
        else:
            row.append(get_frequencies([("SB", "Call")], row_pos,position_list,tree_infos,configs))

        for column_pos in position_list:
            if column_pos == row_pos:
                row.append([])
                continue
            if position_list.index(row_pos) > position_list.index(column_pos):
                row.append((get_frequencies([(column_pos,"Raise")],row_pos,position_list,tree_infos,configs)))
            else:
                row.append((get_frequencies([(row_pos,"Raise"),(column_pos,"Raise")],row_pos,position_list,tree_infos,configs)))
        results.append(row)
    return results

def get_position_frequencies(position_list,position,tree_infos,configs):
        # Info Line
        results=[]
        row = []
        row.append(position)
        for pos in position_list:
            row.append("vs " + pos)
        results.append(row)

        # SB special infos because of limp
        if position == "SB":
            row = ["after Limp"]
            for column_pos in position_list:
                if column_pos == "BB":
                    row.append(get_frequencies([("SB", "Call"), ("BB", "Raise")],position,position_list,tree_infos,configs))
                else:
                    row.append("")
            results.append(row)

        # squeeze line
        row = ["squeeze"]
        for column_pos in position_list:

            pos_index = position_list.index(position)
            rfi_index = position_list.index(column_pos)

            if pos_index <= rfi_index + 1:  # we have to have at least one player in between rfi and coldcaller
                row.append("")
            else:
                row.append(
                    get_frequencies([(column_pos, "Raise"), (position_list[rfi_index+1], "Call")],
                                    position,
                                    position_list,
                                    tree_infos,
                                    configs
                                    ))
        results.append(row)

        # 4bet
        row = ["4bet"]
        for column_pos in position_list:


            pos_index = position_list.index(position)
            threebet_pos_index = position_list.index(column_pos)

            if position == column_pos:
                row.append("")
                continue
            if pos_index > threebet_pos_index:  # cold4bet spot
                if threebet_pos_index == 0:  # vs utg there is no cold4bet
                    row.append("")
                else:
                    row.append(
                        get_frequencies([(position_list[threebet_pos_index-1], "Raise"),
                        (column_pos, "Raise")],position,position_list,tree_infos,configs))
            else:  # std face 3bet spot after open
                row.append(get_frequencies(
                [(position, "Raise"), (column_pos, "Raise")],position,position_list,tree_infos,configs))
        results.append(row)

        # vs 4bet
        row = ["vs 4bet"]
        for column_pos in position_list:

            pos_index = position_list.index(position)
            # both same position or utg spot where there is no possible face 4bet
            if position == column_pos or pos_index == 0:
                row.append("")
                continue
            if pos_index > position_list.index(column_pos):
                # we 3bet and face a 4bet from the opener:
                row.append(get_frequencies([(column_pos, "Raise"), (position, "Raise"), (column_pos, "Raise")],
                                           position,
                                           position_list,
                                           tree_infos,
                                           configs))
            else:
                # we face cold4bet after the position before us opens and we 3bet:
                opener = position_list[pos_index - 1]
                row.append(get_frequencies([(opener, "Raise"), (position, "Raise"),
                            (column_pos, "Raise")],
                                           position,
                                           position_list,
                                           tree_infos,
                                           configs))
        results.append(row)

        # vs squeeze
        row = ["vs squeeze"]
        for column_pos in position_list:
            pos_index = position_list.index(position)
            squeeze_index = position_list.index(column_pos)

            if squeeze_index <= pos_index + 1:  # squeezer must be after opener + at least one coldcall in between
                row.append("")
                continue

            row.append(get_frequencies([(position, "Raise"), (position_list[pos_index+1],
                                              "Call"), (column_pos, "Raise")],
                                       position,
                                       position_list,
                                       tree_infos,
                                       configs))
        results.append(row)

        return results

def format_cell(cell,width=50):
    if type(cell)==str:
        spaces=width-len(cell)
        if spaces < 0:
            print("INCREASE CELL WIDTH")
        leading_spaces=spaces//2
        return " "*leading_spaces+cell+" "*(spaces-leading_spaces)
    if type(cell)==list:
        out_string=""
        cell=cell[1:]
        for item in cell:
            out_string+="{:3.0f}".format(item)
        spaces=width-len(out_string)
        if spaces < 0:
            print("INCREASE CELL WIDTH")
        leading_spaces=spaces//2
        return " "*leading_spaces+out_string+" "*(spaces-leading_spaces)
    print("UNKNOWN ELEMENET")
    return " "*width



def test():
    config = ConfigParser()
    config.read("config.ini")
    config = config["TreeReader"]
    tree = {"folder": "/mnt/e196db6e-5358-4294-8cb4-208fe9585b0e/monker/ranges/Omaha/6-way/150bb-no-rake/",
            "NumPlayers": 6}
    tree = {"folder": "/home/johann/monker-beta/ranges/Omaha5/HU/50bb",
            "NumPlayers": 2}
    #tree = {"folder": "/mnt/e196db6e-5358-4294-8cb4-208fe9585b0e/monker/ranges/Omaha/6-way/50bb-z500/",
    #       "NumPlayers": 6}
    position_list = config["Positions"].split(",")
    position_list = position_list[0:tree['NumPlayers']]
    position_list.reverse()
    action_before_list=[("UTG","Raise")]
    position='MP'
    #freq=get_frequencies(action_before_list,position,position_list,tree,config)
    #print(freq)
    game = "PLO5"
    if game == "PLO5":
        weight_filename = "weight5-lookup.pickle"
    else:
        weight_filename = "weight4-lookup.pickle"

    if os.path.exists(weight_filename):
        with open(weight_filename,"rb") as f:
            global WEIGHTS
            WEIGHTS = pickle.load(f)

    fi_results = get_default_frequencies(position_list,tree,config)

    #print(fi_results)
    #print(position_results)

    for line in fi_results:
        print("".join([format_cell(i,11) for i in line]))
    print("-"*75)
    for pos in position_list:
        position_results = get_position_frequencies(position_list, pos, tree, config)
        for line in position_results:
            print("".join([format_cell(i,11) for i in line]))
        print("-"*75)

    if not os.path.exists(weight_filename):
        with open(weight_filename,"wb") as f:
            pickle.dump(WEIGHTS,f)

if (__name__ == '__main__'):
    test()