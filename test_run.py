from os import walk
from os.path import join
from pathlib import Path
from struct.parser import Parser
from classifier.node_classifier import NodeClassifier

PATH_TO_PARSE='/mnt/RAID/qbit-data/downloads'
#PATH_TO_PARSE='./'


parser = Parser()
classifier = NodeClassifier()

    
root, dirnames, filenames = next(walk(PATH_TO_PARSE))
    
for dir in dirnames:
    head = parser.process_nodes(None, Path(join(root, dir)))
    if head:
        head = classifier.classify(head)


for file in filenames:
    head = parser.process_nodes(None, Path(join(root, file)))
    if head:
        head = classifier.classify(head)


