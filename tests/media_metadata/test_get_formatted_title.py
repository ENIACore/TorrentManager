from models.media_metadata import MediaMetadata
import pytest


def test_no_title():
    metadata = MediaMetadata()
    assert metadata.get_formatted_title() == ''

def test_substitute_special_chars():
    metadata = MediaMetadata()
    metadata.title = 'My !@#$%*()Title'
    assert metadata.get_formatted_title() == 'My.Title'

def test_capitalize_title():
    metadata = MediaMetadata()
    metadata.title = 'MY.TITLE'
    assert metadata.get_formatted_title() == 'My.Title'

def test_strip_title():
    metadata = MediaMetadata()
    metadata.title = '.My.Title.'
    assert metadata.get_formatted_title() == 'My.Title'
