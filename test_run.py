from pathlib import Path
from struct.parser import Parser

#PATH_TO_PARSE='/mnt/RAID/qbit-data/downloads'
PATH_TO_PARSE='./'


parser = Parser()
head = parser.process_nodes(None, Path(PATH_TO_PARSE))
print('printing tree now')
parser.print_tree(head)

