from pathlib import Path
from extractor.base_extractor import BaseExtractor
from models.path_metadata import PathMetadata, FormatType, UnknownType

class PathExtractor(BaseExtractor):

    @classmethod
    def extract_metadata(cls, path: Path) -> PathMetadata:
        cls._logger.debug(f'Extracting path metadata for: {path}')
        
        metadata = PathMetadata()
        # Parts includes ext to enable file/mime type extraction
        parts = cls._get_sanitized_path_parts(path)

        metadata.is_dir = path.is_dir()
        metadata.is_file = path.is_file()
        metadata.format_type = cls._extract_format_type(parts) 
        metadata.ext = cls._extract_ext(parts)

        cls._logger.debug(f'Extracted path metadata - is_dir: {metadata.is_dir}, '
                                f'is_file: {metadata.is_file}, format_type: {metadata.format_type}, '
                                f'ext: {metadata.ext}')

        return metadata

    @classmethod
    def _extract_format_type(cls, parts: list[str]) -> FormatType | UnknownType:

        for i, _ in enumerate(parts):
            if cls._is_video_ext(i, parts):
                cls._logger.debug('Detected format type: VIDEO')
                return 'VIDEO'
            elif cls._is_subtitle_ext(i, parts):
                cls._logger.debug('Detected format type: SUBTITLE')
                return 'SUBTITLE'
            # TODO Audio files currently disabled
            #elif cls._is_audio_ext(i, parts):
            #    return 'AUDIO'

        return 'UNKNOWN'


    @classmethod
    def _extract_ext(cls, parts: list[str]) -> str:

        for i, _ in enumerate(parts):
            if (match := cls._is_ext(i, parts)):
                ext = match.group(0)
                cls._logger.debug(f'Extracted extension: {ext}')
                return ext

        return ''
