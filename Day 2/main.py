def part_1():
    
    beats_map = {
        'rock': 'sissors',
        'sissors': 'paper',
        'paper': 'rock'
    }
    
    translation_map = {
        'a': 'rock',
        'x': 'rock',
        'b': 'paper',
        'y': 'paper',
        'c': 'sissors',
        'z': 'sissors'
    }
    
    value_mapping = {
        'rock': 1,
        'paper': 2,
        'sissors': 3
    }
    
    # Track points
    total_points = 0

    with open('Day 2/input.txt') as data:
        # EX : A X
        for line in data:
            result = 0

            [elf, me] = line.split(' ')
            
            elf = translation_map[elf.lower()]
            me = translation_map[me.lower().replace("\n", "")]
            
            if me == elf:
                result = result + 3
            elif beats_map[me] == elf:
                result = result + 6
            
            result = result + value_mapping[me]
            
            total_points = total_points + result
            
    return total_points

# X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win.
def part_2():
    
    beats_map = {
        'rock': 'sissors',
        'sissors': 'paper',
        'paper': 'rock'
    }
    
    translation_map = {
        'a': 'rock',
        'x': 'rock',
        'b': 'paper',
        'y': 'paper',
        'c': 'sissors',
        'z': 'sissors'
    }
    
    value_mapping = {
        'rock': 1,
        'paper': 2,
        'sissors': 3
    }
    
    # Track points
    total_points = 0

    with open('Day 2/input.txt') as data:
        # EX : A X
        # X Lose, Y Draw, Z Win
        for line in data:
            result = 0

            [elf, result] = line.split(' ')
            
            elf = translation_map[elf.lower()]
            result = result.lower().replace("\n", "")
            me = None
            
            if result == 'x':
                me = beats_map[elf]
                result = 0
            elif result == 'y':
                me = elf
                result = 3
            elif result == 'z':
                me = beats_map[beats_map[elf]]
                result = 6
                
            result = result + value_mapping[me]
            
            total_points = total_points + result
            
    return total_points

res = part_2()
print(res)