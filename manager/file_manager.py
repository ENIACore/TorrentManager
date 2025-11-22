from typing import Literal
from pathlib import Path
from models.media_metadata import MediaMetadata
from extractor.media_extractor import MediaExtractor
import re

# Type definitions
DirectoryType = Literal[
    'SERIES_FOLDER',
    'SEASON_FOLDER', 
    'MOVIE_FOLDER',
    'SUBTITLES_FOLDER',
    'EXTRAS_FOLDER',

    #'MIXED_MEDIA', TODO
    #'MOVIE_COLLECTION', TODO
]

FileType = Literal[
    'MOVIE_FILE',
    'EPISODE_FILE',
    'SUBTITLE_FILE',
    'EXTRA_FILE',


    #'AUDIO_FILE', TODO
]

MediaType = DirectoryType | FileType


class FileManager:
    

    
    SAMPLE_KEYWORDS = ['SAMPLE', 'PROOF', 'RARBG']
    
    SAMPLE_SIZE_THRESHOLD = 100 * 1024 * 1024
    
    SUBTITLE_FOLDER_THRESHOLD = 0.9
    
    EXTRAS_FOLDER_THRESHOLD = 0.5
    
    MAX_RECURSION_DEPTH = 10
    
    def __init__(self):
        self.extractor = MediaExtractor()
    
    def classify_media(self, path: Path) -> MediaType:
        """
        Determines the type of a file or directory.
        
        Args:
            path: Path to file or directory
            
        Returns:
            MediaType: One of the defined directory or file types
        """
        if path.is_dir():
            return self._classify_directory(path)
        else:
            return self._classify_file(path)
    
    def _classify_directory(self, path: Path) -> DirectoryType:
        """
        Classifies a directory based on its contents and structure.
        
        Classification Logic:
        1. Check if all/most files are subtitles → SUBTITLES_FOLDER
        2. Check if contains only season folders → SERIES_ROOT
        3. Check if contains episodes with same season → SEASON_FOLDER
        4. Check if contains multiple movie files → MOVIE_COLLECTION
        5. Check if contains single movie file → MOVIE_FOLDER
        6. Check if contains extras/bonus content → EXTRAS_FOLDER
        7. Check if mixed content → MIXED_MEDIA
        8. Default → UNKNOWN_FOLDER
        
        Args:
            path: Path to directory
            
        Returns:
            DirectoryType: Classified directory type
        """
        if not path.exists():
            return 'UNKNOWN_FOLDER'
        
        # Get all files and subdirectories
        try:
            children = list(path.iterdir())
        except PermissionError:
            return 'UNKNOWN_FOLDER'
        
        if not children:
            return 'UNKNOWN_FOLDER'
        
        files = [f for f in children if f.is_file()]
        subdirs = [d for d in children if d.is_dir()]
        
        # 1. Check if subtitles folder
        if self._is_subtitles_folder(files):
            return 'SUBTITLES_FOLDER'
        
        # 2. Check if series root (contains season folders)
        if self._is_series_root(subdirs):
            return 'SERIES_ROOT'
        
        # 3. Check if season folder (contains episodes from same season)
        video_files = [f for f in files if self._is_video_file(f)]
        if self._is_season_folder(video_files):
            return 'SEASON_FOLDER'
        
        # 4. Check if movie collection (multiple movies)
        if self._is_movie_collection(video_files):
            return 'MOVIE_COLLECTION'
        
        # 5. Check if movie folder (single movie)
        if self._is_movie_folder(video_files):
            return 'MOVIE_FOLDER'
        
        # 6. Check if extras folder
        if self._is_extras_folder(video_files, path):
            return 'EXTRAS_FOLDER'
        
        # 7. Check if mixed media
        if self._is_mixed_media(video_files):
            return 'MIXED_MEDIA'
        
        # 8. Check subdirectories if no video files at this level
        if subdirs and not video_files:
            subdir_classification = self._classify_from_subdirectories(subdirs)
            if subdir_classification:
                return subdir_classification
        
        return 'UNKNOWN_FOLDER'
    
    def _classify_file(self, path: Path) -> FileType:
        """
        Classifies a file based on extension and metadata.
        
        Classification Logic:
        1. Check file extension (subtitle, audio, video)
        2. For video files, determine if episode, movie, extra, or sample
        3. Default to UNKNOWN_FILE
        
        Args:
            path: Path to file
            
        Returns:
            FileType: Classified file type
        """
        if not path.exists():
            return 'UNKNOWN_FILE'
        
        # Check non-video extensions first
        if self._is_subtitle_file(path):
            return 'SUBTITLE_FILE'
        
        if self._is_audio_file(path):
            return 'AUDIO_FILE'
        
        if not self._is_video_file(path):
            return 'UNKNOWN_FILE'
        
        # It's a video file - determine specific type
        
        # Check if sample
        if self._is_sample_file(path):
            return 'SAMPLE_FILE'
        
        # Check if extra/bonus content
        if self._is_extra_file(path):
            return 'EXTRA_FILE'
        
        # Check if episode (has episode number)
        if self._is_episode_file(path):
            return 'EPISODE_FILE'
        
        # Otherwise assume movie
        return 'MOVIE_FILE'
    
    """
    Directory Type Helper Functions
    """
    
    def _is_subtitles_folder(self, files: list[Path]) -> bool:
        """
        Check if directory is primarily subtitle files.
        
        Args:
            files: List of file paths in directory
            
        Returns:
            bool: True if >= 90% of files are subtitles
        """
        if not files:
            return False
        
        subtitle_files = [f for f in files if self._is_subtitle_file(f)]
        return len(subtitle_files) / len(files) >= self.SUBTITLE_FOLDER_THRESHOLD
    
    def _is_series_root(self, subdirs: list[Path]) -> bool:
        """
        Check if directory contains multiple season folders.
        
        Args:
            subdirs: List of subdirectory paths
            
        Returns:
            bool: True if contains 2+ season folders
        """
        season_folders = [d for d in subdirs if self._is_season_folder_name(d)]
        return len(season_folders) >= 2
    
    def _is_season_folder(self, video_files: list[Path]) -> bool:
        """
        Check if directory contains episodes from the same season.
        
        Args:
            video_files: List of video file paths
            
        Returns:
            bool: True if all episodes share the same season number
        """
        episode_files = [f for f in video_files if self._is_episode_file(f)]
        
        if not episode_files:
            return False
        
        # Extract season numbers from all episodes
        seasons = set(self.extractor.extract_season(f) for f in episode_files)
        seasons.discard(None)
        
        # All episodes must have the same season number
        return len(seasons) == 1
    
    def _is_movie_collection(self, video_files: list[Path]) -> bool:
        """
        Check if directory contains multiple movie files.
        
        Args:
            video_files: List of video file paths
            
        Returns:
            bool: True if contains 2+ movie files
        """
        movie_files = [
            f for f in video_files 
            if not self._is_episode_file(f) 
            and not self._is_sample_file(f)
            and not self._is_extra_file(f)
        ]
        return len(movie_files) >= 2
    
    def _is_movie_folder(self, video_files: list[Path]) -> bool:
        """
        Check if directory contains a single movie file.
        
        Args:
            video_files: List of video file paths
            
        Returns:
            bool: True if contains exactly 1 movie file
        """
        movie_files = [
            f for f in video_files 
            if not self._is_episode_file(f) 
            and not self._is_sample_file(f)
            and not self._is_extra_file(f)
        ]
        return len(movie_files) == 1
    
    def _is_extras_folder(self, video_files: list[Path], path: Path) -> bool:
        """
        Check if directory is primarily extras/bonus content.
        
        Args:
            video_files: List of video file paths
            path: Directory path
            
        Returns:
            bool: True if >= 50% of videos are extras OR folder name suggests extras
        """
        if not video_files:
            return self._is_extras_folder_name(path)
        
        extra_files = [f for f in video_files if self._is_extra_file(f)]
        
        # Check if majority are extras
        if len(extra_files) >= len(video_files) * self.EXTRAS_FOLDER_THRESHOLD:
            return True
        
        # Check folder name
        return self._is_extras_folder_name(path)
    
    def _is_mixed_media(self, video_files: list[Path]) -> bool:
        """
        Check if directory contains both movies and episodes.
        
        Args:
            video_files: List of video file paths
            
        Returns:
            bool: True if contains both movie and episode files
        """
        has_episodes = any(self._is_episode_file(f) for f in video_files)
        has_movies = any(
            not self._is_episode_file(f) 
            and not self._is_sample_file(f)
            and not self._is_extra_file(f)
            for f in video_files
        )
        return has_episodes and has_movies
    
    def _classify_from_subdirectories(self, subdirs: list[Path]) -> DirectoryType | None:
        """
        Attempt to classify directory based on subdirectory types.
        Limited recursion to prevent performance issues.
        
        Args:
            subdirs: List of subdirectory paths
            
        Returns:
            DirectoryType or None: Classified type or None if cannot determine
        """
        # Limit number of subdirectories to check
        subdirs_to_check = subdirs[:self.MAX_RECURSION_DEPTH]
        subdir_types = [self._classify_directory(d) for d in subdirs_to_check]
        
        # If contains season folders → series root
        if 'SEASON_FOLDER' in subdir_types:
            return 'SERIES_ROOT'
        
        # If contains multiple movie folders → movie collection
        if subdir_types.count('MOVIE_FOLDER') >= 2:
            return 'MOVIE_COLLECTION'
        
        return None
    
    """
    File Type Helper Functions
    """
    
    def _is_video_file(self, path: Path) -> bool:
        """
        Check if file is a video file.
        
        Args:
            path: File path
            
        Returns:
            bool: True if file has video extension
        """
        parts = self.extractor._get_sanitized_file_or_dir(path).split('.')
        if not parts:
            return False
        return self.extractor._is_video_ext(len(parts) - 1, parts)
    
    def _is_subtitle_file(self, path: Path) -> bool:
        """
        Check if file is a subtitle file.
        
        Args:
            path: File path
            
        Returns:
            bool: True if file has subtitle extension
        """
        parts = self.extractor._get_sanitized_file_or_dir(path).split('.')
        if not parts:
            return False
        return self.extractor._is_subtitle_ext(len(parts) - 1, parts)
    
    def _is_audio_file(self, path: Path) -> bool:
        """
        Check if file is an audio file.
        
        Args:
            path: File path
            
        Returns:
            bool: True if file has audio extension
        """
        parts = self.extractor._get_sanitized_file_or_dir(path).split('.')
        if not parts:
            return False
        return self.extractor._is_audio_ext(len(parts) - 1, parts)
    
    def _is_episode_file(self, path: Path) -> bool:
        """
        Check if video file is an episode.
        
        Args:
            path: File path
            
        Returns:
            bool: True if file has episode number
        """
        return self.extractor.extract_episode(path) is not None
    
    def _is_sample_file(self, path: Path) -> bool:
        """
        Check if file appears to be a sample/proof.
        Checks filename for sample keywords and optionally file size.
        
        Args:
            path: File path
            
        Returns:
            bool: True if appears to be a sample file
        """
        sanitized = self.extractor._get_sanitized_file_or_dir(path)
        
        # Check filename for sample keywords
        for keyword in self.SAMPLE_KEYWORDS:
            if re.search(keyword, sanitized):
                return True
        
        # Optional: Check file size - samples are typically very small
        try:
            if path.stat().st_size < self.SAMPLE_SIZE_THRESHOLD:
                # Only consider it a sample if it's small AND has "sample" in path
                if 'SAMPLE' in str(path.parent).upper() or 'PROOF' in str(path.parent).upper():
                    return True
        except (OSError, FileNotFoundError):
            pass
        
        return False
    
    def _is_extra_file(self, path: Path) -> bool:
        """
        Check if file appears to be extra/bonus content.
        
        Args:
            path: File path
            
        Returns:
            bool: True if appears to be extras
        """
        sanitized = self.extractor._get_sanitized_file_or_dir(path)
        
        for keyword in self.EXTRA_KEYWORDS:
            if re.search(keyword, sanitized):
                return True
        
        return False
    
    """
    Name Pattern Helper Functions
    """
    
    def _is_season_folder_name(self, path: Path) -> bool:
        """
        Check if directory name suggests it's a season folder.
        Matches patterns like "Season 01", "S01", "Season1".
        
        Args:
            path: Directory path
            
        Returns:
            bool: True if name matches season folder pattern
        """
        sanitized = self.extractor._get_sanitized_file_or_dir(path)
        
        patterns = [
            r'^SEASON\.?\d+$',      # "SEASON01" or "SEASON.01"
            r'^S\.?\d+$',           # "S01" or "S.01"
            r'.*SEASON\.?\d+.*'     # Contains "SEASON01" anywhere
        ]
        
        for pattern in patterns:
            if re.match(pattern, sanitized):
                return True
        
        return False
    
    def _is_extras_folder_name(self, path: Path) -> bool:
        """
        Check if directory name suggests it's an extras folder.
        
        Args:
            path: Directory path
            
        Returns:
            bool: True if name matches extras folder pattern
        """
        sanitized = self.extractor._get_sanitized_file_or_dir(path)
        
        for keyword in self.EXTRA_KEYWORDS:
            if re.search(keyword, sanitized):
                return True
        
        return False
    
    """
    Utility Methods
    """
    
    def get_metadata_with_type(self, path: Path) -> MediaMetadata:
        """
        Extract full metadata including classification type.
        
        Args:
            path: Path to file or directory
            
        Returns:
            MediaMetadata: Complete metadata with type classification
        """
        metadata = self.extractor.extract_metadata(path)
        metadata.type = self.classify_media(path)
        return metadata
    
    def analyze_directory_structure(self, path: Path, max_depth: int = 3) -> dict:
        """
        Analyze directory structure and classify all contents.
        Useful for understanding torrent organization before reorganizing.
        
        Args:
            path: Root directory path
            max_depth: Maximum depth to traverse
            
        Returns:
            dict: Structure with classifications and metadata
        """
        if not path.is_dir() or max_depth <= 0:
            return {
                'path': str(path),
                'type': self.classify_media(path),
                'is_file': path.is_file()
            }
        
        result = {
            'path': str(path),
            'type': self.classify_media(path),
            'is_file': False,
            'children': []
        }
        
        try:
            for child in path.iterdir():
                if child.is_dir():
                    result['children'].append(
                        self.analyze_directory_structure(child, max_depth - 1)
                    )
                else:
                    result['children'].append({
                        'path': str(child),
                        'type': self.classify_media(child),
                        'is_file': True
                    })
        except PermissionError:
            pass
        
        return result
