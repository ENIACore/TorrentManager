import pytest
from pathlib import Path
from extractor.media_extractor import MediaExtractor

"""
TODO - Functionality of extraction needs to be expanded to include common static classifiers
"""


@pytest.fixture
def instance():
    return MediaExtractor()


# Year followed by quality descriptor (resolution)
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.1080p", 2020),
    ("Movie.1984.720p", 1984),
    ("Show.2024.4K", 2024),
    ("Film.2015.2160p", 2015),
    ("Series.2019.8K", 2019),
    ("Movie.2010.480p", 2010),
])
def test_extract_year_followed_by_resolution(instance, path, expected):
    """Test year extraction when year is followed by resolution descriptor."""
    assert instance.extract_year(Path(path)) == expected


# Year followed by quality descriptor (codec)
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.x265", 2020),
    ("Movie.1999.x264", 1999),
    ("Film.2018.HEVC", 2018),
    ("Show.2021.H264", 2021),
    ("Series.2017.AV1", 2017),
])
def test_extract_year_followed_by_codec(instance, path, expected):
    """Test year extraction when year is followed by codec descriptor."""
    assert instance.extract_year(Path(path)) == expected


# Year followed by quality descriptor (source)
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.BluRay", 2020),
    ("Movie.2015.WEBRip", 2015),
    ("Show.2019.WEB-DL", 2019),
    ("Film.2021.DVDRip", 2021),
    ("Series.2018.HDTV", 2018),
])
def test_extract_year_followed_by_source(instance, path, expected):
    """Test year extraction when year is followed by source descriptor."""
    assert instance.extract_year(Path(path)) == expected


# Year followed by quality descriptor (audio)
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.DTS", 2020),
    ("Movie.2015.AAC", 2015),
    ("Show.2019.AC3", 2019),
    ("Film.2021.TrueHD", 2021),
    ("Series.2018.EAC3", 2018),
])
def test_extract_year_followed_by_audio(instance, path, expected):
    """Test year extraction when year is followed by audio descriptor."""
    assert instance.extract_year(Path(path)) == expected


# Year followed by multiple quality descriptors
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.1080p.x265.BluRay.DTS", 2020),
    ("Movie.1999.720p.x264.WEBRip.AAC", 1999),
    ("Show.2015.2160p.HEVC.BluRay.TrueHD", 2015),
    ("Film.2018.4K.x265.WEB-DL.AC3", 2018),
])
def test_extract_year_followed_by_multiple_quality_descriptors(instance, path, expected):
    """Test year extraction when year is followed by multiple quality descriptors."""
    assert instance.extract_year(Path(path)) == expected


# Year followed by season/episode patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.S01", 2020),
    ("Show.2024.S01E01", 2024),
    ("Series.2019.Season.1", 2019),
    ("Movie.2020.S02E05", 2020),
    ("Show.2015.S.01", 2015),
    ("Series.2021.SEA01", 2021),
    ("Show.2018.SEASON01", 2018),
])
def test_extract_year_followed_by_season(instance, path, expected):
    """Test year extraction when year is followed by season/episode pattern."""
    assert instance.extract_year(Path(path)) == expected


# Year followed by episode only (no season)
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.E01", 2020),
    ("Movie.2015.E05", 2015),
    ("Show.2019.Episode.1", 2019),
])
def test_extract_year_followed_by_episode(instance, path, expected):
    """Test year extraction when year is followed by episode pattern."""
    assert instance.extract_year(Path(path)) == expected


# Year at end of filename (terminator is end of parts)
@pytest.mark.parametrize("path,expected", [
    ("Title.2020", 2020),
    ("Movie.1984", 1984),
    ("Show.2024", 2024),
    ("The.Matrix.1999", 1999),
    ("Great.Film.2010", 2010),
])
def test_extract_year_at_end(instance, path, expected):
    """Test year extraction when year is at the end (terminator is end of filename)."""
    assert instance.extract_year(Path(path)) == expected


