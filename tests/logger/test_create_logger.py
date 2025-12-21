from logger.logger import Logger
from pathlib import Path
import pytest
import logging

@pytest.fixture
def test_timestamp():
    return '20231208_143000'

@pytest.fixture
def logger_instance(mocker, tmp_path, test_timestamp):
    test_manager_path = tmp_path

    mocker.patch('logger.logger.MANAGER_PATH', str(test_manager_path))

    # Mock datetime.now() for timestamp
    mock_datetime = mocker.patch('logger.logger.datetime')
    mock_datetime.now.return_value.strftime.return_value = test_timestamp
    
    yield Logger()

    Logger.reset()
    Logger._instance = None
    Logger._initialized = False

@pytest.fixture
def mock_get_logger(mocker):
    return mocker.patch('logger.logger.logging.getLogger')

@pytest.fixture
def mock_file_handler(mocker):
    mock = mocker.patch('logger.logger.logging.FileHandler')
    return mock


def test_logger_name_includes_timestamp(mock_get_logger, logger_instance, test_timestamp):
    mock_get_logger.reset_mock() # Reset mock prior to targeted function call
    logger_instance._create_logger(test_timestamp)

    mock_get_logger.assert_called_once_with(f"torrent_manager_{test_timestamp}")

def test_handler_file_path(mock_file_handler, logger_instance, test_timestamp, tmp_path):
    test_session_path = tmp_path / 'logs' / test_timestamp
    info_log_path = Path(test_session_path / 'info.log')
    error_log_path = Path(test_session_path / 'error.log')
    debug_log_path = Path(test_session_path / 'debug.log')

    mock_file_handler.reset_mock() # Reset mock prior to targeted function call
    logger_instance._create_logger(test_timestamp)


    mock_file_handler.assert_any_call(info_log_path, encoding="utf-8") # Test info handler file
    mock_file_handler.assert_any_call(error_log_path, encoding="utf-8") # Test error handler file
    mock_file_handler.assert_any_call(debug_log_path, encoding="utf-8") # Test debug handler file

def test_log_file(logger_instance, test_timestamp, tmp_path):
    test_session_path = tmp_path / 'logs' / test_timestamp
    info_log_path = Path(test_session_path / 'info.log')
    error_log_path = Path(test_session_path / 'error.log')
    debug_log_path = Path(test_session_path / 'debug.log')

    logger_instance._create_logger(test_timestamp)

    assert info_log_path.is_file() is True
    assert error_log_path.is_file() is True
    assert debug_log_path.is_file() is True


def test_handler_levels(logger_instance):

    levels = [handler.level for handler in logger_instance._logger.handlers] 
    assert levels.count(logging.DEBUG) == 2 # Debug has file and console handler
    assert levels.count(logging.INFO) == 1
    assert levels.count(logging.ERROR) == 1


@pytest.mark.parametrize("handler_level,record_level,expected", [
    (logging.DEBUG, logging.DEBUG, True),
    (logging.DEBUG, logging.INFO, True),
    (logging.DEBUG, logging.WARNING, True),
    (logging.DEBUG, logging.ERROR, True),
    (logging.DEBUG, logging.CRITICAL, True),
    (logging.INFO, logging.DEBUG, False),
    (logging.INFO, logging.INFO, True),
    (logging.INFO, logging.WARNING, True),
    (logging.INFO, logging.ERROR, False),
    (logging.INFO, logging.CRITICAL, False),
    (logging.ERROR, logging.DEBUG, False),
    (logging.ERROR, logging.INFO, False),
    (logging.ERROR, logging.WARNING, False),
    (logging.ERROR, logging.ERROR, True),
    (logging.ERROR, logging.CRITICAL, True),
])
def test_handler_filters_parametrized(logger_instance, handler_level, record_level, expected):
    record = logging.LogRecord(
        name="test", level=record_level, pathname="", lineno=0,
        msg="message", 
        args=(), exc_info=None
    )
    
    handler = next(h for h in logger_instance._logger.handlers if h.level == handler_level)
    assert bool(handler.filter(record)) == expected

