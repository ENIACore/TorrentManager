from typing import Any, Match
from pathlib import Path
from models.media_metadata import MediaMetadata
import re
from datetime import datetime
from config.constants import (
    RESOLUTION_PATTERNS,
    CODEC_PATTERNS,
    SOURCE_PATTERNS,
    AUDIO_PATTERNS
    )

class MediaExtractor:
    
    """
    Extraction functions
    """
    def extract_metadata(self, path: Path) -> MediaMetadata:

        sanitized_name = self._get_sanitized_file_or_dir(path)
        return MediaMetadata()
    
    def extract_title(self, path: Path) -> str:
        #parts = self._get_sanitized_file_or_dir(path).split('.')

        return ''
    
    def extract_year(self, path: Path) -> str:
        return ''
    
    def extract_season(self, path: Path) -> str:
        return ''
    
    def extract_episode(self, path: Path) -> str:
        return ''
    
    def extract_resolution(self, path: Path) -> str:
        return ''
    
    def extract_codec(self, path: Path) -> str:
        return ''
    
    def extract_quality(self, path: Path) -> str:
        return ''
    
    def extract_audio(self, path: Path) -> str:
        return ''
    
    def extract_dir_type(self, path: Path) -> str:
        return ''

    def extract_file_type(self, path: Path) -> str:
        return ''
    
    """
    Extraction helper functions
    """
    # Tested ✅
    def _get_sanitized_file_or_dir(self, path: Path) -> str:
        name = path.name
        name = name.rstrip()
        name = name.upper()
        name = name.replace('\'', '')
        name = name.replace('\"', '')
        name = re.sub(r'[^A-Z0-9]+', '.', name) 

        # If file name only consists of special characters
        if name == '.':
            name = ''

        return name

    # Tested ✅
    def _is_valid_year(self, year: str) -> bool: 
        if not year.isdigit():
            return False

        year_num = int(year)
        if year_num > 1900 and year_num <= datetime.now().year:
            return True
        return False
    
    def _is_episode(self, episode: str) -> bool:
        return False

    def _extract_episode_num(self, index: int, parts: list[str]):
        return
    
    def _is_season(self, season: str) -> bool:
        return False

    def _extract_season_num(self, index: int, parts: list[str]):
        return

    # Testing not needed (yet, will be after adding static patterns) ✅
    def _is_quality_descriptor(self, index: int, parts: list[str]) -> bool:
        if (
            self._is_resolution_descriptor(index, parts) or
            self._is_codec_descriptor(index, parts) or
            self._is_source_descriptor(index, parts) or
            self._is_audio_descriptor(index, parts)
            ):
            return True

        return False

    # tested ✅
    def _is_resolution_descriptor(self, index: int, parts: list[str]) -> bool:
        for resolution in RESOLUTION_PATTERNS:
            for pattern in RESOLUTION_PATTERNS[resolution]:
                if self._match_regex(pattern, index, parts):
                    return True
        return False

    # tested ✅
    def _is_codec_descriptor(self, index: int, parts: list[str]) -> bool:
        for codec in CODEC_PATTERNS:
            for pattern in CODEC_PATTERNS[codec]:
                if self._match_regex(pattern, index, parts):
                    return True
        return False

    # tested ✅
    def _is_source_descriptor(self, index: int, parts: list[str]) -> bool:
        for source in SOURCE_PATTERNS:
            for pattern in SOURCE_PATTERNS[source]:
                if self._match_regex(pattern, index, parts):
                    return True
        return False

    # tested ✅
    def _is_audio_descriptor(self, index: int, parts: list[str]) -> bool:
        for audio in AUDIO_PATTERNS:
            for pattern in AUDIO_PATTERNS[audio]:
                if self._match_regex(pattern, index, parts):
                    return True
        return False


    """
    General helper functions
    """
    # Tested ✅
    def _match_regex(self, pattern: str, index: int, parts: list[str]) -> Match[str] | None:
        """
        Matches pattern on one or more full parts of filename
        Parameters:
            - pattern: Pattern to match
            - index: index in parts array to start matching
            - parts: array of filename parts previously separated by '.'
        """

        # Filename parts are split by '.', in order to match patterns containing '.', filename parts must be recombined
        parts_to_match = len(pattern.split('.'))
        combined_parts = ''
        for i in range(index, min(index + parts_to_match, len(parts))):
            if not combined_parts:
                combined_parts = parts[i]
            else:
                combined_parts = combined_parts + '.' + parts[i]

        # Match recombined or individual, filename parts with pattern
        return re.fullmatch(pattern, combined_parts) 

    # Testing not needed ✅
    def _get_next_element(self, index: int, array: list[Any]) -> Any | None:
        if index < len(array) - 1:
            return array[index + 1]
        else:
            return None
