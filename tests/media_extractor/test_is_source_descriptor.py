import pytest
from extractor.media_extractor import MediaExtractor


@pytest.fixture
def instance():
    return MediaExtractor()


# REMUX source tests
@pytest.mark.parametrize("parts,index", [
    (["MY", "MOVIE", "REMUX", "X265"], 2),
    (["REMUX", "CONTENT"], 0),
    (["TITLE", "REMUX", "2160P"], 1),
])
def test_is_source_descriptor_remux(instance, parts, index):
    """Test that REMUX source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# BluRay source tests
@pytest.mark.parametrize("parts,index", [
    (["MY", "MOVIE", "BLURAY", "X265"], 2),
    (["TITLE", "BDRIP", "1080P"], 1),
    (["TITLE", "BD", "RIP", "1080P"], 1),
    (["TITLE", "BDRIP", "1080P"], 1),
    (["TITLE", "BR", "RIP", "1080P"], 1),
    (["TITLE", "BRRIP", "720P"], 1),
    (["TITLE", "BDMV", "REMUX"], 1),
    (["TITLE", "BDISO", "REMUX"], 1),
    (["TITLE", "BD25", "REMUX"], 1),
    (["TITLE", "BD50", "REMUX"], 1),
    (["TITLE", "BD66", "REMUX"], 1),
    (["TITLE", "BD100", "REMUX"], 1),
])
def test_is_source_descriptor_bluray(instance, parts, index):
    """Test that BluRay source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# WEB-DL source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "WEB", "DL", "1080P"], 1),
    (["TITLE", "WEBDL", "1080P"], 1),
    (["TITLE", "WEB", "DL", "720P"], 1),
])
def test_is_source_descriptor_webdl(instance, parts, index):
    """Test that WEB-DL source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# WEBRip source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "WEBRIP", "1080P"], 1),
    (["TITLE", "WEB", "RIP", "1080P"], 1),
    (["TITLE", "WEB", "RIP", "720P"], 1),
])
def test_is_source_descriptor_webrip(instance, parts, index):
    """Test that WEBRip source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# WEB source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "WEB", "1080P"], 1),
    (["SHOW", "S01E01", "WEB", "X264"], 2),
])
def test_is_source_descriptor_web(instance, parts, index):
    """Test that WEB source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# HDRip source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "HDRIP", "720P"], 1),
    (["TITLE", "HD", "RIP", "720P"], 1),
])
def test_is_source_descriptor_hdrip(instance, parts, index):
    """Test that HDRip source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# DVDRip source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "DVDRIP", "XVID"], 1),
    (["TITLE", "DVD", "RIP", "XVID"], 1),
])
def test_is_source_descriptor_dvdrip(instance, parts, index):
    """Test that DVDRip source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# DVD source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "DVD", "XVID"], 1),
    (["TITLE", "DVDSCR", "XVID"], 1),
    (["TITLE", "DVD5", "REMUX"], 1),
    (["TITLE", "DVD9", "REMUX"], 1),
])
def test_is_source_descriptor_dvd(instance, parts, index):
    """Test that DVD source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# HDTV source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "HDTV", "720P"], 1),
    (["TITLE", "HDTVRIP", "720P"], 1),
    (["TITLE", "DTTV", "720P"], 1),
    (["TITLE", "PDTV", "720P"], 1),
    (["TITLE", "SDTV", "480P"], 1),
    (["TITLE", "LDTV", "360P"], 1),
])
def test_is_source_descriptor_hdtv(instance, parts, index):
    """Test that HDTV source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# TELECINE source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "TELECINE", "XVID"], 1),
    (["TITLE", "TC", "XVID"], 1),
])
def test_is_source_descriptor_telecine(instance, parts, index):
    """Test that TELECINE source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# TELESYNC source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "TELESYNC", "XVID"], 1),
    (["TITLE", "TS", "XVID"], 1),
])
def test_is_source_descriptor_telesync(instance, parts, index):
    """Test that TELESYNC source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# SCREENER source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "SCREENER", "XVID"], 1),
    (["TITLE", "SCR", "XVID"], 1),
    (["TITLE", "DVDSCR", "XVID"], 1),
    (["TITLE", "BDSCR", "X264"], 1),
])
def test_is_source_descriptor_screener(instance, parts, index):
    """Test that SCREENER source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# CAM source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "CAMRIP", "XVID"], 1),
    (["TITLE", "CAM", "XVID"], 1),
    (["TITLE", "HDCAM", "X264"], 1),
])
def test_is_source_descriptor_cam(instance, parts, index):
    """Test that CAM source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# WORKPRINT source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "WORKPRINT", "XVID"], 1),
    (["TITLE", "WP", "XVID"], 1),
])
def test_is_source_descriptor_workprint(instance, parts, index):
    """Test that WORKPRINT source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# PPV source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "PPV", "720P"], 1),
    (["TITLE", "PPVRIP", "720P"], 1),
])
def test_is_source_descriptor_ppv(instance, parts, index):
    """Test that PPV source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# VODRip source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "VODRIP", "720P"], 1),
    (["TITLE", "VOD", "720P"], 1),
])
def test_is_source_descriptor_vodrip(instance, parts, index):
    """Test that VODRip source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# HC source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "HC", "XVID"], 1),
    (["TITLE", "HCHDCAM", "X264"], 1),
])
def test_is_source_descriptor_hc(instance, parts, index):
    """Test that HC source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# LINE source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "LINE", "XVID"], 1),
])
def test_is_source_descriptor_line(instance, parts, index):
    """Test that LINE source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# HDTS source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "HDTS", "X264"], 1),
    (["TITLE", "HD", "TS", "X264"], 1),
])
def test_is_source_descriptor_hdts(instance, parts, index):
    """Test that HDTS source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# HDTC source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "HDTC", "X264"], 1),
    (["TITLE", "HD", "TC", "X264"], 1),
])
def test_is_source_descriptor_hdtc(instance, parts, index):
    """Test that HDTC source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# TVRip source tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "TVRIP", "XVID"], 1),
    (["TITLE", "SATRIP", "XVID"], 1),
    (["TITLE", "DTTVRIP", "XVID"], 1),
])
def test_is_source_descriptor_tvrip(instance, parts, index):
    """Test that TVRip source patterns are correctly identified."""
    assert instance._is_source_descriptor(index, parts) is not None


