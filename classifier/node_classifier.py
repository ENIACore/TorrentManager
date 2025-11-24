from models import media_metadata
from struct.node import Node
from config.node import NodeType


# TODO: 
# - Validate all video files have same or no epsidoe in _is_season_dir
# - Enable processing of subtitle direcotries with language directories inside
# - Enable processing of extras direcotries with season directories inside
# - Add extra validations for unwanted files/directories (e.g. season folder inside subtitle folder)

class NodeClassifier:
    """
    recursive top-down classification with context propagation
    """

    def __init__(self) -> None:
        pass

    def classify(self, node: Node) -> Node:
        # Throw error if node parsing not completed properly
        if (not node.media_metadata or not node.path_metadata):
            raise ValueError('Media metadata or path metadata not extracted for node')


        if node.path_metadata.is_dir:
            return self._classify_dir(node)
        elif node.path_metadata.is_file:
            return self._classify_file(node)
        else:
            raise ValueError('Node must be classified as file or directory')

    def _classify_file(self, node: Node) -> Node:
        # Throw error if node parsing not completed properly
        if (not node.media_metadata or not node.path_metadata):
            raise ValueError('Media metadata or path metadata not extracted for node')


        if (
            self._is_video_file(node) and
            node.media_metadata.title and
            (node.media_metadata.season_patterns or node.media_metadata.episode_patterns)
            ):
            node.classification = 'EPISODE_FILE'
        elif (
            self._is_video_file(node) and
            node.media_metadata.title
            ):
            node.classification = 'MOVIE_FILE'
        elif self._is_subtitle_file(node):
            raise ValueError('Only episodes or movies are allowed in top level directory')

        return node
    
    def _classify_dir(self, node: Node) -> Node:
        """
        Classifies parent and child nodes in order of specificity
        """
        # Throw error if node parsing not completed properly
        if (not node.media_metadata or not node.path_metadata):
            raise ValueError('Media metadata or path metadata not extracted for node')

        if self._is_series_dir(node):
            self._classify_series_dir_files(node.children_nodes)
            self._classify_sub_dir(node.children_nodes)

        elif self._is_season_dir(node):
            self._classify_season_dir_files(node.children_nodes)
            self._classify_sub_dir(node.children_nodes)

        elif self._is_subtitle_dir(node):
            self._classify_subtitle_dir_files(node.children_nodes)
            self._classify_sub_dir(node.children_nodes)

        elif self._is_extras_dir(node):
            self._classify_extras_dir_files(node.children_nodes)
            self._classify_sub_dir(node.children_nodes)

        elif self._is_movie_dir(node):
            self._classify_movie_dir_files(node.children_nodes)
            self._classify_sub_dir(node.children_nodes)
        else:
            node.classification = 'UNKNOWN'


        return node

    def _classify_sub_dir(self, nodes: list[Node]) -> None:
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            if node.path_metadata.is_dir:
                self._classify_dir(node)
        

    """
    Functions to classify child files of known directory types
    """
    def _classify_series_dir_files(self, nodes: list[Node]) -> None:
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            # All files in series dir are unknown type
            if node.path_metadata.is_file:
                node.classification = 'UNKNOWN'

    def _classify_season_dir_files(self, nodes: list[Node]) -> None:
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            # All video files in season dir are episode files
            if self._is_video_file(node):
                node.classification = 'EPISODE_FILE'
            elif self._is_subtitle_file(node):
                node.classification = 'SUBTITLE_FILE'
            elif node.path_metadata.is_file:
                node.classification = 'UNKNOWN'

    def _classify_subtitle_dir_files(self, nodes: list[Node]) -> None:
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')
        
            if self._is_subtitle_file(node):
                node.classification = 'SUBTITLE_FILE'
            elif node.path_metadata.is_file:
                node.classification = 'UNKNOWN'

    def _classify_extras_dir_files(self, nodes: list[Node]) -> None:
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')
        
            if self._is_video_file(node):
                node.classification = 'EXTRAS_FILE'
            elif self._is_subtitle_file(node):
                node.classification = 'SUBTITLE_FILE'
            elif node.path_metadata.is_file:
                node.classification = 'UNKNOWN'

    def _classify_movie_dir_files(self, nodes: list[Node]) -> None:
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            if self._is_video_file(node):
                node.classification = 'MOVIE_FILE'
            elif self._is_subtitle_file(node):
                node.classification = 'SUBTITLE_FILE'
            elif node.path_metadata.is_file:
                node.classification = 'UNKNOWN'

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


