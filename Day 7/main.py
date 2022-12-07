"""
--- BLOCK 1 ---
$ cd /
$ ls
dir cwdpn
dir drzllllv
dir fqflwvh
dir jczm
dir jstfcllw
dir lhltq
dir llpmvt
dir tgmt
dir wcbq
--- BLOCK 2 ---
$ cd cwdpn
$ ls
dir mnm
dir nmsvc
dir rgbdq
--- BLOCK 3 ---
$ cd mnm
$ ls
82227 grgj
dir plldwn
dir rtpjd
dir shvplq
"""

# Directory Class
class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.dirs = {}
        self.files = {}
        self.totalSize = 0
        self.parent = parent
        
    def set_parent(self, parent):
        self.parent = parent
        
    def add_file(self, file_name, file_size):
        self.files[file_name] = file_size
        self.totalSize += int(file_size)
        self.update_parent_size(int(file_size))
        
    def add_dir(self, dir):
        self.dirs[dir.name] = dir
        
    def update_parent_size(self, file_size):
        if self.parent:
            self.parent.totalSize += file_size 
            self.parent.update_parent_size(file_size)   

# Create directory mapping given ref of mapping
def create_directory_mapping(input, directory_mapping):
    current_dir = directory_mapping['/']
    for line in input:
        # Navigation - set current to given dir
        if '$ cd' in line and '..' not in line:
            # ex: $ cd <path>
            dir_name = line.replace('$ cd ', '')
            current_dir = current_dir.dirs[dir_name]
        # Navigating up - set current_dir to parent of current
        elif '$ cd' in line and '..' in line:
            # ex: $ cd ..
            current_dir = current_dir.parent
        # Dir - add to the current directory
        elif 'dir' in line:
            # ex: dir <dir_name>
            current_dir.add_dir(Directory(line.split(' ')[1], current_dir))
        # ls - skip line, not required
        elif '$ ls' in line:
            continue
        # It's a file - add to dir & totalSize up the chain
        else:
            # ex: 12345 file_name
            file_size = line.split(' ')[0]
            file_name = line.split(' ')[1]
            current_dir.add_file(file_name, file_size)

def part_1():
    total_available_space = 70000000
    required_unused_space = 30000000
    directory_mapping = {
        '/': Directory('/')
    }

    with open('Day 7/input.txt') as data:
        # EX : A X
        temp = data.read().splitlines()
        
        create_directory_mapping(temp, directory_mapping)

    # Recur to totals - then sum
    def get_dir_totals(dir, totals, dirs):
        if dir.totalSize <= 100000:
            totals.append(dir.totalSize)
            dirs.append(dir)
        for name, dir in dir.dirs.items():
            get_dir_totals(dir, totals, dirs)
                
    totals = []
    dirs = []
    get_dir_totals(directory_mapping['/'], totals, dirs)
    
    # --------- 
    
    # Get list of sizes that would put unusued space over 30000000
    def get_delete_size_list(dir, delete_list, unused_space, unused_space_min = required_unused_space):
        if (unused_space + dir.totalSize) >= unused_space_min:
            delete_list.append(dir.totalSize)
        for name, dir in dir.dirs.items():
            get_delete_size_list(dir, delete_list, unused_space, unused_space_min)
            
    total_size = directory_mapping['/'].totalSize
    unused_space = total_available_space - total_size
    delete_list = []
    get_delete_size_list(directory_mapping['/'], delete_list, unused_space)

    # [part_1, part_2]
    return [sum(totals), sorted(delete_list)[0]]
        
res = part_1()
print(res)