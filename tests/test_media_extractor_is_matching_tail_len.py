import pytest
from extractor.media_extractor import MediaExtractor


@pytest.fixture
def instance():
    return MediaExtractor()


# Basic single-part pattern tests
@pytest.mark.parametrize("pattern,index,parts,expected", [
    # Single-part pattern at end - should match
    ("MKV", 2, ["MOVIE", "2020", "MKV"], True),
    ("MP4", 3, ["TITLE", "1080P", "X265", "MP4"], True),

    # Single-part pattern not at end - should not match
    ("MKV", 1, ["MOVIE", "MKV", "2020"], False),
    ("MP4", 0, ["MP4", "TITLE", "2020"], False),

    # Single-part pattern at beginning (when it's also the end) - should match
    ("MKV", 0, ["MKV"], True),
])
def test_is_matching_tail_len_single_part(instance, pattern, index, parts, expected):
    """Test single-part patterns (e.g., 'MKV', 'MP4')."""
    assert instance._is_matching_tail_len(pattern, index, parts) == expected


# Multi-part pattern tests (patterns containing dots)
@pytest.mark.parametrize("pattern,index,parts,expected", [
    # Two-part pattern at end - should match
    ("X.265", 2, ["MOVIE", "2020", "X", "265"], True),
    ("H.264", 1, ["TITLE", "H", "264"], True),

    # Two-part pattern not at end - should not match
    ("X.265", 1, ["MOVIE", "X", "265", "MKV"], False),
    ("H.264", 0, ["H", "264", "1080P", "MKV"], False),

    # Three-part pattern at end - should match
    ("WEB.DL.1080P", 1, ["MOVIE", "WEB", "DL", "1080P"], True),
    ("BD.RIP.720P", 0, ["BD", "RIP", "720P"], True),

    # Three-part pattern not at end - should not match
    ("WEB.DL.1080P", 0, ["WEB", "DL", "1080P", "X265"], False),
])
def test_is_matching_tail_len_multi_part(instance, pattern, index, parts, expected):
    """Test multi-part patterns with dots (e.g., 'X.265', 'WEB.DL.1080P')."""
    assert instance._is_matching_tail_len(pattern, index, parts) == expected


# Edge case: index at end of parts
@pytest.mark.parametrize("pattern,index,parts,expected", [
    # Index points to last element, pattern is single part - should match
    ("MKV", 4, ["MOVIE", "2020", "1080P", "X265", "MKV"], True),

    # Index points to last element, but pattern has multiple parts - should not match
    ("X.265", 4, ["MOVIE", "2020", "1080P", "X", "265"], False),

    # Index points to second-to-last element, pattern is two parts - should match
    ("X.265", 3, ["MOVIE", "2020", "1080P", "X", "265"], True),
])
def test_is_matching_tail_len_at_end_of_parts(instance, pattern, index, parts, expected):
    """Test patterns when index is at or near the end of parts array."""
    assert instance._is_matching_tail_len(pattern, index, parts) == expected


# Edge case: index out of bounds
@pytest.mark.parametrize("pattern,index,parts,expected", [
    # Index beyond parts length - should not match
    ("MKV", 5, ["MOVIE", "2020", "MKV"], False),
    ("MP4", 10, ["TITLE", "MP4"], False),

    # Index equals parts length - should not match
    ("MKV", 3, ["MOVIE", "2020", "MKV"], False),
])
def test_is_matching_tail_len_index_out_of_bounds(instance, pattern, index, parts, expected):
    """Test behavior when index is beyond the parts array length."""
    assert instance._is_matching_tail_len(pattern, index, parts) == expected


# Edge case: empty parts
def test_is_matching_tail_len_empty_parts(instance):
    """Test with empty parts list."""
    assert instance._is_matching_tail_len("MKV", 0, []) is False


# Edge case: pattern longer than remaining parts
@pytest.mark.parametrize("pattern,index,parts,expected", [
    # Pattern needs 3 parts, but only 2 remaining - should not match
    ("WEB.DL.1080P", 2, ["MOVIE", "2020", "WEB", "DL"], False),

    # Pattern needs 2 parts, but only 1 remaining - should not match
    ("X.265", 2, ["MOVIE", "2020", "X"], False),

    # Pattern needs 4 parts, but only 1 remaining - should not match
    ("A.B.C.D", 3, ["MOVIE", "2020", "X", "Y"], False),
])
def test_is_matching_tail_len_pattern_longer_than_remaining(instance, pattern, index, parts, expected):
    """Test when pattern requires more parts than remain in the array."""
    assert instance._is_matching_tail_len(pattern, index, parts) == expected


# Realistic torrent filename scenarios
@pytest.mark.parametrize("pattern,index,parts,expected", [
    # Video extension at end (typical case) - should match
    ("MKV", 6, ["MOVIE", "NAME", "2020", "1080P", "BLURAY", "X265", "MKV"], True),

    # Codec pattern with dot in middle - should not match at end
    ("X.265", 5, ["MOVIE", "2020", "X", "265", "BLURAY", "MKV"], False),

    # Codec pattern with dot at correct position before extension - should match
    ("X.265", 3, ["MOVIE", "2020", "X", "265", "MKV"], True),

    # Single part in middle that happens to be an extension - should not match
    ("MP4", 2, ["TITLE", "2020", "MP4", "REPACK", "MKV"], False),

    # Extension at very end of long filename - should match
    ("AVI", 9, ["VERY", "LONG", "MOVIE", "TITLE", "2020", "1080P", "X265", "BLURAY", "DUAL", "AVI"], True),
])
def test_is_matching_tail_len_realistic_scenarios(instance, pattern, index, parts, expected):
    """Test realistic torrent filename scenarios."""
    assert instance._is_matching_tail_len(pattern, index, parts) == expected


