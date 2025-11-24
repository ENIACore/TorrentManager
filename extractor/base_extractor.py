import re
from pathlib import Path
from typing import Match, Any, Dict
from config.constants import (
    VIDEO_EXTENSIONS,
    SUBTITLE_EXTENSIONS,
    AUDIO_EXTENSIONS
    )

"""
Contains base extractor helper functions to be used by all extractors
"""
class BaseExtractor:

    """
    Specific reusable helper functions
    """
    def _get_sanitized_path(self, path: Path) -> str | None:
        name = path.name
        name = name.rstrip()
        name = name.upper()
        name = name.replace('\'', '')
        name = name.replace('\"', '')
        name = re.sub(r'[^A-Z0-9]+', '.', name)
        name = name.strip('.')

        if name:
            return name

        return None

    def _get_sanitized_path_parts(self, path: Path) -> list[str]:
        sanitized_name = self._get_sanitized_path(path)
        if sanitized_name:
            return sanitized_name.split('.')

        return []

    def _get_sanitized_stem_parts(self, path: Path) -> list[str]:
        sanitized_name = self._get_sanitized_path(path)

        parts = []
        if sanitized_name:
            parts = sanitized_name.split('.')

        for i, _ in enumerate(parts):
            if (match := self._is_ext(i, parts)):
                num_ext_parts = len(match.group(0).split('.'))
                parts = parts[:num_ext_parts * -1]

        return parts

    def _is_ext(self, index: int, parts: list[str]) -> Match[str] | None:

        if (match := self._is_video_ext(index, parts)):
            return match
        if (match := self._is_subtitle_ext(index, parts)):
            return match
        if (match := self._is_audio_ext(index, parts)):
            return match

        return None

    def _is_video_ext(self, index: int, parts: list[str]) -> Match[str] | None:
        for pattern in VIDEO_EXTENSIONS:
            if self._is_matching_tail_len(pattern, index, parts) and (match := self._match_regex(pattern, index, parts)):
                return match

        return None

    def _is_subtitle_ext(self, index: int, parts: list[str]) -> Match[str] | None:
        for pattern in SUBTITLE_EXTENSIONS:
            if self._is_matching_tail_len(pattern, index, parts) and (match := self._match_regex(pattern, index, parts)):
                return match

        return None

    def _is_audio_ext(self, index: int, parts: list[str]) -> Match[str] | None:
        for pattern in AUDIO_EXTENSIONS:
            if self._is_matching_tail_len(pattern, index, parts) and (match := self._match_regex(pattern, index, parts)):
                return match

        return None


    """
    Generic reusable helper functions
    """
    def _is_matching_tail_len(self, pattern: str, index: int, parts: list[str]) -> int | None:
        """
        Enables matching end of parts array only by ensuring pattern to match has as many parts as are left in filename array 
        """
        if (num_pattern_parts := len(pattern.split('.')) == len(parts) - index):
            return num_pattern_parts
        
        return None

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

    def _get_next_element(self, index: int, array: list[Any]) -> Any | None:
        if index < len(array) - 1:
            return array[index + 1]
        else:
            return None


    def match_pattern_dict(self, path: Path, pattern_dict: Dict[str, str]) -> str | None:
        parts = self._get_sanitized_stem_parts(path)

        for i, _ in enumerate(parts):
            for pattern in pattern_dict:
                if self._match_regex(pattern, i, parts):
                    return pattern

        return None

    def match_pattern_dict_list(self, path: Path, pattern_dict_list: Dict[str, list[str]]) -> str | None:
        parts = self._get_sanitized_stem_parts(path)

        for i, _ in enumerate(parts):
            for res in pattern_dict_list:
                for pattern in pattern_dict_list[res]:
                    if self._match_regex(pattern, i, parts):
                        return res

        return None
