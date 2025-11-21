import pytest
from extractor.media_extractor import MediaExtractor


@pytest.fixture
def instance():
    return MediaExtractor()


# Basic S<number> pattern tests
@pytest.mark.parametrize("parts,index,expected_group", [
    (["MY", "SHOW", "S01", "E05"], 2, "01"),
    (["S02", "COMPLETE"], 0, "02"),
    (["TITLE", "S10", "BLURAY"], 1, "10"),
    (["SHOW", "S1", "E1"], 1, "1"),
    (["SERIES", "S99", "X265"], 1, "99"),
    (["SHOW", "S001", "E001"], 1, "001"),
])
def test_extract_season_num_s_pattern(instance, parts, index, expected_group):
    """Test that S<number> patterns are correctly matched."""
    match = instance._extract_season_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# S.<number> pattern tests
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "S", "01", "E", "05"], 1, "01"),
    (["TITLE", "S", "2", "BLURAY"], 1, "2"),
    (["S", "10", "COMPLETE"], 0, "10"),
])
def test_extract_season_num_s_dot_pattern(instance, parts, index, expected_group):
    """Test that S.<number> patterns are correctly matched."""
    match = instance._extract_season_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# SEA<number> pattern tests
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "SEA01", "E05"], 1, "01"),
    (["TITLE", "SEA2", "BLURAY"], 1, "2"),
    (["SEA10", "COMPLETE"], 0, "10"),
])
def test_extract_season_num_sea_pattern(instance, parts, index, expected_group):
    """Test that SEA<number> patterns are correctly matched."""
    match = instance._extract_season_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# SEA.<number> pattern tests
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "SEA", "01", "E05"], 1, "01"),
    (["TITLE", "SEA", "2", "BLURAY"], 1, "2"),
])
def test_extract_season_num_sea_dot_pattern(instance, parts, index, expected_group):
    """Test that SEA.<number> patterns are correctly matched."""
    match = instance._extract_season_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# SEASON<number> pattern tests
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "SEASON01", "E05"], 1, "01"),
    (["TITLE", "SEASON2", "BLURAY"], 1, "2"),
    (["SEASON10", "COMPLETE"], 0, "10"),
    (["SHOW", "SEASON1", "X265"], 1, "1"),
])
def test_extract_season_num_season_pattern(instance, parts, index, expected_group):
    """Test that SEASON<number> patterns are correctly matched."""
    match = instance._extract_season_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# SEASON.<number> pattern tests
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "SEASON", "01", "E05"], 1, "01"),
    (["TITLE", "SEASON", "2", "BLURAY"], 1, "2"),
])
def test_extract_season_num_season_dot_pattern(instance, parts, index, expected_group):
    """Test that SEASON.<number> patterns are correctly matched."""
    match = instance._extract_season_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# SEASON without number pattern tests
@pytest.mark.parametrize("parts,index", [
    (["SHOW", "SEASON", "E05"], 1),
    (["TITLE", "SEASON", "BLURAY"], 1),
    (["SEASON", "COMPLETE"], 0),
])
def test_extract_season_num_season_no_number(instance, parts, index):
    """Test that standalone SEASON pattern is matched (but has no capture group)."""
    match = instance._extract_season_num(index, parts)
    assert match is not None
    # This pattern has no capture groups, so attempting to access group(1) would raise IndexError
    # We just verify the match exists


# S<number>E<number> pattern tests
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "S01E05", "1080P"], 1, "01"),
    (["TITLE", "S02E10", "BLURAY"], 1, "02"),
    (["S1E1", "WEBRIP"], 0, "1"),
    (["S10E05", "X265"], 0, "10"),
])
def test_extract_season_num_s_e_pattern(instance, parts, index, expected_group):
    """Test that S<number>E<number> patterns extract season number."""
    match = instance._extract_season_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# Invalid season patterns
@pytest.mark.parametrize("parts,index", [
    (["TITLE", "2020", "BLURAY"], 1),  # Year, not season
    (["TITLE", "1080P", "BLURAY"], 1),  # Resolution, not season
    (["TITLE", "X265", "BLURAY"], 1),  # Codec, not season
    (["TITLE", "E05", "BLURAY"], 1),  # Episode only, no season
    (["TITLE", "BLURAY", "X265"], 1),  # Quality, not season
    (["TITLE", "DTS", "BLURAY"], 1),  # Audio, not season
    (["TITLE", "SS01", "BLURAY"], 1),  # Invalid double S
    (["TITLE", "SEASONS", "BLURAY"], 1),  # Plural, not matching pattern
    (["TITLE", "S", "BLURAY"], 1),  # S without number following (no dots)
])
def test_extract_season_num_invalid(instance, parts, index):
    """Test that non-season patterns return None."""
    assert instance._extract_season_num(index, parts) is None


