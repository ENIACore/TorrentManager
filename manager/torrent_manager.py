import os
import shutil
from os import walk, makedirs
from os.path import join, exists
from pathlib import Path
from struct.node import Node
from struct.parser import Parser
from classifier.node_classifier import NodeClassifier
from logger.logger import Logger

# Default paths - can be overridden by environment variables
TORRENT_DOWNLOAD_PATH = os.getenv('TORRENT_DOWNLOAD_PATH', '/mnt/RAID/qbit-data/downloads')
TORRENT_MANAGER_PATH = os.getenv('TORRENT_MANAGER_PATH', '/mnt/RAID/torrent-manager')


class TorrentManager:

    def __init__(self) -> None:
        # Get paths from environment variables or use defaults
        self.download_path = Path(TORRENT_DOWNLOAD_PATH)
        self.manager_path = Path(TORRENT_MANAGER_PATH)
        
        # Validate paths exist
        if not self.download_path.exists():
            raise ValueError(f"Download path does not exist: {self.download_path}")
        
        # Create manager directories if they don't exist
        self.error_path = self.manager_path / 'error'
        self.series_path = self.manager_path / 'series'
        self.movies_path = self.manager_path / 'movies'

        self.logger = Logger(self.manager_path)
        
        for path in [self.error_path, self.series_path, self.movies_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f'TorrentManager initialized with download path {self.download_path}')
        self.logger.info(f'TorrentManager initialized with manager path {self.manager_path}')
        self.logger.info(f'TorrentManager initialized with paths error - {self.error_path}, series - {self.series_path}, movies - {self.movies_path}')



