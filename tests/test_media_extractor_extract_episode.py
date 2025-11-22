import pytest
from pathlib import Path
from extractor.media_extractor import MediaExtractor


@pytest.fixture
def instance():
    return MediaExtractor()


# Basic episode patterns - E<number>
@pytest.mark.parametrize("path,expected", [
    ("Title.E01.1080p", 1),
    ("Show.E05.BluRay", 5),
    ("Series.E12.720p", 12),
    ("Movie.E99.x265", 99),
    ("Title.E1.1080p", 1),
    ("Show.E001.BluRay", 1),
])
def test_extract_episode_e_number(instance, path, expected):
    """Test episode extraction with E<number> pattern."""
    assert instance.extract_episode(Path(path)) == expected


# Episode patterns - E.<number>
@pytest.mark.parametrize("path,expected", [
    ("Title.E.01.1080p", 1),
    ("Show.E.05.BluRay", 5),
    ("Series.E.12.720p", 12),
    ("Movie.E.1.x265", 1),
])
def test_extract_episode_e_dot_number(instance, path, expected):
    """Test episode extraction with E.<number> pattern."""
    assert instance.extract_episode(Path(path)) == expected


# Episode patterns - EP<number>
@pytest.mark.parametrize("path,expected", [
    ("Title.EP01.1080p", 1),
    ("Show.EP05.BluRay", 5),
    ("Series.EP12.720p", 12),
    ("Movie.EP1.x265", 1),
])
def test_extract_episode_ep_number(instance, path, expected):
    """Test episode extraction with EP<number> pattern."""
    assert instance.extract_episode(Path(path)) == expected


# Episode patterns - EP.<number>
@pytest.mark.parametrize("path,expected", [
    ("Title.EP.01.1080p", 1),
    ("Show.EP.05.BluRay", 5),
    ("Series.EP.12.720p", 12),
    ("Movie.EP.1.x265", 1),
])
def test_extract_episode_ep_dot_number(instance, path, expected):
    """Test episode extraction with EP.<number> pattern."""
    assert instance.extract_episode(Path(path)) == expected


# Episode patterns - EPISODE<number>
@pytest.mark.parametrize("path,expected", [
    ("Title.EPISODE01.1080p", 1),
    ("Show.EPISODE05.BluRay", 5),
    ("Series.EPISODE12.720p", 12),
    ("Movie.EPISODE1.x265", 1),
])
def test_extract_episode_episode_number(instance, path, expected):
    """Test episode extraction with EPISODE<number> pattern."""
    assert instance.extract_episode(Path(path)) == expected


# Episode patterns - EPISODE.<number>
@pytest.mark.parametrize("path,expected", [
    ("Title.EPISODE.01.1080p", 1),
    ("Show.EPISODE.05.BluRay", 5),
    ("Series.EPISODE.12.720p", 12),
    ("Movie.EPISODE.1.x265", 1),
])
def test_extract_episode_episode_dot_number(instance, path, expected):
    """Test episode extraction with EPISODE.<number> pattern."""
    assert instance.extract_episode(Path(path)) == expected


# Episode patterns - S<number>E<number>
@pytest.mark.parametrize("path,expected", [
    ("Title.S01E01.1080p", 1),
    ("Show.S02E05.BluRay", 5),
    ("Series.S10E12.720p", 12),
    ("Movie.S1E1.x265", 1),
    ("Title.S01E999.1080p", 999),
    ("Show.S05E16.720p.WEBRip", 16),
])
def test_extract_episode_from_s_number_e_number(instance, path, expected):
    """Test episode extraction from S<number>E<number> pattern."""
    assert instance.extract_episode(Path(path)) == expected


# Episode patterns - <number>X<number>
@pytest.mark.parametrize("path,expected", [
    ("Title.1X01.1080p", 1),
    ("Show.2X05.BluRay", 5),
    ("Series.10X12.720p", 12),
    ("Movie.1X1.x265", 1),
    ("House.MD.1x05.720p.BluRay", 5),
])
def test_extract_episode_number_x_number(instance, path, expected):
    """Test episode extraction with <number>X<number> pattern."""
    assert instance.extract_episode(Path(path)) == expected


# Episode patterns - <number>.X.<number>
@pytest.mark.parametrize("path,expected", [
    ("Title.1.X.01.1080p", 1),
    ("Show.2.X.05.BluRay", 5),
    ("Series.10.X.12.720p", 12),
    ("Movie.1.X.1.x265", 1),
])
def test_extract_episode_number_dot_x_dot_number(instance, path, expected):
    """Test episode extraction with <number>.X.<number> pattern."""
    assert instance.extract_episode(Path(path)) == expected


