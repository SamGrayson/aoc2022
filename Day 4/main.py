"""
In pairs where one assignment fully contains the other, one Elf in the pair would be exclusively cleaning sections their partner will already be cleaning, so these seem like the most in need of reconsideration. In this example, there are 2 such pairs.

In how many assignment pairs does one range fully contain the other?
"""
def create_range(num_range) -> tuple[set[str], str, str]:
    split = num_range.split('-')
    low, high = split[0], split[1]
    return (set(range(int(low), int(high)+1)), int(low), int(high))

def part_1():
    contained_pairs = 0
    with open('Day 4/input.txt') as data:
        for line in data:
            split = line.split(',')
            
            # Create sets & return the low and high values
            set1_range, set1_low, set1_high = create_range(split[0])
            set2_range, set2_low, set2_high = create_range(split[1])
            
            # Whichever set is bigger, see if the other high low values exist in it.
            contains = False
            if len(set1_range) >= len(set2_range):
                contains = (set2_low in set1_range) and (set2_high in set1_range)
            else:
                contains = (set1_low in set2_range) and (set1_high in set2_range)
            
            if contains:
                contained_pairs+=1
    
    return contained_pairs
        
        
"""
Same as before, just any intersection
"""
def part_2():
    contained_pairs = 0
    with open('Day 4/input.txt') as data:
        for line in data:
            split = line.split(',')
            
            # Create sets & return the low and high values
            set1_range, set1_low, set1_high = create_range(split[0])
            set2_range, set2_low, set2_high = create_range(split[1])
            
            # Whichever set is bigger, see if ANY high or low values exist in the set
            contains = False
            if len(set1_range) >= len(set2_range):
                contains = (set2_low in set1_range) or (set2_high in set1_range)
            else:
                contains = (set1_low in set2_range) or (set1_high in set2_range)
            
            if contains:
                contained_pairs+=1
    
    return contained_pairs

res = part_2()
print(res)