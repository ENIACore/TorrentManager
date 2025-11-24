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
            

    def print_tree(self, node: Node | None, indent: int = 0, prefix: str = "", is_last: bool = True) -> None:
        """
        Recursively print the node tree structure showing:
        - Original filename
        - New standardized filename (from media_metadata)
        - Classification type
        
        Args:
            node: The root node to start printing from
            indent: Current indentation level (used internally for recursion)
            prefix: Prefix for the current line (used for tree structure visualization)
            is_last: Whether this is the last child in its parent's list
        """
        if not node:
            return

        # Determine node icon and get original name
        is_directory = node.original_path.is_dir() if node.original_path else False
        node_icon = "📁" if is_directory else "📄"
        original_name = node.original_path.name if node.original_path else "Unknown"
        
        # Generate new standardized name
        new_name = self._generate_new_name(node)
        
        # Get classification with color coding
        classification = self._format_classification(node.classification)
        
        # Print main node line
        print(f"{prefix}{node_icon} {original_name}")
        
        # Prepare indentation for metadata
        if indent == 0:
            metadata_prefix = "  "
        else:
            metadata_prefix = prefix[:-4] + ("    " if is_last else "│   ") + "  "
        
        # Always show classification (even if None/Unknown)
        has_new_name = new_name and new_name != original_name
        
        if has_new_name:
            print(f"{metadata_prefix}├─ 📝 New: {new_name}")
            print(f"{metadata_prefix}└─ 🏷️  Type: {classification}")
        else:
            print(f"{metadata_prefix}└─ 🏷️  Type: {classification}")
        
        # Print children recursively
        if node.children_nodes:
            for i, child in enumerate(node.children_nodes):
                child_is_last = i == len(node.children_nodes) - 1
                
                # Prepare prefix for child
                if indent == 0:
                    child_connector = "└── " if child_is_last else "├── "
                    child_prefix = child_connector
                else:
                    continuation = "    " if is_last else "│   "
                    child_connector = "└── " if child_is_last else "├── "
                    child_prefix = prefix[:-4] + continuation + child_connector
                
                self.print_tree(child, indent + 4, child_prefix, child_is_last)

    def _generate_new_name(self, node: Node) -> str | None:
        """
        Generate the new standardized filename using media_metadata and extension.
        """
        if not node.media_metadata:
            return None
        
        # Generate base name from media metadata
        base_name = str(node.media_metadata)
        
        # Add extension for files
        if node.path_metadata and node.path_metadata.is_file and node.path_metadata.ext:
            # If base_name is empty or just dots, use original name
            if not base_name or base_name.replace('.', '') == '':
                return node.original_path.name if node.original_path else None
            return f"{base_name}.{node.path_metadata.ext}"
        
        # For directories, just return the formatted media metadata
        return base_name if base_name and base_name.replace('.', '') != '' else None

    def _format_classification(self, classification: str | None) -> str:
        """
        Format classification with color coding for better visibility.
        Uses ANSI color codes for terminal output.
        """
        # Handle None or missing classification
        if classification is None:
            classification = "NOT_CLASSIFIED"
        
        # Color mapping for different classification types
        colors = {
            'SERIES_FOLDER': '\033[95m',   # Magenta
            'SEASON_FOLDER': '\033[94m',   # Blue
            'MOVIE_FOLDER': '\033[96m',    # Cyan
            'SUBTITLE_FOLDER': '\033[93m', # Yellow
            'EXTRAS_FOLDER': '\033[92m',   # Green
            'MOVIE_FILE': '\033[96m',      # Cyan
            'EPISODE_FILE': '\033[94m',    # Blue
            'SUBTITLE_FILE': '\033[93m',   # Yellow
            'EXTRAS_FILE': '\033[92m',     # Green
            'AUDIO_FILE': '\033[91m',      # Red
            'UNKNOWN': '\033[90m',         # Gray
            'NOT_CLASSIFIED': '\033[91m',  # Red (to highlight missing classification)
        }
        
        color = colors.get(classification, '\033[0m')
        reset = '\033[0m'
        
        return f"{color}{classification}{reset}"

    def print_tree_simple(self, node: Node | None, indent: int = 0) -> None:
        """
        Simple version without colors for environments that don't support ANSI codes.
        """
        if not node:
            return

        # Determine node icon and get names
        is_directory = node.original_path.is_dir() if node.original_path else False
        node_icon = "[DIR]" if is_directory else "[FILE]"
        original_name = node.original_path.name if node.original_path else "Unknown"
        new_name = self._generate_new_name(node)
        
        # Get classification (show NOT_CLASSIFIED if None)
        classification = node.classification if node.classification else "NOT_CLASSIFIED"
        
        # Print main line with arrow showing transformation
        indent_str = "  " * indent
        if new_name and new_name != original_name:
            print(f"{indent_str}{node_icon} {original_name} → {new_name} [{classification}]")
        else:
            print(f"{indent_str}{node_icon} {original_name} [{classification}]")
        
        # Print children
        for child in node.children_nodes:
            self.print_tree_simple(child, indent + 1)
