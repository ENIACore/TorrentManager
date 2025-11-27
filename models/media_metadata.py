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

    # Booleans to describe if certain patterns have matches, extensible for future use
    # To add more patterns, add variable, then add pattern to constants.py, then add matching to bottom of MediaExtractor.extract()
    season_patterns: bool = False
    episode_patterns: bool = False
    extras_patterns: bool = False


    def __str__(self):
        parts = []

        if self.title:
            parts.append(self.get_formatted_title())
        if self.year:
            parts.append(str(self.year))
        if self.season:
            parts.append(self.get_formatted_season_num())
        if self.episode:
            parts.append(self.get_formatted_episode_num())
        if self.resolution:
            parts.append(self.resolution)
        if self.codec:
            parts.append(self.codec)
        if self.source:
            parts.append(self.source)
        if self.audio:
            parts.append(self.audio)

        return '.'.join(parts)

    def get_formatted_title(self) -> str:
        if self.title:
            # Make title lowercase and remove quotes
            lowercase_title = self.title.lower()
            lowercase_title = lowercase_title.replace('\'', '').replace('\"', '')

            # Remove special characters, and join words with '.'
            alphanumeric_title = re.sub(r'[^a-z0-9]+', '.', lowercase_title)
            # Remove '.' from beginning & end of title
            alphanumeric_title = alphanumeric_title.strip('.')

            # Capitalize each word in title
            words = alphanumeric_title.split('.')
            words = [word.capitalize() for word in words if word]

            return '.'.join(words)
        else:
            return ''

    def get_formatted_season_num(self) -> str:
        season_num = self.season if self.season else 1
        return f'S{str(season_num).zfill(2)}'

    def get_formatted_episode_num(self) -> str:
        ep_num = self.episode if self.episode else 1
        return f'E{str(ep_num).zfill(3)}'
        

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
