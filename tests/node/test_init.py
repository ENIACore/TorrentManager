from tree.node import Node
from pathlib import Path
from unittest.mock import Mock
import pytest

def test_init(mocker):
    mocker.patch('extractor.base_extractor.Logger.get_logger', return_value=Mock())

    mocker.patch('tree.node.MediaExtractor.extract_metadata', return_value=Mock())
    mocker.patch('tree.node.PathExtractor.extract_metadata', return_value=Mock())
    node = Node(Path('/test'))
    
    assert node.media_metadata is not None and isinstance(node.media_metadata, Mock)
    assert node.path_metadata is not None and isinstance(node.media_metadata, Mock)
    assert node.original_path == Path('/test')
    assert node.new_path == Path('/')
    assert node.parent_node is None
    assert not node.children_nodes
    assert node.classification == 'UNKNOWN'
