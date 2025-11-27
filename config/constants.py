"""
Description: Constants for parsing information about a torrent file's quality and contents
Attributes:
    VIDEO_EXTENSIONS: Set of file extensions for video files
    SUBTITLE_EXTENSIONS: Set of file extensions for subtitle files
    AUDIO_EXTENSIONS: Set of file extensions for audio files

    RESOLUTION_PATTERNS: Dict of common patterns used to describe video resolution in file names
    CODEC_PATTERNS: Dict of common patterns used to describe video codec in file names
    QUALITY_PATTERNS: Dict of common patterns used to describe video quality & source in file names
    AUDIO_PATTERNS: Dict of common patterns used to describe audio in file names


    HDR_PATTERNS: Dict of common patterns used to describe HDR in file names
    SHOW_PATTERNS: Dict of common patterns used to identify TV show episodes and seasons
    EPISODES_PATTERNS: List of patterns to match episode identifiers with capture groups
    SEASONS_PATTERNS: List of patterns to match season identifiers with capture groups

    #STATIC_DESCRIPTORS: Set of static descriptors commonly found in torrent filenames
"""

# File extensions
VIDEO_EXTENSIONS = {
    'MP4', 'MKV', 'AVI', 'MOV', 'FLV', 'WMV', 'WEBM', 'M4V', 'TS', 'M2TS',
    'MPG', 'MPEG', 'VOB', '3GP', 'OGV', 'RMVB', 'RM', 'DIVX', 'F4V'
}

SUBTITLE_EXTENSIONS = {
    'SRT', 'ASS', 'SSA', 'SUB', 'VTT', 'SBV', 'JSON', 'SMI', 'LRC',
    'PSB', 'IDX', 'USF', 'TTML'
}

AUDIO_EXTENSIONS = {
    'MP3', 'FLAC', 'AAC', 'OGG', 'WMA', 'M4A', 'OPUS', 'WAV',
    'APE', 'WV', 'DTS', 'AC3', 'MKA'
}

# One word patterns to determine resolution (using re.fullmatch)
RESOLUTION_PATTERNS = {
    # Matches 8k, 4320, 4320P, 4320I, 7680X4320, FULLUHD
    '8K': [r'8K', r'4320[PI]?', r'7680X4320', r'FULLUHD'],
    # Matches 4k, UHD, 2160, 2160P, 2160I, 3840X2160
    '4K': [r'4K', r'UHD', r'2160[PI]?', r'3840X2160'],
    # Matches 2K, 1440, 1440P, 1440I, 2560X1440, QHD, WQHD
    '2K': [r'2K', r'1440[PI]?', r'2560X1440', r'QHD', r'WQHD'],
    # Matches 1080, 1080P, 1080I, FHD, 1920X1080, FULLHD
    '1080p': [r'1080[PI]?', r'FHD', r'1920X1080', r'FULLHD'],
    # Matches 720, 720P, 720I, 1280X720
    '720p': [r'720[PI]?', r'1280X720'],
    # Matches 576, 576P, 576I, PAL
    '576p': [r'576[PI]?', r'PAL'],
    # Matches 480, 480P, 480I, NTSC
    '480p': [r'480[PI]?', r'NTSC'],
    # Matches 360, 360P, 360I
    '360p': [r'360[PI]?'],
    # Matches 240, 240P, 240I
    '240p': [r'240[PI]?']
}

# One word patterns to determine video codec (using re.fullmatch)
CODEC_PATTERNS = {
    # Matches AV1, SVT-AV1, SVTAV1
    'AV1': [r'AV1', r'SVT\.AV1', r'SVTAV1', r'AOV1'],
    # Matches VP9
    'VP9': [r'VP9'],
    # Matches VP8
    'VP8': [r'VP8'],
    # Matches x265, X265, X.265, H265, H.265, HEVC, HEVC10, HEVC10BIT
    'x265': [r'X265', r'X\.265', r'H265', r'H\.265', r'HEVC', r'HEVC10', r'HEVC10BIT', r'H265P'],
    # Matches x264, X264, X.264, H264, H.264, AVC, AVC1
    'x264': [r'X264', r'X\.264', r'H264', r'H\.264', r'AVC', r'AVC1', r'H264P'],
    # Matches x263, X263, X.263, H263, H.263
    'x263': [r'X263', r'X\.263', r'H263', r'H\.263'],
    # Matches XVID, XVID-AF
    'XVID': [r'XVID', r'XVID\.AF'],
    # Matches DIVX, DIV3, DIVX6
    'DIVX': [r'DIVX', r'DIV3', r'DIVX6'],
    # Matches MPEG-4, MPEG4, MP4V
    'MPEG4': [r'MPEG\.4', r'MPEG4', r'MP4V'],
    # Matches MPEG-2, MPEG2, MP2V
    'MPEG2': [r'MPEG\.2', r'MPEG2', r'MP2V'],
    # Matches MPEG-1, MPEG1, MP1V
    'MPEG1': [r'MPEG\.1', r'MPEG1', r'MP1V'],
    # Matches VC-1, VC1, WMV3, WVC1
    'VC1': [r'VC\.1', r'VC1', r'WMV3', r'WVC1'],
    # Matches THEORA
    'THEORA': [r'THEORA'],
    # Matches PRORES, PRORES422, PRORES4444
    'PRORES': [r'PRORES', r'PRORES422', r'PRORES4444', r'PRORES422HQ'],
    # Matches DNxHD, DNXHD, DNxHR, DNXHR
    'DNxHD': [r'DNXHD', r'DNXHR']
}

