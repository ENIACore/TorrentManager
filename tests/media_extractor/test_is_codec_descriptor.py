import pytest
from extractor.media_extractor import MediaExtractor


@pytest.fixture
def instance():
    return MediaExtractor()


# AV1 codec tests
@pytest.mark.parametrize("parts,index", [
    (["MY", "MOVIE", "AV1", "1080P"], 2),
    (["AV1", "CONTENT"], 0),
    (["TITLE", "SVT", "AV1", "BLURAY"], 1),
    (["TITLE", "SVTAV1", "BLURAY"], 1),
    (["TITLE", "AOV1", "BLURAY"], 1),
])
def test_is_codec_descriptor_av1(instance, parts, index):
    """Test that AV1 codec patterns are correctly identified."""
    assert instance._is_codec_descriptor(index, parts) is not None


# VP9 codec tests
@pytest.mark.parametrize("parts,index", [
    (["MY", "MOVIE", "VP9", "1080P"], 2),
    (["TITLE", "VP9", "WEBRIP"], 1),
])
def test_is_codec_descriptor_vp9(instance, parts, index):
    """Test that VP9 codec patterns are correctly identified."""
    assert instance._is_codec_descriptor(index, parts) is not None


# VP8 codec tests
@pytest.mark.parametrize("parts,index", [
    (["MY", "MOVIE", "VP8", "720P"], 2),
    (["TITLE", "VP8", "WEBRIP"], 1),
])
def test_is_codec_descriptor_vp8(instance, parts, index):
    """Test that VP8 codec patterns are correctly identified."""
    assert instance._is_codec_descriptor(index, parts) is not None


# x265/HEVC codec tests
@pytest.mark.parametrize("parts,index", [
    (["MY", "MOVIE", "X265", "1080P"], 2),
    (["TITLE", "X", "265", "BLURAY"], 1),
    (["TITLE", "H265", "BLURAY"], 1),
    (["TITLE", "H", "265", "BLURAY"], 1),
    (["TITLE", "HEVC", "BLURAY"], 1),
    (["TITLE", "HEVC10", "BLURAY"], 1),
    (["TITLE", "HEVC10BIT", "BLURAY"], 1),
    (["TITLE", "H265P", "BLURAY"], 1),
])
def test_is_codec_descriptor_x265(instance, parts, index):
    """Test that x265/HEVC codec patterns are correctly identified."""
    assert instance._is_codec_descriptor(index, parts) is not None


# x264/AVC codec tests
@pytest.mark.parametrize("parts,index", [
    (["MY", "MOVIE", "X264", "1080P"], 2),
    (["TITLE", "X", "264", "BLURAY"], 1),
    (["TITLE", "H264", "BLURAY"], 1),
    (["TITLE", "H", "264", "BLURAY"], 1),
    (["TITLE", "AVC", "BLURAY"], 1),
    (["TITLE", "AVC1", "BLURAY"], 1),
    (["TITLE", "H264P", "BLURAY"], 1),
])
def test_is_codec_descriptor_x264(instance, parts, index):
    """Test that x264/AVC codec patterns are correctly identified."""
    assert instance._is_codec_descriptor(index, parts) is not None


# x263 codec tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "X263", "BLURAY"], 1),
    (["TITLE", "X", "263", "BLURAY"], 1),
    (["TITLE", "H263", "BLURAY"], 1),
    (["TITLE", "H", "263", "BLURAY"], 1),
])
def test_is_codec_descriptor_x263(instance, parts, index):
    """Test that x263 codec patterns are correctly identified."""
    assert instance._is_codec_descriptor(index, parts) is not None


# XVID codec tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "XVID", "DVDRIP"], 1),
    (["TITLE", "XVID", "AF", "DVDRIP"], 1),
])
def test_is_codec_descriptor_xvid(instance, parts, index):
    """Test that XVID codec patterns are correctly identified."""
    assert instance._is_codec_descriptor(index, parts) is not None


