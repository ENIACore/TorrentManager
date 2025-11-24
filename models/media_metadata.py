from typing import Literal
import re


class MediaMetadata:
    # Show, movie, or extra descriptors
    title: str | None = None
    year: int | None = None
    season: int | None = None
    episode: int | None = None

    # Media descriptors
    resolution: str | None = None
    codec: str | None = None
    source: str | None = None
    audio: str | None = None

    language: str | None = None

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
        if self.source:
            parts.append(self.source)
        if self.audio:
            parts.append(self.audio)

        return '.'.join(parts)

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

    def print(self):
        print("MediaMetadata:")
        print(f"  Title:      {self.title}")
        print(f"  Year:       {self.year}")
        print(f"  Season:     {self.season}")
        print(f"  Episode:    {self.episode}")
        print(f"  Resolution: {self.resolution}")
        print(f"  Codec:      {self.codec}")
        print(f"  Source:     {self.source}")
        print(f"  Audio:      {self.audio}")