# Patterns to determine video quality and source (using re.fullmatch)
SOURCE_PATTERNS = {
    # Matches REMUX
    'REMUX': [r'REMUX'],
    # Matches BluRay variants: BLURAY, BDRIP, BD-RIP, BR-RIP, BDMV, BDISO, BD25, BD50, BD66, BD100
    'BluRay': [r'BLURAY', r'BDRIP', r'BD\.RIP', r'BDRIP', r'BR\.RIP', r'BRRIP', r'BDMV', r'BDISO', r'BD25', r'BD50', r'BD66', r'BD100'],
    # Matches WEB-DL, WEBDL, WEB DL
    'WEB-DL': [r'WEB\.DL', r'WEBDL', r'WEB\.DL'],
    # Matches WEBRip, WEB-RIP, WEBRIP, WEB RIP
    'WEBRip': [r'WEBRIP', r'WEB-RIP', r'WEB\.RIP'],
    # Matches WEB (but not WEB-DL or WEBRip)
    'WEB': [r'WEB'],
    # Matches HDRip, HD-RIP, HDRIP, HD RIP
    'HDRip': [r'HDRIP', r'HD\.RIP'],
    # Matches DVDRip, DVD-RIP, DVDRIP, DVD RIP
    'DVDRip': [r'DVDRIP', r'DVD\.RIP'],
    # Matches DVD, DVDSCR, DVD5, DVD9
    'DVD': [r'DVD', r'DVDSCR', r'DVD5', r'DVD9'],
    # Matches HDTV, HDTVRIP, DTTV, PDTV, SDTV, LDTV
    'HDTV': [r'HDTV', r'HDTVRIP', r'DTTV', r'PDTV', r'SDTV', r'LDTV'],
    # Matches TELECINE, TC
    'TELECINE': [r'TELECINE', r'TC'],
    # Matches TELESYNC, TS
    'TELESYNC': [r'TELESYNC', r'TS'],
    # Matches SCREENER, SCR, DVDSCR, BDSCR
    'SCREENER': [r'SCREENER', r'SCR', r'DVDSCR', r'BDSCR'],
    # Matches CAMRIP, CAM, HDCAM
    'CAM': [r'CAMRIP', r'CAM', r'HDCAM'],
    # Matches WORKPRINT, WP
    'WORKPRINT': [r'WORKPRINT', r'WP'],
    # Matches PPV, PPVRIP
    'PPV': [r'PPV', r'PPVRIP'],
    # Matches VODRIP, VOD
    'VODRip': [r'VODRIP', r'VOD'],
    # Matches HC, HCHDCAM
    'HC': [r'HC', r'HCHDCAM'],
    # Matches LINE
    'LINE': [r'LINE'],
    # Matches HDTS, HD-TS, HDTS
    'HDTS': [r'HDTS', r'HD\.TS'],
    # Matches HDTC, HD-TC, HDTC
    'HDTC': [r'HDTC', r'HD\.TC'],
    # Matches TVRIP, SATRIP, DTTVRIP
    'TVRip': [r'TVRIP', r'SATRIP', r'DTTVRIP']
}

