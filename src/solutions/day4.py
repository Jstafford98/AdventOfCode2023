''' Solutions for both parts of Advent of Code Day Four (https://adventofcode.com/2023/day/4) '''
from functools import cache
from itertools import chain
from collections import Counter

DATA_FILE = 'src/files/day4.txt'

SAMPLE_CARDS = [
    'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
    'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
    'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
    'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
    'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
    'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'
]

SAMPLE_ANSWER_ONE = 13
SAMPLE_ANSWER_TWO = 30

PART_ONE_ANSWER = 20117
PART_TWO_ANSWER = 13768818

@cache
def extract_card_details(card : str) -> tuple[str, list[int], list[int]] :
    ''' extract details about a card string and return them as a tuple '''
    
    card_numbering, card_winners_and_actual = card.lower().split(':', 1)
    card_numbering = int(card_numbering.replace('card', '').strip())
    
    winning_numbers, actual_numbers = card_winners_and_actual.split('|')
    winning_numbers = [int(x) for x in winning_numbers.split()]
    actual_numbers = [int(x) for x in actual_numbers.split()]
    
    return card_numbering, winning_numbers, actual_numbers
    
def determine_card_value(
    actual_numbers : list[int], 
    winning_numbers : list[int]
) -> tuple[int, int] :
    ''' 
        determines the total winning numbers of a card and it's value 
        total value of a card is equal to 2^(n_winners-1). The -1 accounts
        for only one winner, when 2**1 would be two, 2**0 would be 1
    '''
    
    overlapping_numbers = set.intersection(
        set(actual_numbers), 
        set(winning_numbers)
    )
    
    n_winners = len(overlapping_numbers)
    card_value = 2**(n_winners-1) if n_winners else 0
    
    return n_winners, card_value

def extract_winnings(
    card : str, 
    card_idx : int, 
) -> dict[str,int] :
    ''' 
        extracts winnings from a card, returns a dictionary 
        with the card's value and the indecies of the card's
        subsequently won by the current card
        
    '''
    
    _, winning_numbers, actual_numbers = extract_card_details(card)
    n_winners, card_value = determine_card_value(
                                actual_numbers, 
                                winning_numbers
                            )
    
    # create indecies for n_winners after current card index
    winner_start = card_idx + 1
    winner_stop = winner_start + n_winners
    winner_idxs = [*range(winner_start, winner_stop)]
    
    return {'card_value' : card_value, 'winner_idxs' : winner_idxs}

def count_total_cards_won(id : int, count_map : dict[int, list[int]]) -> int :
    ''' counts total cards won '''
    
    @cache
    def _wrap(id : int):
        ''' recursively counts winnnings '''
        
        nonlocal count_map
        
        winners = count_map[id]['winner_idxs']
        
        if not winners:
            return [id]
        
        return [id, *chain.from_iterable(_wrap(_id) for _id in winners)]
    
    initial = count_map[id]['winner_idxs']
    
    if not initial:
        return 1
    
    cards_won = [id, *chain.from_iterable(_wrap(_id) for _id in initial)]
    return Counter(cards_won).total()


if __name__ == '__main__':
    
    with open(DATA_FILE, 'r') as f:
        data = f.readlines()
    
    ''' extract relevant information about each card '''
    winnings_map = dict()
    for i,card in enumerate(data):
        winnings_map[i] = extract_winnings(card, i)

    ''' find the total value of all cards '''
    card_values = []
    for i, card_data in winnings_map.items():
        card_values.append(card_data['card_value'])
    total_value_of_cards = sum(card_values)
    
    ''' count the total number of cards won '''
    cards_won = []
    for _id,_ in enumerate(data):
        cards_won.append(count_total_cards_won(id=_id, count_map=winnings_map))
    sum_instances = sum(cards_won)
    
    print('Total Value of Cards: ', total_value_of_cards)
    print('Total Cards Played: ', sum_instances)
    
    assert total_value_of_cards == PART_ONE_ANSWER
    assert sum_instances == PART_TWO_ANSWER    


