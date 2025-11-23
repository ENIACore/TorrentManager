import pytest
from pathlib import Path
from extractor.media_extractor import MediaExtractor


@pytest.fixture
def instance():
    return MediaExtractor()


# AV1 codec patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.AV1.BluRay", "AV1"),
    ("Movie.SVT.AV1.WEB", "AV1"),
    ("Film.SVTAV1.x265", "AV1"),
    ("Show.AOV1.1080p", "AV1"),
])
def test_extract_codec_av1(instance, path, expected):
    """Test codec extraction for AV1 patterns."""
    assert instance.extract_codec(Path(path)) == expected


# VP9 codec patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.VP9.BluRay", "VP9"),
    ("Movie.VP9.1080p", "VP9"),
])
def test_extract_codec_vp9(instance, path, expected):
    """Test codec extraction for VP9 patterns."""
    assert instance.extract_codec(Path(path)) == expected


# VP8 codec patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.VP8.BluRay", "VP8"),
    ("Movie.VP8.720p", "VP8"),
])
def test_extract_codec_vp8(instance, path, expected):
    """Test codec extraction for VP8 patterns."""
    assert instance.extract_codec(Path(path)) == expected


# x265 codec patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.x265.BluRay", "x265"),
    ("Movie.X265.1080p", "x265"),
    ("Film.X.265.WEB", "x265"),
    ("Show.H265.720p", "x265"),
    ("Series.H.265.BluRay", "x265"),
    ("Title.HEVC.1080p", "x265"),
    ("Movie.HEVC10.4K", "x265"),
    ("Film.HEVC10BIT.2160p", "x265"),
    ("Show.H265P.1080p", "x265"),
])
def test_extract_codec_x265(instance, path, expected):
    """Test codec extraction for x265/HEVC patterns."""
    assert instance.extract_codec(Path(path)) == expected


# x264 codec patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.x264.BluRay", "x264"),
    ("Movie.X264.1080p", "x264"),
    ("Film.X.264.WEB", "x264"),
    ("Show.H264.720p", "x264"),
    ("Series.H.264.BluRay", "x264"),
    ("Title.AVC.1080p", "x264"),
    ("Movie.AVC1.720p", "x264"),
    ("Film.H264P.1080p", "x264"),
])
def test_extract_codec_x264(instance, path, expected):
    """Test codec extraction for x264/AVC patterns."""
    assert instance.extract_codec(Path(path)) == expected


# x263 codec patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.x263.BluRay", "x263"),
    ("Movie.X263.480p", "x263"),
    ("Film.X.263.WEB", "x263"),
    ("Show.H263.360p", "x263"),
    ("Series.H.263.DVDRip", "x263"),
])
def test_extract_codec_x263(instance, path, expected):
    """Test codec extraction for x263 patterns."""
    assert instance.extract_codec(Path(path)) == expected


# XVID codec patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.XVID.DVDRip", "XVID"),
    ("Movie.XVID.AF.720p", "XVID"),
])
def test_extract_codec_xvid(instance, path, expected):
    """Test codec extraction for XVID patterns."""
    assert instance.extract_codec(Path(path)) == expected


# DIVX codec patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.DIVX.DVDRip", "DIVX"),
    ("Movie.DIV3.480p", "DIVX"),
    ("Film.DIVX6.720p", "DIVX"),
])
def test_extract_codec_divx(instance, path, expected):
    """Test codec extraction for DIVX patterns."""
    assert instance.extract_codec(Path(path)) == expected


# MPEG4 codec patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.MPEG.4.DVDRip", "MPEG4"),
    ("Movie.MPEG4.720p", "MPEG4"),
    ("Film.MP4V.480p", "MPEG4"),
])
def test_extract_codec_mpeg4(instance, path, expected):
    """Test codec extraction for MPEG4 patterns."""
    assert instance.extract_codec(Path(path)) == expected


# MPEG2 codec patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.MPEG.2.DVDRip", "MPEG2"),
    ("Movie.MPEG2.480p", "MPEG2"),
    ("Film.MP2V.DVD", "MPEG2"),
])
def test_extract_codec_mpeg2(instance, path, expected):
    """Test codec extraction for MPEG2 patterns."""
    assert instance.extract_codec(Path(path)) == expected


