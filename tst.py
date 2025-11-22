import re
from config.constants import (RESOLUTION_PATTERNS)
from extractor.media_extractor import MediaExtractor
from pathlib import Path




example = 'y'
while (example != 'n'):
    example = input('Enter a movie or show (enter n to stop): ')
    path = Path(example)

    extractor = MediaExtractor()
    metadata = extractor.extract_metadata(path)

    metadata.print()






















"""
re_str = r'8K|4320[PI]?|7680X4320|FULLUHD'

match = re.fullmatch(re_str, '4320')

if match:
    print('match found')
else:
    print('match not found')
"""


"""
for key, value in RESOLUTION_PATTERNS.items():
    print('res is: ' + key)
    print('pattern is: ' + value)
"""


"""
pattern = 'MY.P.HI'
filename = 'My pattern is here and it continues on'
extractor = MediaExtractor()
filename = extractor._get_sanitized_file_or_dir(Path(filename))
parts = filename.split('.')
start_index = 0


num_parts = len(pattern.split('.'))
combined_parts =  ''
for i in range(start_index, min(start_index + num_parts, len(parts))):
    if not combined_parts:
        combined_parts = parts[i]
    else:
        combined_parts = combined_parts + '.' + parts[i] 

print('pattern to match will cover ' + str(num_parts) + ' parts')
print('combined parts for pattern is: ' + combined_parts)
"""


"""
for resolution in RESOLUTION_PATTERNS:
    for pattern in RESOLUTION_PATTERNS[resolution]:
        print('resolution is ' + resolution + ' and pattern in resolution patterns is: ' + pattern)
"""