# DIVX codec tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "DIVX", "DVDRIP"], 1),
    (["TITLE", "DIV3", "DVDRIP"], 1),
    (["TITLE", "DIVX6", "DVDRIP"], 1),
])
def test_is_codec_descriptor_divx(instance, parts, index):
    """Test that DIVX codec patterns are correctly identified."""
    assert instance._is_codec_descriptor(index, parts) is not None


# MPEG4 codec tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "MPEG", "4", "DVDRIP"], 1),
    (["TITLE", "MPEG4", "DVDRIP"], 1),
    (["TITLE", "MP4V", "DVDRIP"], 1),
])
def test_is_codec_descriptor_mpeg4(instance, parts, index):
    """Test that MPEG4 codec patterns are correctly identified."""
    assert instance._is_codec_descriptor(index, parts) is not None


# MPEG2 codec tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "MPEG", "2", "DVD"], 1),
    (["TITLE", "MPEG2", "DVD"], 1),
    (["TITLE", "MP2V", "DVD"], 1),
])
def test_is_codec_descriptor_mpeg2(instance, parts, index):
    """Test that MPEG2 codec patterns are correctly identified."""
    assert instance._is_codec_descriptor(index, parts) is not None


# MPEG1 codec tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "MPEG", "1", "DVD"], 1),
    (["TITLE", "MPEG1", "DVD"], 1),
    (["TITLE", "MP1V", "DVD"], 1),
])
def test_is_codec_descriptor_mpeg1(instance, parts, index):
    """Test that MPEG1 codec patterns are correctly identified."""
    assert instance._is_codec_descriptor(index, parts) is not None


# VC1 codec tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "VC", "1", "BLURAY"], 1),
    (["TITLE", "VC1", "BLURAY"], 1),
    (["TITLE", "WMV3", "BLURAY"], 1),
    (["TITLE", "WVC1", "BLURAY"], 1),
])
def test_is_codec_descriptor_vc1(instance, parts, index):
    """Test that VC1 codec patterns are correctly identified."""
    assert instance._is_codec_descriptor(index, parts) is not None


# THEORA codec tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "THEORA", "WEBRIP"], 1),
])
def test_is_codec_descriptor_theora(instance, parts, index):
    """Test that THEORA codec patterns are correctly identified."""
    assert instance._is_codec_descriptor(index, parts) is not None


# PRORES codec tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "PRORES", "REMUX"], 1),
    (["TITLE", "PRORES422", "REMUX"], 1),
    (["TITLE", "PRORES4444", "REMUX"], 1),
    (["TITLE", "PRORES422HQ", "REMUX"], 1),
])
def test_is_codec_descriptor_prores(instance, parts, index):
    """Test that PRORES codec patterns are correctly identified."""
    assert instance._is_codec_descriptor(index, parts) is not None


# DNxHD codec tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "DNXHD", "REMUX"], 1),
    (["TITLE", "DNXHR", "REMUX"], 1),
])
def test_is_codec_descriptor_dnxhd(instance, parts, index):
    """Test that DNxHD codec patterns are correctly identified."""
    assert instance._is_codec_descriptor(index, parts) is not None


# Invalid codec descriptors
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "2020", "BLURAY"], 1),  # Year, not codec
    (["TITLE", "1080P", "BLURAY"], 1),  # Resolution, not codec
    (["TITLE", "BLURAY", "X265"], 1),  # Quality, not codec
    (["TITLE", "S01", "E01"], 1),  # Season, not codec
    (["TITLE", "DTS", "BLURAY"], 1),  # Audio, not codec
    (["TITLE", "X266", "BLURAY"], 1),  # Non-existent codec
    (["TITLE", "H266", "BLURAY"], 1),  # Not yet a standard codec pattern
    (["TITLE", "VP7", "BLURAY"], 1),  # Non-existent codec
    (["TITLE", "123", "BLURAY"], 1),  # Random number
    (["TITLE", "HD", "BLURAY"], 1),  # Generic descriptor
])
def test_is_codec_descriptor_invalid(instance, parts, index):
    """Test that non-codec patterns return False."""
    assert instance._is_codec_descriptor(index, parts) is None


