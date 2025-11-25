import re
from pathlib import Path
from typing import Match, Any, Dict, ClassVar
from config.constants import (
    VIDEO_EXTENSIONS,
    SUBTITLE_EXTENSIONS,
    AUDIO_EXTENSIONS
    )
from logger.logger import Logger


"""
Contains base extractor helper functions to be used by all extractors
"""
class BaseExtractor:
    
    # Class-level logger
    _logger: Logger = Logger(manager_path=Path.cwd())

    @classmethod
    def _get_logger(cls) -> Logger:
        """Get or initialize the class-level logger."""
        if cls._logger is None:
            cls._logger = Logger(manager_path=Path.cwd())
        return cls._logger

    """
    Specific reusable helper functions
    """
    @classmethod
    def _get_sanitized_path(cls, path: Path) -> str | None:
        name = path.name
        name = name.rstrip()
        name = name.upper()
        name = name.replace('\'', '')
        name = name.replace('\"', '')
        name = re.sub(r'[^A-Z0-9]+', '.', name)
        name = name.strip('.')

        if name:
            cls._get_logger().debug(f'Sanitized path: {path.name} -> {name}')
            return name

        cls._get_logger().debug(f'Failed to sanitize path: {path.name}')
        return None

    @classmethod
    def _get_sanitized_path_parts(cls, path: Path) -> list[str]:
        sanitized_name = cls._get_sanitized_path(path)
        if sanitized_name:
            parts = sanitized_name.split('.')
            cls._get_logger().debug(f'Sanitized path parts: {parts}')
            return parts

        return []

    @classmethod
    def _get_sanitized_stem_parts(cls, path: Path) -> list[str]:
        sanitized_name = cls._get_sanitized_path(path)

        parts = []
        if sanitized_name:
            parts = sanitized_name.split('.')

        for i, _ in enumerate(parts):
            if (match := cls._is_ext(i, parts)):
                num_ext_parts = len(match.group(0).split('.'))
                parts = parts[:num_ext_parts * -1]

        if parts:
            cls._get_logger().debug(f'Sanitized stem parts: {parts}')
        return parts

    @classmethod
    def _is_ext(cls, index: int, parts: list[str]) -> Match[str] | None:

        if (match := cls._is_video_ext(index, parts)):
            return match
        if (match := cls._is_subtitle_ext(index, parts)):
            return match
        if (match := cls._is_audio_ext(index, parts)):
            return match

        return None

    @classmethod
    def _is_video_ext(cls, index: int, parts: list[str]) -> Match[str] | None:
        for pattern in VIDEO_EXTENSIONS:
            if cls._is_matching_tail_len(pattern, index, parts) and (match := cls._match_regex(pattern, index, parts)):
                cls._get_logger().debug(f'Matched video extension: {pattern}')
                return match

        return None

    @classmethod
    def _is_subtitle_ext(cls, index: int, parts: list[str]) -> Match[str] | None:
        for pattern in SUBTITLE_EXTENSIONS:
            if cls._is_matching_tail_len(pattern, index, parts) and (match := cls._match_regex(pattern, index, parts)):
                cls._get_logger().debug(f'Matched subtitle extension: {pattern}')
                return match

        return None

    @classmethod
    def _is_audio_ext(cls, index: int, parts: list[str]) -> Match[str] | None:
        for pattern in AUDIO_EXTENSIONS:
            if cls._is_matching_tail_len(pattern, index, parts) and (match := cls._match_regex(pattern, index, parts)):
                cls._get_logger().debug(f'Matched audio extension: {pattern}')
                return match

        return None


    """
    Generic reusable helper functions
    """
    @classmethod
    def _is_matching_tail_len(cls, pattern: str, index: int, parts: list[str]) -> int | None:
        """
        Enables matching end of parts array only by ensuring pattern to match has as many parts as are left in filename array 
        """
        if (num_pattern_parts := len(pattern.split('.')) == len(parts) - index):
            return num_pattern_parts
        
        return None

    @classmethod
    def _match_regex(cls, pattern: str, index: int, parts: list[str]) -> Match[str] | None:
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
        match = re.fullmatch(pattern, combined_parts)
        if match:
            cls._get_logger().debug(f'Regex match: pattern={pattern}, matched={combined_parts}')
        return match

    @classmethod
    def _get_next_element(cls, index: int, array: list[Any]) -> Any | None:
        if index < len(array) - 1:
            return array[index + 1]
        else:
            return None

    @classmethod
    def _match_pattern_dict(cls, parts: list[str], pattern_dict: Dict[str, str]) -> str | None:

        for i, _ in enumerate(parts):
            for pattern in pattern_dict:
                if cls._match_regex(pattern, i, parts):
                    cls._get_logger().debug(f'Matched pattern dict: pattern={pattern}')
                    return pattern

        return None

    @classmethod
    def _match_pattern_list(cls, parts: list[str], pattern_list: list[str]) -> str | None:

        for i, _ in enumerate(parts):
            for pattern in pattern_list:
                if cls._match_regex(pattern, i, parts):
                    cls._get_logger().debug(f'Matched pattern list: pattern={pattern}')
                    return pattern

        return None

    @classmethod
    def _match_pattern_dict_list(cls, parts: list[str], pattern_dict_list: Dict[str, list[str]]) -> str | None:

        for i, _ in enumerate(parts):
            for res in pattern_dict_list:
                for pattern in pattern_dict_list[res]:
                    if cls._match_regex(pattern, i, parts):
                        cls._get_logger().debug(f'Matched pattern dict list: key={res}, pattern={pattern}')
                        return res

        return None
