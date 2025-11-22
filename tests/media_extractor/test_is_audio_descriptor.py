import pytest
from extractor.media_extractor import MediaExtractor


@pytest.fixture
def instance():
    return MediaExtractor()


# Atmos audio tests
@pytest.mark.parametrize("parts,index", [
    (["MY", "MOVIE", "ATMOS", "X265"], 2),
    (["ATMOS", "CONTENT"], 0),
    (["TITLE", "DOLBY", "ATMOS", "BLURAY"], 1),
    (["TITLE", "DOLBY", "ATMOS", "BLURAY"], 1),
    (["TITLE", "DOLBYATMOS", "BLURAY"], 1),
])
def test_is_audio_descriptor_atmos(instance, parts, index):
    """Test that Atmos audio patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# DTS-X audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "DTSX", "BLURAY"], 1),
    (["TITLE", "DTS", "X", "BLURAY"], 1),
])
def test_is_audio_descriptor_dtsx(instance, parts, index):
    """Test that DTS-X audio patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# DTS-HD audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "DTS", "HD", "MA", "BLURAY"], 1),
    (["TITLE", "DTS", "HD", "MA", "BLURAY"], 1),
    (["TITLE", "DTSHD", "MA", "BLURAY"], 1),
    (["TITLE", "DTSHD", "MA", "BLURAY"], 1),
    (["TITLE", "DTS", "HD", "BLURAY"], 1),
    (["TITLE", "DTSHD", "BLURAY"], 1),
])
def test_is_audio_descriptor_dts_hd(instance, parts, index):
    """Test that DTS-HD audio patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# DTS-MA audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "DTS", "MA", "BLURAY"], 1),
    (["TITLE", "DTSMA", "BLURAY"], 1),
    (["TITLE", "DTS", "MA", "BLURAY"], 1),
])
def test_is_audio_descriptor_dts_ma(instance, parts, index):
    """Test that DTS-MA audio patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# DTS-ES audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "DTS", "ES", "BLURAY"], 1),
    (["TITLE", "DTSES", "BLURAY"], 1),
    (["TITLE", "DTS", "ES", "BLURAY"], 1),
])
def test_is_audio_descriptor_dts_es(instance, parts, index):
    """Test that DTS-ES audio patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# DTS audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "DTS", "BLURAY"], 1),
    (["MY", "MOVIE", "DTS", "X265"], 2),
])
def test_is_audio_descriptor_dts(instance, parts, index):
    """Test that DTS audio patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# TrueHD audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "TRUEHD", "BLURAY"], 1),
    (["TITLE", "TRUE", "HD", "BLURAY"], 1),
    (["TITLE", "TRUE", "HD", "BLURAY"], 1),
])
def test_is_audio_descriptor_truehd(instance, parts, index):
    """Test that TrueHD audio patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# DD+ (Dolby Digital Plus) audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "DD", "WEBRIP"], 1),
    (["TITLE", "DDP", "WEBRIP"], 1),
    (["TITLE", "E", "AC", "3", "WEBRIP"], 1),
    (["TITLE", "E", "AC", "3", "WEBRIP"], 1),
    (["TITLE", "EAC3", "WEBRIP"], 1),
    (["TITLE", "DD", "PLUS", "WEBRIP"], 1),
    (["TITLE", "DD", "PLUS", "WEBRIP"], 1),
    (["TITLE", "DDPLUS", "WEBRIP"], 1),
])
def test_is_audio_descriptor_dd_plus(instance, parts, index):
    """Test that DD+ audio patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# DD (Dolby Digital) audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "DD", "BLURAY"], 1),
    (["TITLE", "AC3", "BLURAY"], 1),
    (["TITLE", "DOLBY", "DIGITAL", "BLURAY"], 1),
    (["TITLE", "DOLBY", "DIGITAL", "BLURAY"], 1),
    (["TITLE", "DOLBYDIGITAL", "BLURAY"], 1),
])
def test_is_audio_descriptor_dd(instance, parts, index):
    """Test that DD audio patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# AAC audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "AAC", "WEBRIP"], 1),
    (["TITLE", "HE", "AAC", "WEBRIP"], 1),
    (["TITLE", "HEAAC", "WEBRIP"], 1),
    (["TITLE", "HE", "AAC", "WEBRIP"], 1),
])
def test_is_audio_descriptor_aac(instance, parts, index):
    """Test that AAC audio patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# FLAC audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "FLAC", "BLURAY"], 1),
    (["CONCERT", "FLAC", "REMUX"], 1),
])
def test_is_audio_descriptor_flac(instance, parts, index):
    """Test that FLAC audio patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# MP3 audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "MP3", "WEBRIP"], 1),
    (["OLD", "MOVIE", "MP3", "DVDRIP"], 2),
])
def test_is_audio_descriptor_mp3(instance, parts, index):
    """Test that MP3 audio patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# LPCM audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "LPCM", "BLURAY"], 1),
    (["TITLE", "PCM", "BLURAY"], 1),
])
def test_is_audio_descriptor_lpcm(instance, parts, index):
    """Test that LPCM audio patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# OGG audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "OGG", "WEBRIP"], 1),
    (["TITLE", "VORBIS", "WEBRIP"], 1),
])
def test_is_audio_descriptor_ogg(instance, parts, index):
    """Test that OGG audio patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# OPUS audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "OPUS", "WEBRIP"], 1),
])
def test_is_audio_descriptor_opus(instance, parts, index):
    """Test that OPUS audio patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# 5.1 channel audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "5", "1", "BLURAY"], 1),
    (["TITLE", "5", "1", "BLURAY"], 1),
    (["TITLE", "51", "BLURAY"], 1),
    (["TITLE", "6CH", "BLURAY"], 1),
])
def test_is_audio_descriptor_5_1(instance, parts, index):
    """Test that 5.1 channel patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# 7.1 channel audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "7", "1", "BLURAY"], 1),
    (["TITLE", "7", "1", "BLURAY"], 1),
    (["TITLE", "71", "BLURAY"], 1),
    (["TITLE", "8CH", "BLURAY"], 1),
])
def test_is_audio_descriptor_7_1(instance, parts, index):
    """Test that 7.1 channel patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# 2.0 stereo audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "2", "0", "WEBRIP"], 1),
    (["TITLE", "2", "0", "WEBRIP"], 1),
    (["TITLE", "20", "WEBRIP"], 1),
    (["TITLE", "STEREO", "WEBRIP"], 1),
    (["TITLE", "2CH", "WEBRIP"], 1),
])
def test_is_audio_descriptor_2_0(instance, parts, index):
    """Test that 2.0 stereo patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# DUAL audio tests
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "DUAL", "AUDIO", "BLURAY"], 1),
    (["TITLE", "DUAL", "BLURAY"], 1),
])
def test_is_audio_descriptor_dual(instance, parts, index):
    """Test that DUAL audio patterns are correctly identified."""
    assert instance._is_audio_descriptor(index, parts) is not None


