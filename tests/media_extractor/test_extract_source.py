import pytest
from pathlib import Path
from extractor.media_extractor import MediaExtractor


@pytest.fixture
def instance():
    return MediaExtractor()


# REMUX source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.REMUX.1080p", "REMUX"),
    ("Movie.REMUX.4K", "REMUX"),
])
def test_extract_source_remux(instance, path, expected):
    """Test source extraction for REMUX patterns."""
    assert instance.extract_source(Path(path)) == expected


# BluRay source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.BLURAY.1080p", "BluRay"),
    ("Movie.BDRIP.x265", "BluRay"),
    ("Film.BD.RIP.720p", "BluRay"),
    ("Show.BRRIP.1080p", "BluRay"),
    ("Series.BR.RIP.4K", "BluRay"),
    ("Title.BDMV.1080p", "BluRay"),
    ("Movie.BDISO.720p", "BluRay"),
    ("Film.BD25.1080p", "BluRay"),
    ("Show.BD50.4K", "BluRay"),
    ("Series.BD66.2160p", "BluRay"),
    ("Title.BD100.1080p", "BluRay"),
])
def test_extract_source_bluray(instance, path, expected):
    """Test source extraction for BluRay patterns."""
    assert instance.extract_source(Path(path)) == expected


# WEB-DL source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.WEB.DL.1080p", "WEB-DL"),
    ("Movie.WEBDL.720p", "WEB-DL"),
])
def test_extract_source_webdl(instance, path, expected):
    """Test source extraction for WEB-DL patterns."""
    assert instance.extract_source(Path(path)) == expected


# WEBRip source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.WEBRIP.1080p", "WEBRip"),
    ("Movie.WEB-RIP.720p", "WEBRip"),
    ("Film.WEB.RIP.4K", "WEBRip"),
])
def test_extract_source_webrip(instance, path, expected):
    """Test source extraction for WEBRip patterns."""
    assert instance.extract_source(Path(path)) == expected


# WEB source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.WEB.1080p", "WEB"),
    ("Movie.WEB.720p", "WEB"),
])
def test_extract_source_web(instance, path, expected):
    """Test source extraction for WEB patterns."""
    assert instance.extract_source(Path(path)) == expected


# HDRip source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.HDRIP.1080p", "HDRip"),
    ("Movie.HD.RIP.720p", "HDRip"),
])
def test_extract_source_hdrip(instance, path, expected):
    """Test source extraction for HDRip patterns."""
    assert instance.extract_source(Path(path)) == expected


# DVDRip source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.DVDRIP.720p", "DVDRip"),
    ("Movie.DVD.RIP.480p", "DVDRip"),
])
def test_extract_source_dvdrip(instance, path, expected):
    """Test source extraction for DVDRip patterns."""
    assert instance.extract_source(Path(path)) == expected


# DVD source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.DVD.480p", "DVD"),
    ("Movie.DVDSCR.720p", "DVD"),
    ("Film.DVD5.480p", "DVD"),
    ("Show.DVD9.720p", "DVD"),
])
def test_extract_source_dvd(instance, path, expected):
    """Test source extraction for DVD patterns."""
    assert instance.extract_source(Path(path)) == expected


# HDTV source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.HDTV.1080p", "HDTV"),
    ("Movie.HDTVRIP.720p", "HDTV"),
    ("Film.DTTV.1080p", "HDTV"),
    ("Show.PDTV.720p", "HDTV"),
    ("Series.SDTV.480p", "HDTV"),
    ("Title.LDTV.360p", "HDTV"),
])
def test_extract_source_hdtv(instance, path, expected):
    """Test source extraction for HDTV patterns."""
    assert instance.extract_source(Path(path)) == expected


# TELECINE source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.TELECINE.720p", "TELECINE"),
    ("Movie.TC.480p", "TELECINE"),
])
def test_extract_source_telecine(instance, path, expected):
    """Test source extraction for TELECINE patterns."""
    assert instance.extract_source(Path(path)) == expected


# TELESYNC source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.TELESYNC.720p", "TELESYNC"),
    ("Movie.TS.480p", "TELESYNC"),
])
def test_extract_source_telesync(instance, path, expected):
    """Test source extraction for TELESYNC patterns."""
    assert instance.extract_source(Path(path)) == expected


# SCREENER source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.SCREENER.720p", "SCREENER"),
    ("Movie.SCR.480p", "SCREENER"),
    ("Show.BDSCR.1080p", "SCREENER"),
])
def test_extract_source_screener(instance, path, expected):
    """Test source extraction for SCREENER patterns."""
    assert instance.extract_source(Path(path)) == expected


# CAM source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.CAMRIP.480p", "CAM"),
    ("Movie.CAM.360p", "CAM"),
    ("Film.HDCAM.720p", "CAM"),
])
def test_extract_source_cam(instance, path, expected):
    """Test source extraction for CAM patterns."""
    assert instance.extract_source(Path(path)) == expected


