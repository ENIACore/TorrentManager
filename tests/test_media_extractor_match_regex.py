import pytest
import re
from extractor.media_extractor import MediaExtractor


@pytest.fixture
def instance():
    return MediaExtractor()


# Single-part pattern tests (pattern without dots)
@pytest.mark.parametrize("pattern,index,parts,should_match", [
    ("1080P", 0, ["1080P"], True),
    ("1080P", 0, ["1080P", "X265"], True),
    ("1080P", 1, ["MOVIE", "1080P"], True),
    ("X265", 0, ["X265", "BLURAY"], True),
    ("BLURAY", 2, ["MOVIE", "2020", "BLURAY"], True),
    # No match cases
    ("1080P", 0, ["720P"], False),
    ("X264", 0, ["X265"], False),
    ("MOVIE", 0, ["FILM"], False),
])
def test_match_regex_single_part(instance, pattern, index, parts, should_match):
    """Test matching single-part patterns (no dots in pattern)."""
    result = instance._match_regex(pattern, index, parts)
    if should_match:
        assert result is not None
        assert isinstance(result, re.Match)
    else:
        assert result is None


# Multi-part pattern tests (pattern with dots)
@pytest.mark.parametrize("pattern,index,parts,should_match", [
    ("S01.E01", 0, ["S01", "E01"], True),
    ("S01.E01", 0, ["S01", "E01", "1080P"], True),
    ("S01.E01", 1, ["MOVIE", "S01", "E01"], True),
    ("X265.BLURAY", 0, ["X265", "BLURAY"], True),
    ("X265.BLURAY", 2, ["MOVIE", "2020", "X265", "BLURAY"], True),
    ("1080P.X265.BLURAY", 0, ["1080P", "X265", "BLURAY"], True),
    ("1080P.X265.BLURAY", 1, ["MOVIE", "1080P", "X265", "BLURAY"], True),
    # No match cases
    ("S01.E01", 0, ["S02", "E01"], False),
    ("S01.E01", 0, ["S01", "E02"], False),
    ("X265.BLURAY", 0, ["X264", "BLURAY"], False),
    ("X265.BLURAY", 0, ["X265", "WEBRIP"], False),
])
def test_match_regex_multi_part(instance, pattern, index, parts, should_match):
    """Test matching multi-part patterns (patterns with dots)."""
    result = instance._match_regex(pattern, index, parts)
    if should_match:
        assert result is not None
        assert isinstance(result, re.Match)
    else:
        assert result is None


# Regex pattern tests
@pytest.mark.parametrize("pattern,index,parts,should_match", [
    # Test patterns with alternation
    ("1080[PI]?", 0, ["1080P"], True),
    ("1080[PI]?", 0, ["1080I"], True),
    ("1080[PI]?", 0, ["1080"], True),
    ("1080[PI]?", 0, ["1080X"], False),
    # Test patterns with character classes
    ("[0-9]+", 0, ["123"], True),
    ("[0-9]+", 0, ["2020"], True),
    ("[0-9]+", 0, ["ABC"], False),
    # Test complex patterns
    ("7680X4320", 0, ["7680X4320"], True),
    ("7680X4320", 0, ["7680X4320P"], False),
])
def test_match_regex_with_regex_patterns(instance, pattern, index, parts, should_match):
    """Test matching with actual regex patterns (not just literal strings)."""
    result = instance._match_regex(pattern, index, parts)
    if should_match:
        assert result is not None
        assert isinstance(result, re.Match)
    else:
        assert result is None


# Edge cases - index boundaries
def test_match_regex_index_at_end(instance):
    """Test when index points to the last element."""
    parts = ["MOVIE", "2020", "1080P"]
    result = instance._match_regex("1080P", 2, parts)
    assert result is not None
    assert isinstance(result, re.Match)


def test_match_regex_index_beyond_end(instance):
    """Test when index is beyond the array length."""
    parts = ["MOVIE", "2020", "1080P"]
    result = instance._match_regex("1080P", 10, parts)
    assert result is None


def test_match_regex_multi_part_pattern_extends_beyond_array(instance):
    """Test when multi-part pattern would extend beyond array length."""
    parts = ["MOVIE", "1080P"]
    # Pattern has 3 parts but only 1 part available from index 1
    result = instance._match_regex("1080P.X265.BLURAY", 1, parts)
    # Should try to match just "1080P" against "1080P.X265.BLURAY" - won't match
    assert result is None


def test_match_regex_pattern_longer_than_remaining_parts(instance):
    """Test when pattern requires more parts than are available."""
    parts = ["MOVIE", "S01"]
    # Pattern needs 2 parts, only 1 remaining from index 1
    result = instance._match_regex("S01.E01", 1, parts)
    assert result is None


