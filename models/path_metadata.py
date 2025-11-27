from pathlib import Path
from typing import Literal
from config.types import FormatType, UnknownType


class PathMetadata:
    is_dir: bool
    is_file: bool
    format_type: FormatType
    ext: str

