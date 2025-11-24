from typing import Literal
"""
Description: Types to classify nodes
Attributes:
    DirectoryType: Types of direcotories found in torrents
    FileType: Types of files found in torrents
    UnknownType: Type used to describe files or directories not currently handled
"""

"""
Series Folder:
    Requirements:
        - metadata.title is not None
        - Contains multiple season folders
        # TODO add handling for episode files from different seasons
    Optional:
        - Contains subtitle folder
        - Contains extras folder

Season Folder:
    Requirements:
        - Folder name matches SEASON_PATTERNS OR metadata.season is not None
        - All episode files have same season OR all have None
        - Contains multiple episode files
    Optional:
        - Contains subtitle folder OR multiple subtitle files
        - Contains extras folder

Movie Folder:
    Requirements:
        - metadata.title is not None
        - Contains one movie file
        # TODO handle multiple part movies
    Optional:
        - Contains subtitle folder OR multiple subtitle files
        - Contains extras folder

Subtitles Folder:
    Required:
        - Contains no video files
        - Contains one or more subtitle files

Extras Folder:
    Required:
        - Folder name matches EXTRAS_PATTERNS
        - Contains one or more movie or episode files
        # TODO handle season folders inside extras folder
    Optional:
        - Contains subtitles folder OR multiple subtitle files
"""
DirectoryType = Literal[
    'SERIES_FOLDER',
    'SEASON_FOLDER',
    'MOVIE_FOLDER',
    'SUBTITLE_FOLDER',
    'EXTRAS_FOLDER',
]

"""
Movie File:
    Required:
        - metadata.season is None ✅ (initial pass)
        - metadata.episode is None ✅ (initial pass)
        - metadata.ext is in VIDEO_EXTENSIONS ✅ (initial pass)

Episode File:
    Required:
        - metadata.season is not None OR metadata.episode is not None ✅ (initial pass)
        - metadata.ext is in VIDEO_EXTENSIONS ✅ (initial pass)

Subtitle File:
    Required:
        - metadata.ext is in SUBTITLE_EXTENSIONS ✅ (initial pass)

Extra File:
    Required:
        - Parent directory is EXTRAS_FOLDER
        - metadata.ext is in VIDEO_EXTENSIONS
"""
FileType = Literal[
    'MOVIE_FILE',
    'EPISODE_FILE',
    'SUBTITLE_FILE',
    'EXTRAS_FILE',
]

UnknownType = Literal[
    'UNKNOWN',
]

NodeType = DirectoryType | FileType | UnknownType