# MPEG1 codec patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.MPEG.1.DVDRip", "MPEG1"),
    ("Movie.MPEG1.240p", "MPEG1"),
    ("Film.MP1V.DVD", "MPEG1"),
])
def test_extract_codec_mpeg1(instance, path, expected):
    """Test codec extraction for MPEG1 patterns."""
    assert instance.extract_codec(Path(path)) == expected


# VC1 codec patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.VC.1.BluRay", "VC1"),
    ("Movie.VC1.1080p", "VC1"),
    ("Film.WMV3.720p", "VC1"),
    ("Show.WVC1.BluRay", "VC1"),
])
def test_extract_codec_vc1(instance, path, expected):
    """Test codec extraction for VC1 patterns."""
    assert instance.extract_codec(Path(path)) == expected


# THEORA codec patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.THEORA.WEB", "THEORA"),
    ("Movie.THEORA.480p", "THEORA"),
])
def test_extract_codec_theora(instance, path, expected):
    """Test codec extraction for THEORA patterns."""
    assert instance.extract_codec(Path(path)) == expected


# PRORES codec patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.PRORES.1080p", "PRORES"),
    ("Movie.PRORES422.4K", "PRORES"),
    ("Film.PRORES4444.2160p", "PRORES"),
    ("Show.PRORES422HQ.1080p", "PRORES"),
])
def test_extract_codec_prores(instance, path, expected):
    """Test codec extraction for PRORES patterns."""
    assert instance.extract_codec(Path(path)) == expected


# DNxHD codec patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.DNXHD.1080p", "DNxHD"),
    ("Movie.DNXHR.4K", "DNxHD"),
])
def test_extract_codec_dnxhd(instance, path, expected):
    """Test codec extraction for DNxHD patterns."""
    assert instance.extract_codec(Path(path)) == expected


# Codec with title and year
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.x265.BluRay", "x265"),
    ("Movie.1999.x264.WEB", "x264"),
    ("Film.2018.AV1.1080p", "AV1"),
    ("Show.2021.HEVC.720p", "x265"),
])
def test_extract_codec_with_title_and_year(instance, path, expected):
    """Test codec extraction when filename includes title and year."""
    assert instance.extract_codec(Path(path)) == expected


# Codec with multiple quality descriptors
@pytest.mark.parametrize("path,expected", [
    ("Title.1080p.x265.BluRay.DTS", "x265"),
    ("Movie.720p.x264.WEBRip.AAC", "x264"),
    ("Show.4K.HEVC.BluRay.TrueHD", "x265"),
    ("Film.2160p.AV1.WEB-DL.AC3", "AV1"),
])
def test_extract_codec_with_multiple_quality_descriptors(instance, path, expected):
    """Test codec extraction with multiple quality descriptors."""
    assert instance.extract_codec(Path(path)) == expected


# Codec with season/episode
@pytest.mark.parametrize("path,expected", [
    ("Title.S01E01.x265.1080p", "x265"),
    ("Show.S02.x264.720p.BluRay", "x264"),
    ("Series.S01.HEVC.4K.WEB", "x265"),
])
def test_extract_codec_with_season_episode(instance, path, expected):
    """Test codec extraction when filename includes season/episode."""
    assert instance.extract_codec(Path(path)) == expected


# No codec in filename
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.BluRay", None),
    ("Movie.1999.1080p", None),
    ("Film.WEBRip", None),
    ("Title", None),
    ("Show.S01E01", None),
])
def test_extract_codec_no_codec(instance, path, expected):
    """Test codec extraction when there is no codec in filename."""
    assert instance.extract_codec(Path(path)) == expected


# Multiple codecs (should extract first)
@pytest.mark.parametrize("path,expected", [
    ("Title.x265.x264.BluRay", "x265"),
    ("Movie.HEVC.AV1.1080p", "x265"),
    ("Film.x264.VP9.WEB", "x264"),
])
def test_extract_codec_multiple_codecs(instance, path, expected):
    """Test codec extraction when filename contains multiple codec indicators."""
    assert instance.extract_codec(Path(path)) == expected


