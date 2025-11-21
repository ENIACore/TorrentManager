SUBTITLE_EXTENSIONS = {'SRT', 'ASS', 'SSA', 'SUB', 'VTT', 'SBV', 'JSON', 'SMI', 'LRC', 'PSB', 'IDX', 'USF', 'TTML'}
VIDEO_EXTENSIONS = {'MP4', 'MKV', 'AVI', 'MOV', 'FLV', 'WMV', 'WEBM', 'M4V', 'TS', 'M2TS', 'MPG', 'MPEG', 'VOB', '3GP', 'OGV', 'RMVB', 'RM', 'DIVX', 'F4V'}
AUDIO_EXTENSIONS = {'MP3', 'FLAC', 'AAC', 'OGG', 'WMA', 'M4A', 'OPUS', 'WAV', 'APE', 'WV', 'DTS', 'AC3', 'MKA'}

CODEC_PATTERNS = {
    'AV1': r'AV1',
    'VP9': r'VP9',
    'VP8': r'VP8',
    'x265': r'(?:X\.?265|H\.?265|HEVC|HEVC10)',
    'x264': r'(?:X\.?264|H\.?264|AVC)',
    'x263': r'(?:X\.?263|H\.?263)',
    'XVID': r'XVID',
    'DIVX': r'DIVX?',
    'MPEG4': r'MPEG[\-\s]?4',
    'MPEG2': r'MPEG[\-\s]?2',
    'MPEG1': r'MPEG[\-\s]?1',
    'VC1': r'VC[\-]?1',
    'AVC1': r'AVC1',
    'SVT-AV1': r'SVT[\-]?AV1'
}

QUALITY_PATTERNS = {
    'REMUX': r'REMUX',
    'BluRay': r'(?:BLURAY|BDRIP|BD[\-]?RIP|BR[\-]?RIP|BDMV|BDISO|BD25|BD50|BD66|BD100)',
    'WEB-DL': r'(?:WEB[\-\s]?DL|WEBDL)',
    'WEBRip': r'(?:WEB[\-\s]?RIP|WEBRIP)',
    'WEB': r'WEB(?![\-\s]?(?:DL|RIP))',
    'HDRip': r'(?:HD[\-\s]?RIP|HDRIP)',
    'DVDRip': r'(?:DVD[\-\s]?RIP|DVDRIP)',
    'DVD': r'(?:DVD(?![\-\s]?RIP)|DVDSCR|DVD5|DVD9)',
    'HDTV': r'(?:HDTV|HDTVRIP|DTTV|PDTV|SDTV|LDTV)',
    'TELECINE': r'(?:TELECINE|TC)',
    'TELESYNC': r'(?:TELESYNC|TS)',
    'SCREENER': r'(?:SCREENER|SCR|DVDSCR|BDSCR)',
    'CAM': r'(?:CAMRIP|CAM|HDCAM)',
    'WORKPRINT': r'(?:WORKPRINT|WP)',
    'PPV': r'(?:PPV|PPVRIP)',
    'VODRip': r'(?:VODRIP|VOD)',
    'HC': r'(?:HC|HCHDCAM)',
    'LINE': r'LINE',
    'HDTS': r'(?:HDTS|HD[\-]?TS)',
    'HDTC': r'(?:HDTC|HD[\-]?TC)',
    'TVRip': r'(?:TVRIP|SATRIP|DTTVRIP)'
}

AUDIO_PATTERNS = {
    'Atmos': r'(?:ATMOS|DOLBY[\-\s]?ATMOS)',
    'DTS-X': r'DTS[\-\s]?X',
    'DTS-HD': r'(?:DTS[\-\s]?HD[\-\s]?MA|DTS[\-\s]?HD)',
    'DTS-ES': r'DTS[\-\s]?ES',
    'DTS': r'DTS(?![\-\s]?(?:HD|X|ES))',
    'TrueHD': r'(?:TRUE[\-\s]?HD|TRUEHD)',
    'DD+': r'(?:DD[\+]|DDP|E[\-]?AC[\-]?3|EAC3|DD[\-\s]?PLUS)',
    'DD': r'(?:DD(?![\+\-\s]?(?:PLUS|P))|AC3|DOLBY[\-\s]?DIGITAL)',
    'AAC': r'(?:AAC|HE[\-]?AAC)',
    'FLAC': r'FLAC',
    'MP3': r'MP3',
    'LPCM': r'(?:LPCM|PCM)',
    'OGG': r'(?:OGG|VORBIS)',
    'OPUS': r'OPUS',
    'DTS-MA': r'DTS[\-\s]?MA',
    '5.1': r'(?:5\.1|5[\-\s]?1|51|6CH)',
    '7.1': r'(?:7\.1|7[\-\s]?1|71|8CH)',
    '2.0': r'(?:2\.0|2[\-\s]?0|20|STEREO|2CH)',
    'DUAL': r'(?:DUAL[\-\s]?AUDIO|DUAL)'
}

HDR_PATTERNS = r'(?:HDR10\+?|HDR|DOLBY[\-\s]?VISION|DV)'

