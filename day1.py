''' Solutions for both parts of Advent of Code Day One (https://adventofcode.com/2023/day/1) '''

PART_ONE_ANSWER = 54081
PART_TWO_ANSWER = 54649

DIGIT_MAP = {v:str(i) for i,v in enumerate(['one','two','three','four','five','six','seven','eight','nine'],1)}
MAX_DEPTH = max(map(len, DIGIT_MAP))

def extract_calibration_codes(
    s         : str, 
    max_depth : int, 
    digit_map : dict[str, int]
) -> tuple[str, str] :
    ''' 
        extracts calibration codes for AOC Day 1 Pt. 2, 
        consider string spelling of digits in the solution as well 
        
        i.e 'two1nine' would become '219' and return 29
    '''
    
    digits = []
    for i in range(0, len(s)):
        end_idx = min(i + max_depth + 1, len(s) + 1) # limit end idx
        for j in range(i, end_idx):
            sub_str = s[i:j]
            if sub_str.isdigit():
                digits.append(sub_str)
                break
            elif sub_str in digit_map:
                digits.append(digit_map[sub_str])
                break
    return int(f'{digits[0]}{digits[-1]}')

def extract_calibration(s : str) -> int :
    ''' 
        extracts calibration codes for AOC Day 1 Pt. 1,
        only considering raw digits
        
        i.e two1nine would become 1 and return 11
    '''
    
    digits = list(filter(lambda x : x.isdigit(), s))
    return int(f'{digits[0]}{digits[-1]}')

if __name__ == '__main__':
    
    digits_pt1 = []
    digits_pt2 = []

    with open('day1.txt','r') as f:
        for x in f.readlines():
            digits_pt1.append(extract_calibration(x))
            digits_pt2.append(extract_calibration_codes(x, max_depth=MAX_DEPTH, digit_map=DIGIT_MAP))

    solution_pt1 = sum(digits_pt1)
    solution_pt2 = sum(digits_pt2)
    
    print('AOC Day 1 Part One Sum: ', solution_pt1)
    print('AOC Day 1 Part Two Sum: ', solution_pt2)
    
    assert PART_ONE_ANSWER == solution_pt1
    assert PART_TWO_ANSWER == solution_pt2