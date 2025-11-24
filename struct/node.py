from __future__ import annotations
from pathlib import Path
from models.path_metadata import PathMetadata
from models.media_metadata import MediaMetadata

class Node:
    original_path: Path | None = None # Path to original file

    media_metadata: MediaMetadata | None = None # Metadata regarding media
    path_metadata: PathMetadata | None = None # Metadata regarding file

    parent_node: Node | None = None # Parent node
    children_nodes: list[Node] | list[None] = [] # Children nodes

    #classification: MediaType | None = None # Classification of node (file or directory type)
