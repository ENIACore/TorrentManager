from struct.node import Node
from logger.logger import Logger


# TODO: 
# - Add processing for Episode folders
# - Validate all video files have same or no episode in _is_season_dir
# - Enable processing of subtitle directories with language directories inside
# - Enable processing of extras directories with season directories inside
# - Add extra validations for unwanted files/directories (e.g. season folder inside subtitle folder)

class NodeClassifier:
    """
    recursive top-down classification with context propagation
    """

    _logger: Logger = Logger.get_logger()

    @classmethod
    def classify(cls, node: Node) -> Node:
        """Entry point for classification."""
        cls._logger.debug("=" * 60)
        cls._logger.debug(f"STARTING CLASSIFICATION: {node.original_path}")
        cls._logger.debug("=" * 60)
        
        # Throw error if node parsing not completed properly
        if not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        if node.path_metadata.is_dir:
            result = cls._classify_dir(node)
        elif node.path_metadata.is_file:
            result = cls._classify_file(node)
        else:
            raise ValueError('Node must be classified as file or directory')
        
        cls._logger.debug("=" * 60)
        cls._logger.debug(f"COMPLETED CLASSIFICATION: {node.original_path}")
        cls._logger.debug(f"ROOT CLASSIFICATION: {result.classification}")
        cls._logger.debug("=" * 60)
        
        return result

    @classmethod
    def _classify_file(cls, node: Node) -> Node:
        cls._logger.debug("+------------------------------------------------------+")
        cls._logger.debug(f"Classifying FILE: {node.original_path}")
        
        # Throw error if node parsing not completed properly
        if not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        # Check if it's a video file
        is_video = cls._is_video_file(node)
        cls._logger.debug(f"Is video file: {is_video}")
        cls._logger.debug(f"Format type: {node.path_metadata.format_type}")
        
        if is_video:
            has_title = bool(node.media_metadata.title)
            has_season = bool(node.media_metadata.season_patterns or node.media_metadata.episode_patterns)
            
            cls._logger.debug(f"Has title: {has_title} ('{node.media_metadata.title}')")
            cls._logger.debug(f"Has season/episode patterns: {has_season}")
            
            if has_title and has_season:
                node.classification = 'EPISODE_FILE'
                cls._logger.debug(f"Classified as EPISODE_FILE")
            elif has_title:
                node.classification = 'MOVIE_FILE'
                cls._logger.debug(f"Classified as MOVIE_FILE")
        elif cls._is_subtitle_file(node):
            cls._logger.debug(f"Is subtitle file: True")
            raise ValueError('Only episodes or movies are allowed in top level directory')

        if not node.classification:
            cls._logger.debug(f"Classification failed - no classification assigned")
        
        return node
    
    @classmethod
    def _classify_dir(cls, node: Node) -> Node:
        """
        Classifies parent and child nodes in order of specificity
        """
        cls._logger.debug("+------------------------------------------------------+")
        cls._logger.debug(f"Classifying DIRECTORY: {node.original_path}")
        
        # Throw error if node parsing not completed properly
        if not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        # Log metadata for debugging
        cls._logger.debug(f"Has title: {bool(node.media_metadata.title)} ('{node.media_metadata.title}')")
        cls._logger.debug(f"Season patterns: {node.media_metadata.season_patterns}")
        cls._logger.debug(f"Season number: {node.media_metadata.season}")
        cls._logger.debug(f"Episode number: {node.media_metadata.episode}")
        cls._logger.debug(f"Extras patterns: {node.media_metadata.extras_patterns}")
        
        # Count children types
        num_video = cls._get_num_video_files(node.children_nodes)
        num_subtitle = cls._get_num_subtitle_files(node.children_nodes)
        num_season = cls._get_num_season_dir(node.children_nodes)
        
        cls._logger.debug(f"Children: {len(node.children_nodes)} total")
        cls._logger.debug(f"Video files: {num_video}")
        cls._logger.debug(f"Subtitle files: {num_subtitle}")
        cls._logger.debug(f"Season directories: {num_season}")

        # Check directory types in order of specificity
        if cls._is_series_dir(node):
            node.classification = 'SERIES_FOLDER'
            cls._logger.debug(f"Classified as SERIES_FOLDER")
            cls._logger.debug(f"Reason: Has title, no video/subtitle files, ≥1 season directory")
            cls._classify_series_dir_files(node.children_nodes)
            cls._classify_sub_dir(node.children_nodes)

        elif cls._is_season_dir(node):
            node.classification = 'SEASON_FOLDER'
            cls._logger.debug(f"Classified as SEASON_FOLDER")
            cls._logger.debug(f"Reason: Has season pattern/number, no episode number, ≥1 video file")
            cls._classify_season_dir_files(node.children_nodes)
            cls._classify_sub_dir(node.children_nodes)

        elif cls._is_subtitle_dir(node):
            node.classification = 'SUBTITLE_FOLDER'
            cls._logger.debug(f"Classified as SUBTITLE_FOLDER")
            cls._logger.debug(f"Reason: No video files, ≥1 subtitle file")
            cls._classify_subtitle_dir_files(node.children_nodes)
            cls._classify_sub_dir(node.children_nodes)

        elif cls._is_extras_dir(node):
            node.classification = 'EXTRAS_FOLDER'
            cls._logger.debug(f"Classified as EXTRAS_FOLDER")
            cls._logger.debug(f"Reason: Has extras pattern, ≥1 video file")
            cls._classify_extras_dir_files(node.children_nodes)
            cls._classify_sub_dir(node.children_nodes)

        elif cls._is_movie_dir(node):
            node.classification = 'MOVIE_FOLDER'
            cls._logger.debug(f"Classified as MOVIE_FOLDER")
            cls._logger.debug(f"Reason: Has title, exactly 1 video file, no season directories")
            cls._classify_movie_dir_files(node.children_nodes)
            cls._classify_sub_dir(node.children_nodes)
        else:
            node.classification = 'UNKNOWN'
            cls._logger.debug(f"Classified as UNKNOWN - no classification rules matched")

        return node

    @classmethod
    def _classify_sub_dir(cls, nodes: list[Node]) -> None:
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            if node.path_metadata.is_dir:
                cls._classify_dir(node)

    """
    Functions to classify child files of known directory types
    """
    @classmethod
    def _classify_series_dir_files(cls, nodes: list[Node]) -> None:
        cls._logger.debug("+------------------------------------------------------+")
        cls._logger.debug(f"Classifying SERIES_FOLDER children...")
        
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            # All files in series dir are unknown type
            if node.path_metadata.is_file:
                node.classification = 'UNKNOWN'
                cls._logger.debug(f"File in series dir: {node.original_path.name} -> UNKNOWN")

    @classmethod
    def _classify_season_dir_files(cls, nodes: list[Node]) -> None:
        cls._logger.debug("+------------------------------------------------------+")
        cls._logger.debug(f"Classifying SEASON_FOLDER children...")
        
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            # All video files in season dir are episode files
            if cls._is_video_file(node):
                node.classification = 'EPISODE_FILE'
                cls._logger.debug(f"Video file: {node.original_path.name} -> EPISODE_FILE")
            elif cls._is_subtitle_file(node):
                node.classification = 'SUBTITLE_FILE'
                cls._logger.debug(f"Subtitle file: {node.original_path.name} -> SUBTITLE_FILE")
            elif node.path_metadata.is_file:
                node.classification = 'UNKNOWN'
                cls._logger.debug(f"Other file: {node.original_path.name} -> UNKNOWN")

    @classmethod
    def _classify_subtitle_dir_files(cls, nodes: list[Node]) -> None:
        cls._logger.debug("+------------------------------------------------------+")
        cls._logger.debug(f"Classifying SUBTITLE_FOLDER children...")
        
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')
        
            if cls._is_subtitle_file(node):
                node.classification = 'SUBTITLE_FILE'
                cls._logger.debug(f"Subtitle file: {node.original_path.name} -> SUBTITLE_FILE")
            elif node.path_metadata.is_file:
                node.classification = 'UNKNOWN'
                cls._logger.debug(f"Other file: {node.original_path.name} -> UNKNOWN")

    @classmethod
    def _classify_extras_dir_files(cls, nodes: list[Node]) -> None:
        cls._logger.debug("+------------------------------------------------------+")
        cls._logger.debug(f"Classifying EXTRAS_FOLDER children...")
        
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')
        
            if cls._is_video_file(node):
                node.classification = 'EXTRAS_FILE'
                cls._logger.debug(f"Video file: {node.original_path.name} -> EXTRAS_FILE")
            elif cls._is_subtitle_file(node):
                node.classification = 'SUBTITLE_FILE'
                cls._logger.debug(f"Subtitle file: {node.original_path.name} -> SUBTITLE_FILE")
            elif node.path_metadata.is_file:
                node.classification = 'UNKNOWN'
                cls._logger.debug(f"Other file: {node.original_path.name} -> UNKNOWN")

    @classmethod
    def _classify_movie_dir_files(cls, nodes: list[Node]) -> None:
        cls._logger.debug("+------------------------------------------------------+")
        cls._logger.debug(f"Classifying MOVIE_FOLDER children...")
        
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            if cls._is_video_file(node):
                node.classification = 'MOVIE_FILE'
                cls._logger.debug(f"Video file: {node.original_path.name} -> MOVIE_FILE")
            elif cls._is_subtitle_file(node):
                node.classification = 'SUBTITLE_FILE'
                cls._logger.debug(f"Subtitle file: {node.original_path.name} -> SUBTITLE_FILE")
            elif node.path_metadata.is_file:
                node.classification = 'UNKNOWN'
                cls._logger.debug(f"Other file: {node.original_path.name} -> UNKNOWN")

    """
    _is_* helper functions
    """
    @classmethod
    def _is_series_dir(cls, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        return bool(
                node.path_metadata.is_dir and
                node.media_metadata.title and
                cls._get_num_video_files(node.children_nodes) == 0 and
                cls._get_num_subtitle_files(node.children_nodes) == 0 and
                cls._get_num_season_dir(node.children_nodes) >= 1
                )

    @classmethod
    def _is_season_dir(cls, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        return bool(
                node.path_metadata.is_dir and
                (node.media_metadata.season_patterns or node.media_metadata.season) and
                not node.media_metadata.episode and
                cls._get_num_video_files(node.children_nodes) >= 1
                )

    @classmethod
    def _is_subtitle_dir(cls, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        return bool(
                node.path_metadata.is_dir and
                cls._get_num_video_files(node.children_nodes) == 0 and
                cls._get_num_subtitle_files(node.children_nodes) >= 1
                )

    @classmethod
    def _is_extras_dir(cls, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        return bool(
                node.path_metadata.is_dir and
                node.media_metadata.extras_patterns and
                cls._get_num_video_files(node.children_nodes) >= 1
                )

    @classmethod
    def _is_movie_dir(cls, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        return bool(
                node.path_metadata.is_dir and
                node.media_metadata.title and
                cls._get_num_video_files(node.children_nodes) == 1 and
                cls._get_num_season_dir(node.children_nodes) == 0
                )

    @classmethod
    def _is_video_file(cls, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        return bool(
                node.path_metadata.is_file and
                node.path_metadata.format_type == 'VIDEO'
                )

    @classmethod
    def _is_subtitle_file(cls, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        return bool(
                node.path_metadata.is_file and
                node.path_metadata.format_type == 'SUBTITLE'
                )

    """
    _get_num_* helper functions
    """
    @classmethod
    def _get_num_video_files(cls, nodes: list[Node]) -> int:
        total_video_files = 0
        for node in nodes:
            if cls._is_video_file(node):
                total_video_files += 1
        return total_video_files

    @classmethod
    def _get_num_subtitle_files(cls, nodes: list[Node]) -> int:
        total_subtitle_files = 0
        for node in nodes:
            if cls._is_subtitle_file(node):
                total_subtitle_files += 1
        return total_subtitle_files

    @classmethod
    def _get_num_season_dir(cls, nodes: list[Node]) -> int:
        """
        Returns number of directories with season pattern and no episode pattern
        """
        total_season_dir = 0
        for node in nodes:
            if cls._is_season_dir(node):
                total_season_dir += 1
        return total_season_dir
