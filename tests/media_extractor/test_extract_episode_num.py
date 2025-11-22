import pytest
from extractor.media_extractor import MediaExtractor


@pytest.fixture
def instance():
    return MediaExtractor()


# Basic E<number> pattern tests
@pytest.mark.parametrize("parts,index,expected_group", [
    (["MY", "SHOW", "S01", "E05"], 3, "05"),
    (["E02", "COMPLETE"], 0, "02"),
    (["TITLE", "E10", "BLURAY"], 1, "10"),
    (["SHOW", "S1", "E1"], 2, "1"),
    (["SERIES", "E99", "X265"], 1, "99"),
    (["SHOW", "S001", "E001"], 2, "001"),
])
def test_extract_episode_num_e_pattern(instance, parts, index, expected_group):
    """Test that E<number> patterns are correctly matched."""
    match = instance._extract_episode_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# E.<number> pattern tests
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "S", "01", "E", "05"], 3, "05"),
    (["TITLE", "E", "2", "BLURAY"], 1, "2"),
    (["E", "10", "COMPLETE"], 0, "10"),
])
def test_extract_episode_num_e_dot_pattern(instance, parts, index, expected_group):
    """Test that E.<number> patterns are correctly matched."""
    match = instance._extract_episode_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# EP<number> pattern tests
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "EP01", "1080P"], 1, "01"),
    (["TITLE", "EP2", "BLURAY"], 1, "2"),
    (["EP10", "COMPLETE"], 0, "10"),
])
def test_extract_episode_num_ep_pattern(instance, parts, index, expected_group):
    """Test that EP<number> patterns are correctly matched."""
    match = instance._extract_episode_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# EP.<number> pattern tests
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "EP", "01", "1080P"], 1, "01"),
    (["TITLE", "EP", "2", "BLURAY"], 1, "2"),
])
def test_extract_episode_num_ep_dot_pattern(instance, parts, index, expected_group):
    """Test that EP.<number> patterns are correctly matched."""
    match = instance._extract_episode_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# EPISODE<number> pattern tests
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "EPISODE01", "1080P"], 1, "01"),
    (["TITLE", "EPISODE2", "BLURAY"], 1, "2"),
    (["EPISODE10", "COMPLETE"], 0, "10"),
    (["SHOW", "EPISODE1", "X265"], 1, "1"),
])
def test_extract_episode_num_episode_pattern(instance, parts, index, expected_group):
    """Test that EPISODE<number> patterns are correctly matched."""
    match = instance._extract_episode_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# EPISODE.<number> pattern tests
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "EPISODE", "01", "1080P"], 1, "01"),
    (["TITLE", "EPISODE", "2", "BLURAY"], 1, "2"),
])
def test_extract_episode_num_episode_dot_pattern(instance, parts, index, expected_group):
    """Test that EPISODE.<number> patterns are correctly matched."""
    match = instance._extract_episode_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# EPISODE without number pattern tests
@pytest.mark.parametrize("parts,index,expected_capture", [
    (["SHOW", "EPISODE", "1080P"], 1, "EPISODE"),
    (["TITLE", "EPISODE", "BLURAY"], 1, "EPISODE"),
    (["EPISODE", "COMPLETE"], 0, "EPISODE"),
])
def test_extract_episode_num_episode_no_number(instance, parts, index, expected_capture):
    """Test that standalone EPISODE pattern is matched and captures the word itself."""
    match = instance._extract_episode_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_capture


# EP without number pattern tests
@pytest.mark.parametrize("parts,index,expected_capture", [
    (["SHOW", "EP", "1080P"], 1, "EP"),
    (["TITLE", "EP", "BLURAY"], 1, "EP"),
])
def test_extract_episode_num_ep_no_number(instance, parts, index, expected_capture):
    """Test that standalone EP pattern is matched and captures the word itself."""
    match = instance._extract_episode_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_capture


# S<number>E<number> pattern tests
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "S01E05", "1080P"], 1, "05"),
    (["TITLE", "S02E10", "BLURAY"], 1, "10"),
    (["S1E1", "WEBRIP"], 0, "1"),
    (["S10E05", "X265"], 0, "05"),
    (["S01E99", "COMPLETE"], 0, "99"),
])
def test_extract_episode_num_s_e_pattern(instance, parts, index, expected_group):
    """Test that S<number>E<number> patterns extract episode number."""
    match = instance._extract_episode_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# <number>X<number> pattern tests (e.g., 1x05 for season 1 episode 5)
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "1X05", "1080P"], 1, "05"),
    (["TITLE", "2X10", "BLURAY"], 1, "10"),
    (["1X1", "WEBRIP"], 0, "1"),
    (["10X05", "X265"], 0, "05"),
])
def test_extract_episode_num_x_pattern(instance, parts, index, expected_group):
    """Test that <number>X<number> patterns extract episode number."""
    match = instance._extract_episode_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# <number>.X.<number> pattern tests (e.g., 1.X.05)
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "1", "X", "05", "1080P"], 1, "05"),
    (["TITLE", "2", "X", "10", "BLURAY"], 1, "10"),
    (["1", "X", "01", "WEBRIP"], 0, "01"),
])
def test_extract_episode_num_x_dot_pattern(instance, parts, index, expected_group):
    """Test that <number>.X.<number> patterns extract episode number."""
    match = instance._extract_episode_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# Invalid episode patterns
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "2020", "BLURAY"], 1),  # Year, not episode
    (["TITLE", "1080P", "BLURAY"], 1),  # Resolution, not episode
    (["TITLE", "X265", "BLURAY"], 1),  # Codec, not episode
    (["TITLE", "S05", "BLURAY"], 1),  # Season only, no episode
    (["TITLE", "BLURAY", "X265"], 1),  # Quality, not episode
    (["TITLE", "DTS", "BLURAY"], 1),  # Audio, not episode
    (["TITLE", "EE01", "BLURAY"], 1),  # Invalid double E
    (["TITLE", "EPISODES", "BLURAY"], 1),  # Plural, not matching pattern
])
def test_extract_episode_num_invalid(instance, parts, index):
    """Test that non-episode patterns return None."""
    assert instance._extract_episode_num(index, parts) is None


