from models.media_metadata import MediaMetadata
import pytest

@pytest.fixture
def valid_episode_metadata():
    metadata = MediaMetadata()
    metadata.title = 'MOVIE TITLE'
    metadata.year = 2025
    metadata.season = 1
    metadata.episode = 1
    metadata.resolution = '1080p'
    metadata.codec = 'x264'
    metadata.source = 'WEB-DL'
    metadata.audio = 'DTS'
    metadata.language = 'ENGLISH'
    return metadata


def test_with_all_values(valid_episode_metadata):
    assert str(valid_episode_metadata) == 'Movie.Title.2025.S01.E001.1080p.x264.WEB-DL.DTS'

def test_with_missing_title(valid_episode_metadata):
    valid_episode_metadata.title = None
    assert str(valid_episode_metadata) == '2025.S01.E001.1080p.x264.WEB-DL.DTS'

def test_with_missing_year(valid_episode_metadata):
    valid_episode_metadata.year = None
    assert str(valid_episode_metadata) == 'Movie.Title.S01.E001.1080p.x264.WEB-DL.DTS' 

def test_with_missing_season(valid_episode_metadata):
    valid_episode_metadata.season = None
    assert str(valid_episode_metadata) == 'Movie.Title.2025.E001.1080p.x264.WEB-DL.DTS' 

def test_with_missing_episode(valid_episode_metadata):
    valid_episode_metadata.episode = None
    assert str(valid_episode_metadata) == 'Movie.Title.2025.S01.1080p.x264.WEB-DL.DTS' 

def test_with_missing_resolution(valid_episode_metadata):
    valid_episode_metadata.resolution = None
    assert str(valid_episode_metadata) == 'Movie.Title.2025.S01.E001.x264.WEB-DL.DTS' 

def test_with_missing_codec(valid_episode_metadata):
    valid_episode_metadata.codec = None
    assert str(valid_episode_metadata) == 'Movie.Title.2025.S01.E001.1080p.WEB-DL.DTS' 

def test_with_missing_source(valid_episode_metadata):
    valid_episode_metadata.source = None
    assert str(valid_episode_metadata) == 'Movie.Title.2025.S01.E001.1080p.x264.DTS' 

def test_with_missing_audio(valid_episode_metadata):
    valid_episode_metadata.audio = None
    assert str(valid_episode_metadata) == 'Movie.Title.2025.S01.E001.1080p.x264.WEB-DL' 

def test_without_all_values():
    metadata = MediaMetadata()
    assert str(metadata) == '' 
