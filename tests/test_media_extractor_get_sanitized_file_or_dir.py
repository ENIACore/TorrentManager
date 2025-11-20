import pytest
from pathlib import Path
from extractor.media_extractor import MediaExtractor 


@pytest.fixture
def instance():
    return MediaExtractor()


@pytest.mark.parametrize("input_path,expected_output", [
    (Path("/home/user/My Movie.mkv"), "MY.MOVIE.MKV"),
    (Path("This, Movie\'s File.mp4"), "THIS.MOVIES.FILE.MP4"),
    (Path("Test   .avi"), "TEST.AVI"),
    (Path("Movie (2024) [1080p].mkv"), "MOVIE.2024.1080P.MKV"),
    (Path("/path/to/My_Folder-Name"), "MY.FOLDER.NAME"),
    (Path("file!!!with###special$$$chars.mp4"), "FILE.WITH.SPECIAL.CHARS.MP4"),
    (Path("ALREADY.UPPERCASE.MKV"), "ALREADY.UPPERCASE.MKV"),
])
def test_get_sanitized_file_or_dir(instance, input_path, expected_output):
    assert instance._get_sanitized_file_or_dir(input_path) == expected_output


def test_get_sanitized_file_or_dir_empty_name(instance):
    result = instance._get_sanitized_file_or_dir(Path("."))
    assert result == ''


def test_get_sanitized_file_or_dir_only_special_chars(instance):
    result = instance._get_sanitized_file_or_dir(Path("!!!###$$$"))
    assert result == ''


def test_get_sanitized_file_or_dir_preserves_extension(instance):
    result = instance._get_sanitized_file_or_dir(Path("my-file.mp4"))
    assert result == "MY.FILE.MP4"
