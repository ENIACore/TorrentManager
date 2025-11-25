import shutil
import re
from pathlib import Path
from abc import ABC, abstractmethod
from logger.logger import Logger


class BaseManager(ABC):
    """
    Base class providing common file management utilities.
    
    Subclasses should implement their own initialization and processing logic
    while inheriting these generic file operations.
    """

    def __init__(self, manager_path: Path, dry_run: bool = True) -> None:
        """
        Initialize BaseManager with core configuration.
        
        Args:
            manager_path: Path for manager program files/logs/staging
            dry_run: If True, only log actions without moving files
        """
        self.manager_path = manager_path
        self.dry_run = dry_run
        self.logger = Logger(manager_path=self.manager_path)

    def _validate_paths(self, paths_to_validate: list[tuple[Path, str]]) -> None:
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

    def _create_directories(self, directories: list[Path]) -> None:
        """
        Create all required working directories.
        
        Args:
            directories: List of directory paths to create
        """
        for path in directories:
            path.mkdir(parents=True, exist_ok=True)

    def _get_unique_path(self, path: Path) -> Path:
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
        
        while True:
            new_path = parent / f"{stem}_{counter}{suffix}"
            if not new_path.exists():
                return new_path
            counter += 1
            
            if counter > 1000:
                raise RuntimeError(f"Could not find unique path for {path}")

    def _move_to_directory(self, source: Path, dest_dir: Path) -> bool:
        """
        Move a file or directory to a destination directory.
        
        Args:
            source: Source file or directory path
            dest_dir: Destination directory path
            
        Returns:
            True if successfully moved, False otherwise
        """
        dest = dest_dir / source.name
        dest = self._get_unique_path(dest)
        
        if self.dry_run:
            self.logger.info(f'[DRY RUN] Would move {source} to {dest}')
            return True

        try:
            if source.is_dir():
                shutil.copytree(source, dest)
            else:
                shutil.copy2(source, dest)
            self.logger.info(f'Moved: {source} -> {dest}')
            return True
        except Exception as e:
            self.logger.error(f'Failed to move {source} to {dest}: {e}')
            return False

    def _copy_file(self, source: Path, dest: Path) -> bool:
        """
        Copy a file to a destination path.
        
        Args:
            source: Source file path
            dest: Destination file path
            
        Returns:
            True if successfully copied, False otherwise
        """
        if self.dry_run:
            self.logger.info(f'[DRY RUN] Would copy file: {source} -> {dest}')
            return True
            
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            self.logger.info(f'Copied file: {source} -> {dest}')
            return True
        except Exception as e:
            self.logger.error(f'Failed to copy file {source} to {dest}: {e}')
            return False

    def _create_directory(self, path: Path) -> bool:
        """
        Create a directory at the specified path.
        
        Args:
            path: Directory path to create
            
        Returns:
            True if successfully created, False otherwise
        """
        if self.dry_run:
            self.logger.info(f'[DRY RUN] Would create directory: {path}')
            return True
            
        try:
            path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f'Created directory: {path}')
            return True
        except Exception as e:
            self.logger.error(f'Failed to create directory {path}: {e}')
            return False

    def _remove_path(self, path: Path) -> bool:
        """
        Remove a file or directory.
        
        Args:
            path: Path to remove
            
        Returns:
            True if successfully removed, False otherwise
        """
        if self.dry_run:
            self.logger.info(f'[DRY RUN] Would remove: {path}')
            return True
            
        try:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            self.logger.info(f'Removed: {path}')
            return True
        except Exception as e:
            self.logger.error(f'Failed to remove {path}: {e}')
            return False

    def _sanitize_name(self, name: str) -> str:
        """
        Sanitize a filename by removing special characters and formatting.
        
        Args:
            name: The name to sanitize
            ext: Optional file extension to append
            
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
