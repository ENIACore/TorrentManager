from typing import Literal
from pathlib import Path
from models import media_metadata, path_metadata
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
        elif node.path_metadata.format_type == 'SUBTITLE':
            return 'SUBTITLE_FILE'
        # If contains season or episode pattern and video file
        elif (
             (node.media_metadata.season or node.media_metadata.episode or node.media_metadata.season_patterns or node.media_metadata.episode_patterns) and
             (node.path_metadata.format_type == 'VIDEO')
             ):
            return 'EPISODE_FILE'
        # If contains extras pattern and video file
        elif node.media_metadata.extras_patterns and node.path_metadata.format_type == 'VIDEO':
            return 'EXTRAS_FILE'
        # If video file
        elif node.path_metadata.format_type == 'VIDEO':
            return 'MOVIE_FILE'

        return 'UNKNOWN'


    def _classify_dir_contextless(self, node: Node) -> NodeType:
        """
        Classifies in order of specificity
        """
        
        if not node.media_metadata or not node.path_metadata:
            return 'UNKNOWN'
        # TODO add subtitle patterns for SUBTITLE_FOLDER
        # If contains season or episode pattern
        elif node.media_metadata.season or node.media_metadata.episode or node.media_metadata.season_patterns or node.media_metadata.episode_patterns:
            return 'SEASON_FOLDER'
        # If contains extras pattern and video file
        elif node.media_metadata.extras_patterns:
            return 'EXTRAS_FOLDER'
        # Default to movie folder
        else:
            return 'MOVIE_FOLDER'

    def _classify_file_contextful(self, node: Node) -> NodeType:
        return 'UNKNOWN'

    def _classify_dir_contextful(self, node: Node) -> NodeType:
        return 'UNKNOWN'
        

