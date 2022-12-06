"""
examples: 
bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 5
nppdvjthqldpwncqszvftbrmjlhg: first marker after character 6
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 10
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 11
"""

# -- look for unique 4 packets
example_1 = 'bvwbjplbgvbhsrlpgdmjqwftvncz'
example_2 = 'nppdvjthqldpwncqszvftbrmjlhg'
example_3 = 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'

# -- look for unique 14 packets

example_4 = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb' # first marker after character 19
example_5 = 'bvwbjplbgvbhsrlpgdmjqwftvncz' # first marker after character 23
example_6 = 'nppdvjthqldpwncqszvftbrmjlhg' # first marker after character 23

def packet_checker(unqiue_check=4):
    with open('Day 6/input.txt') as data:
        # EX : A X
        input = data.readline()
        check = []
        char_count = 0
        for s in input:
            # One check is 4, see if it equals the map length, remove the first item.
            if len(check) == unqiue_check:
                if len(check) == len(set(check)):
                    return char_count
                check.pop(0)
            check.append(s)
            char_count+=1
        else:
            if len(check) == unqiue_check:
                if len(check) == len(set(check)):
                    return char_count
                check.pop(0)    
    
## Part 1
# res = packet_checker(4)

## Part 2
res = packet_checker(14)


print(res)