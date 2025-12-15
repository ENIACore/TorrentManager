from logger.logger import Logger
from unittest.mock import Mock
from pathlib import Path

def test_init_values(mocker, tmp_path):
    mock_logger = Mock()
    test_manager_path = tmp_path
    
    # Mock the MANAGER_PATH constant
    mocker.patch('logger.logger.MANAGER_PATH', str(test_manager_path))
    
    # Mock Path.mkdir to prevent actual directory creation
    mock_mkdir = mocker.patch('pathlib.Path.mkdir')
    
    # Mock the _create_logger method
    mock_create_logger = mocker.patch('logger.logger.Logger._create_logger')
    mock_create_logger.return_value = mock_logger
    
    # Mock datetime.now() for timestamp
    mock_datetime = mocker.patch('logger.logger.datetime')
    mock_datetime.now.return_value.strftime.return_value = '20231208_143000'
    
    # Create Logger instance
    logger = Logger()
    
    # Assert manager_path is set correctly
    assert logger.manager_path == Path(test_manager_path)
    
    # Assert log_dir is set correctly
    assert logger.log_dir == Path(test_manager_path) / "logs"
    
    # Assert mkdir was called with correct arguments
    mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    
    # Assert datetime.now().strftime was called with correct format
    mock_datetime.now.assert_called_once()
    mock_datetime.now.return_value.strftime.assert_called_once_with("%Y%m%d_%H%M%S")
    
    # Assert _create_logger was called with the mocked timestamp
    mock_create_logger.assert_called_once_with('20231208_143000')
    
    # Assert _logger is set to the mock logger
    assert logger._logger == mock_logger
    
    # Assert _initialized flag is set
    assert Logger._initialized is True
