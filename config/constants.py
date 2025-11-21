"""
Description: Constants for torrent file parsing
Attributes:

    VIDEO_EXTENSIONS: Set of file extensions for video files
    SUBTITLE_EXTENSIONS: Set of file extensions for subtitle files
    AUDIO_EXTENSIONS: Set of file extensions for audio files

    RESOLUTION_PATTERNS: Dict of common patterns used to describe video resolution in file names
    CODEC_PATTERNS: Dict of common patterns used to describe video codec in file names
    QUALITY_PATTERNS: Dict of common patterns used to describe video quality & source in file names
    AUDIO_PATTERNS: Dict of common patterns used to describe audio in file names

    HDR_PATTERNS: String of common patterns used in file to indicate HDR

"""

# One word patterns to determine resolution (using re.fullmatch)
RESOLUTION_PATTERNS = {
    # Matches 8k, 4320, 4320P, 4320I, 7680X4320, FULLUHD
    '8K': ['8K', '4320[PI]?', '7680X4320', 'FULLUHD'],
    # Matches 4k, UHD, 2160, 2160P, 2160I, 3840X2160
    '4K': ['4K', 'UHD', '2160[PI]?', '3840X2160'],
    # Matches 2K, 1440, 1440P, 1440I, 2560X1440, QHD, WQHD
    '2K': ['2K', '1440[PI]?', '2560X1440', 'QHD', 'WQHD'],
    # Matches 1080, 1080P, 1080I, FHD, 1920X1080, FULLHD
    '1080p': ['1080[PI]?', 'FHD', '1920X1080', 'FULLHD'],
    # Matches 720, 720P, 720I, 1280X720
    '720p': ['720[PI]?', '1280X720'],
    # Matches 576, 576P, 576I, PAL
    '576p': ['576[PI]?', 'PAL'],
    # Matches 480, 480P, 480I, NTSC
    '480p': ['480[PI]?', 'NTSC'],
    # Matches 360, 360P, 360I
    '360p': ['360[PI]?'],
    # Matches 240, 240P, 240I
    '240p': ['240[PI]?']
}
