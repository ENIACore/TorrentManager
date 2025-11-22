from typing import Literal
from pathlib import Path
from models.media_metadata import MediaMetadata
from extractor.media_extractor import MediaExtractor
import re



"""
Series Folder:
    Required Contains: Multiple season folders
    Optional Contains: Subtitle folder
Season Folder:
    Required Contains: Multiple episode files of the same season
    Optional Contains: Subtitle folder OR multiple subtitle files
Movie Folder:
    Required Contains: One media (movie) file
    Optional Contains: (Subtitle folder OR multiple subtitle files) and/or extras folder
Subtitles Folder:
    Required Contains: One or more subtitles files 
Extras Folder:
    Required Contains: One or more media files or folders, folder or subfolders/files are MediaExtractor._is_extras
    Optional Contains: Subtitle folder OR multiple subtitle files
"""
DirectoryType = Literal[
    'SERIES_FOLDER',
    'SEASON_FOLDER', 
    'MOVIE_FOLDER',
    'SUBTITLE_FOLDER',
    'EXTRAS_FOLDER',

    #'MIXED_MEDIA', TODO
    #'MOVIE_COLLECTION', TODO
]

FileType = Literal[
    'MOVIE_FILE',
    'EPISODE_FILE',
    'SUBTITLE_FILE',
    'EXTRA_FILE',


    #'AUDIO_FILE', TODO
]

MediaType = DirectoryType | FileType


class MediaClassifier:
    """
    Classifies media files and folders 
    """
    
    def __init__(self):
        self.extractor = MediaExtractor()
    
    def classify_media(self, path: Path) -> MediaType:

        if path.is_dir():
            return self._classify_directory(path)
        else:
            return self._classify_file(path)
    
    def _classify_directory(self, path: Path) -> DirectoryType:
        return 'EXTRAS_FOLDER'
    
    def _classify_file(self, path: Path) -> FileType:
        return 'MOVIE_FILE'

    def _is_series_folder(self, path: Path) -> bool:
        return False
    def _is_season_folder(self, path: Path) -> bool:
        return False
    def _is_movie_folder(self, path: Path) -> bool:
        return False
    def _is_subtitle_folder(self, path: Path) -> bool:
        return False
    def _is_extras_folder(self, path: Path) -> bool:
        return False

    def _is_movie_file(self, path: Path) -> bool:
        return False
    def _is_episode_file(self, path: Path) -> bool:
        return False
    def _is_subtitle_file(self, path: Path) -> bool:
        return False
    def _is_extra_file(self, path: Path) -> bool:
        return False
