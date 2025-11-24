from os import walk
from os.path import join
from pathlib import Path
from extractor.path_extractor import PathExtractor
from extractor.media_extractor import MediaExtractor
from models import path_metadata
from struct.node import Node

class Parser:
    def __init__(self) -> None:
        self.media_extractor = MediaExtractor()
        self.path_extractor = PathExtractor()

    def process_nodes(self, node: Node | None, path: Path) -> Node | None:
        # If current node DNE, create head node
        if not node:
            node = Node()
            node.original_path = path 
            node.media_metadata = self.media_extractor.extract_metadata(path)
            node.path_metadata = self.path_extractor.extract_metadata(path)
            node.parent_node = None

        if path.is_file():
            return node

        root, dirnames, filenames = next(walk(path))
    
        # Parse children nodes and add them to parent node 
        children_nodes = []

        for file in filenames:
            child_node = Node()
            file_path = Path(join(root, file))

            child_node.original_path = file_path
            child_node.media_metadata = self.media_extractor.extract_metadata(file_path)
            child_node.path_metadata = self.path_extractor.extract_metadata(file_path)
            child_node.parent_node = node 
            child_node.children_nodes = []
            
            # Only append file to child nodes if recognized file format
            if child_node.path_metadata and child_node.path_metadata.format_type:
                children_nodes.append(child_node)

        for dir in dirnames:
            child_node = Node()
            dir_path = Path(join(root, dir)) 
            child_node.original_path = dir_path

            child_node.media_metadata = self.media_extractor.extract_metadata(dir_path)
            child_node.path_metadata = self.path_extractor.extract_metadata(dir_path)
            child_node.parent_node = node
            child_node.children_nodes = []
            
            self.process_nodes(child_node, dir_path) 
            children_nodes.append(child_node)

        node.children_nodes = children_nodes
        return node
