import pytest
from pathlib import Path
from extractor.media_extractor import MediaExtractor


@pytest.fixture
def instance():
    return MediaExtractor()


# 8K resolution patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.8K.BluRay", "8K"),
    ("Movie.4320.x265", "8K"),
    ("Film.4320p.HEVC", "8K"),
    ("Show.4320i.WEB", "8K"),
    ("Series.7680X4320.BluRay", "8K"),
    ("Title.FULLUHD.x265", "8K"),
])
def test_extract_resolution_8k(instance, path, expected):
    """Test resolution extraction for 8K patterns."""
    assert instance.extract_resolution(Path(path)) == expected


# 4K resolution patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.4K.BluRay", "4K"),
    ("Movie.UHD.x265", "4K"),
    ("Film.2160.HEVC", "4K"),
    ("Show.2160p.WEB", "4K"),
    ("Series.2160i.BluRay", "4K"),
    ("Title.3840X2160.x265", "4K"),
])
def test_extract_resolution_4k(instance, path, expected):
    """Test resolution extraction for 4K patterns."""
    assert instance.extract_resolution(Path(path)) == expected


# 2K resolution patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.2K.BluRay", "2K"),
    ("Movie.1440.x265", "2K"),
    ("Film.1440p.HEVC", "2K"),
    ("Show.1440i.WEB", "2K"),
    ("Series.2560X1440.BluRay", "2K"),
    ("Title.QHD.x265", "2K"),
    ("Movie.WQHD.BluRay", "2K"),
])
def test_extract_resolution_2k(instance, path, expected):
    """Test resolution extraction for 2K patterns."""
    assert instance.extract_resolution(Path(path)) == expected


# 1080p resolution patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.1080.BluRay", "1080p"),
    ("Movie.1080p.x265", "1080p"),
    ("Film.1080i.HEVC", "1080p"),
    ("Show.FHD.WEB", "1080p"),
    ("Series.1920X1080.BluRay", "1080p"),
    ("Title.FULLHD.x265", "1080p"),
])
def test_extract_resolution_1080p(instance, path, expected):
    """Test resolution extraction for 1080p patterns."""
    assert instance.extract_resolution(Path(path)) == expected


# 720p resolution patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.720.BluRay", "720p"),
    ("Movie.720p.x265", "720p"),
    ("Film.720i.HEVC", "720p"),
    ("Show.1280X720.WEB", "720p"),
])
def test_extract_resolution_720p(instance, path, expected):
    """Test resolution extraction for 720p patterns."""
    assert instance.extract_resolution(Path(path)) == expected


# 576p resolution patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.576.BluRay", "576p"),
    ("Movie.576p.x265", "576p"),
    ("Film.576i.HEVC", "576p"),
    ("Show.PAL.WEB", "576p"),
])
def test_extract_resolution_576p(instance, path, expected):
    """Test resolution extraction for 576p patterns."""
    assert instance.extract_resolution(Path(path)) == expected


# 480p resolution patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.480.BluRay", "480p"),
    ("Movie.480p.x265", "480p"),
    ("Film.480i.HEVC", "480p"),
    ("Show.NTSC.WEB", "480p"),
])
def test_extract_resolution_480p(instance, path, expected):
    """Test resolution extraction for 480p patterns."""
    assert instance.extract_resolution(Path(path)) == expected


# 360p resolution patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.360.WEB", "360p"),
    ("Movie.360p.x264", "360p"),
    ("Film.360i.x265", "360p"),
])
def test_extract_resolution_360p(instance, path, expected):
    """Test resolution extraction for 360p patterns."""
    assert instance.extract_resolution(Path(path)) == expected


# 240p resolution patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.240.WEB", "240p"),
    ("Movie.240p.x264", "240p"),
    ("Film.240i.x265", "240p"),
])
def test_extract_resolution_240p(instance, path, expected):
    """Test resolution extraction for 240p patterns."""
    assert instance.extract_resolution(Path(path)) == expected


# Resolution with title and year
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.1080p", "1080p"),
    ("Movie.1999.720p.BluRay", "720p"),
    ("Film.2018.4K.x265", "4K"),
    ("Show.2021.2160p.WEB", "4K"),
])
def test_extract_resolution_with_title_and_year(instance, path, expected):
    """Test resolution extraction when filename includes title and year."""
    assert instance.extract_resolution(Path(path)) == expected


# Resolution with multiple quality descriptors
@pytest.mark.parametrize("path,expected", [
    ("Title.1080p.x265.BluRay.DTS", "1080p"),
    ("Movie.720p.x264.WEBRip.AAC", "720p"),
    ("Show.4K.HEVC.BluRay.TrueHD", "4K"),
    ("Film.2160p.x265.WEB-DL.AC3", "4K"),
])
def test_extract_resolution_with_multiple_quality_descriptors(instance, path, expected):
    """Test resolution extraction with multiple quality descriptors."""
    assert instance.extract_resolution(Path(path)) == expected


# Resolution with season/episode
@pytest.mark.parametrize("path,expected", [
    ("Title.S01E01.1080p", "1080p"),
    ("Show.S02.720p.BluRay", "720p"),
    ("Series.S01.4K.WEB", "4K"),
])
def test_extract_resolution_with_season_episode(instance, path, expected):
    """Test resolution extraction when filename includes season/episode."""
    assert instance.extract_resolution(Path(path)) == expected


