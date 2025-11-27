from typing import Literal


UnknownType = Literal[
    'UNKNOWN',
]

# Types to classify purpose of nodes (files and directories)
DirectoryType = Literal[
    'SERIES_FOLDER',
    'SEASON_FOLDER',
    'MOVIE_FOLDER',
    'SUBTITLE_FOLDER',
    'EXTRAS_FOLDER',
]

FileType = Literal[
    'MOVIE_FILE',
    'EPISODE_FILE',
    'SUBTITLE_FILE',
    'EXTRAS_FILE',
]

NodeType = DirectoryType | FileType | UnknownType

# Type to classify format of file
#TODO, Audio files currently disabled
FormatType = Literal['VIDEO', 'SUBTITLE'] | UnknownType

