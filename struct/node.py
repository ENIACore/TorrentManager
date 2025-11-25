from __future__ import annotations
from pathlib import Path
from config.node import NodeType
from models import media_metadata
from models.path_metadata import PathMetadata
from models.media_metadata import MediaMetadata

class Node:
    original_path: Path = Path('/') # Path to original file
    new_path: Path = Path('/') # Path to original file

    media_metadata: MediaMetadata # Metadata regarding media
    path_metadata: PathMetadata # Metadata regarding file

    parent_node: Node | None = None # Parent node
    children_nodes: list[Node] = [] # Children nodes

    classification: NodeType = 'UNKNOWN' # Classification of node (file or directory type)

    def __init__(self, path: Path = Path('/')) -> None:
        self.original_path = path