# Codec at different positions
@pytest.mark.parametrize("path,expected", [
    ("x265.Title.BluRay", "x265"),
    ("Title.Middle.x264.End", "x264"),
    ("Title.HEVC", "x265"),
])
def test_extract_codec_different_positions(instance, path, expected):
    """Test codec extraction at different filename positions."""
    assert instance.extract_codec(Path(path)) == expected


# Realistic torrent filenames
@pytest.mark.parametrize("path,expected", [
    ("The.Matrix.1999.1080p.BluRay.x265", "x265"),
    ("Breaking.Bad.S05E16.720p.WEBRip.x264", "x264"),
    ("Inception.2010.2160p.4K.UHD.BluRay.x265", "x265"),
    ("Game.of.Thrones.S01.Complete.1080p.x264", "x264"),
    ("Interstellar.2014.Directors.Cut.1080p.BluRay.HEVC", "x265"),
    ("The.Office.US.S09E23.720p.WEB-DL.H264", "x264"),
    ("Avatar.2009.Extended.Edition.1080p.x265", "x265"),
    ("Stranger.Things.2016.S04.2160p.Netflix.WEBRip.AV1", "AV1"),
])
def test_extract_codec_realistic_filenames(instance, path, expected):
    """Test codec extraction with realistic torrent filename patterns."""
    assert instance.extract_codec(Path(path)) == expected


# Full path (not just filename)
def test_extract_codec_full_path(instance):
    """Test codec extraction from full path (should only use filename)."""
    path = Path("/some/directory/path/Movie.2020.x265.1080p.mkv")
    assert instance.extract_codec(path) == "x265"


# Whitespace handling
@pytest.mark.parametrize("path,expected", [
    ("Title x265 BluRay", "x265"),
    ("  Movie  .x264.1080p", "x264"),
    ("Film   HEVC  .4K", "x265"),
])
def test_extract_codec_whitespace(instance, path, expected):
    """Test codec extraction with whitespace (gets converted to dots)."""
    assert instance.extract_codec(Path(path)) == expected


# Special characters (sanitized)
@pytest.mark.parametrize("path,expected", [
    ("Title's Movie.x265.BluRay", "x265"),
    ("Title (x264).1080p", "x264"),
    ("Title - Subtitle.HEVC.BluRay", "x265"),
])
def test_extract_codec_special_characters(instance, path, expected):
    """Test codec extraction with special characters (which get sanitized)."""
    assert instance.extract_codec(Path(path)) == expected


# Edge case: Empty and minimal inputs
@pytest.mark.parametrize("path,expected", [
    ("", None),
    ("...", None),
    ("!!!.@@@", None),
])
def test_extract_codec_empty_inputs(instance, path, expected):
    """Test codec extraction with empty or minimal inputs."""
    assert instance.extract_codec(Path(path)) == expected


# Case insensitivity (should work with lowercase after sanitization)
@pytest.mark.parametrize("path,expected", [
    ("title.x265.bluray", "x265"),
    ("movie.x264.1080p", "x264"),
    ("film.hevc.4k", "x265"),
    ("show.av1.web", "AV1"),
    ("series.avc.720p", "x264"),
])
def test_extract_codec_case_insensitivity(instance, path, expected):
    """Test codec extraction is case insensitive (gets uppercased)."""
    assert instance.extract_codec(Path(path)) == expected


# Codec with file extension
@pytest.mark.parametrize("path,expected", [
    ("Title.x265.mkv", "x265"),
    ("Movie.x264.mp4", "x264"),
    ("Film.HEVC.avi", "x265"),
])
def test_extract_codec_with_extension(instance, path, expected):
    """Test codec extraction when filename has file extension."""
    assert instance.extract_codec(Path(path)) == expected


# 10-bit encoding indicators
@pytest.mark.parametrize("path,expected", [
    ("Title.HEVC10.1080p", "x265"),
    ("Movie.HEVC10BIT.4K", "x265"),
])
def test_extract_codec_10bit(instance, path, expected):
    """Test codec extraction with 10-bit encoding indicators."""
    assert instance.extract_codec(Path(path)) == expected


# Codec with profile indicators
@pytest.mark.parametrize("path,expected", [
    ("Title.H264P.1080p", "x264"),
    ("Movie.H265P.4K", "x265"),
])
def test_extract_codec_profile(instance, path, expected):
    """Test codec extraction with profile indicators."""
    assert instance.extract_codec(Path(path)) == expected
