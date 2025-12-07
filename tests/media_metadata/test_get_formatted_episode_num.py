from models.media_metadata import MediaMetadata
import pytest

def test_valid_episode_num():
    metadata = MediaMetadata()
    metadata.episode = 1
    assert metadata.get_formatted_episode_num() == 'E001'

def test_no_episode_num():
    metadata = MediaMetadata()
    assert metadata.get_formatted_episode_num() == 'E???'

def test_negative_episode_num():
    metadata = MediaMetadata()
    metadata.episode = -1
    assert metadata.get_formatted_episode_num() == 'E001'
