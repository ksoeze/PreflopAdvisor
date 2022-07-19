#!/usr/bin/env python3

import logging
import re
import glob
import json
import os

RANK_ORDER = {'A': 12, 'K': 11, 'Q': 10, 'J': 9, 'T': 8, '9': 7,
              '8': 6, '7': 5, '6': 4, '5': 3, '4': 2, '3': 1, '2': 0}
RANKS = list("AKQJT98765432")
SUITS = list("cdhs")

# Converts 4 Card Hand like "AsAcTh3d" to monker tree format
# Added support for 2 Card NL Hands

def convert_hand(hand):
    hand = hand.replace(" ","")
    if len(hand) == 8:
        return convert_omaha_hand(hand)
    elif len(hand) == 4:
        return convert_holdem_hand(hand)
    elif len(hand) == 10:
        return convert_omaha5_hand(hand)
    logging.error(
            "Hand: {} cannot be converted...wrong length".format(hand))
    return hand

def convert_holdem_hand(hand):
    if len(hand) != 4:
        logging.error(
            "NL Hand: {} cannot be converted...wrong length".format(hand))
    ranks = [hand[0],hand[2]]
    suits = [hand[1],hand[3]]
    ranks.sort(key=lambda x: RANK_ORDER[x],reverse=True)
    if ranks[0] == ranks[1]:
        return "{}{}".format(ranks[0],ranks[0])
    if suits[0] == suits[1]:
        return "{}{}{}".format(ranks[0],ranks[1],"s")
    else:
        return "{}{}{}".format(ranks[0],ranks[1],"o")
    
def convert_omaha_hand(hand):
    if len(hand) != 8:
        logging.error(
            "Omaha Hand: {} cannot be converted...wrong length".format(hand))
        return hand
    ranks = [hand[0], hand[2], hand[4], hand[6]]
    suits = [hand[1], hand[3], hand[5], hand[7]]
    for rank in ranks:
        if rank not in RANKS:
            logging.error(
                "Hand: {} cannot be converted...invalid ranks".format(hand))
            return hand
    for suit in suits:
        if suit not in SUITS:
            logging.error(
                "Hand: {} cannot be converted...invalid suits".format(hand))
            return hand
    cards = [hand[0:2], hand[2:4], hand[4:6], hand[6:8]]
    suit_count = {"s": 0, "d": 0, "h": 0, "c": 0}
    for s in suit_count:
        for card_s in suits:
            if card_s == s:
                suit_count[s] += 1
    cards_single_suit = []
    cards_two_suited = []  # nested list
    cards_three_suited = []  # only card list
    cards_four_suited = []
    for s in suit_count:
        if suit_count[s] == 0:
            continue
        elif suit_count[s] == 1:
            for card in cards:
                if card[1] == s:
                    cards_single_suit.append(card)
        elif suit_count[s] == 2:
            two_suits = []
            for card in cards:
                if card[1] == s:
                    two_suits.append(card)
            cards_two_suited.append(two_suits)
        elif suit_count[s] == 3:
            for card in cards:
                if card[1] == s:
                    cards_three_suited.append(card)
        elif suit_count[s] == 4:
            for card in cards:
                if card[1] == s:
                    cards_four_suited.append(card)
    return_hand = ""
    if cards_single_suit:
        cards_single_suit.sort(key=lambda x: RANK_ORDER[x[0]])
        for item in cards_single_suit:
            return_hand += item[0]
    if cards_two_suited:
        for item in cards_two_suited:
            item.sort(key=lambda x: RANK_ORDER[x[0]])
        cards_two_suited.sort(key=lambda x: (RANK_ORDER[x[1][0]],RANK_ORDER[x[0][0]]))
        for item in cards_two_suited:
            return_hand += "(" + item[0][0] + item[1][0] + ")"
    if cards_three_suited:
        cards_three_suited.sort(key=lambda x: RANK_ORDER[x[0]])
        return_hand += "(" + cards_three_suited[0][0] + \
            cards_three_suited[1][0] + cards_three_suited[2][0] + ")"
    if cards_four_suited:
        cards_four_suited.sort(key=lambda x: RANK_ORDER[x[0]])
        return_hand += "("
        for card in cards_four_suited:
            return_hand += card[0]
        return_hand += ")"
    return return_hand


def convert_omaha5_hand(hand):
    if len(hand) != 8 and len(hand) !=10:
        logging.error(
            "Omaha Hand: {} cannot be converted...wrong length".format(hand))
        return hand
    ranks = [x for x in hand if x in RANKS]
    suits = [x for x in hand if x in SUITS]
    if len(ranks) != 4 and len(ranks) != 5 or len(ranks)-len(suits)!=0:
        logging.error(
            "Omaha Hand: {} cannot be converted".format(hand))
        return hand

    cards = [hand[i:i+2] for i in range(0,len(hand),2)]
    suit_ranks = {"s": [], "d": [], "h": [], "c": []}
    for s in suit_ranks:
        for card in cards:
            if card[1] == s:
                suit_ranks[s].append(card[0])
    for s in suit_ranks:
        suit_ranks[s] = sorted(suit_ranks[s],key=lambda  x:RANK_ORDER[x])

    unsuited_cards=[]
    for s in suit_ranks:
        if len(suit_ranks[s]) == 1:
            unsuited_cards.append(suit_ranks[s][0])
    suited_cards=[]
    for s in suit_ranks:
        if len(suit_ranks[s]) > 1:
            suited_cards.append(suit_ranks[s])
    unsuited_string = ''.join(sorted(unsuited_cards,key=lambda  x:RANK_ORDER[x]))
    suited_cards = sorted(suited_cards,key=lambda x:(RANK_ORDER[x[0]],RANK_ORDER[x[1]]))
    suited_string=''
    for item in suited_cards:
        suited_string+="(" + ''.join(item) + ")"
    return unsuited_string+suited_string

