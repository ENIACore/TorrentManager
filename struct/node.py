from __future__ import annotations
from pathlib import Path
from extractor.media_extractor import MediaExtractor
from models.media_metadata import MediaMetadata

class Node:
    original_path: Path | None = None # Path to original file

    metadata: MediaMetadata | None = None # Metadata extracted from original file

    parent_node: Node | None = None # Parent node
    children_nodes: list[Node] | list[None] = [] # Children nodes
