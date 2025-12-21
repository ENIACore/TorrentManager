from models.path_metadata import PathMetadata

def test_member_variables():
    metadata = PathMetadata()
    metadata.is_dir = True
    metadata.is_file = True
    metadata.format_type = 'VIDEO'
    metadata.ext = '.mp4'


    assert metadata.is_dir == True
    assert metadata.is_file == True
    assert metadata.format_type == 'VIDEO'
    assert metadata.ext == '.mp4'


