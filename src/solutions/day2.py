''' Solutions for both parts of Advent of Code Day Two (https://adventofcode.com/2023/day/2) '''

from itertools import groupby
from functools import reduce

''' 
    these answers are only valid for day2.txt that I was given,
    the site generates different puzzle sets for each user
'''
SUM_IDS_ANSWER    = 2541
SUM_POWERS_ANSWER = 66016
DATA_FILE = 'src/files/day2.txt'

CUBE_LIMITS = {
    'red'   : 12,
    'green' : 13,
    'blue'  : 14
}

def evalute_game(
    game_str : str, 
    limits   : dict[str, int]
) -> tuple[int, bool, int] :
    '''
        Evalutes a game string and determines if the game is valid, given the constraints
        of "limits" and returns the game's "power" according to AdventOfCode's 
        prompt
    '''
    
    def _parse_color_counts(cube_str : str) -> list[tuple[str, int]] :
        ''' 
            Extracts each cube color and it's count from the cube string
            The following game string format is assumed:
                color count, color count; color count;
            
            color count, color count; is a cube set
            
            There can be any number of cube sets and colors can be missing
            in a cube set
        '''
        
        color_counts = []
        for cube_set in cube_str.split(';'):
            color_count_strings = cube_set.strip().split(',')
            for color_count_string in color_count_strings:
                color_count, color = color_count_string.strip().split()
                color_count = int(color_count)
                color_counts.append((color, color_count))
        return color_counts
    
    def _ensure_max_counts(
        color_counts : list[tuple[str, int]], 
        max_counts   : dict[str, int]
    ) -> bool :
        '''
            given a dictionary of colors and their maximum allowed counts,
            ensure all color_count pairs are within that maximum value
        '''
        
        for color, count in color_counts:
            if max_counts[color] < count:
                return False
        return True

    def _calculate_game_power(color_counts : list[tuple[str, int]]) -> int :
        ''' 
            determines the minimum number of cubes of each color required
            for this game to be played and returns the product of all 
            minimum counts per color, called the "power"
        '''
        
        minimums = []
        
        sorted_color_counts = sorted(color_counts, key = lambda x : x[0])
        for label, items in groupby(sorted_color_counts, key = lambda x : x[0]):
            _, counts = zip(*items)
            minimums.append(max(counts))
            
        return reduce(lambda x,y : x*y, minimums)
            
    # extract game id and conver to an integer
    id_str, cube_str = game_str.strip().lower().split(':')
    id_str = int(id_str.strip().replace('game ',''))

    color_counts = _parse_color_counts(cube_str)
    is_valid_game = _ensure_max_counts(color_counts, limits)
    game_power = _calculate_game_power(color_counts)
    
    return id_str, is_valid_game, game_power


if __name__ == '__main__':
    
    with open(DATA_FILE, 'r') as f:
        
        valid_ids = []
        game_powers = []
        for game_str in f.readlines():
            
            game_id, is_valid, game_power = evalute_game(game_str, limits=CUBE_LIMITS)
            
            game_powers.append(game_power)
            
            if is_valid:
                valid_ids.append(game_id)
            
        sum_ids = sum(valid_ids)
        sum_powers = sum(game_powers)
        
        print('Sum of valid game ids: ', sum_ids)
        print('Sum of game powers   : ', sum_powers)
        
        assert sum_ids == SUM_IDS_ANSWER
        assert sum_powers == SUM_POWERS_ANSWER
        