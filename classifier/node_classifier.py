from models import media_metadata
from struct.node import Node
from config.node import NodeType
from logger.logger import Logger


# TODO: 
# - Add processing for Episode folders
# - Validate all video files have same or no epsidoe in _is_season_dir
# - Enable processing of subtitle direcotries with language directories inside
# - Enable processing of extras direcotries with season directories inside
# - Add extra validations for unwanted files/directories (e.g. season folder inside subtitle folder)

class NodeClassifier:
    """
    recursive top-down classification with context propagation
    """

    def __init__(self, manager_path=None) -> None:
        self.logger = Logger(manager_path=manager_path)
        self._classification_depth = 0

    def classify(self, node: Node) -> Node:
        """Entry point for classification - logs tree separator for root nodes."""
        # Log tree separator for root level nodes
        if self._classification_depth == 0:
            self.logger.debug("=" * 80)
            self.logger.debug(f"STARTING CLASSIFICATION TREE: {node.original_path}")
            self.logger.debug("=" * 80)
        
        # Throw error if node parsing not completed properly
        if (not node.media_metadata or not node.path_metadata):
            raise ValueError('Media metadata or path metadata not extracted for node')

        self._classification_depth += 1
        try:
            if node.path_metadata.is_dir:
                result = self._classify_dir(node)
            elif node.path_metadata.is_file:
                result = self._classify_file(node)
            else:
                raise ValueError('Node must be classified as file or directory')
            
            # Log completion for root nodes
            if self._classification_depth == 1:
                self.logger.debug("=" * 80)
                self.logger.debug(f"COMPLETED CLASSIFICATION TREE: {node.original_path}")
                self.logger.debug(f"ROOT CLASSIFICATION: {result.classification}")
                self.logger.debug("=" * 80)
                self.logger.debug("")  # Empty line for separation
            
            return result
        finally:
            self._classification_depth -= 1

    def _classify_file(self, node: Node) -> Node:
        indent = "  " * self._classification_depth
        self.logger.debug(f"{indent}Classifying FILE: {node.original_path}")
        
        # Throw error if node parsing not completed properly
        if (not node.media_metadata or not node.path_metadata):
            raise ValueError('Media metadata or path metadata not extracted for node')

        # Check if it's a video file
        is_video = self._is_video_file(node)
        self.logger.debug(f"{indent}  - Is video file: {is_video}")
        self.logger.debug(f"{indent}  - Format type: {node.path_metadata.format_type}")
        
        if is_video:
            has_title = bool(node.media_metadata.title)
            has_season = bool(node.media_metadata.season_patterns or node.media_metadata.episode_patterns)
            
            self.logger.debug(f"{indent}  - Has title: {has_title} ('{node.media_metadata.title}')")
            self.logger.debug(f"{indent}  - Has season/episode patterns: {has_season}")
            
            if has_title and has_season:
                node.classification = 'EPISODE_FILE'
                self.logger.debug(f"{indent}  ✓ Classified as EPISODE_FILE")
            elif has_title:
                node.classification = 'MOVIE_FILE'
                self.logger.debug(f"{indent}  ✓ Classified as MOVIE_FILE")
        elif self._is_subtitle_file(node):
            self.logger.debug(f"{indent}  - Is subtitle file: True")
            raise ValueError('Only episodes or movies are allowed in top level directory')

        if not node.classification:
            self.logger.debug(f"{indent}  ✗ Classification failed - no classification assigned")
        
        return node
    
    def _classify_dir(self, node: Node) -> Node:
        """
        Classifies parent and child nodes in order of specificity
        """
        indent = "  " * self._classification_depth
        self.logger.debug(f"{indent}Classifying DIRECTORY: {node.original_path}")
        
        # Throw error if node parsing not completed properly
        if (not node.media_metadata or not node.path_metadata):
            raise ValueError('Media metadata or path metadata not extracted for node')

        # Log metadata for debugging
        self.logger.debug(f"{indent}  - Has title: {bool(node.media_metadata.title)} ('{node.media_metadata.title}')")
        self.logger.debug(f"{indent}  - Season patterns: {node.media_metadata.season_patterns}")
        self.logger.debug(f"{indent}  - Season number: {node.media_metadata.season}")
        self.logger.debug(f"{indent}  - Episode number: {node.media_metadata.episode}")
        self.logger.debug(f"{indent}  - Extras patterns: {node.media_metadata.extras_patterns}")
        
        # Count children types
        num_video = self._get_num_video_files(node.children_nodes)
        num_subtitle = self._get_num_subtitle_files(node.children_nodes)
        num_season = self._get_num_season_dir(node.children_nodes)
        
        self.logger.debug(f"{indent}  - Children: {len(node.children_nodes)} total")
        self.logger.debug(f"{indent}  - Video files: {num_video}")
        self.logger.debug(f"{indent}  - Subtitle files: {num_subtitle}")
        self.logger.debug(f"{indent}  - Season directories: {num_season}")

        # Check directory types in order of specificity
        if self._is_series_dir(node):
            node.classification = 'SERIES_FOLDER'
            self.logger.debug(f"{indent}  ✓ Classified as SERIES_FOLDER")
            self.logger.debug(f"{indent}    Reason: Has title, no video/subtitle files, ≥1 season directory")
            self._classify_series_dir_files(node.children_nodes)
            self._classify_sub_dir(node.children_nodes)

        elif self._is_season_dir(node):
            node.classification = 'SEASON_FOLDER'
            self.logger.debug(f"{indent}  ✓ Classified as SEASON_FOLDER")
            self.logger.debug(f"{indent}    Reason: Has season pattern/number, no episode number, ≥1 video file")
            self._classify_season_dir_files(node.children_nodes)
            self._classify_sub_dir(node.children_nodes)

        elif self._is_subtitle_dir(node):
            node.classification = 'SUBTITLE_FOLDER'
            self.logger.debug(f"{indent}  ✓ Classified as SUBTITLE_FOLDER")
            self.logger.debug(f"{indent}    Reason: No video files, ≥1 subtitle file")
            self._classify_subtitle_dir_files(node.children_nodes)
            self._classify_sub_dir(node.children_nodes)

        elif self._is_extras_dir(node):
            node.classification = 'EXTRAS_FOLDER'
            self.logger.debug(f"{indent}  ✓ Classified as EXTRAS_FOLDER")
            self.logger.debug(f"{indent}    Reason: Has extras pattern, ≥1 video file")
            self._classify_extras_dir_files(node.children_nodes)
            self._classify_sub_dir(node.children_nodes)

        elif self._is_movie_dir(node):
            node.classification = 'MOVIE_FOLDER'
            self.logger.debug(f"{indent}  ✓ Classified as MOVIE_FOLDER")
            self.logger.debug(f"{indent}    Reason: Has title, exactly 1 video file, no season directories")
            self._classify_movie_dir_files(node.children_nodes)
            self._classify_sub_dir(node.children_nodes)
        else:
            node.classification = 'UNKNOWN'
            self.logger.debug(f"{indent}  ✗ Classified as UNKNOWN - no classification rules matched")

        return node

    def _classify_sub_dir(self, nodes: list[Node]) -> None:
        indent = "  " * self._classification_depth
        self.logger.debug(f"{indent}Classifying subdirectories...")
        
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            if node.path_metadata.is_dir:
                self._classify_dir(node)
        

    """
    Functions to classify child files of known directory types
    """
    def _classify_series_dir_files(self, nodes: list[Node]) -> None:
        indent = "  " * self._classification_depth
        self.logger.debug(f"{indent}Classifying SERIES_FOLDER children...")
        
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            # All files in series dir are unknown type
            if node.path_metadata.is_file:
                node.classification = 'UNKNOWN'
                self.logger.debug(f"{indent}  - File in series dir: {node.original_path.name} -> UNKNOWN")

    def _classify_season_dir_files(self, nodes: list[Node]) -> None:
        indent = "  " * self._classification_depth
        self.logger.debug(f"{indent}Classifying SEASON_FOLDER children...")
        
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            # All video files in season dir are episode files
            if self._is_video_file(node):
                node.classification = 'EPISODE_FILE'
                self.logger.debug(f"{indent}  - Video file: {node.original_path.name} -> EPISODE_FILE")
            elif self._is_subtitle_file(node):
                node.classification = 'SUBTITLE_FILE'
                self.logger.debug(f"{indent}  - Subtitle file: {node.original_path.name} -> SUBTITLE_FILE")
            elif node.path_metadata.is_file:
                node.classification = 'UNKNOWN'
                self.logger.debug(f"{indent}  - Other file: {node.original_path.name} -> UNKNOWN")

    def _classify_subtitle_dir_files(self, nodes: list[Node]) -> None:
        indent = "  " * self._classification_depth
        self.logger.debug(f"{indent}Classifying SUBTITLE_FOLDER children...")
        
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')
        
            if self._is_subtitle_file(node):
                node.classification = 'SUBTITLE_FILE'
                self.logger.debug(f"{indent}  - Subtitle file: {node.original_path.name} -> SUBTITLE_FILE")
            elif node.path_metadata.is_file:
                node.classification = 'UNKNOWN'
                self.logger.debug(f"{indent}  - Other file: {node.original_path.name} -> UNKNOWN")

    def _classify_extras_dir_files(self, nodes: list[Node]) -> None:
        indent = "  " * self._classification_depth
        self.logger.debug(f"{indent}Classifying EXTRAS_FOLDER children...")
        
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')
        
            if self._is_video_file(node):
                node.classification = 'EXTRAS_FILE'
                self.logger.debug(f"{indent}  - Video file: {node.original_path.name} -> EXTRAS_FILE")
            elif self._is_subtitle_file(node):
                node.classification = 'SUBTITLE_FILE'
                self.logger.debug(f"{indent}  - Subtitle file: {node.original_path.name} -> SUBTITLE_FILE")
            elif node.path_metadata.is_file:
                node.classification = 'UNKNOWN'
                self.logger.debug(f"{indent}  - Other file: {node.original_path.name} -> UNKNOWN")

    def _classify_movie_dir_files(self, nodes: list[Node]) -> None:
        indent = "  " * self._classification_depth
        self.logger.debug(f"{indent}Classifying MOVIE_FOLDER children...")
        
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            if self._is_video_file(node):
                node.classification = 'MOVIE_FILE'
                self.logger.debug(f"{indent}  - Video file: {node.original_path.name} -> MOVIE_FILE")
            elif self._is_subtitle_file(node):
                node.classification = 'SUBTITLE_FILE'
                self.logger.debug(f"{indent}  - Subtitle file: {node.original_path.name} -> SUBTITLE_FILE")
            elif node.path_metadata.is_file:
                node.classification = 'UNKNOWN'
                self.logger.debug(f"{indent}  - Other file: {node.original_path.name} -> UNKNOWN")

    """
    _is_* helper functions
    """
    def _is_series_dir(self, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        return bool(
                node.path_metadata.is_dir and
                node.media_metadata.title and # Has title
                self._get_num_video_files(node.children_nodes) == 0 and # Has no video files
                self._get_num_subtitle_files(node.children_nodes) == 0 and # Has no subtitle files
                self._get_num_season_dir(node.children_nodes) >= 1 # Has atleast one season directory
                )

    def _is_season_dir(self, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        return bool(
                node.path_metadata.is_dir and
                (node.media_metadata.season_patterns or node.media_metadata.season) and # Has season number or season pattern
                not node.media_metadata.episode and # Does not have an episode number
                self._get_num_video_files(node.children_nodes) >= 1 # Has atleast one video file
                )

    def _is_subtitle_dir(self, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        return bool(
                node.path_metadata.is_dir and
                self._get_num_video_files(node.children_nodes) == 0 and # Has no video files
                self._get_num_subtitle_files(node.children_nodes) >= 1 # Has atleast one subtitle file
                )

    def _is_extras_dir(self, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        return bool(
                node.path_metadata.is_dir and
                node.media_metadata.extras_patterns and # Has extras pattern
                self._get_num_video_files(node.children_nodes) >= 1 # Has atleast one video file
                )

    def _is_movie_dir(self, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        return bool(
                node.path_metadata.is_dir and
                node.media_metadata.title and # Has title
                self._get_num_video_files(node.children_nodes) == 1 and # Has one video file
                self._get_num_season_dir(node.children_nodes) == 0 # Has no season directory
                )

    def _is_video_file(self, node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        return bool(
                node.path_metadata.is_file and
                node.path_metadata.is_file and node.path_metadata.format_type == 'VIDEO'
                )

    def _is_subtitle_file(self, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        return bool(
                node.path_metadata.is_file and
                node.path_metadata.format_type == 'SUBTITLE'
                )
        


    """
    _get_num_* helper functions
    """
    def _get_num_video_files(self, nodes: list[Node]) -> int:
        total_video_files = 0
        for node in nodes:
            if self._is_video_file(node):
                total_video_files = total_video_files + 1

        return total_video_files

    def _get_num_subtitle_files(self, nodes: list[Node]) -> int:
        total_subtitle_files = 0
        for node in nodes:
            if self._is_subtitle_file(node):
                total_subtitle_files = total_subtitle_files + 1

        return total_subtitle_files

    def _get_num_season_dir(self, nodes: list[Node]) -> int:
        """
        Returns number of directories with season pattern and no episode pattern
        """
        total_season_dir = 0
        for node in nodes:
            if self._is_season_dir(node):
                total_season_dir = total_season_dir + 1

        return total_season_dir