# Edge cases - different positions
def test_extract_episode_num_at_beginning(instance):
    """Test episode at the beginning of parts list."""
    parts = ["E05", "MY", "SHOW", "BLURAY"]
    match = instance._extract_episode_num(0, parts)
    assert match is not None
    assert match.group(1) == "05"


def test_extract_episode_num_at_end(instance):
    """Test episode at the end of parts list."""
    parts = ["MY", "SHOW", "BLURAY", "E05"]
    match = instance._extract_episode_num(3, parts)
    assert match is not None
    assert match.group(1) == "05"


def test_extract_episode_num_single_element(instance):
    """Test episode as the only element."""
    parts = ["E05"]
    match = instance._extract_episode_num(0, parts)
    assert match is not None
    assert match.group(1) == "05"


# Edge cases - index boundaries
def test_extract_episode_num_index_out_of_bounds(instance):
    """Test that index beyond parts length returns None."""
    parts = ["MY", "SHOW", "E05"]
    assert instance._extract_episode_num(10, parts) is None


def test_extract_episode_num_negative_index(instance):
    """Test behavior with negative index."""
    parts = ["MY", "SHOW", "E05"]
    # The function will try to combine parts from -1 onward
    result = instance._extract_episode_num(-1, parts)
    # Should match E05 at negative index
    assert result is not None


# Common torrent filename scenarios
@pytest.mark.parametrize("parts,index,expected_group", [
    (["GAME", "OF", "THRONES", "S01E01", "1080P", "BLURAY", "X265"], 3, "01"),
    (["THE", "WIRE", "S05E12", "720P", "WEBRIP"], 2, "12"),
    (["BREAKING", "BAD", "SEASON", "3", "EPISODE", "5", "1080P"], 4, "5"),
    (["STRANGER", "THINGS", "S04E09", "2160P", "NETFLIX"], 2, "09"),
    (["SHOW", "NAME", "2020", "S02E05", "BLURAY"], 3, "05"),
    (["ANIME", "EP01", "1080P", "DUAL"], 1, "01"),
])
def test_extract_episode_num_realistic_filenames(instance, parts, index, expected_group):
    """Test episode extraction in realistic torrent filename patterns."""
    match = instance._extract_episode_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# Empty and minimal inputs
def test_extract_episode_num_empty_parts(instance):
    """Test with empty parts list."""
    assert instance._extract_episode_num(0, []) is None


def test_extract_episode_num_empty_string_part(instance):
    """Test with empty string in parts."""
    parts = ["TITLE", "", "E05"]
    assert instance._extract_episode_num(1, parts) is None


# Multiple episode patterns in same filename (edge case)
def test_extract_episode_num_multiple_episodes(instance):
    """Test filename with multiple episode patterns (e.g., multi-episode release)."""
    parts = ["SHOW", "S01E01", "E02", "1080P"]
    # First episode pattern (in S01E01)
    match1 = instance._extract_episode_num(1, parts)
    assert match1 is not None
    assert match1.group(1) == "01"
    # Second episode pattern
    match2 = instance._extract_episode_num(2, parts)
    assert match2 is not None
    assert match2.group(1) == "02"


# Leading zeros vs no leading zeros
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "S1", "E1"], 2, "1"),
    (["SHOW", "S01", "E01"], 2, "01"),
    (["SHOW", "S001", "E001"], 2, "001"),
])
def test_extract_episode_num_leading_zeros(instance, parts, index, expected_group):
    """Test that episode numbers with/without leading zeros are captured correctly."""
    match = instance._extract_episode_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# Case sensitivity (should work since patterns are uppercase)
@pytest.mark.parametrize("parts,index", [
    (["SHOW", "S01", "E05"], 2),  # Uppercase (standard after sanitization)
])
def test_extract_episode_num_case_sensitivity(instance, parts, index):
    """Test that episode patterns match uppercase input (post-sanitization)."""
    match = instance._extract_episode_num(index, parts)
    assert match is not None


# Multi-episode releases
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "S01E01", "E02", "E03", "1080P"], 1, "01"),  # First episode in range
    (["SHOW", "S01E01", "E02", "E03", "1080P"], 2, "02"),  # Second episode
    (["SHOW", "S01E01", "E02", "E03", "1080P"], 3, "03"),  # Third episode
])
def test_extract_episode_num_multi_episode(instance, parts, index, expected_group):
    """Test extraction from multi-episode release filenames."""
    match = instance._extract_episode_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# Edge case: Both season and episode in same part (S01E01)
def test_extract_episode_num_combined_season_episode(instance):
    """Test that combined S01E01 format extracts episode correctly."""
    parts = ["SHOW", "S05E12", "BLURAY"]
    match = instance._extract_episode_num(1, parts)
    assert match is not None
    assert match.group(1) == "12"