# Invalid audio descriptors
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "2020", "BLURAY"], 1),  # Year, not audio
    (["TITLE", "X265", "BLURAY"], 1),  # Codec, not audio
    (["TITLE", "1080P", "BLURAY"], 1),  # Resolution, not audio
    (["TITLE", "BLURAY", "X265"], 1),  # Quality, not audio
    (["TITLE", "S01", "E01"], 1),  # Season, not audio
    (["TITLE", "AUDIO", "BLURAY"], 1),  # Generic term, not specific
    (["TITLE", "SOUND", "BLURAY"], 1),  # Generic term
    (["TITLE", "MONO", "BLURAY"], 1),  # Not in patterns
    (["TITLE", "QUAD", "BLURAY"], 1),  # Not in patterns
    (["TITLE", "3D", "BLURAY"], 1),  # Video feature, not audio
])
def test_is_audio_descriptor_invalid(instance, parts, index):
    """Test that non-audio patterns return False."""
    assert instance._is_audio_descriptor(index, parts) is None


# Edge cases - different positions
def test_is_audio_descriptor_at_beginning(instance):
    """Test audio at the beginning of parts list."""
    parts = ["ATMOS", "MY", "MOVIE", "BLURAY"]
    assert instance._is_audio_descriptor(0, parts) is not None


def test_is_audio_descriptor_at_end(instance):
    """Test audio at the end of parts list."""
    parts = ["MY", "MOVIE", "BLURAY", "ATMOS"]
    assert instance._is_audio_descriptor(3, parts) is not None


def test_is_audio_descriptor_single_element(instance):
    """Test audio as the only element."""
    parts = ["DTS"]
    assert instance._is_audio_descriptor(0, parts) is not None


