from typing import Dict, Optional
from pathlib import Path
from models.media_metadata import MediaMetadata
import re
from datetime import datetime
from array import array

class MediaExtractor:
    """
    Business logic class to extract metadata from media file paths.
    
    Supports common torrent filename patterns for movies and TV series:
        - <title>.<year>.<quality descriptors>.<ext>
        - <title>.<year>.<season or episode>.<quality descriptors>.<ext>
        - <title>.<season>.<episode>.<quality descriptors>.<ext>
        - <title>.<quality descriptors>.<ext>
    """
    
    def extract_metadata(self, path: Path) -> MediaMetadata:
        """
        Extract all available metadata from a media file path.
        
        Args:
            path: Full or relative path to the media file
            
        Returns: MediaMetadata object containing all extracted metadata fields
        """

        sanitized_name = self._get_sanitized_file_or_dir(path)
        return MediaMetadata()
    
    def extract_title(self, path: Path) -> str:
        """
        Extract the movie or series title from the file path.
        
        Args:
            path: Full or relative path to the media file
            
        Returns:
            The extracted title, or empty string if not found

        """
        parts = self._get_sanitized_file_or_dir(path).split('.')

        return ''
    
    def extract_year(self, path: Path) -> str:
        """
        Extract the release year from the file path.
        
        Args:
            path: Full or relative path to the media file
            
        Returns:
            The extracted year as a string, or empty string if not found
        """
        return ''
    
    def extract_season(self, path: Path) -> str:
        """
        Extract the season number from the file path for TV series.
        
        Args:
            path: Full or relative path to the media file
            
        Returns:
            The extracted season number as a string, or empty string if not found
        """
        return ''
    
    def extract_episode(self, path: Path) -> str:
        """
        Extract the episode number from the file path for TV series.
        
        Args:
            path: Full or relative path to the media file
            
        Returns:
            The extracted episode number as a string, or empty string if not found
        """
        return ''
    
    def extract_resolution(self, path: Path) -> str:
        """
        Extract the video resolution (e.g., 1080p, 720p, 4K) from the file path.
        
        Args:
            path: Full or relative path to the media file
            
        Returns:
            The extracted resolution as a string, or empty string if not found
        """
        return ''
    
    def extract_codec(self, path: Path) -> str:
        """
        Extract the video codec (e.g., H264, H265, x264, x265) from the file path.
        
        Args:
            path: Full or relative path to the media file
            
        Returns:
            The extracted codec as a string, or empty string if not found
        """
        return ''
    
    def extract_quality(self, path: Path) -> str:
        """
        Extract the quality descriptor (e.g., BluRay, WEB-DL, HDTV) from the file path.
        
        Args:
            path: Full or relative path to the media file
            
        Returns:
            The extracted quality descriptor as a string, or empty string if not found
        """
        return ''
    
    def extract_audio(self, path: Path) -> str:
        """
        Extract the audio format (e.g., AAC, DTS, AC3) from the file path.
        
        Args:
            path: Full or relative path to the media file
            
        Returns:
            The extracted audio format as a string, or empty string if not found
        """
        return ''
    
    def extract_dir_type(self, path: Path) -> str:
        """
        Determine the directory type based on its contents and structure.
        
        Recognized directory types:
            - 'series': Root folder containing season folders for a TV series
            - 'season': Folder containing episode files for a specific season
            - 'movie': Folder containing a movie file and related content
            - 'extras': Folder containing bonus features, featurettes, or behind-the-scenes content
            - 'subtitles': Folder containing subtitle files
        
        Args:
            path: Full or relative path to the directory
            
        Returns:
            Directory type as a string, or empty string if not a directory 
            or type cannot be determined
        """
        return ''

    def extract_file_type(self, path: Path) -> str:
        """
        Determine the file type based on its purpose and content.
        
        Recognized file types:
            - 'movie': Main movie video file
            - 'episode': TV series episode video file
            - 'featurette': Bonus feature or extra content video file
            - 'subtitle': Subtitle or caption file
        
        Args:
            path: Full or relative path to the file
            
        Returns:
            File type as a string, or empty string if not a file 
            or type cannot be determined
        """
        return ''

    def _extract_episode_num(self, index: int, parts: array[str]):
        return
    
    def _get_sanitized_file_or_dir(self, path: Path) -> str:
        """
        Extract and sanitize the filename or directory name from a path.
        
        Args:
            path: Full or relative path to the media file
            
        Returns:
            Sanitized filename or directory name
        """
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
    
    def _is_valid_year(self, year: str) -> bool:
        """
        Validate if a string represents a valid release year.
        
        Args:
            year: String to validate as a year
            
        Returns:
            True if the string is a valid 4-digit year within reasonable bounds
        """
        try:
            year_num = int(year)
            if year_num > 1900 and year_num <= datetime.now().year:
                return True
            return False
        except ValueError:
            # Not valid integer
            return False
    
    def _is_episode(self, episode: str) -> bool:
        """
        Check if a string matches common episode number patterns (e.g., E01, e12).
        
        Args:
            episode: String to check for episode pattern
            
        Returns:
            True if the string matches an episode pattern
        """
        return False
    
    def _is_season(self, season: str) -> bool:
        """
        Check if a string matches common season number patterns (e.g., S01, s02).
        
        Args:
            season: String to check for season pattern
            
        Returns:
            True if the string matches a season pattern
        """
        return False

    def _is_quality_descriptor(self, descriptor) -> bool:
        """
        Check if string is a quality descriptor (resolution, codec, source quality, audio)
        """
        return False

    def _has_next_element(self, index, array) -> bool:
        """
        Helper function to determine if array has another element after the index
        """
        if index < len(array) - 1:
            return True
        else:
            return False 
