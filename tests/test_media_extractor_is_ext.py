import pytest
from extractor.media_extractor import MediaExtractor


@pytest.fixture
def instance():
    return MediaExtractor()


# Video extension tests
@pytest.mark.parametrize("parts,index", [
    (["MOVIE", "NAME", "2020", "1080P", "MP4"], 4),
    (["VIDEO", "MKV"], 1),
    (["TITLE", "AVI"], 1),
    (["MOVIE", "MOV"], 1),
    (["VIDEO", "FLV"], 1),
    (["CONTENT", "WMV"], 1),
    (["FILE", "WEBM"], 1),
    (["VIDEO", "M4V"], 1),
    (["STREAM", "TS"], 1),
    (["BLURAY", "M2TS"], 1),
    (["OLD", "MPG"], 1),
    (["OLD", "MPEG"], 1),
    (["DVD", "VOB"], 1),
    (["MOBILE", "3GP"], 1),
    (["WEB", "OGV"], 1),
    (["OLD", "RMVB"], 1),
    (["OLD", "RM"], 1),
    (["OLD", "DIVX"], 1),
    (["FLASH", "F4V"], 1),
])
def test_is_video_ext_valid(instance, parts, index):
    """Test that video extensions are correctly identified."""
    assert instance._is_video_ext(index, parts) is True


# Subtitle extension tests
@pytest.mark.parametrize("parts,index", [
    (["MOVIE", "NAME", "ENGLISH", "SRT"], 3),
    (["SUBTITLE", "ASS"], 1),
    (["SUBS", "SSA"], 1),
    (["CAPTION", "SUB"], 1),
    (["WEB", "VTT"], 1),
    (["YOUTUBE", "SBV"], 1),
    (["DATA", "JSON"], 1),
    (["OLD", "SMI"], 1),
    (["LYRICS", "LRC"], 1),
    (["CAPTION", "PSB"], 1),
    (["DVDSUB", "IDX"], 1),
    (["UNIVERSAL", "USF"], 1),
    (["TIMED", "TTML"], 1),
])
def test_is_subtitle_ext_valid(instance, parts, index):
    """Test that subtitle extensions are correctly identified."""
    assert instance._is_subtitle_ext(index, parts) is True


# Audio extension tests
@pytest.mark.parametrize("parts,index", [
    (["SONG", "NAME", "2020", "MP3"], 3),
    (["AUDIO", "FLAC"], 1),
    (["MUSIC", "AAC"], 1),
    (["PODCAST", "OGG"], 1),
    (["WINDOWS", "WMA"], 1),
    (["APPLE", "M4A"], 1),
    (["VOICE", "OPUS"], 1),
    (["RAW", "WAV"], 1),
    (["LOSSLESS", "APE"], 1),
    (["COMPRESSED", "WV"], 1),
    (["SURROUND", "DTS"], 1),
    (["DOLBY", "AC3"], 1),
    (["MATROSKA", "MKA"], 1),
])
def test_is_audio_ext_valid(instance, parts, index):
    """Test that audio extensions are correctly identified."""
    assert instance._is_audio_ext(index, parts) is True


# _is_ext tests combining all extension types
@pytest.mark.parametrize("parts,index", [
    # Video extensions
    (["MOVIE", "MP4"], 1),
    (["VIDEO", "MKV"], 1),
    (["CLIP", "AVI"], 1),
    # Subtitle extensions
    (["SUBS", "SRT"], 1),
    (["CAPTION", "VTT"], 1),
    (["TEXT", "ASS"], 1),
    # Audio extensions
    (["SONG", "MP3"], 1),
    (["MUSIC", "FLAC"], 1),
    (["AUDIO", "AAC"], 1),
])
def test_is_ext_valid_all_types(instance, parts, index):
    """Test that _is_ext identifies all extension types."""
    assert instance._is_ext(index, parts) is True


# Invalid extension tests
@pytest.mark.parametrize("parts,index", [
    (["MOVIE", "2020", "1080P"], 1),  # Year, not extension
    (["TITLE", "X265", "BLURAY"], 1),  # Codec, not extension
    (["TITLE", "BLURAY", "X265"], 1),  # Quality, not extension
    (["TITLE", "S01", "E01"], 1),  # Season, not extension
    (["TITLE", "DTS", "BLURAY"], 1),  # Audio codec in middle, not extension
    (["TITLE", "TXT"], 1),  # Text file, not media
    (["TITLE", "DOC"], 1),  # Document, not media
    (["TITLE", "PDF"], 1),  # PDF, not media
    (["TITLE", "ZIP"], 1),  # Archive, not media
    (["TITLE", "RAR"], 1),  # Archive, not media
    (["TITLE", "EXE"], 1),  # Executable, not media
])
def test_is_ext_invalid(instance, parts, index):
    """Test that non-extension patterns return False."""
    assert instance._is_ext(index, parts) is False


