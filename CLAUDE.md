# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TorrentManager is a Python-based media file metadata extraction and standardization tool. It parses torrent file/directory names to extract media information (title, year, season, episode) and quality attributes (resolution, codec, quality, audio), then formats them into standardized filename conventions.

## Architecture

### Core Components

**models/media_metadata.py** - `MediaMetadata` class
- Data class holding parsed media attributes
- Implements `__str__()` to format metadata into standardized filename format (e.g., "Title.2025.01.001.1080p.x265.BluRay.DUAL")
- `_format_title()` normalizes titles: lowercases, removes special chars/quotes, capitalizes words, joins with dots

**extractor/media_extractor.py** - `MediaExtractor` class
- Extracts metadata from file/directory paths using pattern matching
- `_get_sanitized_file_or_dir()` preprocesses filenames: uppercase, removes quotes/special chars, splits by dots
- `_is_valid_year()` validates years are 4-digit numbers between 1900 and current year
- Uses regex pattern matching against constants defined in config
- Still in development - many extraction methods are stubs

**config/constants.py**
- Defines regex patterns for matching media attributes in filenames
- `RESOLUTION_PATTERNS` maps resolution labels (8K, 4K, 2K, 1080p, etc.) to pattern lists
- Patterns designed for use with `re.fullmatch()` on individual filename parts

### Project Structure

```
models/          - Data models (MediaMetadata)
extractor/       - Extraction logic (MediaExtractor)
config/          - Configuration and constants
tests/           - Test suite
old/             - Legacy code and reference files
```

## Development Commands

### Testing

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_media_metadata.py
```

Run tests matching pattern:
```bash
pytest -k "test_name_pattern"
```

### Environment

Python virtual environment is in `venv/` (Python 3.14). Activate with:
```bash
source venv/bin/activate
```

Dependencies in `requirements.txt`:
- pytest 9.0.1 - Testing framework
- pygments 2.19.2 - Syntax highlighting

## Testing Conventions

- Test files follow pattern `test_<module>_<function>.py` for method-specific tests
- Use pytest fixtures for reusable test data (e.g., `base_metadata` fixture)
- Parametrize tests for multiple input scenarios with `@pytest.mark.parametrize`
- Methods marked as "Tested ✅" have corresponding test coverage
- Methods marked "Testing not needed ✅" are simple enough to not require tests

## Pattern Matching Implementation

The extractor uses a multi-step approach:
1. Sanitize filename to uppercase with dot separators via `_get_sanitized_file_or_dir()`
2. Split sanitized name into parts by dots
3. Match parts against regex patterns from constants
4. For multi-part patterns (containing dots), recombine adjacent parts before matching

Example: "My.Movie.2020.1080p" → ["MY", "MOVIE", "2020", "1080P"] → extract year (2020), resolution (1080p)
