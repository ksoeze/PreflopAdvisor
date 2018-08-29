#!/usr/bin/env python3

import logging

RANK_ORDER = {'A': 12, 'K': 11, 'Q': 10, 'J': 9, 'T': 8, '9': 7,
              '8': 6, '7': 5, '6': 4, '5': 3, '4': 2, '3': 1, '2': 0}
RANKS = list("AKQJT98765432")
SUITS = list("cdhs")

# Converts 4 Card Hand like "AsAcTh3d" to monker tree format
# TODO implement NL convertion (should be simpler than omaha / o8)


def convert_hand(hand):
    if len(hand) != 8:
        logging.error(
            "Hand: {} cannot be converted...wrong length".format(hand))
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
        cards_two_suited.sort(key=lambda x: RANK_ORDER[x[1][0]])  # NOT SURE
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
