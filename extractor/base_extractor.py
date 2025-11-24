import re
from pathlib import Path
from typing import Match, Any

class BaseExtractor:
    """
    Contains base extractor helper functions to be used by all extractors
    """
    def _get_sanitized_file_or_dir(self, path: Path) -> str | None:
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

    def _get_sanitized_file_or_dir_parts(self, path: Path) -> list[str]:
        sanitized_name = self._get_sanitized_file_or_dir(path)
        if sanitized_name:
            return sanitized_name.split('.')

        return []

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


