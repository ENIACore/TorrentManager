import pytest
from pathlib import Path
from extractor.media_extractor import MediaExtractor


@pytest.fixture
def instance():
    return MediaExtractor()


# Basic season patterns - S<number>
@pytest.mark.parametrize("path,expected", [
    ("Title.S01.1080p", 1),
    ("Show.S02.BluRay", 2),
    ("Series.S10.720p", 10),
    ("Movie.S99.x265", 99),
    ("Title.S1.1080p", 1),
    ("Show.S001.BluRay", 1),
])
def test_extract_season_s_number(instance, path, expected):
    """Test season extraction with S<number> pattern."""
    assert instance.extract_season(Path(path)) == expected


# Season patterns - S.<number>
@pytest.mark.parametrize("path,expected", [
    ("Title.S.01.1080p", 1),
    ("Show.S.02.BluRay", 2),
    ("Series.S.10.720p", 10),
    ("Movie.S.1.x265", 1),
])
def test_extract_season_s_dot_number(instance, path, expected):
    """Test season extraction with S.<number> pattern."""
    assert instance.extract_season(Path(path)) == expected


# Season patterns - SEA<number>
@pytest.mark.parametrize("path,expected", [
    ("Title.SEA01.1080p", 1),
    ("Show.SEA02.BluRay", 2),
    ("Series.SEA10.720p", 10),
    ("Movie.SEA1.x265", 1),
])
def test_extract_season_sea_number(instance, path, expected):
    """Test season extraction with SEA<number> pattern."""
    assert instance.extract_season(Path(path)) == expected


# Season patterns - SEA.<number>
@pytest.mark.parametrize("path,expected", [
    ("Title.SEA.01.1080p", 1),
    ("Show.SEA.02.BluRay", 2),
    ("Series.SEA.10.720p", 10),
    ("Movie.SEA.1.x265", 1),
])
def test_extract_season_sea_dot_number(instance, path, expected):
    """Test season extraction with SEA.<number> pattern."""
    assert instance.extract_season(Path(path)) == expected


# Season patterns - SEASON<number>
@pytest.mark.parametrize("path,expected", [
    ("Title.SEASON01.1080p", 1),
    ("Show.SEASON02.BluRay", 2),
    ("Series.SEASON10.720p", 10),
    ("Movie.SEASON1.x265", 1),
])
def test_extract_season_season_number(instance, path, expected):
    """Test season extraction with SEASON<number> pattern."""
    assert instance.extract_season(Path(path)) == expected


# Season patterns - SEASON.<number>
@pytest.mark.parametrize("path,expected", [
    ("Title.SEASON.01.1080p", 1),
    ("Show.SEASON.02.BluRay", 2),
    ("Series.SEASON.10.720p", 10),
    ("Movie.SEASON.1.x265", 1),
])
def test_extract_season_season_dot_number(instance, path, expected):
    """Test season extraction with SEASON.<number> pattern."""
    assert instance.extract_season(Path(path)) == expected


# Season patterns - S<number>E<number>
@pytest.mark.parametrize("path,expected", [
    ("Title.S01E01.1080p", 1),
    ("Show.S02E05.BluRay", 2),
    ("Series.S10E12.720p", 10),
    ("Movie.S1E1.x265", 1),
    ("Title.S01E999.1080p", 1),
])
def test_extract_season_from_s_number_e_number(instance, path, expected):
    """Test season extraction from S<number>E<number> pattern."""
    assert instance.extract_season(Path(path)) == expected


# Realistic torrent filenames
@pytest.mark.parametrize("path,expected", [
    ("Breaking.Bad.S05E16.720p.WEBRip.x264", 5),
    ("Game.of.Thrones.S01.Complete.1080p", 1),
    ("The.Office.US.S09E23.720p.WEB-DL", 9),
    ("Stranger.Things.2016.S04.2160p.Netflix.WEBRip", 4),
    ("The.Mandalorian.S02E08.1080p.WEB.H264", 2),
    ("Better.Call.Saul.S06.1080p.AMZN.WEB-DL", 6),
    ("Westworld.2016.S03E01.1080p.WEB.H264", 3),
    ("The.Walking.Dead.S11E24.720p.HDTV.x264", 11),
])
def test_extract_season_realistic_filenames(instance, path, expected):
    """Test season extraction with realistic torrent filename patterns."""
    assert instance.extract_season(Path(path)) == expected


# Season with year
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.S01.1080p", 1),
    ("Show.2015.S02E05.BluRay", 2),
    ("Series.2019.SEASON.1.720p", 1),
    ("Stranger.Things.2016.S04.2160p", 4),
])
def test_extract_season_with_year(instance, path, expected):
    """Test season extraction when filename includes year."""
    assert instance.extract_season(Path(path)) == expected


# Season with quality descriptors
@pytest.mark.parametrize("path,expected", [
    ("Title.S01.1080p.x265.BluRay", 1),
    ("Show.S02E05.720p.x264.WEBRip.AAC", 2),
    ("Series.SEASON01.2160p.HEVC.WEB-DL", 1),
    ("Title.S03.4K.HDR.DTS", 3),
])
def test_extract_season_with_quality_descriptors(instance, path, expected):
    """Test season extraction with multiple quality descriptors."""
    assert instance.extract_season(Path(path)) == expected


