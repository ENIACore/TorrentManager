import pytest
from models.media_metadata import MediaMetadata

"""Create a MediaMetadata instance with standard test values."""
@pytest.fixture
def base_metadata():
    metadata = MediaMetadata()
    metadata.title = 'title'
    metadata.year = 2025
    metadata.season = 1
    metadata.episode = 1
    metadata.resolution = '1080p'
    metadata.codec = 'x265'
    metadata.quality = 'BluRay'
    metadata.audio = 'DUAL'
    return metadata

"""Expected metadata string without title."""
@pytest.fixture
def metadata_str_exc_title():
    return '2025.01.001.1080p.x265.BluRay.DUAL'

"""Test __str__ with a basic title."""
def test_media_metadata_str_with_title(base_metadata, metadata_str_exc_title):
    assert str(base_metadata) == 'Title.' + metadata_str_exc_title

"""Test __str__ when title is None."""
def test_media_metadata_str_without_title(base_metadata, metadata_str_exc_title):
    base_metadata.title = None
    assert str(base_metadata) == metadata_str_exc_title

"""Test __str__ when all attributes are None."""
def test_media_metadata_str_all_none():
    metadata = MediaMetadata()
    assert str(metadata) == ''

"""Test __str__ with various title formats."""
@pytest.mark.parametrize("input_title,expected_formatted", [
    ('My MoViEs tEsT TiTlE', 'My.Movies.Test.Title.'),
    ('{[()]}!My {[()]}!MoViE\'s {[()]}!tEsT {[()]}!TiTlE {[()]}!', 'My.Movies.Test.Title.'),
    ('My.MoViEs.tEsT.TiTlE', 'My.Movies.Test.Title.'),
])
def test_media_metadata_str_title_formatting(base_metadata, metadata_str_exc_title, input_title, expected_formatted):
    base_metadata.title = input_title
    assert str(base_metadata) == expected_formatted + metadata_str_exc_title

"""Test _format_title method with various inputs."""
@pytest.mark.parametrize("input_title,expected_formatted", [
    ('My MoViEs tEsT TiTlE', 'My.Movies.Test.Title'),
    ('{[()]}!My {[()]}!MoViE\'s {[()]}!tEsT {[()]}!TiTlE {[()]}!', 'My.Movies.Test.Title'),
    ('My.MoViEs.tEsT.TiTlE', 'My.Movies.Test.Title'),
])
def test_media_metadata_format_title(input_title, expected_formatted):
    metadata = MediaMetadata()
    assert metadata._format_title(input_title) == expected_formatted

"""Test formatting an empty title."""
def test_media_metadata_format_title_empty_string():
    metadata = MediaMetadata()
    assert metadata._format_title('') == ''
