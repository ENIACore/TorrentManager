import pytest
from pathlib import Path
from extractor.media_extractor import MediaExtractor

"""
Needs to be done - Functionality of extract title needs to be expanded to include common words
"""

@pytest.fixture
def instance():
    return MediaExtractor()


# Basic title extraction - no terminators
@pytest.mark.parametrize("path,expected", [
    ("Title", "TITLE"),
    ("My.Movie", "MY.MOVIE"),
    ("The.Great.Show", "THE.GREAT.SHOW"),
    ("Single", "SINGLE"),
    ("Multiple.Word.Title.Here", "MULTIPLE.WORD.TITLE.HERE"),
])
def test_extract_title_no_terminators(instance, path, expected):
    """Test title extraction when there are no terminators."""
    assert instance.extract_title(Path(path)) == expected


# Title with year at end
@pytest.mark.parametrize("path,expected", [
    ("Title.2020", "TITLE"),
    ("Movie.1984", "MOVIE"),
    ("Show.2024", "SHOW"),
    ("The.Matrix.1999", "THE.MATRIX"),
    ("Great.Film.2010", "GREAT.FILM"),
])
def test_extract_title_with_year_at_end(instance, path, expected):
    """Test title extraction when year is at the end (year is terminator)."""
    assert instance.extract_title(Path(path)) == expected


# Title with year followed by quality descriptor
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.1080p", "TITLE"),
    ("Movie.1984.720p", "MOVIE"),
    ("Show.2024.4K", "SHOW"),
    ("Film.2020.x265", "FILM"),
    ("Series.2019.BluRay", "SERIES"),
    ("Movie.2020.WEBRip", "MOVIE"),
    ("Title.2020.DTS", "TITLE"),
    ("Show.2015.2160p.x265.BluRay", "SHOW"),
])
def test_extract_title_with_year_and_quality(instance, path, expected):
    """Test title extraction when year is followed by quality descriptor."""
    assert instance.extract_title(Path(path)) == expected


# Title with year followed by season/episode
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.S01", "TITLE"),
    ("Show.2024.S01E01", "SHOW"),
    ("Series.2019.Season.1", "SERIES"),
    ("Movie.2020.S02E05", "MOVIE"),
    ("Show.2015.S.01", "SHOW"),
])
def test_extract_title_with_year_and_season(instance, path, expected):
    """Test title extraction when year is followed by season/episode."""
    assert instance.extract_title(Path(path)) == expected


# Title with year NOT followed by terminator (year becomes part of title)
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.Part2.1080p", "TITLE.2020.PART2"),
    ("Movie.1984.Remastered.BluRay", "MOVIE.1984.REMASTERED"),
    ("Show.2024.Extended.4K", "SHOW.2024.EXTENDED"),
    ("Film.2020.Directors.Cut.x265", "FILM.2020.DIRECTORS.CUT"),
    ("Series.2019.Special.Edition.WEBRip", "SERIES.2019.SPECIAL.EDITION"),
])
def test_extract_title_year_as_part_of_title(instance, path, expected):
    """Test title extraction when year is not followed by terminator (year is part of title)."""
    assert instance.extract_title(Path(path)) == expected


# Title ending at quality descriptors (no year)
@pytest.mark.parametrize("path,expected", [
    ("Title.1080p", "TITLE"),
    ("My.Movie.720p", "MY.MOVIE"),
    ("Show.4K", "SHOW"),
    ("Film.x265", "FILM"),
    ("Series.BluRay", "SERIES"),
    ("Movie.WEBRip", "MOVIE"),
    ("Title.DTS", "TITLE"),
    ("Show.2160p.x265", "SHOW"),
])
def test_extract_title_ending_at_quality(instance, path, expected):
    """Test title extraction when title ends at quality descriptor (no year)."""
    assert instance.extract_title(Path(path)) == expected


# Title ending at season/episode patterns (no year)
@pytest.mark.parametrize("path,expected", [
    ("Title.S01", "TITLE"),
    ("My.Show.S01E01", "MY.SHOW"),
    ("Series.Season.1", "SERIES"),
    ("Show.S02E05.1080p", "SHOW"),
    ("Title.S.01.BluRay", "TITLE"),
    ("Show.SEA01", "SHOW"),
    ("Series.SEASON01", "SERIES"),
])
def test_extract_title_ending_at_season(instance, path, expected):
    """Test title extraction when title ends at season/episode pattern (no year)."""
    assert instance.extract_title(Path(path)) == expected


