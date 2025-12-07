from models.media_metadata import MediaMetadata
import pytest




def test_valid_season_num():
    metadata = MediaMetadata()
    metadata.season = 1
    assert metadata.get_formatted_season_num() == 'S01'

def test_no_season_num():
    metadata = MediaMetadata()
    assert metadata.get_formatted_season_num() == 'S??'

def test_negative_season_num():
    metadata = MediaMetadata()
    metadata.season = -1
    assert metadata.get_formatted_season_num() == 'S01'