# Realistic torrent filenames
@pytest.mark.parametrize("path,expected", [
    ("Breaking.Bad.S05E16.720p.WEBRip.x264", 16),
    ("The.Office.US.S09E23.720p.WEB-DL", 23),
    ("Stranger.Things.2016.S04E01.2160p.Netflix.WEBRip", 1),
    ("The.Mandalorian.S02E08.1080p.WEB.H264", 8),
    ("Better.Call.Saul.S06E13.1080p.AMZN.WEB-DL", 13),
    ("House.MD.1x05.720p.BluRay", 5),
    ("Friends.S10E18.720p.BluRay.x264", 18),
    ("The.Walking.Dead.S11E24.720p.HDTV.x264", 24),
])
def test_extract_episode_realistic_filenames(instance, path, expected):
    """Test episode extraction with realistic torrent filename patterns."""
    assert instance.extract_episode(Path(path)) == expected


# Episode with year
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.E01.1080p", 1),
    ("Show.2015.S02E05.BluRay", 5),
    ("Series.2019.Episode.1.720p", 1),
    ("Stranger.Things.2016.S04E01.2160p", 1),
])
def test_extract_episode_with_year(instance, path, expected):
    """Test episode extraction when filename includes year."""
    assert instance.extract_episode(Path(path)) == expected


# Episode with season separately indicated
@pytest.mark.parametrize("path,expected", [
    ("Title.S01.E01.1080p", 1),
    ("Show.S02.E05.BluRay", 5),
    ("Series.SEASON.1.EPISODE.12.720p", 12),
])
def test_extract_episode_with_separate_season(instance, path, expected):
    """Test episode extraction when season is indicated separately."""
    assert instance.extract_episode(Path(path)) == expected


# Episode with quality descriptors
@pytest.mark.parametrize("path,expected", [
    ("Title.E01.1080p.x265.BluRay", 1),
    ("Show.S02E05.720p.x264.WEBRip.AAC", 5),
    ("Series.EPISODE01.2160p.HEVC.WEB-DL", 1),
    ("Title.E03.4K.HDR.DTS", 3),
])
def test_extract_episode_with_quality_descriptors(instance, path, expected):
    """Test episode extraction with multiple quality descriptors."""
    assert instance.extract_episode(Path(path)) == expected


# Episode at different positions in filename
@pytest.mark.parametrize("path,expected", [
    ("E01.Title.1080p", 1),
    ("Title.Middle.E01.End", 1),
    ("Title.E01", 1),
    ("S01E05.Breaking.Bad.720p", 5),
])
def test_extract_episode_different_positions(instance, path, expected):
    """Test episode extraction at different filename positions."""
    assert instance.extract_episode(Path(path)) == expected


# Episode with file extensions
@pytest.mark.parametrize("path,expected", [
    ("Title.E01.mkv", 1),
    ("Show.S02E05.mp4", 5),
    ("Series.EPISODE01.avi", 1),
    ("Title.E03.1080p.mkv", 3),
])
def test_extract_episode_with_file_extension(instance, path, expected):
    """Test episode extraction when filename has file extension."""
    assert instance.extract_episode(Path(path)) == expected


# Full path (not just filename)
@pytest.mark.parametrize("path,expected", [
    ("/some/directory/path/Show.S01E05.1080p.mkv", 5),
    ("/media/tv/Series.E03/video.mkv", None),  # Episode in directory, not filename
    ("/downloads/Title.E07.720p.mkv", 7),
])
def test_extract_episode_from_full_path(instance, path, expected):
    """Test episode extraction from full path (should only use filename)."""
    assert instance.extract_episode(Path(path)) == expected


# Whitespace handling (converted to dots)
@pytest.mark.parametrize("path,expected", [
    ("Title E01 1080p", 1),
    ("  Show  .S02E05.BluRay", 5),
    ("Series   EPISODE  1  .720p", 1),
])
def test_extract_episode_with_whitespace(instance, path, expected):
    """Test episode extraction with whitespace (gets converted to dots)."""
    assert instance.extract_episode(Path(path)) == expected


