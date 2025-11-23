from typing import Any, Match, Dict
from pathlib import Path
from models.media_metadata import MediaMetadata
import re
from datetime import datetime
from config.constants import (
    # Quality descriptor patterns
    EXTRAS_PATTERNS,
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
    AUDIO_EXTENSIONS,

    EXTRAS_PATTERNS
    )
from config.language import LANGUAGE_PATTERNS

class MediaExtractor:
    
    """
    Extraction functions
    """
    def extract_metadata(self, path: Path) -> MediaMetadata:
        metadata = MediaMetadata()
        metadata.title = self.extract_title(path) 
        metadata.year = self.extract_year(path)
        metadata.season = self.extract_season(path)
        metadata.episode = self.extract_episode(path)

        metadata.resolution = self.extract_resolution(path)
        metadata.codec = self.extract_codec(path)
        metadata.source = self.extract_source(path)
        metadata.audio = self.extract_audio(path)

        metadata.language = self.extract_language(path)
        metadata.ext = self.extract_ext(path)

        return metadata
    
    def extract_title(self, path: Path) -> str | None:
        """
        Extracts title of movie or series from filename.

        Title Extraction Logic:
            Title consists of all parts from the start until a terminator is found.

            Terminators (indicators that title has ended):
            - End of filename parts
            - File extension (.mkv, .mp4, etc.)
            - Quality descriptor (resolution, codec, source, audio)
            - Season indicator (S01, S01E01, etc.)
            - Episode indicator (when not part of season pattern)

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
        title = []

        for i, part in enumerate(parts):

            # Skips over year to check for only terminators or end of filename parts
            part_to_match = part
            index_to_match = i
            if self._is_valid_year(part_to_match):
                part_to_match = self._get_next_element(i, parts)
                index_to_match = i + 1

            
            # If teminator after title or year
            if (
                not part_to_match or
                self._is_quality_descriptor(index_to_match, parts) or
                self._extract_season_num(index_to_match, parts) or
                self._extract_episode_num(index_to_match, parts) or
                self._is_ext(index_to_match, parts)
                ):
                break
            else:
                title.append(part)

        if len(title) == 0:
            return None

        return '.'.join(title)
    
    def extract_year(self, path: Path) -> int | None:
        """
        Extracts year of movie or series from filename.

        Year Extraction Logic:
            Year must be a valid year (1900 - current year) preceded by a title and followed by a terminator
            If the year is not preceded only by the title it will not be assumed the year
            If the year is not followed by a terminator it will be assumed a part of the title

            Terminators (indicators that title has ended):
            - End of filename parts
            - File extension (.mkv, .mp4, etc.)
            - Quality descriptor (resolution, codec, source, audio)
            - Season indicator (S01, S01E01, etc.)
            - Episode indicator (when not part of season pattern)

            Year Handling:
            - If a valid year is followed by a terminator → year is captured
            - If a valid year is NOT followed by a terminator → year is part of the title

        Example Patterns:
            Title.2020.1080p          → title="Title", year=2020 (year followed by quality)
            Title.2020.S01E01         → title="Title", year=2020 (year followed by season)
            Title.2020                → title="Title", year=2020 (year at end)
            Title.2020.Part2.1080p    → title="Title.2020.Part2" (2020 not followed by terminator)
            Title.1080p               → title="Title" (no year, ends at quality)
            Title                     → title="Title" (no terminators found)

        Returns:
            int if year found
            None if no year found
        """
        parts = self._get_sanitized_file_or_dir(path).split('.')

        for i, part in enumerate(parts):

            # If terminator found
            if (
                self._is_quality_descriptor(i, parts) or
                self._extract_season_num(i, parts) or
                self._extract_episode_num(i, parts) or
                self._is_ext(i, parts)
                ):
                # If previous part is year, return year
                if (i > 0 and (year := self._is_valid_year(parts[i - 1]))):
                    return year
                # If previous part is not year, no year can come after terminator, return None
                else:
                    return None
            # Returns year if year is last part in filename
            if not self._get_next_element(i, parts):
                if (year := self._is_valid_year(parts[i])):
                    return year
    
    def extract_season(self, path: Path) -> int | None:
        parts = self._get_sanitized_file_or_dir(path).split('.')

        for i, part in enumerate(parts):
            match = self._extract_season_num(i, parts)
            if match and match.group(1):
                return int(match.group(1)) 
        return None
    
    def extract_episode(self, path: Path) -> int | None:
        parts = self._get_sanitized_file_or_dir(path).split('.')

        for i, part in enumerate(parts):
            match = self._extract_episode_num(i, parts)
            if match and match.group(1):
                return int(match.group(1))
        return None
    
    def extract_resolution(self, path: Path) -> str | None:
        parts = self._get_sanitized_file_or_dir(path).split('.')

        for i, part in enumerate(parts):
            resolution = self._is_resolution_descriptor(i, parts)
            if resolution:
                return resolution
        
        return None
            
    
    def extract_codec(self, path: Path) -> str | None:
        parts = self._get_sanitized_file_or_dir(path).split('.')

        for i, part in enumerate(parts):
            codec = self._is_codec_descriptor(i, parts)
            if codec:
                return codec
        
        return None
    
    def extract_source(self, path: Path) -> str | None:
        parts = self._get_sanitized_file_or_dir(path).split('.')

        for i, part in enumerate(parts):
            source = self._is_source_descriptor(i, parts)
            if source:
                return source
        
        return None
    
    def extract_audio(self, path: Path) -> str | None:
        parts = self._get_sanitized_file_or_dir(path).split('.')

        for i, part in enumerate(parts):
            audio = self._is_audio_descriptor(i, parts)
            if audio:
                return audio
        
        return None

    def extract_language(self, path: Path) -> str | None:
        parts = self._get_sanitized_file_or_dir(path).split('.')

        for i, _ in enumerate(parts):
            for language in LANGUAGE_PATTERNS:
                for pattern in LANGUAGE_PATTERNS[language]:
                    if self._match_regex(pattern, i, parts):
                        return language

        return None
        

    def extract_ext(self, path: Path) -> str | None:
        parts = self._get_sanitized_file_or_dir(path).split('.')

        for i, _ in enumerate(parts):
            if (match := self._is_ext(i, parts)):
                return match.group(0)

        return None

    def match_pattern_dict(self, path: Path, pattern_dict: Dict[str, str]) -> str | None:
        parts = self._get_sanitized_file_or_dir(path).split('.')

        for i, _ in enumerate(parts):
            for pattern in pattern_dict:
                if self._match_regex(pattern, i, parts):
                    return pattern

        return None

    def match_pattern_dict_list(self, path: Path, pattern_dict_list: Dict[str, list[str]]) -> str | None:
        parts = self._get_sanitized_file_or_dir(path).split('.')

        for i, _ in enumerate(parts):
            for res in pattern_dict_list:
                for pattern in pattern_dict_list[res]:
                    if self._match_regex(pattern, i, parts):
                        return res

        return None
    
    """
    Extraction helper functions
    """
    def _get_sanitized_file_or_dir(self, path: Path) -> str:
        name = path.name
        name = name.rstrip()
        name = name.upper()
        name = name.replace('\'', '')
        name = name.replace('\"', '')
        name = re.sub(r'[^A-Z0-9]+', '.', name)
        name = name.strip('.')

        # If file name only consists of special characters
        if name == '':
            return ''

        return name

    def _is_valid_year(self, year: str) -> int | None: 
        if not year.isdigit():
            return False

        year_num = int(year)
        if year_num > 1900 and year_num <= datetime.now().year:
            return year_num
        return None

    def _extract_season_num(self, index: int, parts: list[str]) -> Match[str] | None:
        for pattern in SEASONS_PATTERNS:
            match = self._match_regex(pattern, index, parts)
            if match:
                return match

        return None
                
    def _extract_episode_num(self, index: int, parts: list[str]):
        for pattern in EPISODES_PATTERNS:
            match = self._match_regex(pattern, index, parts)
            if match:
                return match

        return None

    def _is_quality_descriptor(self, index: int, parts: list[str]) -> str | None:
        if (
            (descriptor := self._is_resolution_descriptor(index, parts)) or
            (descriptor := self._is_codec_descriptor(index, parts)) or
            (descriptor := self._is_source_descriptor(index, parts)) or
            (descriptor := self._is_audio_descriptor(index, parts))
            ):
            return descriptor

        return None

    def _is_resolution_descriptor(self, index: int, parts: list[str]) -> str | None:
        for resolution in RESOLUTION_PATTERNS:
            for pattern in RESOLUTION_PATTERNS[resolution]:
                if self._match_regex(pattern, index, parts):
                    return resolution
        return None

    def _is_codec_descriptor(self, index: int, parts: list[str]) -> str | None:
        for codec in CODEC_PATTERNS:
            for pattern in CODEC_PATTERNS[codec]:
                if self._match_regex(pattern, index, parts):
                    return codec
        return None

    def _is_source_descriptor(self, index: int, parts: list[str]) -> str | None:
        for source in SOURCE_PATTERNS:
            for pattern in SOURCE_PATTERNS[source]:
                if self._match_regex(pattern, index, parts):
                    return source
        return None

    def _is_audio_descriptor(self, index: int, parts: list[str]) -> str | None:
        for audio in AUDIO_PATTERNS:
            for pattern in AUDIO_PATTERNS[audio]:
                if self._match_regex(pattern, index, parts):
                    return audio
        return None

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

    def _is_matching_tail_len(self, pattern: str, index: int, parts: list[str]) -> int | None:
        """
        Helper function for _is_<type>_ext to ensure ext pattern only matches end of filename parts array.
        Does this by ensuring number of parts in pattern.split('.') is equivalent to remaining parts to match in filename
        """
        if (num_pattern_parts := len(pattern.split('.')) == len(parts) - index):
            return num_pattern_parts
        
        return None

    """
    General helper functions
    """
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