# Year followed by file extension
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.mkv", 2020),
    ("Movie.1999.mp4", 1999),
    ("Film.2018.avi", 2018),
    ("Show.2021.webm", 2021),
    ("Series.2015.mov", 2015),
])
def test_extract_year_followed_by_extension(instance, path, expected):
    """Test year extraction when year is followed by file extension."""
    assert instance.extract_year(Path(path)) == expected


# Year NOT followed by terminator (should return None - year is part of title)
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.Part2.1080p", None),
    ("Movie.1984.Remastered.BluRay", None),
    ("Show.2024.Extended.4K", None),
    ("Film.2020.Directors.Cut.x265", None),
    ("Series.2019.Special.Edition.WEBRip", None),
    ("Movie.2015.Unrated.720p", None),
    ("Title.2020.REPACK.1080p", None),
])
def test_extract_year_not_followed_by_terminator(instance, path, expected):
    """Test year extraction when year is NOT followed by terminator (year is part of title)."""
    assert instance.extract_year(Path(path)) == expected


# No year in filename (should return None)
@pytest.mark.parametrize("path,expected", [
    ("Title.1080p", None),
    ("My.Movie.720p", None),
    ("Show.4K", None),
    ("Film.x265", None),
    ("Series.BluRay", None),
    ("Movie.WEBRip", None),
    ("Title.DTS", None),
    ("Show.S01E01", None),
    ("Movie.Season.1", None),
    ("Title", None),
    ("My.Movie", None),
])
def test_extract_year_no_year(instance, path, expected):
    """Test year extraction when there is no year in filename."""
    assert instance.extract_year(Path(path)) == expected


# Multiple years in filename (should extract the one before terminator)
@pytest.mark.parametrize("path,expected", [
    ("2001.A.Space.Odyssey.1968.1080p", 1968),
    ("1984.2023.Remake.720p", None),  # 2023 not followed by terminator
    ("2012.2009.BluRay", 2009),
    ("1917.2019.4K.BluRay", 2019),
    ("2001.1968.S01", 1968),
])
def test_extract_year_multiple_years(instance, path, expected):
    """Test year extraction when filename contains multiple valid years."""
    assert instance.extract_year(Path(path)) == expected


# Invalid years (year-like numbers that don't meet criteria)
@pytest.mark.parametrize("path,expected", [
    ("Title.1800.BluRay", None),  # 1800 not valid year (<=1900)
    ("Movie.3000.1080p", None),  # 3000 not valid year (future)
    ("Show.1234.S01", None),  # 1234 not valid year
    ("Film.1900.720p", None),  # 1900 not valid year (<=1900)
    ("Series.999.BluRay", None),  # 999 not valid year
    ("Movie.12345.1080p", None),  # Not 4 digits
])
def test_extract_year_invalid_years(instance, path, expected):
    """Test year extraction with year-like numbers that aren't valid years."""
    assert instance.extract_year(Path(path)) == expected


# Edge case: Year boundary values
@pytest.mark.parametrize("path,expected", [
    ("Title.1901.BluRay", 1901),  # First valid year (1900 < year)
    ("Movie.2025.1080p", 2025),  # Current year should be valid
])
def test_extract_year_boundary_values(instance, path, expected):
    """Test year extraction with boundary year values."""
    assert instance.extract_year(Path(path)) == expected


# Realistic torrent filenames
@pytest.mark.parametrize("path,expected", [
    ("The.Matrix.1999.1080p.BluRay.x265", 1999),
    ("Breaking.Bad.S05E16.720p.WEBRip.x264", None),  # No year
    ("Inception.2010.2160p.4K.UHD.BluRay.x265", 2010),
    ("Game.of.Thrones.S01.Complete.1080p", None),  # No year
    ("Interstellar.2014.Directors.Cut.1080p.BluRay", None),  # 2014 not followed by terminator
    ("The.Office.US.S09E23.720p.WEB-DL", None),  # No year
    ("Avatar.2009.Extended.Edition.1080p.x265", None),  # 2009 not followed by terminator
    ("Stranger.Things.2016.S04.2160p.Netflix.WEBRip", 2016),
])
def test_extract_year_realistic_filenames(instance, path, expected):
    """Test year extraction with realistic torrent filename patterns."""
    assert instance.extract_year(Path(path)) == expected


