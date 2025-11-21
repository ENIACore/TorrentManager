# Patterns to determine HDR format (using re.fullmatch)
HDR_PATTERNS = {
    # Matches HDR10+, HDR10PLUS, HDR10+
    'HDR10+': ['HDR10\+', 'HDR10PLUS'],
    # Matches HDR10
    'HDR10': ['HDR10'],
    # Matches HDR
    'HDR': ['HDR'],
    # Matches DOLBY-VISION, DOLBY VISION, DOLBYVISION, DV
    'DolbyVision': ['DOLBY-VISION', 'DOLBY\.VISION', 'DOLBYVISION', 'DV'],
    # Matches HLG (Hybrid Log-Gamma)
    'HLG': ['HLG'],
    # Matches PQ (Perceptual Quantizer)
    'PQ': ['PQ'],
    # Matches DOVI
    'DOVI': ['DOVI']
}

# Static descriptors commonly found in torrent filenames
STATIC_DESCRIPTORS = {
    # Release types and versions
    'EXTENDED', 'UNRATED', 'DIRECTORS', 'CUT', 'THEATRICAL', 'UNCUT',
    'PROPER', 'REPACK', 'INTERNAL', 'LIMITED', 'IMAX', 'FESTIVAL',
    'RETAIL', 'SUBBED', 'DUBBED', 'FINAL', 'REMASTERED', 'RESTORED',
    'COLORIZED', 'CRITERION', 'SPECIAL', 'EDITION', 'COLLECTORS',
    'ULTIMATE', 'ALTERNATE', 'REDUX', 'ANNIVERSARY',
    'DELUXE', 'ENHANCED', 'SE', 'CE', 'UE', 'DC', 'UC',

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

    # Container formats
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

# Patterns to identify TV show episodes and seasons (using regex with capture groups)
SHOW_PATTERNS = {
    # Matches EPISODE or EP (used to identify episode keyword)
    'EPISODE': r'(?:EPISODE|EP)',
    # Matches SEASON (used to identify season keyword)
    'SEASON': r'SEASON',
    # Matches S## format (e.g., S01, S1)
    'SDD': r'S(\d{1,2})',
    # Matches E### format (e.g., E001, E01, E1)
    'EDDD': r'E(\d{1,3})',
    # Matches ##x### format (e.g., 1x01, 01x001)
    'DDXDDD': r'(\d{1,2})X(\d{1,3})',
    # Matches S##E### format (e.g., S01E01, S1E1)
    'SDDEDDD': r'S(\d{1,2})E(\d{1,3})'
}


