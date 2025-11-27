import os

# Default paths - can be overridden by environment variables
TORRENT_PATH = os.getenv('TORRENT_DOWNLOAD_PATH', '/mnt/RAID/qbit-data/downloads')
MANAGER_PATH = os.getenv('TORRENT_MANAGER_PATH', '/mnt/RAID/torrent-manager')
MEDIA_PATH = os.getenv('MEDIA_SERVER_PATH', '/mnt/RAID/jelly/media')

# Dry run mode - set to 'true' to only log actions without moving files
DRY_RUN = os.getenv('TORRENT_MANAGER_DRY_RUN', 'true').lower() == 'true'