# Title ending at file extension
@pytest.mark.parametrize("path,expected", [
    ("Title.mkv", "TITLE"),
    ("My.Movie.mp4", "MY.MOVIE"),
    ("Show.S01E01.avi", "SHOW"),
    ("Film.2020.mkv", "FILM"),
    ("Movie.2020.1080p.mkv", "MOVIE"),
    ("Title.en.srt", "TITLE.EN"),
    ("Show.S01.1080p.mkv", "SHOW"),
])
def test_extract_title_ending_at_extension(instance, path, expected):
    """Test title extraction when title ends at file extension."""
    assert instance.extract_title(Path(path)) == expected


# Complex realistic torrent filenames
@pytest.mark.parametrize("path,expected", [
    ("The.Matrix.1999.1080p.BluRay.x265", "THE.MATRIX"),
    ("Breaking.Bad.S05E16.720p.WEBRip.x264", "BREAKING.BAD"),
    ("Inception.2010.2160p.4K.UHD.BluRay.x265", "INCEPTION"),
    ("Game.of.Thrones.S01.Complete.1080p", "GAME.OF.THRONES"),
    ("Interstellar.2014.Directors.Cut.1080p.BluRay", "INTERSTELLAR.2014.DIRECTORS.CUT"),
    ("The.Office.US.S09E23.720p.WEB-DL", "THE.OFFICE.US"),
    ("Avatar.2009.Extended.Edition.1080p.x265", "AVATAR.2009.EXTENDED.EDITION"),
    ("Stranger.Things.2016.S04.2160p.Netflix.WEBRip", "STRANGER.THINGS"),
])
def test_extract_title_realistic_filenames(instance, path, expected):
    """Test title extraction with realistic torrent filename patterns."""
    assert instance.extract_title(Path(path)) == expected


# Edge case: Multiple years in filename
@pytest.mark.parametrize("path,expected", [
    ("2001.A.Space.Odyssey.1968.1080p", "2001.A.SPACE.ODYSSEY"),
    ("1984.2023.Remake.720p", "1984.2023.REMAKE"),
    ("2012.2009.BluRay", "2012"),
])
def test_extract_title_multiple_years(instance, path, expected):
    """Test title extraction when filename contains multiple valid years."""
    assert instance.extract_title(Path(path)) == expected


# Edge case: Year-like numbers that aren't years
@pytest.mark.parametrize("path,expected", [
    ("Title.1800.BluRay", "TITLE.1800"),  # 1800 not valid year (<=1900)
    ("Movie.3000.1080p", "MOVIE.3000"),  # 3000 not valid year (future)
    ("Show.1234.S01", "SHOW.1234"),  # 1234 not valid year
])
def test_extract_title_invalid_years(instance, path, expected):
    """Test title extraction with year-like numbers that aren't valid years."""
    assert instance.extract_title(Path(path)) == expected


# Edge case: Title with numbers
@pytest.mark.parametrize("path,expected", [
    ("Title123.2020.1080p", "TITLE123"),
    ("007.Skyfall.2012.BluRay", "007.SKYFALL"),
    ("Apollo.13.1995.720p", "APOLLO.13"),
    ("District.9.2009.1080p", "DISTRICT.9"),
])
def test_extract_title_with_numbers(instance, path, expected):
    """Test title extraction when title contains numbers."""
    assert instance.extract_title(Path(path)) == expected


# Edge case: Special characters (sanitized)
@pytest.mark.parametrize("path,expected", [
    ("Title's Movie.2020.1080p", "TITLES.MOVIE"),
    ("Title (2020).1080p", "TITLE"),
    ("Title - Subtitle.2020.BluRay", "TITLE.SUBTITLE"),
    ("Title: The Beginning.2020.720p", "TITLE.THE.BEGINNING"),
    ("Title & Title.2020.1080p", "TITLE.TITLE"),
])
def test_extract_title_special_characters(instance, path, expected):
    """Test title extraction with special characters (which get sanitized)."""
    assert instance.extract_title(Path(path)) == expected