def sort_monker_2_hand(hand):
    if "(" not in hand:
        if hand[0] not in RANKS:
            print(hand)
        return ''.join(sorted(hand,key=lambda x: RANK_ORDER[x[0]]))
    if hand.count("(") == 1:
        suited = re.search('\((.+?)\)',hand).group(1)
        unsuited = re.sub('\((.+?)\)','',hand)
        return ''.join(sorted(unsuited,key=lambda x: RANK_ORDER[x[0]])) + "(" + ''.join(sorted(suited,key=lambda x: RANK_ORDER[x[0]])) + ")"
    if hand.count("(") == 2:
        suited1 = hand[0:4]
        if RANK_ORDER[suited1[1]] > RANK_ORDER[suited1[2]]:
            suited1 = "("+suited1[2]+suited1[1] + ")"
        suited2 = hand[4:8]
        #print(suited1)
        #print(suited2)
        if RANK_ORDER[suited2[1]] > RANK_ORDER[suited2[2]]:
            suited2 = "("+suited2[2]+suited2[1] + ")"

        if RANK_ORDER[suited1[2]] == RANK_ORDER[suited2[2]]:
            if RANK_ORDER[suited1[1]] > RANK_ORDER[suited2[1]]:
                return suited2 + suited1
            else:
                return suited1 + suited2
        if RANK_ORDER[suited1[2]] > RANK_ORDER[suited2[2]]:
            return suited2 + suited1
        else:
            return suited1 + suited2
    return hand

def sort_omaha5_hand(hand):
    if hand.count("(") == 1:
        suited = re.search('\((.+?)\)',hand).group(1)
        unsuited = re.sub('\((.+?)\)','',hand)
        return ''.join(sorted(unsuited,key=lambda x: RANK_ORDER[x[0]])) + "(" + ''.join(sorted(suited,key=lambda x: RANK_ORDER[x[0]])) + ")"
    else:
        suited = re.findall('\((.+?)\)',hand)
        unsuited = re.sub('\((.+?)\)(.*?)\((.+?)\)','',hand)
        suited_list = []
        for item in suited:
            suited_list.append(''.join(sorted(item,key=lambda x: RANK_ORDER[x[0]])))
        suited_list = sorted(suited_list,key=lambda x: (RANK_ORDER[x[0]],RANK_ORDER[x[1]]))
        suited = "("+''.join(suited_list[0])+")"+"("+''.join(suited_list[1])+")"
        return ''.join(sorted(unsuited,key=lambda x: RANK_ORDER[x[0]])) + suited
    print("convert error! {}".format(hand))

def replace_monker_2_hands(filename):
    new_content=""
    with open(filename,'r') as f:
        #print(filename)
        for line in f:
            if ";" not in line and line[0]!="0": #hand not ev values
                new_content += sort_monker_2_hand(line[0:-1]) + "\n"
            else:
                new_content+=line
    with open(filename,"w") as f:
        f.write(new_content)

def replace_all_monker_2_files(path):
    all_files = glob.glob(path+"*.rng")
    for file in all_files:
        replace_monker_2_hands(file)

def move_plo5_file(work_path,inputfilename,outputfilename):
    input_file = os.path.join(work_path,inputfilename)
    with open(input_file,'r') as json_file:
        data = json.load(json_file)

    hands = data["items"]
    output_file = os.path.join(work_path,outputfilename)
    with open(output_file,'w') as range_file:
        for item in hands:
            range_file.write(
                sort_omaha5_hand(item["combo"].replace("[","(").replace("]",")"))+"\n")
            range_file.write(str(item["frequency"])+";"+str(item["ev"])+"\n")

def move_plo5_postflop_file(work_path,inputfilename,outputfilename):
    input_file = os.path.join(work_path,inputfilename)
    with open(input_file,'r') as json_file:
        data = json.load(json_file)

    hands = data["items"]
    output_file = os.path.join(work_path,outputfilename)
    with open(output_file,'w') as range_file:
        for item in hands:
            range_file.write(item["combo"]+"," + str(item["weight"])+"," + str(item["ev"]*1000)+"\n")

def test():
    #print(convert_hand("Ad8s7h2c4c"))
    #print(sort_monker_2_hand("(98)(T7)"))
    #print(sort_monker_2_hand("(QA)(3A)"))
    #replace_monker_2_hands("/media/johann/MONKER/monker-beta/ranges/Omaha/6-way/40bb/0.0.rng")

    #replace_all_monker_2_files("/home/johann/monker-beta/ranges/Omaha5/6-way/100bb/")

    #move_plo5_postflop_file("/home/johann/monker-beta/ranges","CHECK","CHECK.csv")
    #move_plo5_postflop_file("/home/johann/monker-beta/ranges","BET75","BET75.csv")
if (__name__ == '__main__'):
    test()
