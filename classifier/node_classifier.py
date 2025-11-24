from typing import Literal
from pathlib import Path
from models import media_metadata
from struct.node import Node
from extractor.base_extractor import BaseExtractor
from config.node import NodeType
from config.constants import (
    VIDEO_EXTENSIONS,
    SUBTITLE_EXTENSIONS,
    AUDIO_EXTENSIONS,
    SEASONS_PATTERNS,
    EPISODES_PATTERNS,
    EXTRAS_PATTERNS
)
import re

class NodeClassifier:
    """
    Two pass classifier

    Pass 1: Classifies contextless bottom up, classifies 1 node at a time
    Pass 2: Classifies contextful top down, classifies 1 node and its children at a time
    """

    def __init__(self) -> None:
        pass

    def classify(self, node: Node) -> Node:

        return node


    def _classify_file_contextless(self, node: Node) -> NodeType:
        """
        Classifies in order of specificity
        """

        if not node.media_metadata or not node.path_metadata:
            return 'UNKNOWN'
        if node.path_metadata.format_type == 'SUBTITLE':
            return 'SUBTITLE_FILE'
        #if node.media_metadata.season or node.media_metadata.episode or 

        return 'UNKNOWN'


    def _classify_dir_contextless(self, node: Node) -> NodeType:
        return 'UNKNOWN'

    def _classify_file_contextful(self, node: Node) -> NodeType:
        return 'UNKNOWN'

    def _classify_dir_contextful(self, node: Node) -> NodeType:
        return 'UNKNOWN'
        

