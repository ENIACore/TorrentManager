import pytest
from pathlib import Path
from extractor.media_extractor import MediaExtractor


@pytest.fixture
def instance():
    return MediaExtractor()


# Atmos audio patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.ATMOS.BluRay", "Atmos"),
    ("Movie.DOLBY-ATMOS.1080p", "Atmos"),
    ("Film.DOLBY.ATMOS.4K", "Atmos"),
    ("Show.DOLBYATMOS.720p", "Atmos"),
])
def test_extract_audio_atmos(instance, path, expected):
    """Test audio extraction for Atmos patterns."""
    assert instance.extract_audio(Path(path)) == expected


# DTS-X audio patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.DTSX.BluRay", "DTS-X"),
    ("Movie.DTS.X.1080p", "DTS-X"),
])
def test_extract_audio_dtsx(instance, path, expected):
    """Test audio extraction for DTS-X patterns."""
    assert instance.extract_audio(Path(path)) == expected


# DTS-HD audio patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.DTS.HD.MA.BluRay", "DTS-HD"),
    ("Movie.DTSHD-MA.1080p", "DTS-HD"),
    ("Film.DTSHD.MA.4K", "DTS-HD"),
    ("Show.DTS.HD.720p", "DTS-HD"),
    ("Series.DTSHD.1080p", "DTS-HD"),
])
def test_extract_audio_dtshd(instance, path, expected):
    """Test audio extraction for DTS-HD patterns."""
    assert instance.extract_audio(Path(path)) == expected


# DTS-MA audio patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.DTS.MA.BluRay", "DTS-MA"),
    ("Movie.DTSMA.1080p", "DTS-MA"),
])
def test_extract_audio_dtsma(instance, path, expected):
    """Test audio extraction for DTS-MA patterns."""
    assert instance.extract_audio(Path(path)) == expected


# DTS-ES audio patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.DTS.ES.BluRay", "DTS-ES"),
    ("Movie.DTSES.1080p", "DTS-ES"),
])
def test_extract_audio_dtses(instance, path, expected):
    """Test audio extraction for DTS-ES patterns."""
    assert instance.extract_audio(Path(path)) == expected


# DTS audio patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.DTS.BluRay", "DTS"),
    ("Movie.DTS.1080p", "DTS"),
])
def test_extract_audio_dts(instance, path, expected):
    """Test audio extraction for DTS patterns."""
    assert instance.extract_audio(Path(path)) == expected


# TrueHD audio patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.TRUEHD.BluRay", "TrueHD"),
    ("Movie.TRUE.HD.1080p", "TrueHD"),
])
def test_extract_audio_truehd(instance, path, expected):
    """Test audio extraction for TrueHD patterns."""
    assert instance.extract_audio(Path(path)) == expected


# DD+ (Dolby Digital Plus / E-AC-3) audio patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.DD.WEBRip", "DD"),
    ("Movie.DDP.1080p", "DD+"),
    ("Film.E.AC.3.720p", "DD+"),
    ("Show.EAC3.1080p", "DD+"),
    ("Series.DD.PLUS.720p", "DD+"),
    ("Title.DDPLUS.1080p", "DD+"),
])
def test_extract_audio_ddplus(instance, path, expected):
    """Test audio extraction for DD+ (Dolby Digital Plus) patterns."""
    assert instance.extract_audio(Path(path)) == expected


# DD (Dolby Digital / AC3) audio patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.DD.BluRay", "DD"),
    ("Movie.AC3.720p", "DD"),
    ("Film.DOLBY-DIGITAL.1080p", "DD"),
    ("Show.DOLBY.DIGITAL.720p", "DD"),
    ("Series.DOLBYDIGITAL.1080p", "DD"),
])
def test_extract_audio_dd(instance, path, expected):
    """Test audio extraction for DD (Dolby Digital) patterns."""
    assert instance.extract_audio(Path(path)) == expected


