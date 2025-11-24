
class FileClassifier:
    def __init__(self) -> None:
        pass

    """
        metadata.format_type = self.extract_format_type(path)
        metadata.ext = self.extract_ext(path)



    def extract_ext(self, path: Path) -> str | None:
        parts = self._get_sanitized_file_or_dir(path).split('.')

        for i, _ in enumerate(parts):
            if (match := self._is_ext(i, parts)):
                return match.group(0)

        return None

    def extract_format_type(self, path: Path) -> FormatType | None:
        parts = self._get_sanitized_file_or_dir(path).split('.')

        for i, _ in enumerate(parts):
            if (match := self._is_video_ext(i, parts)):
                return match.group(0)
            elif (match := self._is_subtitle_ext(i, parts)):
                return match.group(0)
            elif (match := self._is_audio_ext(i, parts)):
                return match.group(0)

        return None

    def _is_ext(self, index: int, parts: list[str]) -> Match[str] | None:

        if (match := self._is_video_ext(index, parts)):
            return match
        if (match := self._is_subtitle_ext(index, parts)):
            return match
        if (match := self._is_audio_ext(index, parts)):
            return match

        return None

    def _is_video_ext(self, index: int, parts: list[str]) -> Match[str] | None:
        for pattern in VIDEO_EXTENSIONS:
            if self._is_matching_tail_len(pattern, index, parts) and (match := self._match_regex(pattern, index, parts)):
                return match

        return None

    def _is_subtitle_ext(self, index: int, parts: list[str]) -> Match[str] | None:
        for pattern in SUBTITLE_EXTENSIONS:
            if self._is_matching_tail_len(pattern, index, parts) and (match := self._match_regex(pattern, index, parts)):
                return match

        return None

    def _is_audio_ext(self, index: int, parts: list[str]) -> Match[str] | None:
        for pattern in AUDIO_EXTENSIONS:
            if self._is_matching_tail_len(pattern, index, parts) and (match := self._match_regex(pattern, index, parts)):
                return match

        return None
    """