# Edge cases - different positions
def test_is_codec_descriptor_at_beginning(instance):
    """Test codec at the beginning of parts list."""
    parts = ["X265", "MY", "MOVIE", "BLURAY"]
    assert instance._is_codec_descriptor(0, parts) is not None


def test_is_codec_descriptor_at_end(instance):
    """Test codec at the end of parts list."""
    parts = ["MY", "MOVIE", "BLURAY", "X265"]
    assert instance._is_codec_descriptor(3, parts) is not None


def test_is_codec_descriptor_single_element(instance):
    """Test codec as the only element."""
    parts = ["X265"]
    assert instance._is_codec_descriptor(0, parts) is not None


# Edge cases - index boundaries
def test_is_codec_descriptor_index_out_of_bounds(instance):
    """Test that index beyond parts length returns False."""
    parts = ["MY", "MOVIE", "X265"]
    assert instance._is_codec_descriptor(10, parts) is None


def test_is_codec_descriptor_negative_index(instance):
    """Test behavior with negative index."""
    parts = ["MY", "MOVIE", "X265"]
    result = instance._is_codec_descriptor(-1, parts)
    assert isinstance(result, (str, type(None)))


# Multi-part codec patterns (with dots)
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "X", "265", "BLURAY"], 1),
    (["TITLE", "H", "264", "BLURAY"], 1),
    (["TITLE", "H", "265", "BLURAY"], 1),
    (["TITLE", "VC", "1", "BLURAY"], 1),
    (["TITLE", "MPEG", "4", "DVDRIP"], 1),
    (["TITLE", "MPEG", "2", "DVD"], 1),
    (["TITLE", "XVID", "AF", "DVDRIP"], 1),
    (["TITLE", "SVT", "AV1", "BLURAY"], 1),
])
def test_is_codec_descriptor_multipart_patterns(instance, parts, index):
    """Test codec patterns that span multiple parts with dots."""
    assert instance._is_codec_descriptor(index, parts) is not None


# Common torrent filename scenarios
@pytest.mark.parametrize("parts,index", [
    (["MOVIE", "NAME", "2020", "1080P", "BLURAY", "X265"], 5),
    (["TV", "SHOW", "S01E01", "720P", "X264", "WEBRIP"], 4),
    (["DOCUMENTARY", "4K", "HDR", "2160P", "HEVC", "REMUX"], 4),
    (["ANIME", "MOVIE", "1080P", "X264", "DUAL", "BLURAY"], 3),
    (["CONCERT", "2023", "UHD", "AV1", "BLURAY"], 3),
    (["OLD", "MOVIE", "1995", "XVID", "DVDRIP"], 3),
])
def test_is_codec_descriptor_realistic_filenames(instance, parts, index):
    """Test codec detection in realistic torrent filename patterns."""
    assert instance._is_codec_descriptor(index, parts) is not None


# Empty and minimal inputs
def test_is_codec_descriptor_empty_parts(instance):
    """Test with empty parts list."""
    assert instance._is_codec_descriptor(0, []) is None


def test_is_codec_descriptor_empty_string_part(instance):
    """Test with empty string in parts."""
    parts = ["TITLE", "", "X265"]
    assert instance._is_codec_descriptor(1, parts) is None


# Multiple codecs in same filename (uncommon but possible)
def test_is_codec_descriptor_multiple_codecs(instance):
    """Test filename with multiple codec patterns."""
    parts = ["MOVIE", "X264", "TO", "X265", "CONVERTED"]
    assert instance._is_codec_descriptor(1, parts) is not None
    assert instance._is_codec_descriptor(3, parts) is not None
