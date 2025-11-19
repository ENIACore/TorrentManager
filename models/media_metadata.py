
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

    def __str__(self):
        parts = []

        if self.title:
            parts.append(self.title)
        if self.year:
            parts.append(str(self.year))
        if self.season:
            parts.append(str(self.season))
        if self.episode:
            parts.append(str(self.episode))
        if self.resolution:
            parts.append(self.resolution)
        if self.codec:
            parts.append(self.codec)
        if self.quality:
            parts.append(self.quality)
        if self.audio:
            parts.append(self.audio)

        return '.'.join(parts)
