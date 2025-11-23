from typing import Literal
from pathlib import Path
from models.media_metadata import MediaMetadata
from extractor.media_extractor import MediaExtractor
import re



"""
Show Folder:
    Requirements: 
        - extract title is not None
        - contains multiple season folders
        # TODO add multiple episodes from different seasons not in season folders
    Optional:
        - contains subtitle folder
        - contains extras folder

Season Folder:
    Requirements:
        - pattern match from SEASON_PATTERNS
        - MediaMetadata.season is not None
        -   All contained episode files' MediaMetadata.season are the same 
            OR all contained episode files' MediaMetadata.season are None 
        - Contains multiple episode files
    Optional: 
        -   Contains subtitle folder 
            OR contains multiple subtitle files
        - Contains extras folder

Movie Folder:
    Requirements:
        - MediaMetadata.type is movie
        - Contains one movie file
        # TODO handle multiple part movies
    Optional:
        -   Contains subtitle folder 
            OR contains multiple subtitle files
        - Contains extras folder

Subtitles Folder:
    Required: 
        - Contains no media files
        - Contains one or more subtitles files 

Extras Folder:
    Required:
        - MediaMetadata.type is extras
        - Contains one or more media files
        # TODO Add handling for season folders inside extras folder and extras folders inside extras folder
    Optional: 
        -   Contains subtitles folder 
            OR contains multiple subtitle files
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

"""
Movie File:
    Required:
        - MediaMetadata.season is None
        - MediaMetadata.episode is None
        - MediaMetadata.title is not None
        - MediaExtractor.has_pattern with EPISODES_PATTERNS is None
        - MediaExtractor.has_pattern with SEASON_PATTERNS is None
        - MediaMetadata.ext is in VIDEO_EXTENSIONS

Episode File:
    Required:
        -   MediaMetadata.season is not None 
            OR MediaMetadata.episode is not None
            OR MediaExtractor.has_pattern with SEASON_PATTERNS is not None
            OR MediaExtractor.has_pattern with EPISODES_PATTERNS is not None
        - MediaMetadata.ext is in VIDEO_EXTENSIONS

Subtitle File:
    Required:
        - MediaMetadata.ext is in SUBTITLE_EXTENSIONS
        # TODO Add common subtitle patterns

Extra File:
    Required
        - MediaMetadata.ext is in VIDEO_EXTENSIONS


EXTRAS_PATTERNS
"""
FileType = Literal[
    'MOVIE_OR_EXTRAS_FILE',
    'EPISODE_FILE',
    'SUBTITLE_FILE',


    #'AUDIO_FILE', TODO
]

MediaType = DirectoryType | FileType


class MediaClassifier:
    """
    Classifies media files and folders 
    """
    
    def __init__(self):
        self.extractor = MediaExtractor()
    
    def classify_media(self, path: Path) -> MediaType | None:

        if path.is_dir():
            return self._classify_directory(path)
        elif path.is_file():
            return self._classify_file(path)
        else:
            return None
    
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
