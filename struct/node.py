from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING
from models.media_metadata import MediaMetadata

if TYPE_CHECKING:
    from extractor.media_classifier import MediaType

class Node:
    original_path: Path | None = None # Path to original file

    metadata: MediaMetadata | None = None # Metadata extracted from original file

    classification: MediaType | None = None # Classification of node (file or directory type)

    parent_node: Node | None = None # Parent node
    children_nodes: list[Node] | list[None] = [] # Children nodes