# WORKPRINT source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.WORKPRINT.720p", "WORKPRINT"),
    ("Movie.WP.480p", "WORKPRINT"),
])
def test_extract_source_workprint(instance, path, expected):
    """Test source extraction for WORKPRINT patterns."""
    assert instance.extract_source(Path(path)) == expected


# PPV source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.PPV.720p", "PPV"),
    ("Movie.PPVRIP.1080p", "PPV"),
])
def test_extract_source_ppv(instance, path, expected):
    """Test source extraction for PPV patterns."""
    assert instance.extract_source(Path(path)) == expected


# VODRip source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.VODRIP.720p", "VODRip"),
    ("Movie.VOD.1080p", "VODRip"),
])
def test_extract_source_vodrip(instance, path, expected):
    """Test source extraction for VODRip patterns."""
    assert instance.extract_source(Path(path)) == expected


# HC source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.HC.720p", "HC"),
    ("Movie.HCHDCAM.480p", "HC"),
])
def test_extract_source_hc(instance, path, expected):
    """Test source extraction for HC patterns."""
    assert instance.extract_source(Path(path)) == expected


# LINE source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.LINE.720p", "LINE"),
    ("Movie.LINE.480p", "LINE"),
])
def test_extract_source_line(instance, path, expected):
    """Test source extraction for LINE patterns."""
    assert instance.extract_source(Path(path)) == expected


# HDTS source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.HDTS.720p", "HDTS"),
    ("Movie.HD-TS.480p", "HDTS"),
    ("Film.HD.TS.720p", "HDTS"),
])
def test_extract_source_hdts(instance, path, expected):
    """Test source extraction for HDTS patterns."""
    assert instance.extract_source(Path(path)) == expected


# HDTC source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.HDTC.720p", "HDTC"),
    ("Movie.HD-TC.480p", "HDTC"),
    ("Film.HD.TC.720p", "HDTC"),
])
def test_extract_source_hdtc(instance, path, expected):
    """Test source extraction for HDTC patterns."""
    assert instance.extract_source(Path(path)) == expected


# TVRip source patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.TVRIP.720p", "TVRip"),
    ("Movie.SATRIP.480p", "TVRip"),
    ("Film.DTTVRIP.720p", "TVRip"),
])
def test_extract_source_tvrip(instance, path, expected):
    """Test source extraction for TVRip patterns."""
    assert instance.extract_source(Path(path)) == expected


# Source with title and year
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.BluRay.1080p", "BluRay"),
    ("Movie.1999.WEBRip.720p", "WEBRip"),
    ("Film.2018.WEB-DL.4K", "WEB-DL"),
    ("Show.2021.HDTV.1080p", "HDTV"),
])
def test_extract_source_with_title_and_year(instance, path, expected):
    """Test source extraction when filename includes title and year."""
    assert instance.extract_source(Path(path)) == expected


# Source with multiple quality descriptors
@pytest.mark.parametrize("path,expected", [
    ("Title.1080p.BluRay.x265.DTS", "BluRay"),
    ("Movie.720p.WEBRip.x264.AAC", "WEBRip"),
    ("Show.4K.WEB-DL.HEVC.TrueHD", "WEB-DL"),
    ("Film.2160p.HDTV.x265.AC3", "HDTV"),
])
def test_extract_source_with_multiple_quality_descriptors(instance, path, expected):
    """Test source extraction with multiple quality descriptors."""
    assert instance.extract_source(Path(path)) == expected


# Source with season/episode
@pytest.mark.parametrize("path,expected", [
    ("Title.S01E01.BluRay.1080p", "BluRay"),
    ("Show.S02.WEBRip.720p.x264", "WEBRip"),
    ("Series.S01.WEB-DL.4K.HEVC", "WEB-DL"),
])
def test_extract_source_with_season_episode(instance, path, expected):
    """Test source extraction when filename includes season/episode."""
    assert instance.extract_source(Path(path)) == expected


# No source in filename
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.1080p", None),
    ("Movie.1999.x265", None),
    ("Film.4K", None),
    ("Title", None),
    ("Show.S01E01", None),
])
def test_extract_source_no_source(instance, path, expected):
    """Test source extraction when there is no source in filename."""
    assert instance.extract_source(Path(path)) == expected


# Multiple sources (should extract first)
@pytest.mark.parametrize("path,expected", [
    ("Title.BluRay.WEBRip.1080p", "BluRay"),
    ("Movie.WEB-DL.HDTV.720p", "WEB-DL"),
    ("Film.DVDRip.BluRay.480p", "DVDRip"),
])
def test_extract_source_multiple_sources(instance, path, expected):
    """Test source extraction when filename contains multiple source indicators."""
    assert instance.extract_source(Path(path)) == expected


# Source at different positions
@pytest.mark.parametrize("path,expected", [
    ("BluRay.Title.1080p", "BluRay"),
    ("Title.Middle.WEBRip.End", "WEBRip"),
    ("Title.HDTV", "HDTV"),
])
def test_extract_source_different_positions(instance, path, expected):
    """Test source extraction at different filename positions."""
    assert instance.extract_source(Path(path)) == expected