# Static descriptors describing file
STATIC_DESCRIPTORS = {
    # Release types and versions
    'EXTENDED', 'UNRATED', 'DIRECTORS', 'CUT', 'THEATRICAL', 'UNCUT',
    'PROPER', 'REPACK', 'INTERNAL', 'LIMITED', 'IMAX', 'FESTIVAL',
    'RETAIL', 'SUBBED', 'DUBBED', 'FINAL', 'REMASTERED', 'RESTORED',
    'COLORIZED', 'CRITERION', 'SPECIAL', 'EDITION', 'COLLECTORS',
    'ULTIMATE', 'EXTENDED', 'ALTERNATE', 'REDUX', 'ANNIVERSARY',
    'DELUXE', 'ENHANCED', 'SE', 'CE', 'UE', 'DC', 'TC', 'UC',
    
    # Video features
    'DOLBY', 'VISION', 'DV', 'SDR',
    '10BIT', '12BIT', '8BIT', 'HLG', 'PQ', 'DOVI', 'DCI',
    '3D', 'HSBS', 'HOU', 'SBS', 'HALF', 'FULL', 'MVC',
    
    # Frame rates
    '23', '976FPS', '24FPS', '25FPS', '29', '97FPS', '30FPS',
    '48FPS', '50FPS', '59', '94FPS', '60FPS', '120FPS',
    
    # Language and subtitle related
    'MULTI', 'DUAL', 'SUBS', 'SUBBED', 'HARDSUB', 'SOFTSUB',
    'ENGSUB', 'FANSUB', 'VOSTFR', 'FORCED', 'COMMENTARY',
    
    # Streaming services
    'NETFLIX', 'NF', 'AMZN', 'AMAZON', 'PRIME', 'ATVP', 'APPLETV',
    'APPLE', 'HULU', 'DSNP', 'DISNEY', 'DISNEYPLUS', 'HMAX',
    'HBOMAX', 'HBO', 'PEACOCK', 'PCOK', 'PARAMOUNT', 'PMTP',
    'STAN', 'CRAV', 'CRAVE', 'NOW', 'BBC', 'IPLAYER', 'ITV',
    'ALL4', 'CC', 'COMEDYCENTRAL', 'DCU', 'DCUNIVERSE', 'FTV',
    'FREEFORM', 'HOTSTAR', 'HS', 'IQIYI', 'IQ', 'MUBI', 'MTV',
    'NEON', 'NICK', 'NICKELODEON', 'RED', 'YOUTUBE', 'YT',
    'ROKU', 'SHOWTIME', 'SHO', 'SKYGO', 'SKY', 'STARZ', 'STZ',
    'SYFY', 'TFOU', 'TUBI', 'TVN', 'VIKI', 'VIU', 'VLIVE',
    
    # TV related
    'PDTV', 'HDTV', 'SDTV', 'LDTV', 'DTTV', 'UHDTV', 'WEBCAST',
    'COMPLETE', 'SEASON', 'S01', 'S02', 'EP', 'E01', 'E02',
    'PILOT', 'FINALE', 'MINISERIES', 'TVSPECIAL',
    
    # Region codes
    'NTSC', 'PAL', 'SECAM', 'RC', 'R0', 'R1', 'R2', 'R3', 'R4',
    'R5', 'R6', 'RA', 'RB', 'RC', 'REGION', 'FREE',
    
    # Container formats (might appear mid-string)
    'MKV', 'MP4', 'AVI', 'MOV', 'WMV', 'FLV', 'WEBM', 'M4V',
    'MPG', 'MPEG', 'TS', 'M2TS', 'VOB', 'ISO', 'IMG',
    
    # Scene groups and tags
    'NUKED', 'UNNUKED', 'PROOFFIX', 'RARBG', 'YIFY', 'YTS',
    'ETRG', 'SPARKS', 'AXXO', 'FGT', 'PSA', 'STUTTERSHIT',
    'DIMENSION', 'LOL', 'FLEET', 'EVOLVE', 'IMMERSE', 'AVS',
    'SVA', 'REWARD', 'NTB', 'DEMAND', 'FUM', 'CROOKS', 'BATV',
    
    # Quality indicators
    'HQ', 'LQ', 'MQ', 'SQ', 'VHS', 'VCD', 'SVCD', 'LASERDISC',
    'LD', 'MD', 'MICROHD', 'MINIBLURAY', 'MINIDVD',
    
    # Other technical specs
    'NTFS', 'FAT32', 'EXFAT', 'HFS', 'APFS', 'EXT4',
    'CRF', 'CBR', 'VBR', 'ABR', '2PASS', '1PASS',
    'CUSTOM', 'RETAIL', 'BOOTLEG', 'PIRATE', 'LEAKED',
   
    # Additional audio terms
    'MONO', 'SURROUND', 'QUADRAPHONIC', 'BINAURAL', 'AMBISONIC',
    
    # Aspect ratios
    '16X9', '4X3', '21X9', '185X1', '240X1', 'FULLSCREEN',
    'WIDESCREEN', 'LETTERBOX', 'PILLARBOX', 'ANAMORPHIC',
    
    # Miscellaneous
    'SAMPLE', 'TRAILER', 'TEASER', 'PROMO', 'EXTRAS', 'BONUS',
    'FEATURETTE', 'INTERVIEW', 'BTS', 'BEHINDTHESCENES',
    'MAKINGOF', 'DELETED', 'SCENES', 'OUTTAKES', 'BLOOPERS',
    'GAG', 'REEL', 'COMMENTARY', 'DUPE', 'READNFO', 'PROOF'
}

#('r'\d{1,3}',
SHOW_PATTERNS = {
    # Used to match SEASON.<number> EPISODE.<number>
    'EPISODE': r'(EPISODE|EP)',
    'SEASON': r'SEASON',
    'SDD': r'S(\d{1,2})',
    'EDDD': r'E(\d{1,3})',  
    'DDXDDD': r'(\d{1,2})X(\d{1,3})',
    'SDDEDDD': r'S(\d{1,2})E(\d{1,3})'
}