# Edge cases - empty and special cases
def test_match_regex_empty_parts_list(instance):
    """Test with an empty parts list."""
    result = instance._match_regex("PATTERN", 0, [])
    assert result is None


def test_match_regex_single_part_in_list(instance):
    """Test with a single-part list."""
    result = instance._match_regex("MOVIE", 0, ["MOVIE"])
    assert result is not None
    assert isinstance(result, re.Match)


def test_match_regex_empty_pattern(instance):
    """Test with an empty pattern."""
    parts = ["MOVIE", "2020"]
    result = instance._match_regex("", 0, parts)
    # Empty pattern should not match non-empty string
    assert result is None


def test_match_regex_empty_part_in_list(instance):
    """Test when parts list contains empty strings."""
    parts = ["MOVIE", "", "2020"]
    result = instance._match_regex("", 1, parts)
    # Empty pattern should match empty part
    assert result is not None


# Real-world torrent filename examples
@pytest.mark.parametrize("pattern,index,parts,expected_match", [
    # Resolution patterns from constants.py
    ("1080[PI]?", 3, ["MOVIE", "NAME", "2020", "1080P", "X265"], True),
    ("4K", 2, ["MOVIE", "2020", "4K", "HDR"], True),
    ("720[PI]?", 3, ["TV", "SHOW", "S01E01", "720P"], True),
    # Codec patterns
    ("X265", 4, ["MOVIE", "2020", "1080P", "BLURAY", "X265"], True),
    ("X264", 3, ["MOVIE", "2020", "720P", "X264"], True),
    # Combined patterns
    ("S[0-9]+", 2, ["SHOW", "NAME", "S01", "E01"], True),
    ("E[0-9]+", 3, ["SHOW", "NAME", "S01", "E01"], True),
])
def test_match_regex_real_world_examples(instance, pattern, index, parts, expected_match):
    """Test with realistic torrent filename patterns."""
    result = instance._match_regex(pattern, index, parts)
    if expected_match:
        assert result is not None
        assert isinstance(result, re.Match)
    else:
        assert result is None


# Return value tests
def test_match_regex_returns_match_object_on_success(instance):
    """Test that successful match returns a re.Match object."""
    result = instance._match_regex("1080P", 0, ["1080P"])
    assert result is not None
    assert isinstance(result, re.Match)
    assert result.group() == "1080P"


def test_match_regex_returns_none_on_failure(instance):
    """Test that failed match returns None."""
    result = instance._match_regex("1080P", 0, ["720P"])
    assert result is None


def test_match_regex_match_object_content(instance):
    """Test that Match object contains expected matched string."""
    parts = ["MOVIE", "2020", "1080P", "X265"]
    result = instance._match_regex("1080P", 2, parts)
    assert result is not None
    assert result.group() == "1080P"


def test_match_regex_multi_part_match_object_content(instance):
    """Test that multi-part Match object contains full matched string."""
    parts = ["MOVIE", "S01", "E01", "1080P"]
    result = instance._match_regex("S01.E01", 1, parts)
    assert result is not None
    assert result.group() == "S01.E01"


# Index variation tests
@pytest.mark.parametrize("index", [0, 1, 2, 3, 4])
def test_match_regex_pattern_found_at_various_indices(instance, index):
    """Test matching pattern at different positions in the parts list."""
    parts = ["A", "B", "TARGET", "C", "D", "E"]
    result = instance._match_regex("TARGET", index, parts)
    if index == 2:
        assert result is not None
    else:
        assert result is None


# Case sensitivity tests
def test_match_regex_case_sensitive(instance):
    """Test that matching is case-sensitive (as per fullmatch behavior)."""
    parts = ["movie", "2020", "1080p"]
    # Pattern is uppercase, part is lowercase
    result = instance._match_regex("1080P", 2, parts)
    assert result is None


def test_match_regex_exact_case_match(instance):
    """Test that exact case match succeeds."""
    parts = ["MOVIE", "2020", "1080P"]
    result = instance._match_regex("1080P", 2, parts)
    assert result is not None


# Partial match tests (fullmatch requires complete match)
def test_match_regex_no_partial_match(instance):
    """Test that partial matches are rejected (fullmatch behavior)."""
    parts = ["1080P-EXTENDED"]
    result = instance._match_regex("1080P", 0, parts)
    # Should not match because fullmatch requires exact match
    assert result is None


def test_match_regex_no_substring_match(instance):
    """Test that substring matches are rejected."""
    parts = ["PREFIX-1080P-SUFFIX"]
    result = instance._match_regex("1080P", 0, parts)
    assert result is None