# Invalid source descriptors
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "2020", "1080P"], 1),  # Year, not source
    (["TITLE", "X265", "1080P"], 1),  # Codec, not source
    (["TITLE", "1080P", "X265"], 1),  # Resolution, not source
    (["TITLE", "S01", "E01"], 1),  # Season, not source
    (["TITLE", "DTS", "X265"], 1),  # Audio, not source
    (["TITLE", "STREAM", "1080P"], 1),  # Generic term
    (["TITLE", "ONLINE", "1080P"], 1),  # Generic term
    (["TITLE", "NETFLIX", "1080P"], 1),  # Platform, not source quality
    (["TITLE", "HULU", "1080P"], 1),  # Platform, not source quality
])
def test_is_source_descriptor_invalid(instance, parts, index):
    """Test that non-source patterns return False."""
    assert instance._is_source_descriptor(index, parts) is None


# Edge cases - different positions
def test_is_source_descriptor_at_beginning(instance):
    """Test source at the beginning of parts list."""
    parts = ["BLURAY", "MY", "MOVIE", "X265"]
    assert instance._is_source_descriptor(0, parts) is not None


def test_is_source_descriptor_at_end(instance):
    """Test source at the end of parts list."""
    parts = ["MY", "MOVIE", "X265", "BLURAY"]
    assert instance._is_source_descriptor(3, parts) is not None


def test_is_source_descriptor_single_element(instance):
    """Test source as the only element."""
    parts = ["BLURAY"]
    assert instance._is_source_descriptor(0, parts) is not None


# Edge cases - index boundaries
def test_is_source_descriptor_index_out_of_bounds(instance):
    """Test that index beyond parts length returns False."""
    parts = ["MY", "MOVIE", "BLURAY"]
    assert instance._is_source_descriptor(10, parts) is None


def test_is_source_descriptor_negative_index(instance):
    """Test behavior with negative index."""
    parts = ["MY", "MOVIE", "BLURAY"]
    result = instance._is_source_descriptor(-1, parts)
    assert isinstance(result, (str, type(None)))


# Multi-part source patterns (with dots)
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "WEB", "DL", "1080P"], 1),
    (["TITLE", "WEB", "RIP", "720P"], 1),
    (["TITLE", "BD", "RIP", "1080P"], 1),
    (["TITLE", "BR", "RIP", "1080P"], 1),
    (["TITLE", "HD", "RIP", "720P"], 1),
    (["TITLE", "DVD", "RIP", "XVID"], 1),
    (["TITLE", "HD", "TS", "X264"], 1),
    (["TITLE", "HD", "TC", "X264"], 1),
])
def test_is_source_descriptor_multipart_patterns(instance, parts, index):
    """Test source patterns that span multiple parts with dots."""
    assert instance._is_source_descriptor(index, parts) is not None


# Common torrent filename scenarios
@pytest.mark.parametrize("parts,index", [
    (["MOVIE", "NAME", "2020", "1080P", "BLURAY", "X265"], 4),
    (["TV", "SHOW", "S01E01", "720P", "WEBRIP", "X264"], 4),
    (["DOCUMENTARY", "4K", "WEB", "DL", "2160P", "X265"], 2),
    (["ANIME", "MOVIE", "1080P", "BDRIP", "X264"], 3),
    (["CONCERT", "2023", "UHD", "REMUX", "BLURAY"], 3),
    (["OLD", "MOVIE", "1995", "DVDRIP", "XVID"], 3),
])
def test_is_source_descriptor_realistic_filenames(instance, parts, index):
    """Test source detection in realistic torrent filename patterns."""
    assert instance._is_source_descriptor(index, parts) is not None


# Empty and minimal inputs
def test_is_source_descriptor_empty_parts(instance):
    """Test with empty parts list."""
    assert instance._is_source_descriptor(0, []) is None


def test_is_source_descriptor_empty_string_part(instance):
    """Test with empty string in parts."""
    parts = ["TITLE", "", "BLURAY"]
    assert instance._is_source_descriptor(1, parts) is None


# Multiple sources in same filename (uncommon but possible for re-encodes)
def test_is_source_descriptor_multiple_sources(instance):
    """Test filename with multiple source patterns."""
    parts = ["MOVIE", "HDTV", "TO", "BLURAY", "CONVERSION"]
    assert instance._is_source_descriptor(1, parts) is not None
    assert instance._is_source_descriptor(3, parts) is not None


# Ambiguous cases - WEB vs WEB-DL vs WEBRip
def test_is_source_descriptor_web_variants(instance):
    """Test that different WEB variants are all detected."""
    assert instance._is_source_descriptor(1, ["TITLE", "WEB", "1080P"]) is not None
    assert instance._is_source_descriptor(1, ["TITLE", "WEB", "DL", "1080P"]) is not None
    assert instance._is_source_descriptor(1, ["TITLE", "WEBRIP", "1080P"]) is not None