# Edge cases - index boundaries
def test_is_audio_descriptor_index_out_of_bounds(instance):
    """Test that index beyond parts length returns False."""
    parts = ["MY", "MOVIE", "DTS"]
    assert instance._is_audio_descriptor(10, parts) is None


def test_is_audio_descriptor_negative_index(instance):
    """Test behavior with negative index."""
    parts = ["MY", "MOVIE", "DTS"]
    result = instance._is_audio_descriptor(-1, parts)
    assert isinstance(result, (str, type(None)))


# Multi-part audio patterns (with dots)
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "DOLBY", "ATMOS", "BLURAY"], 1),
    (["TITLE", "DTS", "X", "BLURAY"], 1),
    (["TITLE", "DTS", "HD", "MA", "BLURAY"], 1),
    (["TITLE", "DTS", "MA", "BLURAY"], 1),
    (["TITLE", "DTS", "ES", "BLURAY"], 1),
    (["TITLE", "TRUE", "HD", "BLURAY"], 1),
    (["TITLE", "DD", "PLUS", "WEBRIP"], 1),
    (["TITLE", "DOLBY", "DIGITAL", "BLURAY"], 1),
    (["TITLE", "HE", "AAC", "WEBRIP"], 1),
    (["TITLE", "5", "1", "BLURAY"], 1),
    (["TITLE", "7", "1", "BLURAY"], 1),
    (["TITLE", "2", "0", "WEBRIP"], 1),
    (["TITLE", "DUAL", "AUDIO", "BLURAY"], 1),
    (["TITLE", "E", "AC", "3", "WEBRIP"], 1),
])
def test_is_audio_descriptor_multipart_patterns(instance, parts, index):
    """Test audio patterns that span multiple parts with dots."""
    assert instance._is_audio_descriptor(index, parts) is not None


# Common torrent filename scenarios
@pytest.mark.parametrize("parts,index", [
    (["MOVIE", "NAME", "2020", "1080P", "BLURAY", "ATMOS", "X265"], 5),
    (["TV", "SHOW", "S01E01", "720P", "WEBRIP", "AAC", "X264"], 5),
    (["DOCUMENTARY", "4K", "WEB", "DL", "DTS", "HD", "MA", "X265"], 4),
    (["ANIME", "MOVIE", "1080P", "BDRIP", "DUAL", "AAC", "X264"], 4),
    (["CONCERT", "2023", "UHD", "REMUX", "FLAC", "2", "0"], 4),
    (["OLD", "MOVIE", "1995", "DVDRIP", "AC3", "XVID"], 4),
])
def test_is_audio_descriptor_realistic_filenames(instance, parts, index):
    """Test audio detection in realistic torrent filename patterns."""
    assert instance._is_audio_descriptor(index, parts) is not None


# Empty and minimal inputs
def test_is_audio_descriptor_empty_parts(instance):
    """Test with empty parts list."""
    assert instance._is_audio_descriptor(0, []) is None


def test_is_audio_descriptor_empty_string_part(instance):
    """Test with empty string in parts."""
    parts = ["TITLE", "", "DTS"]
    assert instance._is_audio_descriptor(1, parts) is None


# Multiple audio descriptors in same filename
def test_is_audio_descriptor_multiple_audio(instance):
    """Test filename with multiple audio patterns (e.g., Atmos with 7.1)."""
    parts = ["MOVIE", "ATMOS", "7", "1", "BLURAY"]
    assert instance._is_audio_descriptor(1, parts) is not None
    assert instance._is_audio_descriptor(2, parts) is not None


# Complex audio combinations
@pytest.mark.parametrize("parts,index", [
    (["MOVIE", "DTS", "HD", "MA", "7", "1", "ATMOS"], 1),  # DTS-HD
    (["MOVIE", "DTS", "HD", "MA", "7", "1", "ATMOS"], 4),  # 7.1
    (["MOVIE", "DTS", "HD", "MA", "7", "1", "ATMOS"], 6),  # Atmos
    (["MOVIE", "TRUEHD", "ATMOS", "7", "1", "X265"], 1),  # TrueHD
    (["MOVIE", "TRUEHD", "ATMOS", "7", "1", "X265"], 2),  # Atmos
    (["MOVIE", "TRUEHD", "ATMOS", "7", "1", "X265"], 3),  # 7.1
])
def test_is_audio_descriptor_complex_combinations(instance, parts, index):
    """Test complex audio combinations found in high-quality releases."""
    assert instance._is_audio_descriptor(index, parts) is not None
