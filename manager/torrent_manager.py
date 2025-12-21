from os import walk
from os.path import join
from pathlib import Path
from typing import Callable, Dict
from tree.node import Node
from tree.parser import Parser
from classifier.node_classifier import NodeClassifier
from manager.base_manager import BaseManager


class TorrentManager(BaseManager):

    @classmethod
    def validate(cls, node: Node) -> bool:
        """
        Validate that all nodes are properly classified.
        """

        if node.classification == 'UNKNOWN':
            cls._get_logger().error(f'Node has unknown classification: {node.original_path}')
            return False
        
        # These classifications are only valid as children, not at root level
        child_only_classifications = {
            'SUBTITLE_FOLDER', 'EXTRAS_FOLDER', 'SUBTITLE_FILE', 'EXTRAS_FILE'
        }
        
        if not node.parent_node and node.classification in child_only_classifications:
            cls._get_logger().error(
                f'Invalid root classification {node.classification}: {node.original_path}'
            )
            return False

        # Recursively validate children
        for child_node in node.children_nodes:
            if not cls.validate(child_node):
                return False

        return True

    @classmethod
    def process_torrents(cls):
        """
        Process all torrents in the download directory.
        
        Returns:
            Dictionary with processing statistics
        """
        cls._log_initialization()

        # Validate all critical paths exist
        cls._validate_paths([
            (cls._torrent_path, "Torrent download path"),
            (cls._manager_path, "Manager path parent"),
            (cls._media_path, "Media path parent"),
        ])


        cls.stats = {
            'processed': 0,
            'failed_validation': 0,
            'failed_processing': 0,
            'skipped': 0,
        }

        try:
            root, dirs, files = next(walk(cls._torrent_path))
        except StopIteration:
            cls._get_logger().warning(f'Torrent directory is empty or inaccessible: {cls._torrent_path}')
            return
        
        if not dirs and not files:
            cls._get_logger().info('No torrents found to process')
    
        # Process directories
        for dir_name in dirs:
            dir_path = Path(join(root, dir_name))
            cls._process_torrent(dir_path)

        # Process files
        for file_name in files:
            file_path = Path(join(root, file_name))
            cls._process_torrent(file_path)
        
        cls._get_logger().info(f'Processing complete')
        cls._get_logger().info(f'Successfully processed: {cls.stats['processed']}')
        cls._get_logger().info(f'Failed validation: {cls.stats['failed_validation']}')
        cls._get_logger().info(f'Failed Processing: {cls.stats['failed_processing']}')
        cls._get_logger().info(f'Skipped: {cls.stats['skipped']}')

    @classmethod
    def _process_torrent(cls, path: Path):
        """
        Process torrent file or directory.
        """

        cls._get_logger().debug("=" * 80)
        cls._get_logger().debug(f"STARTING TORRENT PROCESSING: {path.name}")
        cls._get_logger().debug(f"Full path: {path}")
        cls._get_logger().debug("=" * 80)
        
        try:
            cls._get_logger().info(f'Processing: {path}')
            
            # Stage 1: Parse
            cls._get_logger().debug("-" * 40)
            cls._get_logger().debug("STAGE 1: PARSING NODE TREE")
            cls._get_logger().debug("-" * 40)
            head = Parser.process_nodes(None, path)

            if not head:
                cls._get_logger().error(f'Unable to process nodes for path {path}, moving to error dir')
                cls._move_path_to_error_dir(path)
                return
            
            # Stage 2: Classify
            cls._get_logger().debug("-" * 40)
            cls._get_logger().debug("STAGE 2: CLASSIFYING NODE TREE")
            cls._get_logger().debug("-" * 40)
            head = NodeClassifier.classify(head)
            
            # Stage 3: Validate
            cls._get_logger().debug("-" * 40)
            cls._get_logger().debug("STAGE 3: VALIDATING CLASSIFICATIONS")
            cls._get_logger().debug("-" * 40)
            if not cls.validate(head):
                cls._get_logger().error(f'Validation failed, moving to error dir: {path}')
                cls._move_to_error_dir(head)
                cls.stats['failed_validation'] += 1
                return

            # Stage 4: Process
            cls._get_logger().debug("-" * 40)
            cls._get_logger().debug("STAGE 4: PROCESSING NODE TREE")
            cls._get_logger().debug("-" * 40)
            if not cls._assign_paths(head):
                cls._get_logger().error(f'Processing failed, moving to error dir: {path}')
                cls._move_to_error_dir(head)
                cls.stats['failed_processing'] += 1
                return

            # Stage 5: Move to staging
            cls._get_logger().debug("-" * 40)
            cls._get_logger().debug("STAGE 5: MOVING TO STAGING")
            cls._get_logger().debug("-" * 40)
            cls._move_to_staging(head)
            cls.stats['processed'] += 1

                    
        except Exception as e:
            cls._get_logger().error(f'Exception processing {path}: {e}', exc_info=True)
            cls.stats['skipped'] += 1

    @classmethod
    def _assign_paths(cls, node: Node) -> bool:
        """
        Recursively process a torrent node and assign new_path to all nodes.
        """
        cls._get_logger().info(f'Processing node: {node.original_path}')
        

        if node.classification == 'MOVIE_FOLDER':
            return cls._process_movie_folder(node)
        elif node.classification == 'SERIES_FOLDER':
            return cls._process_series_folder(node)
        elif node.classification == 'SEASON_FOLDER':
            return cls._process_season_folder(node)
        elif node.classification == 'MOVIE_FILE':
            return cls._process_movie_file(node)
        elif node.classification == 'EPISODE_FILE':
            return cls._process_episode_file(node)
        else:
            cls._get_logger().warning(f'No root handler for classification: {node.classification}')
            return False

    @classmethod
    def _process_movie_folder(cls, node: Node) -> bool:
        # Get relative path for folder
        parent_node = node.parent_node.new_path if (node.parent_node and node.parent_node.new_path) else Path('/')
        node.new_path = parent_node / cls._get_formatted_folder_name(node)

        cls._get_logger().info(f'Processing movie folder: {node.original_path} -> {node.new_path}')

        # Validate all required children exist
        required_classifications = {
            'MOVIE_FILE'
        }

        if not cls._validate_required_children(node, required_classifications):
            return False

        # Process children with handlers appropriate to classifications
        child_handlers = {
            'MOVIE_FILE': cls._process_movie_file,
            'SUBTITLE_FILE': cls._process_subtitle_file,
            'SUBTITLE_FOLDER': cls._process_subtitle_folder,
            'EXTRAS_FOLDER': cls._process_extras_folder
        }

        return cls._process_children(node, child_handlers)

    @classmethod
    def _process_series_folder(cls, node: Node) -> bool: 
        # Get relative path for folder
        parent_node = node.parent_node.new_path if (node.parent_node and node.parent_node.new_path) else Path('/')
        node.new_path = parent_node / cls._get_formatted_folder_name(node)

        cls._get_logger().info(f'Processing series folder: {node.original_path} -> {node.new_path}')

        required_classifications = {
            'SEASON_FOLDER'
        }

        if not cls._validate_required_children(node, required_classifications):
            return False
        
        child_handlers = {
            'SEASON_FOLDER': cls._process_season_folder,
            'SUBTITLE_FOLDER': cls._process_subtitle_folder,
            'EXTRAS_FOLDER': cls._process_extras_folder,
        }
        
        return cls._process_children(node, child_handlers)

    @classmethod
    def _process_season_folder(cls, node: Node) -> bool:
        parent_node = node.parent_node.new_path if (node.parent_node and node.parent_node.new_path) else Path('/')
        node.new_path = parent_node / f'S{node.media_metadata.get_formatted_season_num()}'

        cls._get_logger().info(f'Processing season folder: {node.original_path} -> {node.new_path}')

        required_classifications = {
            'EPISODE_FILE'
        }
    
        if not cls._validate_required_children(node, required_classifications):
            return False

        child_handlers = {
            'EPISODE_FILE': cls._process_episode_file,
            'SUBTITLE_FILE': cls._process_subtitle_file,
            'SUBTITLE_FOLDER': cls._process_subtitle_folder,
            'EXTRAS_FOLDER': cls._process_extras_folder,
        }
        
        return cls._process_children(node, child_handlers)

    @classmethod
    def _process_subtitle_folder(cls, node: Node) -> bool:
        # Get relative path for folder
        parent_node = node.parent_node.new_path if (node.parent_node and node.parent_node.new_path) else Path('/')
        node.new_path = parent_node / 'Subtitles'

        cls._get_logger().info(f'Processing subtitle folder: {node.original_path} -> {node.new_path}')

        required_classifications = {
            'SUBTITLE_FILE'
        }
    
        if not cls._validate_required_children(node, required_classifications):
            return False
        
        child_handlers = {
            'SUBTITLE_FILE': cls._process_subtitle_file,
        }
        
        return cls._process_children(node, child_handlers)

    @classmethod
    def _process_extras_folder(cls, node: Node) -> bool:
        # Get relative path for folder
        parent_node = node.parent_node.new_path if (node.parent_node and node.parent_node.new_path) else Path('/')
        node.new_path = parent_node / 'Extras'

        cls._get_logger().info(f'Processing extras folder: {node.original_path} -> {node.new_path}')
        
        """
        # TODO - Add check for extras file OR season folder
        required_classifications = {
            'EXTRAS_FILE'
        }
    
        if not cls._validate_required_children(node, required_classifications):
            return False
        """
        
        child_handlers = {
            'EXTRAS_FILE': cls._process_extras_file,
            'SUBTITLE_FILE': cls._process_subtitle_file,
            'SUBTITLE_FOLDER': cls._process_subtitle_folder,
            'SEASON_FOLDER': cls._process_season_folder,
        }
        
        return cls._process_children(node, child_handlers)

    @classmethod
    def _process_movie_file(cls, node: Node) -> bool:
        parent_path = node.parent_node.new_path if (node.parent_node and node.parent_node.new_path) else Path('/')
        node.new_path = parent_path / cls._get_formatted_file_name(node) 
            
        cls._get_logger().info(f'Processing movie file: {node.original_path} -> {node.new_path}')

        return True

    @classmethod
    def _process_episode_file(cls, node: Node) -> bool:
        parent_path = node.parent_node.new_path if (node.parent_node and node.parent_node.new_path) else Path('/')
        node.new_path = parent_path / cls._get_formatted_file_name(node) 
        
        cls._get_logger().info(f'Processing episode file: {node.original_path} -> {node.new_path}')

        return True

    @classmethod
    def _process_subtitle_file(cls, node: Node) -> bool:
        parent_path = node.parent_node.new_path if (node.parent_node and node.parent_node.new_path) else Path('/')
        file_name = cls._sanitize_name(node.original_path.stem) + '.' + node.path_metadata.ext.lower()
        if node.media_metadata.language:
            file_name = 'subtitle_' + node.media_metadata.language
        node.new_path = parent_path / file_name
            
        cls._get_logger().info(f'Processing subtitle file: {node.original_path} -> {node.new_path}')

        return True

    @classmethod
    def _process_extras_file(cls, node: Node) -> bool:
        parent_path = node.parent_node.new_path if (node.parent_node and node.parent_node.new_path) else Path('/')
        file_name = cls._sanitize_name(node.original_path.stem) + '.' + node.path_metadata.ext
        node.new_path = parent_path / file_name
        
        cls._get_logger().info(f'Processing extras file: {node.original_path} -> {node.new_path}')

        return True

    @classmethod
    def _move_to_staging(cls, node: Node) -> None:
        """
        Move a single node and its children to staging.
        Creates directories as needed, copies files.
        """
        if not node.original_path or not node.new_path:
            cls._get_logger().error(f'Node missing original_path or new_path: {node}')
            raise ValueError(f'Node missing original_path or new_path: {node}')

        # Calculate the full destination path
        relative_new_path = node.new_path
        if str(relative_new_path).startswith('/'):
            relative_new_path = Path(str(relative_new_path)[1:])
        
        dest_path = cls._staging_path / relative_new_path
        
        # Ensure path is unique
        dest_path = cls._get_unique_path(dest_path)

        if node.path_metadata and node.path_metadata.is_dir:
            cls._move_directory_to_staging(node, dest_path)
        elif node.path_metadata and node.path_metadata.is_file:
            cls._move_file_to_staging(node, dest_path)

    @classmethod
    def _move_directory_to_staging(cls, node: Node, dest_path: Path) -> None:
        if not cls._create_directory(dest_path):
            return

        for child in node.children_nodes:
            cls._move_to_staging(child)

    @classmethod
    def _move_file_to_staging(cls, node: Node, dest_path: Path) -> None:
        # CHANGED: This now moves files instead of copying them
        cls._copy_file(node.original_path, dest_path)


    @classmethod
    def cleanup_original(cls, node: Node) -> bool:
        return cls._remove_path(node.original_path)

    
    @classmethod
    def _validate_required_children(cls, node: Node, required_classifications: set[str] | list[str]) -> bool:
        for classification in required_classifications:
            res = False

            for child in node.children_nodes:
                if child.classification == classification:
                    res = True
                    break

            if not res:
                cls._get_logger().error(f'Child classification {classification} not found in node {node.classification}')
                return False

        return True

    @classmethod
    def _process_children(cls, node: Node, handlers: Dict[str, Callable]) -> bool:
        
        for child in node.children_nodes:
            handler = handlers.get(child.classification)

            if not handler:
                cls._get_logger().error(f' Unexpected node type {child.classification} for {node.classification}')
                return False

            if not handler(child):
                return False

        return True

    @classmethod
    def _get_formatted_folder_name(cls, node: Node) -> str:
        meta = node.media_metadata
        
        if not meta.title:
            return 'UNKNOWN'
        
        title = meta.get_formatted_title()
        return f'{title}.{meta.year}' if meta.year else title

    @classmethod
    def _get_formatted_file_name(cls, node: Node) -> str:
        
        base_name = str(node.media_metadata)
        ext = node.path_metadata.ext.lower()
        
            
        return base_name + '.' + ext.lower()
