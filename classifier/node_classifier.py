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

        print(f"\n{'='*80}")
        print(f"[CLASSIFY] Starting classification for: {node.original_path}")
        print(f"[CLASSIFY] Is dir: {node.path_metadata.is_dir}, Is file: {node.path_metadata.is_file}")

        if node.path_metadata.is_dir:
            print(f"[CLASSIFY] Routing to _classify_dir()")
            return self._classify_dir(node)
        elif node.path_metadata.is_file:
            print(f"[CLASSIFY] Routing to _classify_file()")
            return self._classify_file(node)
        else:
            raise ValueError('Node must be classified as file or directory')

    def _classify_file(self, node: Node) -> Node:
        print(f"[_classify_file] Classifying file: {node.original_path}")

        # Throw error if node parsing not completed properly
        if (not node.media_metadata or not node.path_metadata):
            raise ValueError('Media metadata or path metadata not extracted for node')

        is_video = self._is_video_file(node)
        print(f"[_classify_file] Is video file: {is_video}")
        print(f"[_classify_file] Has title: {bool(node.media_metadata.title)}")
        print(f"[_classify_file] Title value: {node.media_metadata.title}")
        print(f"[_classify_file] Season patterns: {node.media_metadata.season_patterns}")
        print(f"[_classify_file] Episode patterns: {node.media_metadata.episode_patterns}")

        if (
            self._is_video_file(node) and
            node.media_metadata.title and
            (node.media_metadata.season_patterns or node.media_metadata.episode_patterns)
            ):
            node.classification = 'EPISODE_FILE'
            print(f"[_classify_file] ✓ Classified as EPISODE_FILE")
        elif (
            self._is_video_file(node) and
            node.media_metadata.title
            ):
            node.classification = 'MOVIE_FILE'
            print(f"[_classify_file] ✓ Classified as MOVIE_FILE")
        elif self._is_subtitle_file(node):
            print(f"[_classify_file] ✗ Error: Subtitle file in top level directory")
            raise ValueError('Only episodes or movies are allowed in top level directory')
        else:
            print(f"[_classify_file] ✗ No classification matched - remains UNKNOWN")

        return node
    
    def _classify_dir(self, node: Node) -> Node:
        """
        Classifies parent and child nodes in order of specificity
        """
        print(f"\n[_classify_dir] Classifying directory: {node.original_path}")
        print(f"[_classify_dir] Number of children: {len(node.children_nodes)}")

        # Throw error if node parsing not completed properly
        if (not node.media_metadata or not node.path_metadata):
            raise ValueError('Media metadata or path metadata not extracted for node')

        print(f"[_classify_dir] Checking if SERIES_DIR...")
        if self._is_series_dir(node):
            print(f"[_classify_dir] ✓ Classified as SERIES_DIR")
            self._classify_series_dir_files(node.children_nodes)
            self._classify_sub_dir(node.children_nodes)

        elif self._is_season_dir(node):
            print(f"[_classify_dir] ✓ Classified as SEASON_DIR")
            self._classify_season_dir_files(node.children_nodes)
            self._classify_sub_dir(node.children_nodes)

        elif self._is_subtitle_dir(node):
            print(f"[_classify_dir] ✓ Classified as SUBTITLE_DIR")
            self._classify_subtitle_dir_files(node.children_nodes)
            self._classify_sub_dir(node.children_nodes)

        elif self._is_extras_dir(node):
            print(f"[_classify_dir] ✓ Classified as EXTRAS_DIR")
            self._classify_extras_dir_files(node.children_nodes)
            self._classify_sub_dir(node.children_nodes)

        elif self._is_movie_dir(node):
            print(f"[_classify_dir] ✓ Classified as MOVIE_DIR")
            self._classify_movie_dir_files(node.children_nodes)
            self._classify_sub_dir(node.children_nodes)
        else:
            node.classification = 'UNKNOWN'
            print(f"[_classify_dir] ✗ NO MATCH - Classified as UNKNOWN")


        return node

    def _classify_sub_dir(self, nodes: list[Node]) -> None:
        print(f"  [_classify_sub_dir] Processing {len(nodes)} nodes for subdirectories")
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            if node.path_metadata.is_dir:
                print(f"  [_classify_sub_dir] Found subdirectory: {node.original_path}, recursing...")
                self._classify_dir(node)
        

    """
    Functions to classify child files of known directory types
    """
    def _classify_series_dir_files(self, nodes: list[Node]) -> None:
        print(f"  [_classify_series_dir_files] Classifying {len(nodes)} child nodes")
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            # All files in series dir are unknown type
            if node.path_metadata.is_file:
                node.classification = 'UNKNOWN'
                print(f"    [_classify_series_dir_files] File {node.original_path} -> UNKNOWN")

    def _classify_season_dir_files(self, nodes: list[Node]) -> None:
        print(f"  [_classify_season_dir_files] Classifying {len(nodes)} child nodes")
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            # All video files in season dir are episode files
            if self._is_video_file(node):
                node.classification = 'EPISODE_FILE'
                print(f"    [_classify_season_dir_files] File {node.original_path} -> EPISODE_FILE")
            elif self._is_subtitle_file(node):
                node.classification = 'SUBTITLE_FILE'
                print(f"    [_classify_season_dir_files] File {node.original_path} -> SUBTITLE_FILE")
            elif node.path_metadata.is_file:
                node.classification = 'UNKNOWN'
                print(f"    [_classify_season_dir_files] File {node.original_path} -> UNKNOWN")

    def _classify_subtitle_dir_files(self, nodes: list[Node]) -> None:
        print(f"  [_classify_subtitle_dir_files] Classifying {len(nodes)} child nodes")
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            if self._is_subtitle_file(node):
                node.classification = 'SUBTITLE_FILE'
                print(f"    [_classify_subtitle_dir_files] File {node.original_path} -> SUBTITLE_FILE")
            elif node.path_metadata.is_file:
                node.classification = 'UNKNOWN'
                print(f"    [_classify_subtitle_dir_files] File {node.original_path} -> UNKNOWN")

    def _classify_extras_dir_files(self, nodes: list[Node]) -> None:
        print(f"  [_classify_extras_dir_files] Classifying {len(nodes)} child nodes")
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            if self._is_video_file(node):
                node.classification = 'EXTRAS_FILE'
                print(f"    [_classify_extras_dir_files] File {node.original_path} -> EXTRAS_FILE")
            elif self._is_subtitle_file(node):
                node.classification = 'SUBTITLE_FILE'
                print(f"    [_classify_extras_dir_files] File {node.original_path} -> SUBTITLE_FILE")
            elif node.path_metadata.is_file:
                node.classification = 'UNKNOWN'
                print(f"    [_classify_extras_dir_files] File {node.original_path} -> UNKNOWN")

    def _classify_movie_dir_files(self, nodes: list[Node]) -> None:
        print(f"  [_classify_movie_dir_files] Classifying {len(nodes)} child nodes")
        for node in nodes:
            if not node or not node.media_metadata or not node.path_metadata:
                raise ValueError('Media metadata or path metadata not extracted for node')

            if self._is_video_file(node):
                node.classification = 'MOVIE_FILE'
                print(f"    [_classify_movie_dir_files] File {node.original_path} -> MOVIE_FILE")
            elif self._is_subtitle_file(node):
                node.classification = 'SUBTITLE_FILE'
                print(f"    [_classify_movie_dir_files] File {node.original_path} -> SUBTITLE_FILE")
            elif node.path_metadata.is_file:
                node.classification = 'UNKNOWN'
                print(f"    [_classify_movie_dir_files] File {node.original_path} -> UNKNOWN")

    """
    _is_* helper functions
    """
    def _is_series_dir(self, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        is_dir = node.path_metadata.is_dir
        has_title = bool(node.media_metadata.title)
        num_video_files = self._get_num_video_files(node.children_nodes)
        num_subtitle_files = self._get_num_subtitle_files(node.children_nodes)
        num_season_dirs = self._get_num_season_dir(node.children_nodes)

        print(f"  [_is_series_dir] is_dir={is_dir}, has_title={has_title} ('{node.media_metadata.title}')")
        print(f"  [_is_series_dir] video_files={num_video_files}, subtitle_files={num_subtitle_files}, season_dirs={num_season_dirs}")

        result = bool(
                is_dir and
                has_title and # Has title
                num_video_files == 0 and # Has no video files
                num_subtitle_files == 0 and # Has no subtitle files
                num_season_dirs >= 1 # Has atleast one season directory
                )

        print(f"  [_is_series_dir] Result: {result}")
        return result

    def _is_season_dir(self, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        is_dir = node.path_metadata.is_dir
        has_season = bool(node.media_metadata.season_patterns or node.media_metadata.season)
        has_episode = bool(node.media_metadata.episode)
        num_video_files = self._get_num_video_files(node.children_nodes)

        print(f"  [_is_season_dir] is_dir={is_dir}, has_season={has_season}, has_episode={has_episode}")
        print(f"  [_is_season_dir] season_patterns={node.media_metadata.season_patterns}, season={node.media_metadata.season}")
        print(f"  [_is_season_dir] episode={node.media_metadata.episode}, video_files={num_video_files}")

        result = bool(
                is_dir and
                has_season and # Has season number or season pattern
                not has_episode and # Does not have an episode number
                num_video_files >= 1 # Has atleast one video file
                )

        print(f"  [_is_season_dir] Result: {result}")
        return result

    def _is_subtitle_dir(self, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        is_dir = node.path_metadata.is_dir
        num_video_files = self._get_num_video_files(node.children_nodes)
        num_subtitle_files = self._get_num_subtitle_files(node.children_nodes)

        print(f"  [_is_subtitle_dir] is_dir={is_dir}, video_files={num_video_files}, subtitle_files={num_subtitle_files}")

        result = bool(
                is_dir and
                num_video_files == 0 and # Has no video files
                num_subtitle_files >= 1 # Has atleast one subtitle file
                )

        print(f"  [_is_subtitle_dir] Result: {result}")
        return result

    def _is_extras_dir(self, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        is_dir = node.path_metadata.is_dir
        has_extras_patterns = bool(node.media_metadata.extras_patterns)
        num_video_files = self._get_num_video_files(node.children_nodes)

        print(f"  [_is_extras_dir] is_dir={is_dir}, has_extras_patterns={has_extras_patterns}")
        print(f"  [_is_extras_dir] extras_patterns={node.media_metadata.extras_patterns}, video_files={num_video_files}")

        result = bool(
                is_dir and
                has_extras_patterns and # Has extras pattern
                num_video_files >= 1 # Has atleast one video file
                )

        print(f"  [_is_extras_dir] Result: {result}")
        return result

    def _is_movie_dir(self, node: Node) -> bool:
        if not node or not node.media_metadata or not node.path_metadata:
            raise ValueError('Media metadata or path metadata not extracted for node')

        is_dir = node.path_metadata.is_dir
        has_title = bool(node.media_metadata.title)
        num_video_files = self._get_num_video_files(node.children_nodes)
        num_season_dirs = self._get_num_season_dir(node.children_nodes)

        print(f"  [_is_movie_dir] is_dir={is_dir}, has_title={has_title} ('{node.media_metadata.title}')")
        print(f"  [_is_movie_dir] video_files={num_video_files}, season_dirs={num_season_dirs}")

        result = bool(
                is_dir and
                has_title and # Has title
                num_video_files == 1 and # Has one video file
                num_season_dirs == 0 # Has no season directory
                )

        print(f"  [_is_movie_dir] Result: {result}")
        return result

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
        video_files = []
        for node in nodes:
            if self._is_video_file(node):
                total_video_files = total_video_files + 1
                video_files.append(node.original_path)

        if video_files:
            print(f"    [_get_num_video_files] Found {total_video_files} video files: {video_files}")
        return total_video_files

    def _get_num_subtitle_files(self, nodes: list[Node]) -> int:
        total_subtitle_files = 0
        subtitle_files = []
        for node in nodes:
            if self._is_subtitle_file(node):
                total_subtitle_files = total_subtitle_files + 1
                subtitle_files.append(node.original_path)

        if subtitle_files:
            print(f"    [_get_num_subtitle_files] Found {total_subtitle_files} subtitle files: {subtitle_files}")
        return total_subtitle_files

    def _get_num_season_dir(self, nodes: list[Node]) -> int:
        """
        Returns number of directories with season pattern and no episode pattern
        """
        total_season_dir = 0
        season_dirs = []
        print(f"    [_get_num_season_dir] Checking {len(nodes)} nodes for season directories")
        for node in nodes:
            if node.path_metadata and node.path_metadata.is_dir:
                print(f"      [_get_num_season_dir] Checking directory: {node.original_path}")
            if self._is_season_dir(node):
                total_season_dir = total_season_dir + 1
                season_dirs.append(node.original_path)

        print(f"    [_get_num_season_dir] Found {total_season_dir} season directories: {season_dirs}")
        return total_season_dir


