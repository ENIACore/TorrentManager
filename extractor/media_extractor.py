from typing import Any, Match
from pathlib import Path
from models.media_metadata import MediaMetadata
import re
from datetime import datetime
from config.constants import (
    # Quality descriptor patterns
    RESOLUTION_PATTERNS,
    CODEC_PATTERNS,
    SOURCE_PATTERNS,
    AUDIO_PATTERNS,

    # Series patterns
    SEASONS_PATTERNS,
    EPISODES_PATTERNS,

    # File extensions
    VIDEO_EXTENSIONS,
    SUBTITLE_EXTENSIONS,
    AUDIO_EXTENSIONS
    )

class MediaExtractor:
    
    """
    Extraction functions
    """
    def extract_metadata(self, path: Path) -> MediaMetadata:

        sanitized_name = self._get_sanitized_file_or_dir(path)
        return MediaMetadata()
    
    def extract_title(self, path: Path) -> str:
        """
        Extracts title of movie or series from filename.

        Title Extraction Logic:
            Title consists of all parts from the start until a terminator is found.

            Terminators (indicators that title has ended):
            - Quality descriptor (resolution, codec, source, audio)
            - Season indicator (S01, S01E01, etc.)
            - Episode indicator (when not part of season pattern)
            - File extension (.mkv, .mp4, etc.)
            - End of filename parts

            Year Handling:
            - If a valid year is followed by a terminator → year ends the title
            - If a valid year is NOT followed by a terminator → year is part of the title

        Example Patterns:
            Title.2020.1080p          → title="Title", year=2020 (year followed by quality)
            Title.2020.S01E01         → title="Title", year=2020 (year followed by season)
            Title.2020                → title="Title", year=2020 (year at end)
            Title.2020.Part2.1080p    → title="Title.2020.Part2" (2020 not followed by terminator)
            Title.1080p               → title="Title" (no year, ends at quality)
            Title                     → title="Title" (no terminators found)
        """
        parts = self._get_sanitized_file_or_dir(path).split('.')
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

    # Tested ✅
    def _extract_season_num(self, index: int, parts: list[str]) -> Match[str] | None:
        for pattern in SEASONS_PATTERNS:
            match = self._match_regex(pattern, index, parts)
            if match:
                return match

        return None
                
    # Tested ✅
    def _extract_episode_num(self, index: int, parts: list[str]):
        for pattern in EPISODES_PATTERNS:
            match = self._match_regex(pattern, index, parts)
            if match:
                return match

        return None

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

    # tested ✅
    def _is_ext(self, index: int, parts: list[str]) -> bool:
        if (
            self._is_video_ext(index, parts) or
            self._is_subtitle_ext(index, parts) or
            self._is_audio_ext(index, parts)
            ):
            return True

        return False

    # tested ✅
    def _is_video_ext(self, index: int, parts: list[str]) -> bool:
        for pattern in VIDEO_EXTENSIONS:
            if self._is_matching_tail_len(pattern, index, parts) and self._match_regex(pattern, index, parts):
                return True

        return False

    # tested ✅
    def _is_subtitle_ext(self, index: int, parts: list[str]) -> bool:
        for pattern in SUBTITLE_EXTENSIONS:
            if self._is_matching_tail_len(pattern, index, parts) and self._match_regex(pattern, index, parts):
                return True

        return False

    # tested ✅
    def _is_audio_ext(self, index: int, parts: list[str]) -> bool:
        for pattern in AUDIO_EXTENSIONS:
            if self._is_matching_tail_len(pattern, index, parts) and self._match_regex(pattern, index, parts):
                return True

        return False

    # tested ✅
    def _is_matching_tail_len(self, pattern: str, index: int, parts: list[str]) -> bool:
        """
        Helper function for _is_<type>_ext to ensure ext pattern only matches end of filename parts array.
        Does this by ensuring number of parts in pattern.split('.') is equivalent to remaining parts to match in filename
        """
        num_pattern_parts = len(pattern.split('.'))
        num_filename_parts_left = len(parts) - index 
        
        return num_filename_parts_left == num_pattern_parts

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
