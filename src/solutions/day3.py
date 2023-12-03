''' Solutions for both parts of Advent of Code Day Three (https://adventofcode.com/2023/day/3) '''
from functools import reduce, cache

DATA_FILE = 'src/files/day3.txt'

SAMPLE_SCHEMATIC = [
    '467..114..',
    '...*......',
    '..35..633.',
    '......#...',
    '617*......',
    '.....+.58.',
    '..592.....',
    '......755.',
    '...$.*....',
    '.664.598..'
]
SAMPLE_ANSWER_ONE = 4361
SAMPLE_ANSWER_TWO = 467835

PART_ONE_ANSWER = 535078
PART_TWO_ANSWER = 75312571

DEADSPACE = '.'
GEAR = '*'

def is_gear(c : str) -> bool :
    ''' checks if a character is an asterisk '''
    return c == GEAR

def is_symbol(c : str) -> bool:
    ''' checks if a character is not a digit or period '''
    return not c.isdigit() and not c == DEADSPACE

def slices_intersect(sl : slice, sl2 : slice) -> bool :
    ''' checks if two slices overlap '''
    
    def range_from_slice(sl : slice) -> list[int]:
        ''' generates a range of integers given a slice '''
        return [*range(sl.start, sl.stop)]

    s1_range, s2_range = range_from_slice(sl), range_from_slice(sl2)
    s1_set, s2_set = set(s1_range), set(s2_range)
    intersec = set.intersection(s1_set, s2_set)
    return bool(intersec)

def seek_gears(s : str) -> list[slice] :
    ''' finds all gears in a given string, returning slices for those gears '''
    gears = []
    for i,c in enumerate(s):
        if is_gear(c):
            gears.append(slice(i,i+1))
    return gears
  
@cache
def seek_digits(s : str) -> list[slice]:
    ''' 
        finds all numbers in a string and returns a list of slices for those digits 
        '123$4@$5 would return slices for ['123', '4', '5']
    '''
    
    def _seek_until_terminate(s : str) -> int | None :
        ''' 
            searches a string until a non-numeric character 
            is reached and returns that index 
        '''
        for idx, val in enumerate(s):
            if not val.isdigit():
                return idx
    
    if s.isdigit():
        ''' 
            short-circuits if string is a digit, slice 
            will return the whole string when used 
            
            while slice(None, None) gives the same result, it breaks some other
            functions later on
        '''
        return [slice(len(s))]
    
    cursor = 0
    digit_ranges = []
    while cursor < len(s):
        ''' extract digits in string until end is reached '''
        
        if not s[cursor].isdigit():
            ''' first char isn't a digit so increment it and try again '''
            cursor+=1
            continue

        if s[cursor:].isdigit():
            ''' 
                remaining string is a digit 
                slice(cursor) would work the same, but it breaks
                other functions later one
            '''
            digit_ranges.append(slice(cursor, len(s))) 
            break
        
        ''' look until a non-digit is encountered starting from cursor '''
        end = _seek_until_terminate(s[cursor:])
        
        digit = slice(cursor,cursor+end)
        digit_ranges.append(digit)
        
        cursor += end
        
    return digit_ranges
    
def has_adjacent_symbol(
    s     : str, 
    sl    : slice,
    above : str | None = None, 
    below : str | None = None
) -> bool :
    ''' 
        check for an adjacent symbol by slice in string 
        by checking if any of the immediatly surrounding 
        characters in the array are symbols
        
        digit strings with an adjacent symbol, in the context of 
        Advent of Code, are considered valid digits. This checks
        that for the purpose of part one
    '''
    
    # grab character immediately to the left of string
    adjacent_left = s[sl.start-1] if sl.start else None
    if adjacent_left and is_symbol(adjacent_left):
        return True
    
    # grab character immediately to the right of string
    adjacent_right = s[sl.stop] if sl.stop < (len(s)) else None
    if adjacent_right and is_symbol(adjacent_right):
        return True
    
    start_left = sl.start - 1 if sl.start else 0
    start_right = sl.stop + 1
    
    # grab string immediately above
    adjacent_top = above[start_left:start_right] if above else None
    
    # check if any characters in adjacent top are symbols
    if adjacent_top and any(map(is_symbol, adjacent_top)):
        return True
    
    # grab string immediately below
    adjacent_bottom = below[start_left:start_right] if below else None
    
    # check if any characters in adjacent bottom are symbols
    if adjacent_bottom and any(map(is_symbol, adjacent_bottom)):
        return True
    
    return False
    
