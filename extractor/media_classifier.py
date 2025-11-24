from typing import Literal
from pathlib import Path
from struct.node import Node
from config.constants import (
    VIDEO_EXTENSIONS,
    SUBTITLE_EXTENSIONS,
    AUDIO_EXTENSIONS,
    SEASONS_PATTERNS,
    EPISODES_PATTERNS,
    EXTRAS_PATTERNS
)


"""
Series Folder:
    Requirements:
        - metadata.title is not None
        - Contains multiple season folders
    Optional:
        - Contains subtitle folder
        - Contains extras folder

Season Folder:
    Requirements:
        - Folder name matches SEASON_PATTERNS OR metadata.season is not None
        - All episode files have same season OR all have None
        - Contains multiple episode files
    Optional:
        - Contains subtitle folder OR multiple subtitle files
        - Contains extras folder

Movie Folder:
    Requirements:
        - metadata.title is not None
        - Contains one movie file
        # TODO handle multiple part movies
    Optional:
        - Contains subtitle folder OR multiple subtitle files
        - Contains extras folder

Subtitles Folder:
    Required:
        - Contains no video files
        - Contains one or more subtitle files

Extras Folder:
    Required:
        - Folder name matches EXTRAS_PATTERNS
        - Contains one or more movie or episode files files
        # TODO handle season folders inside extras folder
    Optional:
        - Contains subtitles folder OR multiple subtitle files
"""
DirectoryType = Literal[
    'SERIES_FOLDER',
    'SEASON_FOLDER',
    'MOVIE_FOLDER',
    'SUBTITLE_FOLDER',
    'EXTRAS_FOLDER',
    'UNKNOWN_FOLDER'
]

"""
Movie File:
    Required:
        - metadata.season is None
        - metadata.episode is None
        - metadata.ext is in VIDEO_EXTENSIONS

Episode File:
    Required:
        - metadata.season is not None OR metadata.episode is not None
        - metadata.ext is in VIDEO_EXTENSIONS

Subtitle File:
    Required:
        - metadata.ext is in SUBTITLE_EXTENSIONS

Extra File:
    Required:
        - Filename matches EXTRAS_PATTERNS
        - metadata.ext is in VIDEO_EXTENSIONS
"""
FileType = Literal[
    'MOVIE_FILE',
    'EPISODE_FILE',
    'SUBTITLE_FILE',
    'EXTRAS_FILE',
    'AUDIO_FILE',
    'UNKNOWN_FILE'
]

MediaType = DirectoryType | FileType