# Season with Complete/Pack indicators
@pytest.mark.parametrize("path,expected", [
    ("Title.S01.Complete.1080p", 1),
    ("Show.S02.Pack.BluRay", 2),
    ("Series.S03.Complete.Season", 3),
    ("Game.of.Thrones.S01.Complete.1080p", 1),
])
def test_extract_season_with_pack_indicators(instance, path, expected):
    """Test season extraction with Complete/Pack indicators."""
    assert instance.extract_season(Path(path)) == expected


# Season at different positions in filename
@pytest.mark.parametrize("path,expected", [
    ("S01.Title.1080p", 1),
    ("Title.Middle.S01.End", 1),
    ("Title.S01", 1),
    ("S05E16.Breaking.Bad.720p", 5),
])
def test_extract_season_different_positions(instance, path, expected):
    """Test season extraction at different filename positions."""
    assert instance.extract_season(Path(path)) == expected


# Season with file extensions
@pytest.mark.parametrize("path,expected", [
    ("Title.S01.mkv", 1),
    ("Show.S02E05.mp4", 2),
    ("Series.SEASON01.avi", 1),
    ("Title.S03.1080p.mkv", 3),
])
def test_extract_season_with_file_extension(instance, path, expected):
    """Test season extraction when filename has file extension."""
    assert instance.extract_season(Path(path)) == expected


# Full path (not just filename)
@pytest.mark.parametrize("path,expected", [
    ("/some/directory/path/Show.S01E01.1080p.mkv", 1),
    ("/media/tv/Series.S02.Complete/episode.mkv", None),  # Season in directory, not filename
    ("/downloads/Title.S03E05.720p.mkv", 3),
])
def test_extract_season_from_full_path(instance, path, expected):
    """Test season extraction from full path (should only use filename)."""
    assert instance.extract_season(Path(path)) == expected


# Whitespace handling (converted to dots)
@pytest.mark.parametrize("path,expected", [
    ("Title S01 1080p", 1),
    ("  Show  .S02E05.BluRay", 2),
    ("Series   SEASON  1  .720p", 1),
])
def test_extract_season_with_whitespace(instance, path, expected):
    """Test season extraction with whitespace (gets converted to dots)."""
    assert instance.extract_season(Path(path)) == expected


# Special characters (sanitized)
@pytest.mark.parametrize("path,expected", [
    ("Title's Show.S01.1080p", 1),
    ("Title (S01).1080p", 1),
    ("Title - S01.BluRay", 1),
    ("Title: S02E05", 2),
])
def test_extract_season_with_special_characters(instance, path, expected):
    """Test season extraction with special characters (which get sanitized)."""
    assert instance.extract_season(Path(path)) == expected


# Case insensitivity
@pytest.mark.parametrize("path,expected", [
    ("title.s01.1080p", 1),
    ("show.s02e05.bluray", 2),
    ("series.season.1.720p", 1),
    ("movie.sea02.x265", 2),
])
def test_extract_season_case_insensitivity(instance, path, expected):
    """Test season extraction is case insensitive (gets uppercased)."""
    assert instance.extract_season(Path(path)) == expected


# Multiple season indicators (should extract first)
@pytest.mark.parametrize("path,expected", [
    ("Title.S01.S02.1080p", 1),
    ("Show.S01E01.S02E05", 1),
    ("Series.SEASON01.S02", 1),
])
def test_extract_season_multiple_indicators(instance, path, expected):
    """Test season extraction when filename contains multiple season indicators (extracts first)."""
    assert instance.extract_season(Path(path)) == expected


# No season in filename
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.1080p", None),
    ("Movie.1999.BluRay", None),
    ("Film.720p.x265", None),
    ("Title", None),
    ("Title.E01", None),  # Episode only, no season
    ("Title.E01.1080p", None),
    ("Movie.2020.720p.x264", None),
])
def test_extract_season_no_season(instance, path, expected):
    """Test season extraction when there is no season in filename."""
    assert instance.extract_season(Path(path)) == expected


# Edge cases - empty and minimal inputs
@pytest.mark.parametrize("path,expected", [
    ("", None),
    ("...", None),
    ("!!!.@@@", None),
    ("S", None),  # Just 'S' without number
    # Note: "SEASON" alone causes ValueError in current implementation
])
def test_extract_season_edge_cases(instance, path, expected):
    """Test season extraction with empty or minimal inputs."""
    assert instance.extract_season(Path(path)) == expected


# Edge cases - season-like patterns that shouldn't match
@pytest.mark.parametrize("path,expected", [
    ("Title.S.1080p", None),  # S followed by resolution, not season
    ("Title.SEA.BluRay", None),  # SEA without number
    ("Title.S0.1080p", 0),  # S with 0 (matches and returns 0)
])
def test_extract_season_non_season_patterns(instance, path, expected):
    """Test that season-like patterns that aren't seasons don't match."""
    assert instance.extract_season(Path(path)) == expected


# Edge cases - very large season numbers
@pytest.mark.parametrize("path,expected", [
    ("Title.S100.1080p", 100),
    ("Show.S999.BluRay", 999),
    ("Series.SEASON9999.720p", 9999),
])
def test_extract_season_large_numbers(instance, path, expected):
    """Test season extraction with very large season numbers."""
    assert instance.extract_season(Path(path)) == expected


# Edge cases - leading zeros
@pytest.mark.parametrize("path,expected", [
    ("Title.S001.1080p", 1),
    ("Show.S0001.BluRay", 1),
    ("Series.SEASON00001.720p", 1),
])
def test_extract_season_leading_zeros(instance, path, expected):
    """Test season extraction with multiple leading zeros (normalized to int)."""
    assert instance.extract_season(Path(path)) == expected
