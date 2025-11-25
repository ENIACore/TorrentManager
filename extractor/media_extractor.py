from typing import Any, Match, Dict
from pathlib import Path
from extractor.base_extractor import BaseExtractor
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

    )


from config.language import LANGUAGE_PATTERNS

class MediaExtractor(BaseExtractor):

    """
    Main extraction function
    """
    @classmethod
    def extract_metadata(cls, path: Path) -> MediaMetadata:
        cls._get_logger().debug(f'Extracting media metadata for: {path}')

        metadata = MediaMetadata()
        # Parts do not include ext, not needed for media identification
        parts = cls._get_sanitized_stem_parts(path)

        metadata.title = cls._extract_title(parts) 
        metadata.year = cls._extract_year(parts)
        metadata.season = cls._extract_season(parts)
        metadata.episode = cls._extract_episode(parts)

        metadata.resolution = cls._extract_resolution(parts)
        metadata.codec = cls._extract_codec(parts)
        metadata.source = cls._extract_source(parts)
        metadata.audio = cls._extract_audio(parts)

        metadata.language = cls._extract_language(parts)

        # Extensible pattern matching variables
        metadata.season_patterns = bool(cls._match_pattern_list(parts, SEASONS_PATTERNS))
        metadata.episode_patterns = bool(cls._match_pattern_list(parts, EPISODES_PATTERNS))
        metadata.extras_patterns = bool(cls._match_pattern_list(parts, EXTRAS_PATTERNS))

        cls._get_logger().debug(f'Extracted metadata - title: {metadata.title}, year: {metadata.year}, '
                                f'season: {metadata.season}, episode: {metadata.episode}')

        return metadata
    
    """
    Extraction functions
    """
    @classmethod
    def _extract_title(cls, parts: list[str]) -> str | None:
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

        title = []

        for i, part in enumerate(parts):

            # Skips over year to check for only terminators or end of filename parts
            part_to_match = part
            index_to_match = i
            if cls._is_valid_year(part_to_match):
                part_to_match = cls._get_next_element(i, parts)
                index_to_match = i + 1

            
            # If teminator after title or year
            if (
                not part_to_match or
                cls._is_quality_descriptor(index_to_match, parts) or
                cls._extract_season_num(index_to_match, parts) or
                cls._extract_episode_num(index_to_match, parts)
                ):
                break
            else:
                title.append(part)

        if len(title) == 0:
            cls._get_logger().debug('No title found')
            return None

        title_str = '.'.join(title)
        cls._get_logger().debug(f'Extracted title: {title_str}')
        return title_str
    
    @classmethod
    def _extract_year(cls, parts: list[str]) -> int | None:
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

        for i, part in enumerate(parts):

            # If terminator found
            if (
                cls._is_quality_descriptor(i, parts) or
                cls._extract_season_num(i, parts) or
                cls._extract_episode_num(i, parts)
                ):
                # If previous part is year, return year
                if (i > 0 and (year := cls._is_valid_year(parts[i - 1]))):
                    cls._get_logger().debug(f'Extracted year: {year}')
                    return year
                # If previous part is not year, no year can come after terminator, return None
                else:
                    cls._get_logger().debug('No year found')
                    return None
            # Returns year if year is last part in filename
            if not cls._get_next_element(i, parts):
                if (year := cls._is_valid_year(parts[i])):
                    cls._get_logger().debug(f'Extracted year (end of parts): {year}')
                    return year
    
    @classmethod
    def _extract_season(cls, parts: list[str]) -> int | None:

        for i, part in enumerate(parts):
            match = cls._extract_season_num(i, parts)
            #if match and match.groups() and len(match.groups()) >= 1 and match.group(1):
            if match and len(match.groups()) >= 1 and match.group(1):
                season = int(match.group(1))
                cls._get_logger().debug(f'Extracted season: {season}')
                return season
        return None
    
    @classmethod
    def _extract_episode(cls, parts: list[str]) -> int | None:

        for i, part in enumerate(parts):
            match = cls._extract_episode_num(i, parts)
            #if match and match.group(1):
            if match and len(match.groups()) >= 1 and match.group(1):
                episode = int(match.group(1))
                cls._get_logger().debug(f'Extracted episode: {episode}')
                return episode
        return None
    
    @classmethod
    def _extract_resolution(cls, parts: list[str]) -> str | None:

        for i, part in enumerate(parts):
            resolution = cls._is_resolution_descriptor(i, parts)
            if resolution:
                cls._get_logger().debug(f'Extracted resolution: {resolution}')
                return resolution
        
        return None
            
    @classmethod
    def _extract_codec(cls, parts: list[str]) -> str | None:

        for i, part in enumerate(parts):
            codec = cls._is_codec_descriptor(i, parts)
            if codec:
                cls._get_logger().debug(f'Extracted codec: {codec}')
                return codec
        
        return None
    
    @classmethod
    def _extract_source(cls, parts: list[str]) -> str | None:

        for i, part in enumerate(parts):
            source = cls._is_source_descriptor(i, parts)
            if source:
                cls._get_logger().debug(f'Extracted source: {source}')
                return source
        
        return None
    
    @classmethod
    def _extract_audio(cls, parts: list[str]) -> str | None:

        for i, part in enumerate(parts):
            audio = cls._is_audio_descriptor(i, parts)
            if audio:
                cls._get_logger().debug(f'Extracted audio: {audio}')
                return audio
        
        return None

    @classmethod
    def _extract_language(cls, parts: list[str]) -> str | None:

        for i, _ in enumerate(parts):
            for language in LANGUAGE_PATTERNS:
                for pattern in LANGUAGE_PATTERNS[language]:
                    if cls._match_regex(pattern, i, parts):
                        cls._get_logger().debug(f'Extracted language: {language}')
                        return language

        return None
    
    """
    Extraction helper functions
    """
    @classmethod
    def _is_valid_year(cls, year: str) -> int | None: 
        if not year.isdigit():
            return False

        year_num = int(year)
        if year_num > 1900 and year_num <= datetime.now().year:
            return year_num
        return None

    @classmethod
    def _extract_season_num(cls, index: int, parts: list[str]) -> Match[str] | None:
        for pattern in SEASONS_PATTERNS:
            match = cls._match_regex(pattern, index, parts)
            if match:
                return match

        return None
                
    @classmethod
    def _extract_episode_num(cls, index: int, parts: list[str]):
        for pattern in EPISODES_PATTERNS:
            match = cls._match_regex(pattern, index, parts)
            if match:
                return match

        return None

    @classmethod
    def _is_quality_descriptor(cls, index: int, parts: list[str]) -> str | None:
        if (
            (descriptor := cls._is_resolution_descriptor(index, parts)) or
            (descriptor := cls._is_codec_descriptor(index, parts)) or
            (descriptor := cls._is_source_descriptor(index, parts)) or
            (descriptor := cls._is_audio_descriptor(index, parts))
            ):
            return descriptor

        return None

    @classmethod
    def _is_resolution_descriptor(cls, index: int, parts: list[str]) -> str | None:
        for resolution in RESOLUTION_PATTERNS:
            for pattern in RESOLUTION_PATTERNS[resolution]:
                if cls._match_regex(pattern, index, parts):
                    return resolution
        return None

    @classmethod
    def _is_codec_descriptor(cls, index: int, parts: list[str]) -> str | None:
        for codec in CODEC_PATTERNS:
            for pattern in CODEC_PATTERNS[codec]:
                if cls._match_regex(pattern, index, parts):
                    return codec
        return None

    @classmethod
    def _is_source_descriptor(cls, index: int, parts: list[str]) -> str | None:
        for source in SOURCE_PATTERNS:
            for pattern in SOURCE_PATTERNS[source]:
                if cls._match_regex(pattern, index, parts):
                    return source
        return None

    @classmethod
    def _is_audio_descriptor(cls, index: int, parts: list[str]) -> str | None:
        for audio in AUDIO_PATTERNS:
            for pattern in AUDIO_PATTERNS[audio]:
                if cls._match_regex(pattern, index, parts):
                    return audio
        return None