# No resolution in filename
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.BluRay", None),
    ("Movie.1999.x265", None),
    ("Film.WEBRip", None),
    ("Title", None),
    ("Show.S01E01", None),
])
def test_extract_resolution_no_resolution(instance, path, expected):
    """Test resolution extraction when there is no resolution in filename."""
    assert instance.extract_resolution(Path(path)) == expected


# Multiple resolutions (should extract first)
@pytest.mark.parametrize("path,expected", [
    ("Title.1080p.720p.BluRay", "1080p"),
    ("Movie.4K.2160p.x265", "4K"),
    ("Film.UHD.1080p.HEVC", "4K"),
])
def test_extract_resolution_multiple_resolutions(instance, path, expected):
    """Test resolution extraction when filename contains multiple resolution indicators."""
    assert instance.extract_resolution(Path(path)) == expected


# Resolution at different positions
@pytest.mark.parametrize("path,expected", [
    ("1080p.Title.BluRay", "1080p"),
    ("Title.Middle.720p.End", "720p"),
    ("Title.4K", "4K"),
])
def test_extract_resolution_different_positions(instance, path, expected):
    """Test resolution extraction at different filename positions."""
    assert instance.extract_resolution(Path(path)) == expected


# Realistic torrent filenames
@pytest.mark.parametrize("path,expected", [
    ("The.Matrix.1999.1080p.BluRay.x265", "1080p"),
    ("Breaking.Bad.S05E16.720p.WEBRip.x264", "720p"),
    ("Inception.2010.2160p.4K.UHD.BluRay.x265", "4K"),
    ("Game.of.Thrones.S01.Complete.1080p", "1080p"),
    ("Interstellar.2014.Directors.Cut.1080p.BluRay", "1080p"),
    ("The.Office.US.S09E23.720p.WEB-DL", "720p"),
    ("Avatar.2009.Extended.Edition.1080p.x265", "1080p"),
    ("Stranger.Things.2016.S04.2160p.Netflix.WEBRip", "4K"),
])
def test_extract_resolution_realistic_filenames(instance, path, expected):
    """Test resolution extraction with realistic torrent filename patterns."""
    assert instance.extract_resolution(Path(path)) == expected


# Full path (not just filename)
def test_extract_resolution_full_path(instance):
    """Test resolution extraction from full path (should only use filename)."""
    path = Path("/some/directory/path/Movie.2020.1080p.mkv")
    assert instance.extract_resolution(path) == "1080p"


# Whitespace handling
@pytest.mark.parametrize("path,expected", [
    ("Title 1080p BluRay", "1080p"),
    ("  Movie  .720p.x265", "720p"),
    ("Film   4K  .HEVC", "4K"),
])
def test_extract_resolution_whitespace(instance, path, expected):
    """Test resolution extraction with whitespace (gets converted to dots)."""
    assert instance.extract_resolution(Path(path)) == expected


# Special characters (sanitized)
@pytest.mark.parametrize("path,expected", [
    ("Title's Movie.1080p.BluRay", "1080p"),
    ("Title (1080p).x265", "1080p"),
    ("Title - Subtitle.720p.BluRay", "720p"),
])
def test_extract_resolution_special_characters(instance, path, expected):
    """Test resolution extraction with special characters (which get sanitized)."""
    assert instance.extract_resolution(Path(path)) == expected


# Edge case: Empty and minimal inputs
@pytest.mark.parametrize("path,expected", [
    ("", None),
    ("...", None),
    ("!!!.@@@", None),
])
def test_extract_resolution_empty_inputs(instance, path, expected):
    """Test resolution extraction with empty or minimal inputs."""
    assert instance.extract_resolution(Path(path)) == expected


# Case insensitivity (should work with lowercase after sanitization)
@pytest.mark.parametrize("path,expected", [
    ("title.1080p.bluray", "1080p"),
    ("movie.720p.x265", "720p"),
    ("film.4k.hevc", "4K"),
    ("show.uhd.web", "4K"),
    ("series.fhd.bluray", "1080p"),
])
def test_extract_resolution_case_insensitivity(instance, path, expected):
    """Test resolution extraction is case insensitive (gets uppercased)."""
    assert instance.extract_resolution(Path(path)) == expected


# Resolution with file extension
@pytest.mark.parametrize("path,expected", [
    ("Title.1080p.mkv", "1080p"),
    ("Movie.720p.mp4", "720p"),
    ("Film.4K.avi", "4K"),
])
def test_extract_resolution_with_extension(instance, path, expected):
    """Test resolution extraction when filename has file extension."""
    assert instance.extract_resolution(Path(path)) == expected


# Progressive vs interlaced indicators
@pytest.mark.parametrize("path,expected", [
    ("Title.1080p.BluRay", "1080p"),
    ("Movie.1080i.x265", "1080p"),
    ("Film.720p.HEVC", "720p"),
    ("Show.720i.WEB", "720p"),
])
def test_extract_resolution_progressive_interlaced(instance, path, expected):
    """Test resolution extraction with progressive (p) and interlaced (i) indicators."""
    assert instance.extract_resolution(Path(path)) == expected


# Resolution with aspect ratio formats
@pytest.mark.parametrize("path,expected", [
    ("Title.1920X1080.BluRay", "1080p"),
    ("Movie.3840X2160.x265", "4K"),
    ("Film.7680X4320.HEVC", "8K"),
    ("Show.2560X1440.WEB", "2K"),
    ("Series.1280X720.BluRay", "720p"),
])
def test_extract_resolution_aspect_ratio(instance, path, expected):
    """Test resolution extraction with aspect ratio format (WIDTHxHEIGHT)."""
    assert instance.extract_resolution(Path(path)) == expected
