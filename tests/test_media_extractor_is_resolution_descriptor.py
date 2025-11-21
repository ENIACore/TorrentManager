import pytest
from extractor.media_extractor import MediaExtractor


@pytest.fixture
def instance():
    return MediaExtractor()


# 8K resolution tests
@pytest.mark.parametrize("parts,index", [
    (["MY", "MOVIE", "8K", "X265"], 2),
    (["8K", "CONTENT"], 0),
    (["TITLE", "4320", "BLURAY"], 1),
    (["TITLE", "4320P", "BLURAY"], 1),
    (["TITLE", "4320I", "BLURAY"], 1),
    (["TITLE", "7680X4320", "BLURAY"], 1),
    (["TITLE", "FULLUHD", "BLURAY"], 1),
])
def test_is_resolution_descriptor_8k(instance, parts, index):
    """Test that 8K resolution patterns are correctly identified."""
    assert instance._is_resolution_descriptor(index, parts) is True


# 4K/UHD resolution tests
@pytest.mark.parametrize("parts,index", [
    (["MY", "MOVIE", "4K", "X265"], 2),
    (["TITLE", "UHD", "BLURAY"], 1),
    (["TITLE", "2160", "BLURAY"], 1),
    (["TITLE", "2160P", "BLURAY"], 1),
    (["TITLE", "2160I", "BLURAY"], 1),
    (["TITLE", "3840X2160", "BLURAY"], 1),
])
def test_is_resolution_descriptor_4k(instance, parts, index):
    """Test that 4K/UHD resolution patterns are correctly identified."""
    assert instance._is_resolution_descriptor(index, parts) is True


# 2K resolution tests
@pytest.mark.parametrize("parts,index", [
    (["MY", "MOVIE", "2K", "X265"], 2),
    (["TITLE", "1440", "BLURAY"], 1),
    (["TITLE", "1440P", "BLURAY"], 1),
    (["TITLE", "1440I", "BLURAY"], 1),
    (["TITLE", "2560X1440", "BLURAY"], 1),
    (["TITLE", "QHD", "BLURAY"], 1),
    (["TITLE", "WQHD", "BLURAY"], 1),
])
def test_is_resolution_descriptor_2k(instance, parts, index):
    """Test that 2K resolution patterns are correctly identified."""
    assert instance._is_resolution_descriptor(index, parts) is True


# 1080p resolution tests
@pytest.mark.parametrize("parts,index", [
    (["MY", "MOVIE", "1080", "X265"], 2),
    (["TITLE", "1080P", "BLURAY"], 1),
    (["TITLE", "1080I", "BLURAY"], 1),
    (["TITLE", "FHD", "BLURAY"], 1),
    (["TITLE", "1920X1080", "BLURAY"], 1),
    (["TITLE", "FULLHD", "BLURAY"], 1),
])
def test_is_resolution_descriptor_1080p(instance, parts, index):
    """Test that 1080p resolution patterns are correctly identified."""
    assert instance._is_resolution_descriptor(index, parts) is True


# 720p resolution tests
@pytest.mark.parametrize("parts,index", [
    (["MY", "MOVIE", "720", "X265"], 2),
    (["TITLE", "720P", "BLURAY"], 1),
    (["TITLE", "720I", "BLURAY"], 1),
    (["TITLE", "1280X720", "BLURAY"], 1),
])
def test_is_resolution_descriptor_720p(instance, parts, index):
    """Test that 720p resolution patterns are correctly identified."""
    assert instance._is_resolution_descriptor(index, parts) is True


# 576p resolution tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "576", "BLURAY"], 1),
    (["TITLE", "576P", "BLURAY"], 1),
    (["TITLE", "576I", "BLURAY"], 1),
    (["TITLE", "PAL", "BLURAY"], 1),
])
def test_is_resolution_descriptor_576p(instance, parts, index):
    """Test that 576p resolution patterns are correctly identified."""
    assert instance._is_resolution_descriptor(index, parts) is True


# 480p resolution tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "480", "BLURAY"], 1),
    (["TITLE", "480P", "BLURAY"], 1),
    (["TITLE", "480I", "BLURAY"], 1),
    (["TITLE", "NTSC", "BLURAY"], 1),
])
def test_is_resolution_descriptor_480p(instance, parts, index):
    """Test that 480p resolution patterns are correctly identified."""
    assert instance._is_resolution_descriptor(index, parts) is True


# 360p resolution tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "360", "BLURAY"], 1),
    (["TITLE", "360P", "BLURAY"], 1),
    (["TITLE", "360I", "BLURAY"], 1),
])
def test_is_resolution_descriptor_360p(instance, parts, index):
    """Test that 360p resolution patterns are correctly identified."""
    assert instance._is_resolution_descriptor(index, parts) is True