# Critical test: extensions in middle of filename should NOT match
@pytest.mark.parametrize("parts,index", [
    # Extension-like string in middle, not at end - should NOT match
    (["MKV", "MOVIE", "2020", "1080P"], 0),  # MKV at beginning
    (["MOVIE", "MP4", "REPACK", "2020"], 1),  # MP4 in middle
    (["TITLE", "AVI", "EDITION", "X265", "BLURAY"], 1),  # AVI in middle
    (["SRT", "SUBTITLE", "ENGLISH"], 0),  # SRT at beginning
    (["AUDIO", "MP3", "VERSION", "REMASTER"], 1),  # MP3 in middle
])
def test_is_ext_not_at_tail_returns_false(instance, parts, index):
    """Test that extension strings in middle of filename do NOT match due to tail check."""
    assert instance._is_ext(index, parts) is False


# Test: extensions only match at the tail (end) of parts array
@pytest.mark.parametrize("parts,index", [
    # Extension at the actual end - should match
    (["MKV", "MOVIE", "2020", "MKV"], 3),  # MKV at end (not beginning)
    (["MOVIE", "MP4", "REPACK", "MP4"], 3),  # MP4 at end (not middle)
    (["PREFIX", "AVI", "MIDDLE", "AVI"], 3),  # AVI at end (not in middle)
])
def test_is_ext_only_matches_at_tail(instance, parts, index):
    """Test that extensions only match when at the tail of the parts array."""
    assert instance._is_ext(index, parts) is True


def test_is_video_ext_invalid(instance):
    """Test that non-video extensions return False."""
    assert instance._is_video_ext(1, ["MOVIE", "SRT"]) is False
    assert instance._is_video_ext(1, ["MOVIE", "MP3"]) is False
    assert instance._is_video_ext(1, ["MOVIE", "TXT"]) is False


def test_is_subtitle_ext_invalid(instance):
    """Test that non-subtitle extensions return False."""
    assert instance._is_subtitle_ext(1, ["MOVIE", "MP4"]) is False
    assert instance._is_subtitle_ext(1, ["MOVIE", "MP3"]) is False
    assert instance._is_subtitle_ext(1, ["MOVIE", "TXT"]) is False


def test_is_audio_ext_invalid(instance):
    """Test that non-audio extensions return False."""
    assert instance._is_audio_ext(1, ["MOVIE", "MP4"]) is False
    assert instance._is_audio_ext(1, ["MOVIE", "SRT"]) is False
    assert instance._is_audio_ext(1, ["MOVIE", "TXT"]) is False


# Edge cases - different positions
def test_is_ext_at_beginning(instance):
    """Test extension at the beginning of parts list (only if it's also the only element)."""
    # When extension is at beginning but not the only element, should NOT match
    parts = ["MP4", "MY", "MOVIE", "BLURAY"]
    assert instance._is_ext(0, parts) is False  # Not at tail!


def test_is_ext_at_end(instance):
    """Test extension at the end of parts list."""
    parts = ["MY", "MOVIE", "BLURAY", "MKV"]
    assert instance._is_ext(3, parts) is True


def test_is_ext_single_element(instance):
    """Test extension as the only element (at tail since it's the only part)."""
    parts = ["MP4"]
    assert instance._is_ext(0, parts) is True

def test_is_ext_beginning_is_also_tail(instance):
    """Test that extension at position 0 matches only when it's also the tail."""
    # Single element - position 0 is also the tail
    assert instance._is_ext(0, ["MKV"]) is True

    # Multiple elements - position 0 is NOT the tail
    assert instance._is_ext(0, ["MKV", "MOVIE"]) is False


# Edge cases - index boundaries
def test_is_ext_index_out_of_bounds(instance):
    """Test that index beyond parts length returns False."""
    parts = ["MY", "MOVIE", "MP4"]
    assert instance._is_ext(10, parts) is False


def test_is_video_ext_index_out_of_bounds(instance):
    """Test that index beyond parts length returns False for video ext."""
    parts = ["MY", "MOVIE", "MP4"]
    assert instance._is_video_ext(10, parts) is False


