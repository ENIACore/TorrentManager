from pathlib import Path
from extractor.base_extractor import BaseExtractor
from models.path_metadata import PathMetadata, FormatType

class PathExtractor(BaseExtractor):


    def extract_metadata(self, path: Path) -> PathMetadata:
        metadata = PathMetadata()
        # Parts includes ext to enable file/mime type extraction
        parts = self._get_sanitized_path_parts(path)


        metadata.is_dir = path.is_dir()
        metadata.is_file = path.is_file()
        metadata.format_type = self._extract_format_type(parts) 
        metadata.ext = self._extract_ext(parts)


        return metadata

    def _extract_format_type(self, parts: list[str]) -> FormatType | None:

        for i, _ in enumerate(parts):
            if self._is_video_ext(i, parts):
                return 'VIDEO'
            elif self._is_subtitle_ext(i, parts):
                return 'SUBTITLE'
            # TODO Audio files currently disabled
            #elif self._is_audio_ext(i, parts):
            #    return 'AUDIO'

        return None

    def _extract_ext(self, parts: list[str]) -> str | None:

        for i, _ in enumerate(parts):
            if (match := self._is_ext(i, parts)):
                return match.group(0)

        return None
