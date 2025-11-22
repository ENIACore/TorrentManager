import pytest
from datetime import datetime
from extractor.media_extractor import MediaExtractor


@pytest.fixture
def instance():
    return MediaExtractor()


# Valid year tests
@pytest.mark.parametrize("year", [
    "1901",  # Just after minimum threshold
    "1950",  # Mid 20th century
    "1980",  # Late 20th century
    "2000",  # Turn of millennium
    "2020",  # Recent year
    "2024",  # Recent year
    str(datetime.now().year),  # Current year
])
def test_is_valid_year_valid_years(instance, year):
    """Test that valid years between 1901 and current year return True."""
    assert instance._is_valid_year(year) is True


# Invalid year tests - out of range
@pytest.mark.parametrize("year", [
    "1900",  # Exactly at threshold (should be invalid based on > 1900)
    "1899",  # Just before minimum threshold
    "1800",  # Way before minimum
    "0",     # Zero
    "1000",  # Medieval times
    str(datetime.now().year + 1),  # Next year (future)
    str(datetime.now().year + 10), # Far future
    "2100",  # Far future
    "3000",  # Very far future
    "9999",  # Extreme future
])
def test_is_valid_year_out_of_range(instance, year):
    """Test that years outside the valid range return False."""
    assert instance._is_valid_year(year) is False


# Invalid year tests - non-numeric strings
@pytest.mark.parametrize("year", [
    "abc",           # Alphabetic
    "20a4",          # Alphanumeric
    "year",          # Word
    "2024.5",        # Decimal
    "2024.0",        # Float-like
    "20 24",         # Contains space
    "2024-01-01",    # Date format
    "",              # Empty string
    "  ",            # Whitespace
    "2024\n",        # Contains newline
    "two thousand",  # Written out
    "-2024",         # Negative number
    "+2024",         # Plus sign
    "2,024",         # Contains comma
])
def test_is_valid_year_non_numeric(instance, year):
    """Test that non-numeric strings return False."""
    assert instance._is_valid_year(year) is False


def test_is_valid_year_boundary_lower(instance):
    """Test the lower boundary (1900 should be invalid, 1901 valid)."""
    assert instance._is_valid_year("1900") is False
    assert instance._is_valid_year("1901") is True


def test_is_valid_year_boundary_upper(instance):
    """Test the upper boundary (current year valid, next year invalid)."""
    current_year = datetime.now().year
    assert instance._is_valid_year(str(current_year)) is True
    assert instance._is_valid_year(str(current_year + 1)) is False


def test_is_valid_year_negative_numbers(instance):
    """Test that negative numbers are handled correctly."""
    assert instance._is_valid_year("-1") is False
    assert instance._is_valid_year("-2024") is False
    assert instance._is_valid_year("-100") is False


def test_is_valid_year_very_large_numbers(instance):
    """Test that very large numbers return False."""
    assert instance._is_valid_year("999999") is False
    assert instance._is_valid_year("12345678") is False


def test_is_valid_year_leading_zeros(instance):
    """Test years with leading zeros."""
    # These should work as int() handles leading zeros
    assert instance._is_valid_year("02024") is True
    assert instance._is_valid_year("002024") is True
    assert instance._is_valid_year("01950") is True


def test_is_valid_year_special_characters(instance):
    """Test that strings with special characters return False."""
    assert instance._is_valid_year("2024!") is False
    assert instance._is_valid_year("@2024") is False
    assert instance._is_valid_year("2024#") is False
    assert instance._is_valid_year("(2024)") is False
    assert instance._is_valid_year("[2024]") is False


# Common torrent file year patterns
@pytest.mark.parametrize("year", [
    "1984",  # Classic movie year
    "1994",  # 90s classic
    "1999",  # Pre-2000
    "2001",  # Post-2000
    "2010",  # 2010s
    "2015",  # Mid 2010s
    "2019",  # Pre-pandemic
    "2021",  # Recent
    "2023",  # Very recent
])
def test_is_valid_year_common_movie_years(instance, year):
    """Test common years found in movie/TV torrent files."""
    assert instance._is_valid_year(year) is True