# AAC audio patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.AAC.WEBRip", "AAC"),
    ("Movie.HE.AAC.720p", "AAC"),
    ("Film.HEAAC.1080p", "AAC"),
])
def test_extract_audio_aac(instance, path, expected):
    """Test audio extraction for AAC patterns."""
    assert instance.extract_audio(Path(path)) == expected


# FLAC audio patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.FLAC.BluRay", "FLAC"),
    ("Movie.FLAC.1080p", "FLAC"),
])
def test_extract_audio_flac(instance, path, expected):
    """Test audio extraction for FLAC patterns."""
    assert instance.extract_audio(Path(path)) == expected


# MP3 audio patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.MP3.WEBRip", "MP3"),
    ("Movie.MP3.720p", "MP3"),
])
def test_extract_audio_mp3(instance, path, expected):
    """Test audio extraction for MP3 patterns."""
    assert instance.extract_audio(Path(path)) == expected


# LPCM/PCM audio patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.LPCM.BluRay", "LPCM"),
    ("Movie.PCM.1080p", "LPCM"),
])
def test_extract_audio_lpcm(instance, path, expected):
    """Test audio extraction for LPCM/PCM patterns."""
    assert instance.extract_audio(Path(path)) == expected


# OGG/Vorbis audio patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.OGG.WEBRip", "OGG"),
    ("Movie.VORBIS.720p", "OGG"),
])
def test_extract_audio_ogg(instance, path, expected):
    """Test audio extraction for OGG/Vorbis patterns."""
    assert instance.extract_audio(Path(path)) == expected


# OPUS audio patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.OPUS.WEBRip", "OPUS"),
    ("Movie.OPUS.720p", "OPUS"),
])
def test_extract_audio_opus(instance, path, expected):
    """Test audio extraction for OPUS patterns."""
    assert instance.extract_audio(Path(path)) == expected


# 5.1 channel configuration patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.5.1.BluRay", "5.1"),
    ("Movie.51.1080p", "5.1"),
    ("Film.6CH.720p", "5.1"),
])
def test_extract_audio_5_1(instance, path, expected):
    """Test audio extraction for 5.1 channel configuration patterns."""
    assert instance.extract_audio(Path(path)) == expected


# 7.1 channel configuration patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.7.1.BluRay", "7.1"),
    ("Movie.71.1080p", "7.1"),
    ("Film.8CH.720p", "7.1"),
])
def test_extract_audio_7_1(instance, path, expected):
    """Test audio extraction for 7.1 channel configuration patterns."""
    assert instance.extract_audio(Path(path)) == expected


# 2.0 stereo channel configuration patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.2.0.WEBRip", "2.0"),
    ("Movie.20.720p", "2.0"),
    ("Film.STEREO.1080p", "2.0"),
    ("Show.2CH.720p", "2.0"),
])
def test_extract_audio_2_0(instance, path, expected):
    """Test audio extraction for 2.0 stereo channel configuration patterns."""
    assert instance.extract_audio(Path(path)) == expected


# DUAL audio patterns
@pytest.mark.parametrize("path,expected", [
    ("Title.DUAL.AUDIO.BluRay", "DUAL"),
    ("Movie.DUAL.1080p", "DUAL"),
])
def test_extract_audio_dual(instance, path, expected):
    """Test audio extraction for DUAL audio patterns."""
    assert instance.extract_audio(Path(path)) == expected


# Audio with title and year
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.DTS.BluRay", "DTS"),
    ("Movie.1999.AAC.WEBRip", "AAC"),
    ("Film.2018.ATMOS.1080p", "Atmos"),
    ("Show.2021.TrueHD.720p", "TrueHD"),
])
def test_extract_audio_with_title_and_year(instance, path, expected):
    """Test audio extraction when filename includes title and year."""
    assert instance.extract_audio(Path(path)) == expected


