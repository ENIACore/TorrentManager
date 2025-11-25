from pathlib import Path
from typing import Literal

FormatType = Literal[
    'VIDEO',
    'SUBTITLE',
    #'AUDIO' - TODO, Audio files currently disabled
]

UnknownType = Literal[
    'UNKNOWN'
]

class PathMetadata:
    is_dir: bool
    is_file: bool
    format_type: FormatType | UnknownType
    ext: str