# Edge case: Empty and minimal inputs
@pytest.mark.parametrize("path,expected", [
    ("", ""),  # Empty string
    ("...", ""),  # Only dots
    ("!!!.@@@", ""),  # Only special chars
])
def test_extract_title_empty_inputs(instance, path, expected):
    """Test title extraction with empty or minimal inputs."""
    assert instance.extract_title(Path(path)) == expected


# Edge case: Only quality descriptors (no title)
@pytest.mark.parametrize("path,expected", [
    ("1080p", ""),
    ("BluRay", ""),
    ("x265", ""),
    ("S01E01", ""),
])
def test_extract_title_only_descriptors(instance, path, expected):
    """Test title extraction when filename starts with quality/season descriptor."""
    assert instance.extract_title(Path(path)) == expected


# Edge case: Only year
@pytest.mark.parametrize("path,expected", [
    ("2020", ""),
    ("1999", ""),
    ("2024", ""),
])
def test_extract_title_only_year(instance, path, expected):
    """Test title extraction when filename is only a year."""
    assert instance.extract_title(Path(path)) == expected


# Title with episode only (no season)
@pytest.mark.parametrize("path,expected", [
    ("Title.E01.1080p", "TITLE"),
    ("Movie.E05.BluRay", "MOVIE"),
    ("Show.Episode.1", "SHOW"),
])
def test_extract_title_ending_at_episode(instance, path, expected):
    """Test title extraction when title ends at episode pattern (no season)."""
    assert instance.extract_title(Path(path)) == expected


# Full path (not just filename)
def test_extract_title_full_path(instance):
    """Test title extraction from full path (should only use filename)."""
    path = Path("/some/directory/path/Movie.2020.1080p.mkv")
    assert instance.extract_title(path) == "MOVIE"


# Whitespace handling
@pytest.mark.parametrize("path,expected", [
    ("Title with Spaces.2020.1080p", "TITLE.WITH.SPACES"),
    ("  Title  .2020", "TITLE"),
    ("Title   2020  .BluRay", "TITLE"),
])
def test_extract_title_whitespace(instance, path, expected):
    """Test title extraction with whitespace (gets converted to dots)."""
    assert instance.extract_title(Path(path)) == expected


# Mixed quality descriptors
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.1080p.x265.BluRay.DTS", "TITLE"),
    ("Movie.720p.x264.WEBRip.AAC", "MOVIE"),
    ("Show.S01.1080p.HEVC.BluRay.DTS-HD", "SHOW"),
])
def test_extract_title_mixed_quality_descriptors(instance, path, expected):
    """Test title extraction with multiple quality descriptors."""
    assert instance.extract_title(Path(path)) == expected


# Common edge cases from real torrents
@pytest.mark.parametrize("path,expected", [
    # Multi-episode patterns
    ("Show.S01E01-E03.1080p", "SHOW"),
    # Complete season
    ("Show.2020.S01.Complete.720p", "SHOW"),
    # Dual audio
    ("Movie.2020.1080p.BluRay.DUAL", "MOVIE"),
    # Repack/Proper
    ("Title.2020.1080p.REPACK", "TITLE"),
    ("Title.2020.PROPER.1080p", "TITLE.2020.PROPER"),
])
def test_extract_title_torrent_edge_cases(instance, path, expected):
    """Test title extraction with common edge cases found in torrents."""
    assert instance.extract_title(Path(path)) == expected


# Case where year is immediately before extension
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.mkv", "TITLE"),
    ("Movie.1999.mp4", "MOVIE"),
])
def test_extract_title_year_before_extension(instance, path, expected):
    """Test title extraction when year is immediately before file extension."""
    assert instance.extract_title(Path(path)) == expected


# Case where no year but has season/episode and quality
@pytest.mark.parametrize("path,expected", [
    ("Title.S01E01.1080p.BluRay", "TITLE"),
    ("Show.Season.1.720p.WEBRip", "SHOW"),
])
def test_extract_title_no_year_with_season_quality(instance, path, expected):
    """Test title extraction without year but with season and quality."""
    assert instance.extract_title(Path(path)) == expected