class MediaClassifier:
    """
    Classifies media files and folders by traversing a Node tree
    """

    def classify_tree(self, node: Node) -> None:
        """
        Recursively traverses Node tree and classifies each node

        Args:
            node: Root node to start classification from
        """
        if not node:
            return

        # Classify current node
        if node.original_path and node.original_path.is_dir():
            node.classification = self._classify_directory(node)
        elif node.original_path and node.original_path.is_file():
            node.classification = self._classify_file(node)

        # Recursively classify children
        if hasattr(node, 'children_nodes') and node.children_nodes:
            for child in node.children_nodes:
                self.classify_tree(child)

    def _classify_directory(self, node: Node) -> DirectoryType:
        """Classifies a directory node"""
        if not node.children_nodes:
            return 'UNKNOWN_FOLDER'

        # Check each classification in order of specificity
        if self._is_subtitle_folder(node):
            return 'SUBTITLE_FOLDER'
        if self._is_extras_folder(node):
            return 'EXTRAS_FOLDER'
        if self._is_season_folder(node):
            return 'SEASON_FOLDER'
        if self._is_series_folder(node):
            return 'SERIES_FOLDER'
        if self._is_movie_folder(node):
            return 'MOVIE_FOLDER'

        return 'UNKNOWN_FOLDER'

    def _classify_file(self, node: Node) -> FileType:
        """Classifies a file node"""
        if not node.metadata or not node.metadata.ext:
            return 'UNKNOWN_FILE'

        ext = node.metadata.ext.upper()

        # Check file extension type
        if ext in SUBTITLE_EXTENSIONS:
            return 'SUBTITLE_FILE'

        if ext in AUDIO_EXTENSIONS:
            return 'AUDIO_FILE'

        if ext not in VIDEO_EXTENSIONS:
            return 'UNKNOWN_FILE'

        # Check if extras file
        if self._is_extras_file(node):
            return 'EXTRAS_FILE'

        # Check if episode file
        if self._is_episode_file(node):
            return 'EPISODE_FILE'

        # Default to movie file for video files without season/episode
        if self._is_movie_file(node):
            return 'MOVIE_FILE'

        return 'UNKNOWN_FILE'

    # Directory classification helpers

    def _is_series_folder(self, node: Node) -> bool:
        """
        Series folder contains multiple season folders
        """
        if not node.children_nodes:
            return False

        season_folder_count = 0
        for child in node.children_nodes:
            if child.original_path and child.original_path.is_dir():
                if self._is_season_folder(child):
                    season_folder_count += 1

        return season_folder_count >= 2

    def _is_season_folder(self, node: Node) -> bool:
        """
        Season folder has season pattern in name and contains episode files
        """
        if not node.children_nodes or not node.metadata:
            return False

        # Check if folder name matches season pattern
        has_season_pattern = node.metadata.season is not None

        # Count episode files
        episode_files = [
            child for child in node.children_nodes
            if child.original_path and child.original_path.is_file()
            and self._is_episode_file(child)
        ]

        # Need season pattern and multiple episodes
        return has_season_pattern and len(episode_files) >= 2

    def _is_movie_folder(self, node: Node) -> bool:
        """
        Movie folder contains exactly one movie file
        """
        if not node.children_nodes:
            return False

        movie_files = [
            child for child in node.children_nodes
            if child.original_path and child.original_path.is_file()
            and self._is_movie_file(child)
        ]

        return len(movie_files) == 1

    def _is_subtitle_folder(self, node: Node) -> bool:
        """
        Subtitle folder contains only subtitle files, no video files
        """
        if not node.children_nodes:
            return False

        has_subtitles = False
        has_video = False

        for child in node.children_nodes:
            if not child.original_path or not child.original_path.is_file():
                continue

            if not child.metadata or not child.metadata.ext:
                continue

            ext = child.metadata.ext.upper()
            if ext in SUBTITLE_EXTENSIONS:
                has_subtitles = True
            if ext in VIDEO_EXTENSIONS:
                has_video = True

        return has_subtitles and not has_video

    def _is_extras_folder(self, node: Node) -> bool:
        """
        Extras folder has extras pattern in name or contains extra files
        """
        if not node.children_nodes or not node.original_path:
            return False

        # Check folder name for extras patterns
        folder_name = node.original_path.name.upper()
        for pattern in EXTRAS_PATTERNS:
            # Simple pattern matching without regex for now
            pattern_clean = pattern.replace('[s]', '').replace('[S]', '').replace('.', '')
            if pattern_clean in folder_name:
                return True

        # Check if contains extra files
        for child in node.children_nodes:
            if child.original_path and child.original_path.is_file():
                if self._is_extras_file(child):
                    return True

        return False

    # File classification helpers

    def _is_movie_file(self, node: Node) -> bool:
        """
        Movie file has no season/episode and is a video file
        """
        if not node.metadata or not node.metadata.ext:
            return False

        ext = node.metadata.ext.upper()
        if ext not in VIDEO_EXTENSIONS:
            return False

        # Movie files should NOT have season/episode info
        return node.metadata.season is None and node.metadata.episode is None

    def _is_episode_file(self, node: Node) -> bool:
        """
        Episode file has season or episode metadata and is a video file
        """
        if not node.metadata or not node.metadata.ext:
            return False

        ext = node.metadata.ext.upper()
        if ext not in VIDEO_EXTENSIONS:
            return False

        # Episode files should have season OR episode info
        return node.metadata.season is not None or node.metadata.episode is not None

    def _is_subtitle_file(self, node: Node) -> bool:
        """
        Subtitle file has subtitle extension
        """
        if not node.metadata or not node.metadata.ext:
            return False

        return node.metadata.ext.upper() in SUBTITLE_EXTENSIONS

    def _is_extras_file(self, node: Node) -> bool:
        """
        Extras file has extras pattern in filename
        """
        if not node.original_path:
            return False

        filename = node.original_path.name.upper()
        for pattern in EXTRAS_PATTERNS:
            # Simple pattern matching
            pattern_clean = pattern.replace('[s]', '').replace('[S]', '').replace('.', '')
            if pattern_clean in filename:
                return True

        return False