# Patterns to determine audio codec and channel configuration (using re.fullmatch)
AUDIO_PATTERNS = {
    # Matches ATMOS, DOLBY-ATMOS, DOLBY ATMOS, DOLBYATMOS
    'Atmos': [r'ATMOS', r'DOLBY-ATMOS', r'DOLBY\.ATMOS', r'DOLBYATMOS'],
    # Matches DTS-X, DTSX, DTS X
    'DTS-X': [r'DTSX', r'DTS\.X'],
    # Matches DTS-HD-MA, DTS-HD, DTSHD-MA, DTSHD
    'DTS-HD': [r'DTS\.HD\.MA', r'DTS\.HD\.MA', r'DTSHD-MA', r'DTSHD\.MA', r'DTS\.HD', r'DTSHD'],
    # Matches DTS-MA, DTSMA
    'DTS-MA': [r'DTS\.MA', r'DTSMA', r'DTS\.MA'],
    # Matches DTS-ES, DTSES, DTS ES
    'DTS-ES': [r'DTS\.ES', r'DTSES', r'DTS\.ES'],
    # Matches DTS (standalone, not part of other DTS variants)
    'DTS': [r'DTS'],
    # Matches TrueHD, TRUE-HD, TRUEHD, TRUE HD
    'TrueHD': [r'TRUEHD', r'TRUE\.HD', r'TRUE\.HD'],
    # Matches DD+, DDP, E-AC-3, EAC3, DD-PLUS, DDPLUS
    'DD+': [r'DDP', r'E\.AC\.3', r'E\.AC\.3', r'EAC3', r'DD\.PLUS', r'DD\.PLUS', r'DDPLUS'],
    # Matches DD, AC3, DOLBY-DIGITAL, DOLBY DIGITAL (but not DD+ or variants)
    'DD': [r'DD', r'AC3', r'DOLBY-DIGITAL', r'DOLBY\.DIGITAL', r'DOLBYDIGITAL'],
    # Matches AAC, HE-AAC, HEAAC, HE AAC
    'AAC': [r'AAC', r'HE\.AAC', r'HEAAC', r'HE\.AAC'],
    # Matches FLAC
    'FLAC': [r'FLAC'],
    # Matches MP3
    'MP3': [r'MP3'],
    # Matches LPCM, PCM
    'LPCM': [r'LPCM', r'PCM'],
    # Matches OGG, VORBIS
    'OGG': [r'OGG', r'VORBIS'],
    # Matches OPUS
    'OPUS': [r'OPUS'],
    # Matches 5.1, 5-1, 51, 6CH
    '5.1': [r'5\.1', r'5\.1', r'51', r'6CH'],
    # Matches 7.1, 7-1, 71, 8CH
    '7.1': [r'7\.1', r'7\.1', r'71', r'8CH'],
    # Matches 2.0, 2-0, 20, STEREO, 2CH
    '2.0': [r'2\.0', r'2\.0', r'20', r'STEREO', r'2CH'],
    # Matches DUAL-AUDIO, DUAL AUDIO, DUAL
    'DUAL': [r'DUAL\.AUDIO', r'DUAL']
}

# If season number exists, it is capture group 1, for all matches
SEASONS_PATTERNS = [
    # Matches S<number>
    r'S(\d+)',
    # Matches S.<number>
    r'S\.(\d+)',

    # Matches SEA<number>
    r'SEA(\d+)',
    # Matches SEA.<number>
    r'SEA\.(\d+)',

    # Matches SEASON<number>
    r'SEASON(\d+)',
    # Matches SEASON.<number>
    r'SEASON\.(\d+)',

    # Matches SEASON
    r'SEASON',

    # Matches S<number>E<number>
    r'S(\d+)E\d+',
]

# If season number exists, it is capture group 1, for all matches
EPISODES_PATTERNS = [
    # Matches E<number>
    r'E(\d+)',
    # Matches E.<number>
    r'E\.(\d+)',

    # Matches EP<number>
    r'EP(\d+)',
    # Matches EP.<number>
    r'EP\.(\d+)',

    # Matches EPISODE<number>
    r'EPISODE(\d+)',
    # Matches EPISODE.<number>
    r'EPISODE\.(\d+)',

    # Matches EPISODE
    r'EPISODE',
    # Matches EP
    r'EP',

    # Matches S<number>E<number>
    r'S\d+E(\d+)',
    # Matches <number>X<number>
    r'\d+X(\d+)',
    # Matches <number>.X.<number> (e.g., 1.X.01, 2.X.15)
    r'\d+\.X\.(\d+)',

]

# Pattenrs for
EXTRAS_PATTERNS = [
    'EXTRA[S]', 
    'FEATURETTE[s]', 
    'BEHIND.THE.SCENE[S]', 
    'BTS',
    'DELETED.SCENE[S]', 
    'MAKING.OF', 
    'TRAILER',
    'BONUS', 
    'DOCUMENTARY', 
    'DOCUMENTARIES'
]