# Patterns with varying number of parts
@pytest.mark.parametrize("pattern,num_parts_in_pattern", [
    ("SINGLE", 1),
    ("TWO.PARTS", 2),
    ("THREE.PART.PATTERN", 3),
    ("FOUR.PART.PATTERN.HERE", 4),
    ("A.B.C.D.E", 5),
])
def test_is_matching_tail_len_pattern_part_counting(instance, pattern, num_parts_in_pattern):
    """Test that pattern part counting works correctly for various patterns."""
    # Create parts array with exact match at end
    parts = ["PREFIX"] * 3 + pattern.split('.')
    index = len(parts) - num_parts_in_pattern

    # Should match when positioned at the tail
    assert instance._is_matching_tail_len(pattern, index, parts) is True

    # Should not match when not at the tail
    if index > 0:
        assert instance._is_matching_tail_len(pattern, index - 1, parts) is False


# Zero index tests
@pytest.mark.parametrize("pattern,parts,expected", [
    # Pattern matches entire parts array from index 0 - should match
    ("MKV", ["MKV"], True),
    ("X.265", ["X", "265"], True),
    ("A.B.C", ["A", "B", "C"], True),

    # Pattern at index 0 but more parts follow - should not match
    ("MKV", ["MKV", "EXTRA"], False),
    ("X.265", ["X", "265", "EXTRA"], False),
])
def test_is_matching_tail_len_zero_index(instance, pattern, parts, expected):
    """Test patterns starting at index 0."""
    assert instance._is_matching_tail_len(pattern, 0, parts) == expected


# Complex multi-part patterns (4+ parts)
@pytest.mark.parametrize("pattern,index,parts,expected", [
    # Four-part pattern at end - should match
    ("A.B.C.D", 2, ["PREFIX", "X", "A", "B", "C", "D"], True),

    # Four-part pattern not at end - should not match
    ("A.B.C.D", 1, ["PREFIX", "A", "B", "C", "D", "SUFFIX"], False),

    # Five-part pattern at end - should match
    ("ONE.TWO.THREE.FOUR.FIVE", 0, ["ONE", "TWO", "THREE", "FOUR", "FIVE"], True),
])
def test_is_matching_tail_len_complex_patterns(instance, pattern, index, parts, expected):
    """Test complex patterns with many parts."""
    assert instance._is_matching_tail_len(pattern, index, parts) == expected


# Pattern with single dot (two empty parts)
def test_is_matching_tail_len_pattern_edge_cases(instance):
    """Test edge cases in pattern format."""
    # Pattern with actual content
    assert instance._is_matching_tail_len("A.B", 0, ["A", "B"]) is True

    # Pattern with single character parts
    assert instance._is_matching_tail_len("A.B.C.D.E.F", 0, ["A", "B", "C", "D", "E", "F"]) is True


# Negative index (should not occur in practice, but testing behavior)
@pytest.mark.parametrize("pattern,index,parts", [
    ("MKV", -1, ["MOVIE", "MKV"]),
    ("MP4", -2, ["TITLE", "2020", "MP4"]),
])
def test_is_matching_tail_len_negative_index(instance, pattern, index, parts):
    """Test behavior with negative indices (edge case)."""
    # The function calculates: len(parts) - index
    # With negative index: len(parts) - (-1) = len(parts) + 1
    # This should not match pattern length (which is typically 1)
    # For pattern "MKV" (1 part) and parts ["MOVIE", "MKV"] (2 elements):
    # index = -1 → remaining = 2 - (-1) = 3 → 3 ≠ 1 → False
    assert instance._is_matching_tail_len(pattern, index, parts) is False


# Same number of parts but different positions
def test_is_matching_tail_len_same_parts_different_positions(instance):
    """Test that position matters, not just part count."""
    parts = ["A", "B", "C", "D", "E"]
    pattern = "C.D"  # 2-part pattern

    # Should only match at index 3 (positions 3-4, which are "C" and "D" at the end)
    assert instance._is_matching_tail_len(pattern, 3, parts) is True

    # Should not match at other positions
    assert instance._is_matching_tail_len(pattern, 0, parts) is False
    assert instance._is_matching_tail_len(pattern, 1, parts) is False
    assert instance._is_matching_tail_len(pattern, 2, parts) is False
    assert instance._is_matching_tail_len(pattern, 4, parts) is False


# All parts match pattern length but at wrong position
def test_is_matching_tail_len_correct_length_wrong_position(instance):
    """Test patterns with correct length but wrong position in parts array."""
    parts = ["MOVIE", "2020", "1080P", "X265", "BLURAY"]

    # Two-part pattern, but not at the end
    pattern = "1080P.X265"
    assert instance._is_matching_tail_len(pattern, 2, parts) is False  # Not at end

    # Would need to be at index 3 to match the tail
    parts_modified = ["MOVIE", "2020", "1080P", "X265"]
    assert instance._is_matching_tail_len(pattern, 2, parts_modified) is True  # At end
