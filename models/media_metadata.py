import re

"""
    Description: Data class for media file metadata information
    Attributes:

        title (optional): Title of movie or series
        year (optional): Year of movie or series
        season (optional): Season of series
        episode (optional): Episode of series & season

        resolution (optional): Resolution of media file
        codec (optional): Codec of media file
        quality (optional): quality of media file
        audio (optional): audio of media file

"""
class MediaMetadata:
    # Descriptors of show or movie
    title: str | None = None
    year: int | None = None
    season: int | None = None
    episode: int | None = None

    # Descriptors of media file encoding
    resolution: str | None = None
    codec: str | None = None
    quality: str | None = None
    audio: str | None = None
    ext: str | None = None

    """
        Description: Returns metadata in filename format without file ext
    """
    def __str__(self):
        parts = []

        if self.title:
            parts.append(self._format_title(self.title))
        if self.year:
            parts.append(str(self.year))
        if self.season:
            parts.append(str(self.season).zfill(2))
        if self.episode:
            parts.append(str(self.episode).zfill(3))
        if self.resolution:
            parts.append(self.resolution)
        if self.codec:
            parts.append(self.codec)
        if self.quality:
            parts.append(self.quality)
        if self.audio:
            parts.append(self.audio)

        return '.'.join(parts)

    """
        Description: Returns movie title in filename format
    """
    def _format_title(self, title) -> str | None:
        if title:
            # Make title lowercase and remove quotes
            lowercase_title = title.lower()
            lowercase_title = lowercase_title.replace('\'', '').replace('\"', '')

            # Remove special characters, and join words with '.'
            alphanumeric_title = re.sub(r'[^a-z0-9]+', '.', lowercase_title)            
            # Remove '.' from beginning & end of title
            alphanumeric_title = alphanumeric_title.strip('.')

            # Capitalize each word in title
            words = alphanumeric_title.split('.')
            words = [word.capitalize() for word in words if word]

            return '.'.join(words)
        elif title == '':
            return ''
        else:
            return None