# Audio with multiple quality descriptors
@pytest.mark.parametrize("path,expected", [
    ("Title.1080p.x265.BluRay.DTS", "DTS"),
    ("Movie.720p.x264.WEBRip.AAC", "AAC"),
    ("Show.4K.HEVC.BluRay.TrueHD", "TrueHD"),
    ("Film.2160p.x265.WEB-DL.AC3", "DD"),
])
def test_extract_audio_with_multiple_quality_descriptors(instance, path, expected):
    """Test audio extraction with multiple quality descriptors."""
    assert instance.extract_audio(Path(path)) == expected


# Audio with season/episode
@pytest.mark.parametrize("path,expected", [
    ("Title.S01E01.DTS.1080p", "DTS"),
    ("Show.S02.AAC.720p.WEBRip", "AAC"),
    ("Series.S01.ATMOS.4K.BluRay", "Atmos"),
])
def test_extract_audio_with_season_episode(instance, path, expected):
    """Test audio extraction when filename includes season/episode."""
    assert instance.extract_audio(Path(path)) == expected


# No audio in filename
@pytest.mark.parametrize("path,expected", [
    ("Title.2020.BluRay", None),
    ("Movie.1999.1080p", None),
    ("Film.x265", None),
    ("Title", None),
    ("Show.S01E01", None),
])
def test_extract_audio_no_audio(instance, path, expected):
    """Test audio extraction when there is no audio in filename."""
    assert instance.extract_audio(Path(path)) == expected


# Multiple audio indicators (should extract first)
@pytest.mark.parametrize("path,expected", [
    ("Title.DTS.AAC.BluRay", "DTS"),
    ("Movie.ATMOS.TrueHD.1080p", "Atmos"),
    ("Film.5.1.STEREO.720p", "5.1"),
])
def test_extract_audio_multiple_audio(instance, path, expected):
    """Test audio extraction when filename contains multiple audio indicators."""
    assert instance.extract_audio(Path(path)) == expected


# Audio at different positions
@pytest.mark.parametrize("path,expected", [
    ("DTS.Title.BluRay", "DTS"),
    ("Title.Middle.AAC.End", "AAC"),
    ("Title.ATMOS", "Atmos"),
])
def test_extract_audio_different_positions(instance, path, expected):
    """Test audio extraction at different filename positions."""
    assert instance.extract_audio(Path(path)) == expected


# Realistic torrent filenames
@pytest.mark.parametrize("path,expected", [
    ("The.Matrix.1999.1080p.BluRay.x265.DTS", "DTS"),
    ("Breaking.Bad.S05E16.720p.WEBRip.x264.AAC", "AAC"),
    ("Inception.2010.2160p.4K.UHD.BluRay.x265.TrueHD", "TrueHD"),
    ("Game.of.Thrones.S01.Complete.1080p.BluRay.DD.5.1", "DD"),
    ("Interstellar.2014.Directors.Cut.1080p.BluRay.ATMOS", "Atmos"),
    ("The.Office.US.S09E23.720p.WEB-DL.AAC.2.0", "AAC"),
    ("Avatar.2009.Extended.Edition.1080p.x265.DTS-HD", "DTS-HD"),
    ("Stranger.Things.2016.S04.2160p.Netflix.WEBRip.DUAL", "DUAL"),
])
def test_extract_audio_realistic_filenames(instance, path, expected):
    """Test audio extraction with realistic torrent filename patterns."""
    assert instance.extract_audio(Path(path)) == expected


# Full path (not just filename)
def test_extract_audio_full_path(instance):
    """Test audio extraction from full path (should only use filename)."""
    path = Path("/some/directory/path/Movie.2020.DTS.BluRay.1080p.mkv")
    assert instance.extract_audio(path) == "DTS"


# Whitespace handling
@pytest.mark.parametrize("path,expected", [
    ("Title DTS BluRay", "DTS"),
    ("  Movie  .AAC.1080p", "AAC"),
    ("Film   ATMOS  .4K", "Atmos"),
])
def test_extract_audio_whitespace(instance, path, expected):
    """Test audio extraction with whitespace (gets converted to dots)."""
    assert instance.extract_audio(Path(path)) == expected


