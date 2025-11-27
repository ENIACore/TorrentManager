import shutil
import re
from pathlib import Path
from abc import ABC
from logger.logger import Logger
from config.settings import (MANAGER_PATH, DRY_RUN, MANAGER_PATH, MEDIA_PATH, TORRENT_PATH)
from struct.node import Node


class BaseManager(ABC):

    _logger: Logger = Logger.get_logger()
    _dry_run: bool = DRY_RUN

    # Main paths
    _manager_path: Path = Path(MANAGER_PATH)
    _torrent_path: Path = Path(TORRENT_PATH)
    _media_path: Path = Path(MEDIA_PATH)

    # Manager Paths
    _error_path = Path(MANAGER_PATH) / 'error'
    _staging_path = Path(MANAGER_PATH) / 'staging'
        
    # Media Sub paths
    _series_path = Path(MEDIA_PATH) / 'shows'
    _movies_path = Path(MEDIA_PATH) / 'movies'

    """
    Base class providing common file management utilities.
    """
    @classmethod
    def _validate_paths(cls, paths_to_validate: list[tuple[Path, str]]) -> None:
        """
        Validate that all required paths exist.
        
        Args:
            paths_to_validate: List of (path, description) tuples
            
        Raises:
            ValueError: If any required paths do not exist
        """
        missing_paths = []
        for path, description in paths_to_validate:
            if not path.exists():
                missing_paths.append(f"{description}: {path}")
        
        if missing_paths:
            raise ValueError(
                f"Required paths do not exist:\n" + "\n".join(f"  - {p}" for p in missing_paths)
            )

    @classmethod
    def _create_directories(cls, directories: list[Path]) -> None:
        """
        Create all required working directories.
        
        Args:
            directories: List of directory paths to create
        """
        for path in directories:
            path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _get_unique_path(cls, path: Path) -> Path:
        """
        Get a unique path by appending a counter if the path already exists.
        
        Args:
            path: The desired path
            
        Returns:
            A unique path that doesn't conflict with existing files
            
        Raises:
            RuntimeError: If unable to find a unique path within 1000 attempts
        """
        if not path.exists():
            return path
            
        counter = 1
        stem = path.stem
        suffix = path.suffix
        parent = path.parent

        while counter < 1000:
            new_path = parent / f"{stem}_{counter}{suffix}"
            if not new_path.exists():
                return new_path
            counter += 1
                
        raise RuntimeError(f"Could not find unique path for {path}")

    @classmethod
    def _move_to_directory(cls, source: Path, dest_dir: Path) -> bool:
        """
        Move a file or directory to a destination directory.
        
        Args:
            source: Source file or directory path
            dest_dir: Destination directory path
            
        Returns:
            True if successfully moved, False otherwise
        """
        dest = dest_dir / source.name
        dest = cls._get_unique_path(dest)
        
        if cls._dry_run:
            cls._logger.info(f'[DRY RUN] Would move {source} to {dest}')
            return True

        try:
            if source.is_dir():
                shutil.copytree(source, dest)
            else:
                shutil.copy2(source, dest)
            cls._logger.info(f'Moved: {source} -> {dest}')
            return True
        except Exception as e:
            cls._logger.error(f'Failed to move {source} to {dest}: {e}')
            return False

    @classmethod
    def _copy_file(cls, source: Path, dest: Path) -> bool:
        """
        Copy a file to a destination path.
        
        Args:
            source: Source file path
            dest: Destination file path
            
        Returns:
            True if successfully copied, False otherwise
        """
        if cls._dry_run:
            cls._logger.info(f'[DRY RUN] Would copy file: {source} -> {dest}')
            return True
            
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            cls._logger.info(f'Copied file: {source} -> {dest}')
            return True
        except Exception as e:
            cls._logger.error(f'Failed to copy file {source} to {dest}: {e}')
            return False

    @classmethod
    def _create_directory(cls, path: Path) -> bool:
        """
        Create a directory at the specified path.
        
        Args:
            path: Directory path to create
            
        Returns:
            True if successfully created, False otherwise
        """
        if cls._dry_run:
            cls._logger.info(f'[DRY RUN] Would create directory: {path}')
            return True
            
        try:
            path.mkdir(parents=True, exist_ok=True)
            cls._logger.info(f'Created directory: {path}')
            return True
        except Exception as e:
            cls._logger.error(f'Failed to create directory {path}: {e}')
            return False

    @classmethod
    def _remove_path(cls, path: Path) -> bool:
        """
        Remove a file or directory.
        
        Args:
            path: Path to remove
            
        Returns:
            True if successfully removed, False otherwise
        """
        if cls._dry_run:
            cls._logger.info(f'[DRY RUN] Would remove: {path}')
            return True
            
        try:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            cls._logger.info(f'Removed: {path}')
            return True
        except Exception as e:
            cls._logger.error(f'Failed to remove {path}: {e}')
            return False

    @classmethod
    def _sanitize_name(cls, name: str) -> str:
        """
        Sanitize a filename by removing special characters and formatting.
        
        Args:
            name: The name to sanitize
            
        Returns:
            Sanitized name with words capitalized and joined by dots
        """
        if not name:
            return ''
            
        lowercase_title = name.lower()
        lowercase_title = lowercase_title.replace('\'', '').replace('\"', '')

        # Remove special characters and join words with '.'
        alphanumeric_title = re.sub(r'[^a-z0-9]+', '.', lowercase_title)
        # Remove '.' from beginning & end
        alphanumeric_title = alphanumeric_title.strip('.')

        # Capitalize each word
        words = alphanumeric_title.split('.')
        words = [word.capitalize() for word in words if word]

        return '.'.join(words)

    @classmethod
    def _move_to_error_dir(cls, node: Node) -> bool:
        """
        Move unprocessable torrent to error directory for manual handling.
        """

        if not node.original_path:
            cls._logger.error('Cannot move node without original path to error directory')
            return False
            
        return cls._move_to_directory(node.original_path, cls._error_path)


    @classmethod
    def _move_path_to_error_dir(cls, path: Path) -> bool:
        return cls._move_to_directory(path, cls._error_path)


    @classmethod
    def _log_initialization(cls) -> None:
        """Log initialization details."""
        cls._logger.info(f'TorrentManager initialized')
        cls._logger.info(f'  Download path: {cls._torrent_path}')
        cls._logger.info(f'  Manager path: {cls._manager_path}')
        cls._logger.info(f'  Media path: {cls._media_path}')
        cls._logger.info(f'  Staging path: {cls._staging_path}')
        cls._logger.info(f'  Error path: {cls._error_path}')
        cls._logger.info(f'  Dry run mode: {cls._dry_run}')