def test_is_subtitle_ext_index_out_of_bounds(instance):
    """Test that index beyond parts length returns False for subtitle ext."""
    parts = ["MY", "MOVIE", "SRT"]
    assert instance._is_subtitle_ext(10, parts) is False


def test_is_audio_ext_index_out_of_bounds(instance):
    """Test that index beyond parts length returns False for audio ext."""
    parts = ["MY", "SONG", "MP3"]
    assert instance._is_audio_ext(10, parts) is False


# Common torrent filename scenarios
@pytest.mark.parametrize("parts,index", [
    (["MOVIE", "NAME", "2020", "1080P", "BLURAY", "X265", "MKV"], 6),
    (["TV", "SHOW", "S01E01", "720P", "WEBRIP", "MP4"], 5),
    (["DOCUMENTARY", "4K", "HDR", "2160P", "X265", "M4V"], 5),
    (["ANIME", "MOVIE", "1080P", "DUAL", "BLURAY", "AVI"], 5),
    (["CONCERT", "2023", "UHD", "BLURAY", "WEBM"], 4),
])
def test_is_ext_realistic_video_filenames(instance, parts, index):
    """Test video extension detection in realistic torrent filename patterns."""
    assert instance._is_ext(index, parts) is True


@pytest.mark.parametrize("parts,index", [
    (["MOVIE", "NAME", "2020", "ENGLISH", "SRT"], 4),
    (["TV", "SHOW", "S01E01", "SPANISH", "ASS"], 4),
    (["ANIME", "JAPANESE", "SSA"], 2),
    (["DOCUMENTARY", "FRENCH", "VTT"], 2),
])
def test_is_ext_realistic_subtitle_filenames(instance, parts, index):
    """Test subtitle extension detection in realistic filename patterns."""
    assert instance._is_ext(index, parts) is True


@pytest.mark.parametrize("parts,index", [
    (["SONG", "ARTIST", "2020", "ALBUM", "MP3"], 4),
    (["SOUNDTRACK", "MOVIE", "LOSSLESS", "FLAC"], 3),
    (["AUDIOBOOK", "CHAPTER", "01", "M4A"], 3),
    (["PODCAST", "EPISODE", "123", "AAC"], 3),
])
def test_is_ext_realistic_audio_filenames(instance, parts, index):
    """Test audio extension detection in realistic filename patterns."""
    assert instance._is_ext(index, parts) is True


# Empty and minimal inputs
def test_is_ext_empty_parts(instance):
    """Test with empty parts list."""
    assert instance._is_ext(0, []) is False


def test_is_video_ext_empty_parts(instance):
    """Test with empty parts list for video ext."""
    assert instance._is_video_ext(0, []) is False


def test_is_subtitle_ext_empty_parts(instance):
    """Test with empty parts list for subtitle ext."""
    assert instance._is_subtitle_ext(0, []) is False


def test_is_audio_ext_empty_parts(instance):
    """Test with empty parts list for audio ext."""
    assert instance._is_audio_ext(0, []) is False


def test_is_ext_empty_string_part(instance):
    """Test with empty string in parts."""
    parts = ["TITLE", "", "MP4"]
    assert instance._is_ext(1, parts) is False


# Case sensitivity tests (all parts should be uppercase per sanitization)
@pytest.mark.parametrize("parts,index", [
    (["MOVIE", "MP4"], 1),
    (["MOVIE", "MKV"], 1),
    (["MOVIE", "AVI"], 1),
])
def test_is_ext_uppercase_only(instance, parts, index):
    """Test that extensions are matched in uppercase (as per sanitization)."""
    assert instance._is_ext(index, parts) is True


# Multiple extension types in same filename (e.g., video with subtitle)
def test_is_ext_multiple_file_types(instance):
    """Test filename patterns with multiple media types referenced."""
    # Video file with subtitle reference in name
    parts = ["MOVIE", "2020", "1080P", "WITH", "SRT", "SUBS", "MKV"]
    assert instance._is_ext(4, parts) is False  # SRT in middle (not at tail)
    assert instance._is_ext(6, parts) is True  # MKV at end


# Ambiguous cases (DTS, AC3 could be audio codec or extension)
def test_is_ext_ambiguous_dts(instance):
    """Test DTS which appears in both audio extensions and audio patterns."""
    parts = ["MOVIE", "DTS"]
    # DTS is in AUDIO_EXTENSIONS, so it should be recognized as an extension
    assert instance._is_audio_ext(1, parts) is True
    assert instance._is_ext(1, parts) is True


