import os
from os import walk
from os.path import join
from pathlib import Path
from struct.node import Node
from struct.parser import Parser
from classifier.node_classifier import NodeClassifier
from base_manager import BaseManager


# Default paths - can be overridden by environment variables
TORRENT_PATH = os.getenv('TORRENT_DOWNLOAD_PATH', '/mnt/RAID/qbit-data/downloads')
MANAGER_PATH = os.getenv('TORRENT_MANAGER_PATH', '/mnt/RAID/torrent-manager')
MEDIA_PATH = os.getenv('MEDIA_SERVER_PATH', '/mnt/RAID/jelly/media')

# Dry run mode - set to 'true' to only log actions without moving files
DRY_RUN = os.getenv('TORRENT_MANAGER_DRY_RUN', 'true').lower() == 'true'


class TorrentManager(BaseManager):

    def __init__(self, 
                 torrent_path: Path | None = None,
                 manager_path: Path | None = None,
                 media_path: Path | None = None,
                 dry_run: bool | None = None) -> None:
        """
        Initialize TorrentManager with configurable paths.
        
        Args:
            torrent_path: Path where raw torrent files are downloaded
            manager_path: Path for TorrentManager program files/logs/staging
            media_path: Path for media server (Plex/Jellyfin)
            dry_run: If True, only log actions without moving files
        """
        resolved_manager_path = manager_path or Path(MANAGER_PATH)
        resolved_dry_run = dry_run if dry_run is not None else DRY_RUN
        
        super().__init__(manager_path=resolved_manager_path, dry_run=resolved_dry_run)
        
        self.torrent_path = torrent_path or Path(TORRENT_PATH)
        self.media_path = media_path or Path(MEDIA_PATH)
        
        # Track processing depth for tree separation
        self._processing_depth = 0
        
        # Validate all critical paths exist
        self._validate_paths([
            (self.torrent_path, "Torrent download path"),
            (self.manager_path.parent, "Manager path parent"),
            (self.media_path.parent, "Media path parent"),
        ])

        # Path for files or dirs unable to be parsed automatically
        self.error_path = self.manager_path / 'error'
        # Path for parsed movies and shows to be moved to
        self.series_path = self.media_path / 'shows'
        self.movies_path = self.media_path / 'movies'
        # Staging path for processed torrents
        self.staging_path = self.manager_path / 'staging'

        # Create required directories
        self._create_directories([
            self.error_path,
            self.series_path,
            self.movies_path,
            self.staging_path,
            self.manager_path / 'logs',
        ])
        
        self._log_initialization()

    def _log_initialization(self) -> None:
        """Log initialization details."""
        self.logger.info(f'TorrentManager initialized')
        self.logger.info(f'  Download path: {self.torrent_path}')
        self.logger.info(f'  Manager path: {self.manager_path}')
        self.logger.info(f'  Media path: {self.media_path}')
        self.logger.info(f'  Staging path: {self.staging_path}')
        self.logger.info(f'  Error path: {self.error_path}')
        self.logger.info(f'  Dry run mode: {self.dry_run}')

    def validate(self, node: Node) -> bool:
        """
        Validate that all nodes are properly classified.
        
        Args:
            node: The node to validate
            
        Returns:
            True if node and all children are properly classified
            
        Raises:
            ValueError: If required metadata is missing
        """
        if not node or not node.path_metadata or not node.media_metadata:
            raise ValueError(f'Missing metadata for node: {node}')

        if node.classification == 'UNKNOWN':
            self.logger.error(f'Node has unknown classification: {node.original_path}')
            return False
        
        # These classifications are only valid as children, not at root level
        child_only_classifications = {
            'SUBTITLE_FOLDER', 'EXTRAS_FOLDER', 'SUBTITLE_FILE', 'EXTRAS_FILE'
        }
        
        if not node.parent_node and node.classification in child_only_classifications:
            self.logger.error(
                f'Invalid root classification {node.classification}: {node.original_path}'
            )
            return False

        # Recursively validate children
        for child_node in node.children_nodes:
            if not self.validate(child_node):
                return False

        return True
        
    def move_to_error_dir(self, node: Node) -> bool:
        """
        Move unprocessable torrent to error directory for manual handling.
        
        Args:
            node: The node to move to error directory
            
        Returns:
            True if successfully moved, False otherwise
        """
        if not node.original_path:
            self.logger.error('Cannot move node without original path to error directory')
            return False
            
        return self._move_to_directory(node.original_path, self.error_path)

    def process_torrents(self) -> dict:
        """
        Process all torrents in the download directory.
        
        Returns:
            Dictionary with processing statistics
        """
        parser = Parser()
        classifier = NodeClassifier(manager_path=self.manager_path)
        
        stats = {
            'processed': 0,
            'failed_validation': 0,
            'failed_processing': 0,
            'skipped': 0,
        }

        try:
            root, dirs, files = next(walk(self.torrent_path))
        except StopIteration:
            self.logger.warning(f'Torrent directory is empty or inaccessible: {self.torrent_path}')
            return stats
        
        if not dirs and not files:
            self.logger.info('No torrents found to process')
            return stats
    
        # Process directories
        for dir_name in dirs:
            dir_path = Path(join(root, dir_name))
            result = self._process_single_torrent(dir_path, parser, classifier)
            stats[result] += 1

        # Process files
        for file_name in files:
            file_path = Path(join(root, file_name))
            result = self._process_single_torrent(file_path, parser, classifier)
            stats[result] += 1
        
        self.logger.info(f'Processing complete: {stats}')
        return stats

    def _process_single_torrent(self, path: Path, parser: Parser, classifier: NodeClassifier) -> str:
        """
        Process a single torrent file or directory.
        
        Args:
            path: Path to the torrent file or directory
            parser: Parser instance
            classifier: NodeClassifier instance
            
        Returns:
            Result status: 'processed', 'failed_validation', 'failed_processing', or 'skipped'
        """
        # Log tree separator for root level torrents
        if self._processing_depth == 0:
            self.logger.debug("=" * 80)
            self.logger.debug(f"STARTING TORRENT PROCESSING: {path.name}")
            self.logger.debug(f"Full path: {path}")
            self.logger.debug("=" * 80)
        
        self._processing_depth += 1
        result = 'skipped'
        
        try:
            self.logger.info(f'Processing: {path}')
            
            # Stage 1: Parse
            self.logger.debug("-" * 40)
            self.logger.debug("STAGE 1: PARSING NODE TREE")
            self.logger.debug("-" * 40)
            head = parser.process_nodes(None, path)
            
            # Stage 2: Classify
            self.logger.debug("-" * 40)
            self.logger.debug("STAGE 2: CLASSIFYING NODE TREE")
            self.logger.debug("-" * 40)
            head = classifier.classify(head)
            
            # Stage 3: Validate
            self.logger.debug("-" * 40)
            self.logger.debug("STAGE 3: VALIDATING CLASSIFICATIONS")
            self.logger.debug("-" * 40)
            if not self.validate(head):
                self.logger.error(f'Validation failed, moving to error dir: {path}')
                self.move_to_error_dir(head)
                result = 'failed_validation'
            else:
                # Stage 4: Process
                self.logger.debug("-" * 40)
                self.logger.debug("STAGE 4: PROCESSING NODE TREE")
                self.logger.debug("-" * 40)
                if self._process_torrent(head):
                    # Stage 5: Move to staging
                    self.logger.debug("-" * 40)
                    self.logger.debug("STAGE 5: MOVING TO STAGING")
                    self.logger.debug("-" * 40)
                    self._move_to_staging(head)
                    result = 'processed'
                else:
                    self.logger.error(f'Processing failed, moving to error dir: {path}')
                    self.move_to_error_dir(head)
                    result = 'failed_processing'
                    
        except Exception as e:
            self.logger.error(f'Exception processing {path}: {e}', exc_info=True)
            result = 'skipped'
        finally:
            self._processing_depth -= 1
            
            # Log completion for root level torrents
            if self._processing_depth == 0:
                self.logger.debug("=" * 80)
                if result == 'processed':
                    self.logger.debug(f"✓ COMPLETED TORRENT PROCESSING: {path.name}")
                    self.logger.debug(f"STATUS: SUCCESS")
                elif result == 'failed_validation':
                    self.logger.debug(f"✗ COMPLETED TORRENT PROCESSING: {path.name}")
                    self.logger.debug(f"STATUS: VALIDATION FAILED")
                elif result == 'failed_processing':
                    self.logger.debug(f"✗ COMPLETED TORRENT PROCESSING: {path.name}")
                    self.logger.debug(f"STATUS: PROCESSING FAILED")
                else:
                    self.logger.debug(f"✗ COMPLETED TORRENT PROCESSING: {path.name}")
                    self.logger.debug(f"STATUS: SKIPPED (Exception)")
                self.logger.debug("=" * 80)
                self.logger.debug("")  # Empty line for separation
        
        return result

    def _process_torrent(self, node: Node) -> bool:
        """
        Process a torrent node and assign new_path to all nodes.
        
        Args:
            node: The root node to process
            
        Returns:
            True if torrent successfully processed
        """
        self.logger.info(f'Processing node: {node.original_path}')
        
        classification_handlers = {
            'MOVIE_FOLDER': self._process_movie_folder,
            'SERIES_FOLDER': self._process_series_folder,
            'SEASON_FOLDER': lambda n: self._process_season_folder(n, parent_path=Path('/')),
            'MOVIE_FILE': lambda n: self._process_movie_file(n, parent_path=Path('/')),
            'EPISODE_FILE': lambda n: self._process_episode_file(n, parent_path=Path('/')),
        }
        
        handler = classification_handlers.get(node.classification)
        if handler:
            return handler(node)
        
        self.logger.warning(f'No handler for classification: {node.classification}')
        return False

    def _get_formatted_folder_name(self, node: Node) -> str:
        """
        Get formatted folder name for movie/series folders.
        
        Format: Title (Year) e.g., "The Matrix (1999)"
        
        Args:
            node: Node with media_metadata
            
        Returns:
            Formatted folder name
        """
        if not node.media_metadata:
            raise ValueError('Media metadata not extracted for node')
        
        if node.media_metadata.title and node.media_metadata.year:
            return node.media_metadata.get_formatted_title() + '.' + str(node.media_metadata.year)
        else:
            return 'UNKNOWN'

    def _get_formatted_file_name(self, node: Node) -> str:
        """
        Get formatted file name using media_metadata string representation.
        
        Args:
            node: Node with media_metadata and path_metadata
            
        Returns:
            Formatted file name with extension
        """
        if not node.media_metadata or not node.path_metadata:
            raise ValueError('Metadata not extracted for node')
        
        base_name = str(node.media_metadata)
        ext = node.path_metadata.ext
        
        if ext and not ext.startswith('.'):
            ext = '.' + ext
            
        return base_name + ext.lower()

    def _process_movie_folder(self, node: Node, parent_path: Path = Path('/')) -> bool:
        """
        Process movie folder structure.
        
        Expected structure:
            folder/
                - movie file (max 1 media file)
                - subtitle files OR subtitle folder OR None
                - extras folder OR None
        """
        if not node.media_metadata:
            return False
            
        folder_name = self._get_formatted_folder_name(node)
        node.new_path = parent_path / folder_name
        
        self.logger.info(f'Processing movie folder: {node.original_path} -> {node.new_path}')
        
        child_handlers = {
            'MOVIE_FILE': lambda c: self._process_movie_file(c, node.new_path),
            'SUBTITLE_FILE': lambda c: self._process_subtitle_file(c, node.new_path),
            'SUBTITLE_FOLDER': lambda c: self._process_subtitle_folder(c, node.new_path),
            'EXTRAS_FOLDER': lambda c: self._process_extras_folder(c, node.new_path),
        }
        
        return self._process_children(node, child_handlers, 'movie folder')

    def _process_series_folder(self, node: Node, parent_path: Path = Path('/')) -> bool:
        """
        Process series folder structure.
        
        Expected structure:
            folder/
                - 1 or more Season folders
                - Subtitle folder OR None
                - Extras folder OR None
        """
        if not node.media_metadata:
            return False
            
        folder_name = self._get_formatted_folder_name(node)
        node.new_path = parent_path / folder_name
        
        self.logger.info(f'Processing series folder: {node.original_path} -> {node.new_path}')
        
        child_handlers = {
            'SEASON_FOLDER': lambda c: self._process_season_folder(c, node.new_path),
            'SUBTITLE_FOLDER': lambda c: self._process_subtitle_folder(c, node.new_path),
            'EXTRAS_FOLDER': lambda c: self._process_extras_folder(c, node.new_path),
        }
        
        return self._process_children(node, child_handlers, 'series folder')

    def _process_season_folder(self, node: Node, parent_path: Path = Path('/')) -> bool:
        """
        Process season folder structure.
        
        Expected structure:
            folder/
                - 1 or more episode files
                - subtitle files OR subtitle folder OR None
                - Extras folder OR None
        """
        if not node.media_metadata:
            return False
            
        node.new_path = parent_path / f'S{node.media_metadata.get_formatted_season_num}'
        
        self.logger.info(f'Processing season folder: {node.original_path} -> {node.new_path}')
        
        child_handlers = {
            'EPISODE_FILE': lambda c: self._process_episode_file(c, node.new_path),
            'SUBTITLE_FILE': lambda c: self._process_subtitle_file(c, node.new_path),
            'SUBTITLE_FOLDER': lambda c: self._process_subtitle_folder(c, node.new_path),
            'EXTRAS_FOLDER': lambda c: self._process_extras_folder(c, node.new_path),
        }
        
        return self._process_children(node, child_handlers, 'season folder')

    def _process_subtitle_folder(self, node: Node, parent_path: Path) -> bool:
        """
        Process subtitle folder structure.
        
        Expected structure:
            Subtitles/
                - 1 or more subtitle files
        """
        node.new_path = parent_path / 'Subtitles'
        
        self.logger.info(f'Processing subtitle folder: {node.original_path} -> {node.new_path}')
        
        child_handlers = {
            'SUBTITLE_FILE': lambda c: self._process_subtitle_file(c, node.new_path),
        }
        
        return self._process_children(node, child_handlers, 'subtitle folder')

    def _process_extras_folder(self, node: Node, parent_path: Path) -> bool:
        """
        Process extras folder structure.
        
        Expected structure:
            Extras/
                - 1 or more season folders OR 1 or more extras files
                - subtitle files OR subtitle folder OR None
        """
        node.new_path = parent_path / 'Extras'
        
        self.logger.info(f'Processing extras folder: {node.original_path} -> {node.new_path}')
        
        child_handlers = {
            'EXTRAS_FILE': lambda c: self._process_extras_file(c, node.new_path),
            'SUBTITLE_FILE': lambda c: self._process_subtitle_file(c, node.new_path),
            'SUBTITLE_FOLDER': lambda c: self._process_subtitle_folder(c, node.new_path),
            'SEASON_FOLDER': lambda c: self._process_season_folder(c, node.new_path),
        }
        
        return self._process_children(node, child_handlers, 'extras folder')

    def _process_children(self, node: Node, handlers: dict, context: str) -> bool:
        """
        Process all children of a node using the appropriate handlers.
        
        Args:
            node: Parent node
            handlers: Dictionary mapping classification to handler function
            context: Context string for logging
            
        Returns:
            True (always succeeds, warnings logged for unexpected types)
        """
        for child in node.children_nodes:
            handler = handlers.get(child.classification)
            if handler:
                handler(child)
            else:
                self.logger.warning(
                    f'Unexpected node type {child.classification} in {context}: {child.original_path}'
                )
        return True

    def _process_movie_file(self, node: Node, parent_path: Path = Path('/')) -> bool:
        """Process a movie file and assign its new path."""
        if not node.media_metadata or not node.path_metadata:
            return False
            
        file_name = self._get_formatted_file_name(node)
        node.new_path = parent_path / file_name
        
        self.logger.info(f'Processing movie file: {node.original_path} -> {node.new_path}')
        return True

    def _process_episode_file(self, node: Node, parent_path: Path = Path('/')) -> bool:
        """Process an episode file and assign its new path."""
        if not node.media_metadata or not node.path_metadata:
            return False
            
        file_name = self._get_formatted_file_name(node)
        node.new_path = parent_path / file_name
        
        self.logger.info(f'Processing episode file: {node.original_path} -> {node.new_path}')
        return True

    def _process_subtitle_file(self, node: Node, parent_path: Path) -> bool:
        """
        Process a subtitle file and assign its new path.
        Preserves the original filename to maintain language info.
        """
        if not node.original_path:
            return False
            
        file_name = self._sanitize_name(node.original_path.name) + '.' + node.path_metadata.ext
        if node.media_metadata.language:
            file_name = Path('subtitle_' + node.media_metadata.language)

        node.new_path = parent_path / file_name
        
        self.logger.info(f'Processing subtitle file: {node.original_path} -> {node.new_path}')
        return True

    def _process_extras_file(self, node: Node, parent_path: Path) -> bool:
        """Process an extras file and assign its new path."""
        if not node.original_path:
            return False
            
        file_name = self._sanitize_name(node.original_path.stem) + '.' + node.path_metadata.ext
        node.new_path = parent_path / file_name
        
        self.logger.info(f'Processing extras file: {node.original_path} -> {node.new_path}')
        return True

    def _move_to_staging(self, node: Node) -> None:
        """
        Recursively move all files in the node tree to staging directory.
        
        Args:
            node: Root node to move
        """
        self._move_node_to_staging(node)

    def _move_node_to_staging(self, node: Node) -> None:
        """
        Move a single node and its children to staging.
        Creates directories as needed, copies files.
        """
        if not node.original_path or not hasattr(node, 'new_path') or not node.new_path:
            self.logger.error(f'Node missing original_path or new_path: {node}')
            return

        # Calculate the full destination path
        relative_new_path = node.new_path
        if str(relative_new_path).startswith('/'):
            relative_new_path = Path(str(relative_new_path)[1:])
        
        dest_path = self.staging_path / relative_new_path
        
        # Check for conflicts in staging
        if dest_path.exists():
            dest_path = self._get_unique_path(dest_path)
            self.logger.warning(f'Staging conflict resolved: {node.new_path} -> {dest_path}')

        if node.path_metadata and node.path_metadata.is_dir:
            self._move_directory_to_staging(node, dest_path)
        elif node.path_metadata and node.path_metadata.is_file:
            self._move_file_to_staging(node, dest_path)

    def _move_directory_to_staging(self, node: Node, dest_path: Path) -> None:
        """Move a directory node to staging."""
        if not self._create_directory(dest_path):
            return

        for child in node.children_nodes:
            self._move_node_to_staging(child)

    def _move_file_to_staging(self, node: Node, dest_path: Path) -> None:
        """Move a file node to staging."""
        self._copy_file(node.original_path, dest_path)

    def get_staging_summary(self, node: Node, indent: int = 0) -> str:
        """
        Get a formatted string showing the planned file structure.
        Useful for reviewing what will be created.
        
        Args:
            node: Root node to summarize
            indent: Current indentation level
            
        Returns:
            Formatted string representation of the structure
        """
        lines = []
        prefix = '  ' * indent
        
        if hasattr(node, 'new_path') and node.new_path:
            node_type = 'DIR' if node.path_metadata and node.path_metadata.is_dir else 'FILE'
            lines.append(f'{prefix}[{node_type}] {node.new_path}')
            
            for child in node.children_nodes:
                child_summary = self.get_staging_summary(child, indent + 1)
                if child_summary:
                    lines.append(child_summary)
                
        return '\n'.join(lines)

    def cleanup_original(self, node: Node) -> bool:
        """
        Remove original torrent files after successful staging.
        Call this after verifying staging was successful.
        
        Args:
            node: Root node whose original files should be removed
            
        Returns:
            True if cleanup successful
        """
        return self._remove_path(node.original_path)