# 240p resolution tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "240", "BLURAY"], 1),
    (["TITLE", "240P", "BLURAY"], 1),
    (["TITLE", "240I", "BLURAY"], 1),
])
def test_is_resolution_descriptor_240p(instance, parts, index):
    """Test that 240p resolution patterns are correctly identified."""
    assert instance._is_resolution_descriptor(index, parts) is True


# Invalid resolution descriptors
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "2020", "BLURAY"], 1),  # Year, not resolution
    (["TITLE", "X265", "BLURAY"], 1),  # Codec, not resolution
    (["TITLE", "BLURAY", "X265"], 1),  # Quality, not resolution
    (["TITLE", "S01", "E01"], 1),  # Season, not resolution
    (["TITLE", "DTS", "BLURAY"], 1),  # Audio, not resolution
    (["TITLE", "123", "BLURAY"], 1),  # Random number
    (["TITLE", "HD", "BLURAY"], 1),  # Generic HD, not specific
    (["TITLE", "1080X720", "BLURAY"], 1),  # Invalid resolution format
    (["TITLE", "540P", "BLURAY"], 1),  # Non-standard resolution
    (["TITLE", "900P", "BLURAY"], 1),  # Non-standard resolution
    (["TITLE", "1440X1080", "BLURAY"], 1),  # Invalid resolution format
])
def test_is_resolution_descriptor_invalid(instance, parts, index):
    """Test that non-resolution patterns return False."""
    assert instance._is_resolution_descriptor(index, parts) is False


# Edge cases - different positions
def test_is_resolution_descriptor_at_beginning(instance):
    """Test resolution at the beginning of parts list."""
    parts = ["1080P", "MY", "MOVIE", "BLURAY"]
    assert instance._is_resolution_descriptor(0, parts) is True


def test_is_resolution_descriptor_at_end(instance):
    """Test resolution at the end of parts list."""
    parts = ["MY", "MOVIE", "BLURAY", "1080P"]
    assert instance._is_resolution_descriptor(3, parts) is True


def test_is_resolution_descriptor_single_element(instance):
    """Test resolution as the only element."""
    parts = ["1080P"]
    assert instance._is_resolution_descriptor(0, parts) is True


# Edge cases - index boundaries
def test_is_resolution_descriptor_index_out_of_bounds(instance):
    """Test that index beyond parts length returns False."""
    parts = ["MY", "MOVIE", "1080P"]
    assert instance._is_resolution_descriptor(10, parts) is False


def test_is_resolution_descriptor_negative_index(instance):
    """Test behavior with negative index."""
    # Python allows negative indexing, but the function should handle this gracefully
    parts = ["MY", "MOVIE", "1080P"]
    # This tests current implementation behavior
    result = instance._is_resolution_descriptor(-1, parts)
    # The function will try to combine parts from -1 onward, which may not match
    assert isinstance(result, bool)


# Multi-part resolution patterns
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "1920X1080", "BLURAY"], 1),
    (["TITLE", "3840X2160", "BLURAY"], 1),
    (["TITLE", "7680X4320", "BLURAY"], 1),
    (["TITLE", "2560X1440", "BLURAY"], 1),
    (["TITLE", "1280X720", "BLURAY"], 1),
])
def test_is_resolution_descriptor_dimension_formats(instance, parts, index):
    """Test resolution patterns in WIDTHxHEIGHT format."""
    assert instance._is_resolution_descriptor(index, parts) is True


# Common torrent filename scenarios
@pytest.mark.parametrize("parts,index", [
    (["MOVIE", "NAME", "2020", "1080P", "BLURAY", "X265"], 3),
    (["TV", "SHOW", "S01E01", "720P", "WEBRIP"], 3),
    (["DOCUMENTARY", "4K", "HDR", "2160P", "X265"], 1),
    (["DOCUMENTARY", "4K", "HDR", "2160P", "X265"], 3),
    (["ANIME", "MOVIE", "1080P", "DUAL", "BLURAY"], 2),
    (["CONCERT", "2023", "UHD", "BLURAY"], 2),
])
def test_is_resolution_descriptor_realistic_filenames(instance, parts, index):
    """Test resolution detection in realistic torrent filename patterns."""
    assert instance._is_resolution_descriptor(index, parts) is True


# Empty and minimal inputs
def test_is_resolution_descriptor_empty_parts(instance):
    """Test with empty parts list."""
    assert instance._is_resolution_descriptor(0, []) is False


def test_is_resolution_descriptor_empty_string_part(instance):
    """Test with empty string in parts."""
    parts = ["TITLE", "", "1080P"]
    assert instance._is_resolution_descriptor(1, parts) is False


# Mixed resolution patterns in same filename
def test_is_resolution_descriptor_multiple_resolutions(instance):
    """Test filename with multiple resolution-like patterns."""
    # Some torrents might have upscaled info like "720P.TO.1080P"
    parts = ["MOVIE", "720P", "TO", "1080P", "UPSCALED"]
    assert instance._is_resolution_descriptor(1, parts) is True
    assert instance._is_resolution_descriptor(3, parts) is True