def test_is_ext_ambiguous_ac3(instance):
    """Test AC3 which appears in both audio extensions and audio patterns."""
    parts = ["MOVIE", "AC3"]
    # AC3 is in AUDIO_EXTENSIONS, so it should be recognized as an extension
    assert instance._is_audio_ext(1, parts) is True
    assert instance._is_ext(1, parts) is True


def test_is_ext_ambiguous_json(instance):
    """Test JSON which is listed as subtitle extension."""
    parts = ["SUBTITLE", "DATA", "JSON"]
    # JSON is in SUBTITLE_EXTENSIONS
    assert instance._is_subtitle_ext(2, parts) is True
    assert instance._is_ext(2, parts) is True


# All video extension coverage
@pytest.mark.parametrize("ext", [
    'MP4', 'MKV', 'AVI', 'MOV', 'FLV', 'WMV', 'WEBM', 'M4V', 'TS', 'M2TS',
    'MPG', 'MPEG', 'VOB', '3GP', 'OGV', 'RMVB', 'RM', 'DIVX', 'F4V'
])
def test_is_video_ext_all_extensions(instance, ext):
    """Test all video extensions from VIDEO_EXTENSIONS constant."""
    parts = ["MOVIE", ext]
    assert instance._is_video_ext(1, parts) is True


# All subtitle extension coverage
@pytest.mark.parametrize("ext", [
    'SRT', 'ASS', 'SSA', 'SUB', 'VTT', 'SBV', 'JSON', 'SMI', 'LRC',
    'PSB', 'IDX', 'USF', 'TTML'
])
def test_is_subtitle_ext_all_extensions(instance, ext):
    """Test all subtitle extensions from SUBTITLE_EXTENSIONS constant."""
    parts = ["SUBTITLE", ext]
    assert instance._is_subtitle_ext(1, parts) is True


# All audio extension coverage
@pytest.mark.parametrize("ext", [
    'MP3', 'FLAC', 'AAC', 'OGG', 'WMA', 'M4A', 'OPUS', 'WAV',
    'APE', 'WV', 'DTS', 'AC3', 'MKA'
])
def test_is_audio_ext_all_extensions(instance, ext):
    """Test all audio extensions from AUDIO_EXTENSIONS constant."""
    parts = ["AUDIO", ext]
    assert instance._is_audio_ext(1, parts) is True


# Additional tail-matching validation tests
@pytest.mark.parametrize("ext", ['MP4', 'MKV', 'AVI', 'SRT', 'MP3'])
def test_is_ext_only_at_tail_comprehensive(instance, ext):
    """Comprehensive test that extensions only match at the tail, not in middle or beginning."""
    # Should match at tail (last position)
    assert instance._is_ext(2, ["MOVIE", "2020", ext]) is True

    # Should NOT match in middle
    assert instance._is_ext(1, ["MOVIE", ext, "2020"]) is False

    # Should NOT match at beginning (unless it's the only element)
    assert instance._is_ext(0, [ext, "MOVIE", "2020"]) is False

    # Should match at beginning if it's the only element (beginning = tail)
    assert instance._is_ext(0, [ext]) is True


# Test combinations of multiple media types in filename
def test_is_ext_complex_multi_media_filename(instance):
    """Test complex filenames with multiple media-like terms."""
    # Filename: "MP4.CONVERTER.TOOL.OUTPUT.MKV"
    # Should only recognize MKV at the end, not MP4 at beginning
    parts = ["MP4", "CONVERTER", "TOOL", "OUTPUT", "MKV"]

    assert instance._is_ext(0, parts) is False  # MP4 not at tail
    assert instance._is_ext(4, parts) is True   # MKV at tail


# Test that tail matching works with realistic complete filenames
@pytest.mark.parametrize("parts,correct_ext_index", [
    # Format: Movie.Name.2020.1080p.BluRay.x265.mkv
    (["MOVIE", "NAME", "2020", "1080P", "BLURAY", "X265", "MKV"], 6),

    # Format: Show.S01E01.720p.WEB-DL.mp4
    (["SHOW", "S01E01", "720P", "WEB", "DL", "MP4"], 5),

    # Format: Documentary.2023.4K.HDR.avi
    (["DOCUMENTARY", "2023", "4K", "HDR", "AVI"], 4),
])
def test_is_ext_only_last_position_matches(instance, parts, correct_ext_index):
    """Test that in complete realistic filenames, only the last extension position matches."""
    # Only the correct index (tail) should return True
    assert instance._is_ext(correct_ext_index, parts) is True

    # All other indices should return False
    for i in range(len(parts)):
        if i != correct_ext_index:
            assert instance._is_ext(i, parts) is False
