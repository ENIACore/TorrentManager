from pathlib import Path
from struct.parser import Parser
from classifier.node_classifier import NodeClassifier

#PATH_TO_PARSE='/mnt/RAID/qbit-data/downloads'
PATH_TO_PARSE='./'


parser = Parser()
head = parser.process_nodes(None, Path(PATH_TO_PARSE))

classifier = NodeClassifier()
if head:
    head = classifier.classify(head)
    parser.print_tree(head)
else:
    print('error retrieving head')