# Full path (not just filename)
def test_extract_year_full_path(instance):
    """Test year extraction from full path (should only use filename)."""
    path = Path("/some/directory/path/Movie.2020.1080p.mkv")
    assert instance.extract_year(path) == 2020


# Whitespace handling
@pytest.mark.parametrize("path,expected", [
    ("Title 2020 1080p", 2020),
    ("  Title  .2020.BluRay", 2020),
    ("Movie   2015  .720p", 2015),
])
def test_extract_year_whitespace(instance, path, expected):
    """Test year extraction with whitespace (gets converted to dots)."""
    assert instance.extract_year(Path(path)) == expected


# Special characters (sanitized)
@pytest.mark.parametrize("path,expected", [
    ("Title's Movie.2020.1080p", 2020),
    ("Title (2020).1080p", 2020),  # Year from (2020) becomes part of title after sanitization
    ("Title - Subtitle.2020.BluRay", 2020),
    ("Title: The Beginning.2020.720p", 2020),
])
def test_extract_year_special_characters(instance, path, expected):
    """Test year extraction with special characters (which get sanitized)."""
    assert instance.extract_year(Path(path)) == expected


# Edge case: Empty and minimal inputs
@pytest.mark.parametrize("path,expected", [
    ("", None),  # Empty string
    ("...", None),  # Only dots
    ("!!!.@@@", None),  # Only special chars
])
def test_extract_year_empty_inputs(instance, path, expected):
    """Test year extraction with empty or minimal inputs."""
    assert instance.extract_year(Path(path)) == expected


# Edge case: Only quality descriptors (no title, no year)
@pytest.mark.parametrize("path,expected", [
    ("1080p", None),
    ("BluRay", None),
    ("x265", None),
    ("S01E01", None),
])
def test_extract_year_only_descriptors(instance, path, expected):
    """Test year extraction when filename starts with quality/season descriptor."""
    assert instance.extract_year(Path(path)) == expected

# Year with title containing numbers
@pytest.mark.parametrize("path,expected", [
    ("Title123.2020.1080p", 2020),
    ("007.Skyfall.2012.BluRay", 2012),
    ("Apollo.13.1995.720p", 1995),
    ("District.9.2009.1080p", 2009),
])
def test_extract_year_title_with_numbers(instance, path, expected):
    """Test year extraction when title contains numbers."""
    assert instance.extract_year(Path(path)) == expected


# Year followed by season and quality
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.S01.1080p", 2020),
    ("Show.2019.S01E01.720p.BluRay", 2019),
    ("Series.2021.Season.1.4K", 2021),
])
def test_extract_year_with_season_and_quality(instance, path, expected):
    """Test year extraction when year is followed by both season and quality."""
    assert instance.extract_year(Path(path)) == expected


# Edge case: Year in middle not preceded by title only
# (According to docs: "If the year is not preceded only by the title it will not be assumed the year")
# However, the implementation doesn't seem to check what comes before, only after
# These tests document current behavior
@pytest.mark.parametrize("path,expected", [
    ("1080p.2020.BluRay", None),  # Year after quality descriptor
    ("S01.2020.720p", None),  # Year after season
    ("BluRay.2020", None),  # Year after quality at end
])
def test_extract_year_not_preceded_by_title(instance, path, expected):
    """Test year extraction when year is not preceded by title."""
    assert instance.extract_year(Path(path)) == expected


# Common torrent edge cases
@pytest.mark.parametrize("path,expected", [
    ("Show.2020.S01.Complete.720p", 2020),
    ("Movie.2020.1080p.BluRay.DUAL", 2020),
    ("Title.2020.PROPER.1080p", None),  # 2020 not followed by terminator
    ("Movie.2015.REPACK", None),  # 2015 not followed by terminator
    ("Film.2018.mkv", 2018),
])
def test_extract_year_torrent_edge_cases(instance, path, expected):
    """Test year extraction with common edge cases found in torrents."""
    assert instance.extract_year(Path(path)) == expected