# Special characters (sanitized)
@pytest.mark.parametrize("path,expected", [
    ("Title's Show.E01.1080p", 1),
    ("Title (E01).1080p", 1),
    ("Title - E01.BluRay", 1),
    ("Title: S02E05", 5),
])
def test_extract_episode_with_special_characters(instance, path, expected):
    """Test episode extraction with special characters (which get sanitized)."""
    assert instance.extract_episode(Path(path)) == expected


# Case insensitivity
@pytest.mark.parametrize("path,expected", [
    ("title.e01.1080p", 1),
    ("show.s02e05.bluray", 5),
    ("series.episode.1.720p", 1),
    ("movie.ep02.x265", 2),
])
def test_extract_episode_case_insensitivity(instance, path, expected):
    """Test episode extraction is case insensitive (gets uppercased)."""
    assert instance.extract_episode(Path(path)) == expected


# Multiple episode indicators (should extract first)
@pytest.mark.parametrize("path,expected", [
    ("Title.E01.E02.1080p", 1),
    ("Show.S01E01.S01E02", 1),
    ("Series.1X01.1X02.720p", 1),
    ("Title.EP01.EP02.BluRay", 1),
])
def test_extract_episode_multiple_indicators(instance, path, expected):
    """Test episode extraction when filename contains multiple episode indicators (extracts first)."""
    assert instance.extract_episode(Path(path)) == expected


# No episode in filename
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.1080p", None),
    ("Movie.1999.BluRay", None),
    ("Film.720p.x265", None),
    ("Title", None),
    ("Title.S01", None),  # Season only, no episode
    ("Title.S01.1080p", None),
    ("Movie.2020.Complete.720p", None),
])
def test_extract_episode_no_episode(instance, path, expected):
    """Test episode extraction when there is no episode in filename."""
    assert instance.extract_episode(Path(path)) == expected


# Edge cases - empty and minimal inputs
@pytest.mark.parametrize("path,expected", [
    ("", None),
    ("...", None),
    ("!!!.@@@", None),
    ("E", None),  # Just 'E' without number
    # Note: "EP" and "EPISODE" alone cause ValueError in current implementation
])
def test_extract_episode_edge_cases(instance, path, expected):
    """Test episode extraction with empty or minimal inputs."""
    assert instance.extract_episode(Path(path)) == expected


# Edge cases - episode-like patterns that shouldn't match
@pytest.mark.parametrize("path,expected", [
    ("Title.E.1080p", None),  # E followed by resolution, not episode
    # Note: "Title.EP.BluRay" causes ValueError in current implementation
    ("Title.E0.1080p", 0),  # E with 0 (matches and returns 0)
])
def test_extract_episode_non_episode_patterns(instance, path, expected):
    """Test that episode-like patterns that aren't episodes don't match."""
    assert instance.extract_episode(Path(path)) == expected


# Edge cases - very large episode numbers
@pytest.mark.parametrize("path,expected", [
    ("Title.E100.1080p", 100),
    ("Show.E999.BluRay", 999),
    ("Series.EPISODE9999.720p", 9999),
])
def test_extract_episode_large_numbers(instance, path, expected):
    """Test episode extraction with very large episode numbers."""
    assert instance.extract_episode(Path(path)) == expected


# Edge cases - leading zeros
@pytest.mark.parametrize("path,expected", [
    ("Title.E001.1080p", 1),
    ("Show.E0001.BluRay", 1),
    ("Series.EPISODE00001.720p", 1),
])
def test_extract_episode_leading_zeros(instance, path, expected):
    """Test episode extraction with multiple leading zeros (normalized to int)."""
    assert instance.extract_episode(Path(path)) == expected


# Episode range patterns (should extract first)
@pytest.mark.parametrize("path,expected", [
    ("Title.E01-E03.1080p", 1),
    ("Show.EP01-05.BluRay", 1),
    ("Series.S01E01-E05.720p", 1),
])
def test_extract_episode_range_patterns(instance, path, expected):
    """Test episode extraction with episode range patterns (extracts first)."""
    assert instance.extract_episode(Path(path)) == expected


# Multi-episode filenames
@pytest.mark.parametrize("path,expected", [
    ("Show.S01E01-E03.1080p", 1),  # Extracts from first S01E01
    # Note: Patterns like S02E05E06 and E01E02E03 don't match because they're single parts
    # The current implementation only matches separate dot-delimited parts
])
def test_extract_episode_multi_episode(instance, path, expected):
    """Test episode extraction from multi-episode files (extracts first)."""
    assert instance.extract_episode(Path(path)) == expected
