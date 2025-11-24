from pathlib import Path
from typing import Literal

FormatType = Literal[
    'VIDEO',
    'SUBTITLE',
    #'AUDIO' - TODO, Audio files currently disabled
]

class PathMetadata:
    is_dir: bool = False
    is_file: bool = False
    format_type: FormatType | None = None
    ext: str | None = None