# Realistic torrent filenames
@pytest.mark.parametrize("path,expected", [
    ("The.Matrix.1999.1080p.BluRay.x265", "BluRay"),
    ("Breaking.Bad.S05E16.720p.WEBRip.x264", "WEBRip"),
    ("Inception.2010.2160p.4K.UHD.BluRay.x265", "BluRay"),
    ("Game.of.Thrones.S01.Complete.1080p.BluRay", "BluRay"),
    ("Interstellar.2014.Directors.Cut.1080p.BluRay", "BluRay"),
    ("The.Office.US.S09E23.720p.WEB-DL", "WEB-DL"),
    ("Avatar.2009.Extended.Edition.1080p.BluRay.x265", "BluRay"),
    ("Stranger.Things.2016.S04.2160p.Netflix.WEBRip", "WEBRip"),
])
def test_extract_source_realistic_filenames(instance, path, expected):
    """Test source extraction with realistic torrent filename patterns."""
    assert instance.extract_source(Path(path)) == expected


# Full path (not just filename)
def test_extract_source_full_path(instance):
    """Test source extraction from full path (should only use filename)."""
    path = Path("/some/directory/path/Movie.2020.BluRay.1080p.mkv")
    assert instance.extract_source(path) == "BluRay"


# Whitespace handling
@pytest.mark.parametrize("path,expected", [
    ("Title BluRay 1080p", "BluRay"),
    ("  Movie  .WEBRip.720p", "WEBRip"),
    ("Film   WEB-DL  .4K", "WEB-DL"),
])
def test_extract_source_whitespace(instance, path, expected):
    """Test source extraction with whitespace (gets converted to dots)."""
    assert instance.extract_source(Path(path)) == expected


# Special characters (sanitized)
@pytest.mark.parametrize("path,expected", [
    ("Title's Movie.BluRay.1080p", "BluRay"),
    ("Title (BluRay).720p", "BluRay"),
    ("Title - Subtitle.WEBRip.1080p", "WEBRip"),
])
def test_extract_source_special_characters(instance, path, expected):
    """Test source extraction with special characters (which get sanitized)."""
    assert instance.extract_source(Path(path)) == expected


# Edge case: Empty and minimal inputs
@pytest.mark.parametrize("path,expected", [
    ("", None),
    ("...", None),
    ("!!!.@@@", None),
])
def test_extract_source_empty_inputs(instance, path, expected):
    """Test source extraction with empty or minimal inputs."""
    assert instance.extract_source(Path(path)) == expected


# Case insensitivity (should work with lowercase after sanitization)
@pytest.mark.parametrize("path,expected", [
    ("title.bluray.1080p", "BluRay"),
    ("movie.webrip.720p", "WEBRip"),
    ("film.web-dl.4k", "WEB-DL"),
    ("show.hdtv.1080p", "HDTV"),
    ("series.dvdrip.480p", "DVDRip"),
])
def test_extract_source_case_insensitivity(instance, path, expected):
    """Test source extraction is case insensitive (gets uppercased)."""
    assert instance.extract_source(Path(path)) == expected


# Source with file extension
@pytest.mark.parametrize("path,expected", [
    ("Title.BluRay.1080p.mkv", "BluRay"),
    ("Movie.WEBRip.720p.mp4", "WEBRip"),
    ("Film.WEB-DL.4K.avi", "WEB-DL"),
])
def test_extract_source_with_extension(instance, path, expected):
    """Test source extraction when filename has file extension."""
    assert instance.extract_source(Path(path)) == expected


# Source with codec
@pytest.mark.parametrize("path,expected", [
    ("Title.BluRay.x265.1080p", "BluRay"),
    ("Movie.WEBRip.x264.720p", "WEBRip"),
    ("Film.WEB-DL.HEVC.4K", "WEB-DL"),
])
def test_extract_source_with_codec(instance, path, expected):
    """Test source extraction when filename includes codec."""
    assert instance.extract_source(Path(path)) == expected


# BluRay disc size variants
@pytest.mark.parametrize("path,expected", [
    ("Title.BD25.1080p", "BluRay"),
    ("Movie.BD50.1080p", "BluRay"),
    ("Film.BD66.2160p", "BluRay"),
    ("Show.BD100.4K", "BluRay"),
])
def test_extract_source_bluray_disc_sizes(instance, path, expected):
    """Test source extraction for BluRay disc size variants."""
    assert instance.extract_source(Path(path)) == expected


# Hyphenated vs dotted variants
@pytest.mark.parametrize("path,expected", [
    ("Title.WEB-DL.1080p", "WEB-DL"),
    ("Movie.WEB.DL.720p", "WEB-DL"),
    ("Film.WEB-RIP.1080p", "WEBRip"),
    ("Show.WEB.RIP.720p", "WEBRip"),
    ("Series.BD-RIP.1080p", "BluRay"),
    ("Title.BD.RIP.720p", "BluRay"),
])
def test_extract_source_hyphenated_dotted_variants(instance, path, expected):
    """Test source extraction with hyphenated and dotted pattern variants."""
    assert instance.extract_source(Path(path)) == expected
