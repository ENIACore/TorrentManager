from os import walk
from os.path import join
from pathlib import Path
from struct.node import Node

class Parser:

    @classmethod
    def process_nodes(cls, node: Node | None, path: Path) -> Node:
        # If current node DNE, create head node
        if not node:
            node = Node(path)

        if path.is_file():
            return node

        root, dirnames, filenames = next(walk(path))
    
        # Parse children nodes and add them to parent node 
        children_nodes = []

        for file in filenames:
            file_path = Path(join(root, file))
            child_node = Node(file_path)
            child_node.parent_node = node 
            
            # Only append file to child nodes if recognized file format
            if child_node.path_metadata.format_type != 'UNKNOWN':
                children_nodes.append(child_node)

        for dir in dirnames:
            dir_path = Path(join(root, dir)) 
            child_node = Node(dir_path)
            child_node.parent_node = node
            
            cls.process_nodes(child_node, dir_path) 
            children_nodes.append(child_node)

        node.children_nodes = children_nodes
        return node