# Edge cases - different positions
def test_extract_season_num_at_beginning(instance):
    """Test season at the beginning of parts list."""
    parts = ["S01", "MY", "SHOW", "BLURAY"]
    match = instance._extract_season_num(0, parts)
    assert match is not None
    assert match.group(1) == "01"


def test_extract_season_num_at_end(instance):
    """Test season at the end of parts list."""
    parts = ["MY", "SHOW", "BLURAY", "S01"]
    match = instance._extract_season_num(3, parts)
    assert match is not None
    assert match.group(1) == "01"


def test_extract_season_num_single_element(instance):
    """Test season as the only element."""
    parts = ["S01"]
    match = instance._extract_season_num(0, parts)
    assert match is not None
    assert match.group(1) == "01"


# Edge cases - index boundaries
def test_extract_season_num_index_out_of_bounds(instance):
    """Test that index beyond parts length returns None."""
    parts = ["MY", "SHOW", "S01"]
    assert instance._extract_season_num(10, parts) is None


def test_extract_season_num_negative_index(instance):
    """Test behavior with negative index."""
    parts = ["MY", "SHOW", "S01"]
    # The function will try to combine parts from -1 onward
    result = instance._extract_season_num(-1, parts)
    # Should match S01 at negative index
    assert result is not None


# Common torrent filename scenarios
@pytest.mark.parametrize("parts,index,expected_group", [
    (["GAME", "OF", "THRONES", "S01E01", "1080P", "BLURAY", "X265"], 3, "01"),
    (["THE", "WIRE", "S05", "720P", "WEBRIP"], 2, "05"),
    (["BREAKING", "BAD", "SEASON", "3", "1080P"], 2, "3"),
    (["STRANGER", "THINGS", "S04", "2160P", "NETFLIX"], 2, "04"),
    (["SHOW", "NAME", "2020", "S02E05", "BLURAY"], 3, "02"),
])
def test_extract_season_num_realistic_filenames(instance, parts, index, expected_group):
    """Test season extraction in realistic torrent filename patterns."""
    match = instance._extract_season_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# Empty and minimal inputs
def test_extract_season_num_empty_parts(instance):
    """Test with empty parts list."""
    assert instance._extract_season_num(0, []) is None


def test_extract_season_num_empty_string_part(instance):
    """Test with empty string in parts."""
    parts = ["TITLE", "", "S01"]
    assert instance._extract_season_num(1, parts) is None


# Multiple season patterns in same filename (edge case)
def test_extract_season_num_multiple_seasons(instance):
    """Test filename with multiple season patterns."""
    parts = ["SHOW", "S01", "TO", "S05", "COMPLETE"]
    # First season pattern
    match1 = instance._extract_season_num(1, parts)
    assert match1 is not None
    assert match1.group(1) == "01"
    # Second season pattern
    match2 = instance._extract_season_num(3, parts)
    assert match2 is not None
    assert match2.group(1) == "05"


# Leading zeros vs no leading zeros
@pytest.mark.parametrize("parts,index,expected_group", [
    (["SHOW", "S1", "E1"], 1, "1"),
    (["SHOW", "S01", "E01"], 1, "01"),
    (["SHOW", "S001", "E001"], 1, "001"),
])
def test_extract_season_num_leading_zeros(instance, parts, index, expected_group):
    """Test that season numbers with/without leading zeros are captured correctly."""
    match = instance._extract_season_num(index, parts)
    assert match is not None
    assert match.group(1) == expected_group


# Case sensitivity (should work since patterns are uppercase)
@pytest.mark.parametrize("parts,index", [
    (["SHOW", "S01", "E05"], 1),  # Uppercase (standard after sanitization)
])
def test_extract_season_num_case_sensitivity(instance, parts, index):
    """Test that season patterns match uppercase input (post-sanitization)."""
    match = instance._extract_season_num(index, parts)
    assert match is not None