def find_adjacent_digits(
    current : str,
    sl      : slice,
    above   : str | None,
    below   : str | None
) -> list[str] | None :
    ''' 
        checks for adjacent digits relative to a gear by identifying 
        all digits in the current, above, and below strings via seek_digits
        and then checking to see which slices "intersect" our gear's slice.
        
        While it looks like there is only ever two adjacent digits, this can
        handle ANY number of adjacent digits ( max should ever be 4 )
    '''
    n_adjacent = 0
    adjacent_digits = []
    
    # sl is just the single index of our gear, so expand that out to encompass
    # sl += 1 if possible to catch adjacents
    gear_slice = slice(
        max(sl.start - 1, 0),
        min(sl.stop + 1, len(current))
    )
    
    above_slices = seek_digits(above) # returns empty list if none found
    for above_slice in above_slices:
        ''' identify any digits above gear that are adjacent '''
        if slices_intersect(gear_slice, above_slice):
            adjacent_digits.append(above[above_slice])
            n_adjacent+=1
    
    below_slices = seek_digits(below) 
    for below_slice in below_slices:
        if slices_intersect(gear_slice, below_slice):
            adjacent_digits.append(below[below_slice])
            n_adjacent+=1
    
    current_slices = seek_digits(current)
    for current_slice in current_slices:
        if slices_intersect(gear_slice, current_slice):
            adjacent_digits.append(current[current_slice])
            n_adjacent += 1

    return [int(x) for x in adjacent_digits] if n_adjacent >= 2 else []

def validate_codes(slices : list[slice], s : str, above : str | None, below : str | None) -> list[int]:
    ''' 
        checks all extracted digits in a string, using slices returned 
        from seek_digits, to see if they have adjacent symbols
    '''
    codes = []
    for sl in slices:
        if has_adjacent_symbol(s, sl, above, below):
            codes.append(int(s[sl]))
    return codes

def validate_gears(
    slices : list[slice], 
    s      : str, 
    above  : str | None, 
    below  : str | None
) -> list[int]:
    ''' 
        checks if "gears" in a string are "valid", i.e they have 2 
        (or more) adjacent digits 
    '''
    gears = []
    for sl in slices:
        adjacent_digits = find_adjacent_digits(s, sl, above, below)
        if adjacent_digits:
            gears.append(adjacent_digits)
    return gears
    
if __name__ == '__main__':

    with open(DATA_FILE, 'r') as f:
        data = [x.strip() for x in f.readlines()]
            
    valid_codes = []
    products = []
    
    for i, test_case in enumerate(data):
        
        ''' extract slices for all digits in test_case and gears '''
        digit_ranges = seek_digits(test_case)
        gear_ranges = seek_gears(test_case)
        
        ''' get strings above/below test_case if possible '''
        above = data[i-1] if i else None
        below = data[i+1] if i < len(data) - 1 else None
        
        ''' extract valid codes if any digits found in test_case '''
        _valid_codes = validate_codes(digit_ranges, test_case, above, below) if digit_ranges else []
        for code in _valid_codes:
            valid_codes.append(code)
        
        ''' extract valid gears in test_case if any found '''
        gear_ratios = validate_gears(gear_ranges, test_case, above, below) if gear_ranges else []
        if not gear_ratios:
            continue
        
        ''' 
            AOC challenge calls for finding the product all valid gear 
            "serial numbers", i.e a gear has two or more adjacent digits
            
            validate_gears may find multiple valid gears in a string, so 
            we account for that using a list comprehension
        '''
        gear_products = [reduce(lambda x, y : x*y, z) for z in gear_ratios]
        for x in gear_products:
            products.append(x)        

    sum_of_valid_codes   = sum(valid_codes)
    sum_of_gear_products = sum(products)
    
    print('Sum of codes: ', sum_of_valid_codes)
    print('Sum of gear products: ', sum_of_gear_products)
    
    assert sum_of_valid_codes == PART_ONE_ANSWER
    assert sum_of_gear_products == PART_TWO_ANSWER
    
    