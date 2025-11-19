from os import listdir, walk
from os.path import isfile, join
import re
from typing import Any, Dict
from datetime import date
from constants import (
        VIDEO_EXTENSIONS,
        AUDIO_EXTENSIONS,
        SUBTITLE_EXTENSIONS,
        RESOLUTION_PATTERNS,
        CODEC_PATTERNS,
        QUALITY_PATTERNS,
        AUDIO_PATTERNS,
        HDR_PATTERNS,
        STATIC_DESCRIPTORS,
        SHOW_PATTERNS
    )


class FileExtractor:
    
    def __init__(self, filename):
        self.filename = filename
        self.sanitize_filename()

    # Sanitizes filename
    def sanitize_filename(self):
        self.filename = self.filename.rstrip()
        self.filename = self.filename.upper()
        self.filename = self.filename.replace('\'', '')
        self.filename = self.filename.replace('\"', '')
        self.filename = re.sub(r'[^A-Z0-9]+', '.', self.filename)

    def is_video_file(self) -> bool:
        file_extension = self.filename.split('.')[-1]
        return file_extension in VIDEO_EXTENSIONS

    def is_subtitle_file(self) -> bool:
        file_extension = self.filename.split('.')[-1]
        return file_extension in SUBTITLE_EXTENSIONS

    def parse_file_encoding(self):
         
        for res_name, pattern in RESOLUTION_PATTERNS.items():
            if re.search(pattern, self.filename):
                self.resolution = res_name
                break
        
        for codec_name, pattern in CODEC_PATTERNS.items():
            if re.search(pattern, self.filename):
                self.codec = codec_name
                break
        
        for quality_name, pattern in QUALITY_PATTERNS.items():
            if re.search(pattern, self.filename):
                self.quality = quality_name
                break
        
        for audio_name, pattern in AUDIO_PATTERNS.items():
            if re.search(pattern, self.filename):
                self.audio = audio_name
                break
        
        if re.search(HDR_PATTERNS, self.filename):
            self.hdr = True

    def parse_video_info(self):
        parts = self.filename.split('.')

        self.episode = -1
        self.season = -1
        self.type = None
        
        print('========== ' + self.filename)
        for i, part in enumerate(parts):
            match = None
            
            if (match := re.fullmatch(SHOW_PATTERNS['SDD'], part)):
                print('matched SDD with value: ' + match.group(1))
                self.season = int(match.group(1))
            elif (match := re.fullmatch(SHOW_PATTERNS['EDDD'], part)):
                self.episode = int(match.group(1))
            elif (match := re.fullmatch(SHOW_PATTERNS['SDDEDDD'], part)):
                self.season = int(match.group(1))
                self.episode = int(match.group(2))
            elif (match := re.fullmatch(SHOW_PATTERNS['DDXDDD'], part)):
                self.season = int(match.group(1))
                self.episode = int(match.group(2))
            elif (match := re.fullmatch(SHOW_PATTERNS['SEASON'], part)):
                print('later')   

            if (match := re.fullmatch(SHOW_PATTERNS['EPISODE'], part) and i < len(parts) - 1):
                print('matched episode')

    def parse_subtitle_info(self):
        print('hi')


    def is_descriptor(self, substr: str) -> bool:

        if (substr in SUBTITLE_EXTENSIONS or 
            substr in VIDEO_EXTENSIONS or
            substr in AUDIO_EXTENSIONS):
            return True
        
        for patterns in [RESOLUTION_PATTERNS.items(), CODEC_PATTERNS.items(), 
                        QUALITY_PATTERNS, AUDIO_PATTERNS]:
            for pattern in patterns.values():
                if re.match(f'^{pattern}$', substr):
                    return True

        if re.match(f'^{HDR_PATTERNS}$', substr, re.IGNORECASE):
            return True
        
        
        if substr in STATIC_DESCRIPTORS:
            return True
        
        return False






file_names = [
    'Smiling.Friends.S01E07.Frowning.Friends.2160p.Web.AI.AV1.AC3.Dual-[Enrav1sh].mkv',
    'Smiling.Friends.S01E08.Charlie.Dies.and.Doesnt.Come.Back.2160p.Web.AI.AV1.AC3.Dual-[Enrav1sh].mkv',
    'Smiling.Friends.S01E09.The.Smiling.Friends.Go.To.Brazil.2160p.Web.AI.AV1.AC3.Dual-[Enrav1sh].mkv',
    'Stranger Things S01E07 Chapter Seven The Bathtub 2160p NF WEB-DL TrueHD 5 1IMDb',
    'Stranger Things S01E05 Chapter Five The Flea and the Acrobat 2160p NF WEB-DIMDb',
    'Stranger Things S01E08 Chapter Eight The Upside Down 2160p NF WEB-DL TrueHDIMDb',
    'Mickey.Mouse.Clubhouse.Plus.S01E13.480p.x264-mSD[EZTVx.to].mkv', 	
    'The Trades (CA) 2024 S02E02 720p hevc x265 [WD-13].mkv',
]

for name in file_names:
    file_parser = FileExtractor(name)
    file_parser.parse_video_info()
"""
with open('file_tree_input.txt', 'r') as file:
    for line in file:
        file_parser = FileParser(line)
"""




"""
RAID_PATH = '/mnt/RAID'
QBIT_PATH = RAID_PATH + '/qbit-data'
QBIT_DOWNLOAD_PATH = QBIT_PATH + '/downloads'
def print_dir(path: str):
    for root, dirs, files in walk(path):

        for file in files:
            full_path = join(root, file)
        
        for dir in dirs:
            print_dir(dir)
"""