# Special characters (sanitized)
@pytest.mark.parametrize("path,expected", [
    ("Title's Movie.DTS.BluRay", "DTS"),
    ("Title (AAC).1080p", "AAC"),
    ("Title - Subtitle.ATMOS.BluRay", "Atmos"),
])
def test_extract_audio_special_characters(instance, path, expected):
    """Test audio extraction with special characters (which get sanitized)."""
    assert instance.extract_audio(Path(path)) == expected


# Edge case: Empty and minimal inputs
@pytest.mark.parametrize("path,expected", [
    ("", None),
    ("...", None),
    ("!!!.@@@", None),
])
def test_extract_audio_empty_inputs(instance, path, expected):
    """Test audio extraction with empty or minimal inputs."""
    assert instance.extract_audio(Path(path)) == expected


# Case insensitivity (should work with lowercase after sanitization)
@pytest.mark.parametrize("path,expected", [
    ("title.dts.bluray", "DTS"),
    ("movie.aac.1080p", "AAC"),
    ("film.atmos.4k", "Atmos"),
    ("show.truehd.720p", "TrueHD"),
    ("series.flac.1080p", "FLAC"),
])
def test_extract_audio_case_insensitivity(instance, path, expected):
    """Test audio extraction is case insensitive (gets uppercased)."""
    assert instance.extract_audio(Path(path)) == expected


# Audio with file extension
@pytest.mark.parametrize("path,expected", [
    ("Title.DTS.BluRay.mkv", "DTS"),
    ("Movie.AAC.720p.mp4", "AAC"),
    ("Film.ATMOS.4K.avi", "Atmos"),
])
def test_extract_audio_with_extension(instance, path, expected):
    """Test audio extraction when filename has file extension."""
    assert instance.extract_audio(Path(path)) == expected


# Combined audio codec and channel configuration
# !!! TODO Enable audio codec and channel combination
@pytest.mark.parametrize("path,expected", [
    ("Title.DTS.5.1.BluRay", "DTS"),
    ("Movie.AAC.2.0.720p", "AAC"),
    ("Film.DD.5.1.1080p", "DD"),
    ("Show.TrueHD.7.1.4K", "TrueHD"),
])
def test_extract_audio_codec_with_channels(instance, path, expected):
    """Test audio extraction when both codec and channel config are present (should extract codec first)."""
    assert instance.extract_audio(Path(path)) == expected


# DTS variants hierarchy (should match more specific first)
@pytest.mark.parametrize("path,expected", [
    ("Title.DTS-X.BluRay", "DTS-X"),
    ("Movie.DTS-HD.1080p", "DTS-HD"),
    ("Film.DTS-MA.BluRay", "DTS-MA"),
    ("Show.DTS-ES.720p", "DTS-ES"),
    ("Series.DTS.1080p", "DTS"),
])
def test_extract_audio_dts_variants(instance, path, expected):
    """Test audio extraction for different DTS variant patterns."""
    assert instance.extract_audio(Path(path)) == expected


# Dolby variants
@pytest.mark.parametrize("path,expected", [
    ("Title.DOLBY-ATMOS.BluRay", "Atmos"),
    ("Movie.DOLBYATMOS.1080p", "Atmos"),
    ("Film.DOLBY.DIGITAL.720p", "DD"),
    ("Show.DOLBYDIGITAL.1080p", "DD"),
])
def test_extract_audio_dolby_variants(instance, path, expected):
    """Test audio extraction for Dolby brand variant patterns."""
    assert instance.extract_audio(Path(path)) == expected


# Hyphenated vs dotted audio variants
@pytest.mark.parametrize("path,expected", [
    ("Title.DTS-HD.BluRay", "DTS-HD"),
    ("Movie.DTS.HD.1080p", "DTS-HD"),
    ("Film.E-AC-3.720p", "DD+"),
    ("Show.E.AC.3.1080p", "DD+"),
])
def test_extract_audio_hyphenated_dotted_variants(instance, path, expected):
    """Test audio extraction with hyphenated and dotted pattern variants."""
    assert instance.extract_audio(Path(path)) == expected
