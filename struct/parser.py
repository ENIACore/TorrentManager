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
            
    def print_tree(self, node: Node | None, indent: int = 0, prefix: str = "") -> None:
        """
        Recursively print the node tree structure with media and path metadata.

        Args:
            node: The root node to start printing from
            indent: Current indentation level (used internally for recursion)
            prefix: Prefix for the current line (used for tree structure visualization)
        """
        if not node:
            return

        # Print current node info
        node_type = "📁" if node.original_path.is_dir() else "📄"
        print(f"{prefix}{node_type} {node.original_path.name}")

        # Print media metadata if available
        if node.media_metadata:
            metadata_indent = " " * (indent + 2)
            print(f"{metadata_indent}├─ Media: {node.media_metadata}")

        # Print path metadata if available
        if node.path_metadata:
            metadata_indent = " " * (indent + 2)
            print(f"{metadata_indent}├─ Path: {node.path_metadata}")

        # Print children recursively
        if node.children_nodes:
            for i, child in enumerate(node.children_nodes):
                is_last = i == len(node.children_nodes) - 1
                extension = "└─ " if is_last else "├─ "
                continuation = "   " if is_last else "│  "

                child_prefix = " " * indent + extension
                self.print_tree(child, indent + 3, child_prefix)
