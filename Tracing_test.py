import platform
import pytest
from Tracing import LogTrace, LOG_LEVEL_DEBUG, LOG_LEVEL_INFO, LOG_LEVEL_WARNING, LOG_LEVEL_ERROR
from pathlib import Path
from Unit_test_common import get_test_log_file_name, clear_test_file


TEST_LOGGER = 'test_logger'

ERROR = 0
WARNING = 1
INFO = 2
DEBUG = 3

LOG_TEST_DATA = [{
  'LOG_LINE': 'error log trace',
  'LINE_TYPE': '| ERROR |'
}, {
  'LOG_LINE': 'warning log trace',
  'LINE_TYPE': '| WARNING |'
}, {
  'LOG_LINE': 'info log trace',
  'LINE_TYPE': '| INFO |'
}, {
  'LOG_LINE': 'debug log trace',
  'LINE_TYPE': '| DEBUG |'
}]


def get_file_content(fileName):
  try:
    with open(fileName, "r") as file:
      content = file.read()
      return content
  except Exception as e:
    print(f"An error occurred: {e}")


def log_contains(value, logContent):
  return value in logContent


def count_lines(file_path):
  with open(file_path, 'r') as file:
    line_count = sum(1 for line in file)
  return line_count


def get_log_name(method):
  return get_test_log_file_name(__name__ + '-' + method.__name__)

def log_and_verify_file(traceFun, type, shouldLog, method):
  fileName = get_log_name(method)
  line = LOG_TEST_DATA[type].get('LOG_LINE')
  lineType = LOG_TEST_DATA[type].get('LINE_TYPE')
  traceFun(line)
  content = get_file_content(fileName)
  assert log_contains(
    line, content) == shouldLog, f"Expected {line} in log to be {shouldLog}"
  assert log_contains(
    lineType,
    content) == shouldLog, f"Expected {lineType} in log to be {shouldLog}"


def check_line_count(method, count):
  fileName = get_log_name(method)
  actual = count_lines(fileName)
  assert actual == count, f"Expected {count} lines in {fileName}, found {actual}"


def verify_assert_and_no_tracing(expectedAssert, testLogger, logFile, level, logFileName):
  tracer = None
  with pytest.raises(expectedAssert):
    tracer = LogTrace(testLogger, logFile, level)

  file_path = Path(logFileName)
  assert tracer == None, "Expected tracer to be None"
  assert file_path.exists(
  ) == False, f"Expected file {logFileName} to not exist"



def get_logger_and_clean_previous(method, logLevel):
  fileName = get_log_name(method)
  clear_test_file(fileName, f"{__name__} - {method}")
  return LogTrace(method, fileName, logLevel)


def test_debug_logging():
  tracer = get_logger_and_clean_previous(test_debug_logging, LOG_LEVEL_DEBUG)
  log_and_verify_file(tracer.debug, DEBUG, True, test_debug_logging)
  check_line_count(test_debug_logging, 1)
  log_and_verify_file(tracer.info, INFO, True, test_debug_logging)
  check_line_count(test_debug_logging, 2)
  log_and_verify_file(tracer.warning, WARNING, True, test_debug_logging)
  check_line_count(test_debug_logging, 3)
  log_and_verify_file(tracer.error, ERROR, True, test_debug_logging)
  check_line_count(test_debug_logging, 4)


def test_info_logging():
  tracer = get_logger_and_clean_previous(test_info_logging, LOG_LEVEL_INFO)
  log_and_verify_file(tracer.debug, DEBUG, False, test_info_logging)
  check_line_count(test_info_logging, 0)
  log_and_verify_file(tracer.info, INFO, True, test_info_logging)
  check_line_count(test_info_logging, 1)
  log_and_verify_file(tracer.warning, WARNING, True, test_info_logging)
  check_line_count(test_info_logging, 2)
  log_and_verify_file(tracer.error, ERROR, True, test_info_logging)
  check_line_count(test_info_logging, 3)


def test_warn_logging():
  tracer = get_logger_and_clean_previous(test_warn_logging, LOG_LEVEL_WARNING)
  log_and_verify_file(tracer.debug, DEBUG, False, test_warn_logging)
  check_line_count(test_warn_logging, 0)
  log_and_verify_file(tracer.info, INFO, False, test_warn_logging)
  check_line_count(test_warn_logging, 0)
  log_and_verify_file(tracer.warning, WARNING, True, test_warn_logging)
  check_line_count(test_warn_logging, 1)
  log_and_verify_file(tracer.error, ERROR, True, test_warn_logging)
  check_line_count(test_warn_logging, 2)


def test_error_logging():
  tracer = get_logger_and_clean_previous(test_error_logging, LOG_LEVEL_ERROR)
  log_and_verify_file(tracer.debug, DEBUG, False, test_error_logging)
  check_line_count(test_error_logging, 0)
  log_and_verify_file(tracer.info, INFO, False, test_error_logging)
  check_line_count(test_error_logging, 0)
  log_and_verify_file(tracer.warning, WARNING, False, test_error_logging)
  check_line_count(test_error_logging, 0)
  log_and_verify_file(tracer.error, ERROR, True, test_error_logging)
  check_line_count(test_error_logging, 1)


def test_empty_logger_name():
  logger_file_name = get_log_name(test_empty_logger_name)
  tracer = LogTrace('', logger_file_name, LOG_LEVEL_ERROR)
  file_path = Path(logger_file_name)
  assert file_path.exists() == True, f"Expected file {logger_file_name} to exist"


def test_none_logger_name():
  logger_file_name = get_log_name(test_none_logger_name)
  tracer = LogTrace(None, logger_file_name, LOG_LEVEL_ERROR)
  file_path = Path(logger_file_name)
  assert file_path.exists() == True, f"Expected file {logger_file_name} to exist"


def test_empty_file_name():
  expected_assert = None
  if platform.system() == "Windows":
    expected_assert = PermissionError
  else:
    expected_assert = IsADirectoryError
  verify_assert_and_no_tracing(expected_assert, TEST_LOGGER, '',
                               LOG_LEVEL_ERROR, get_log_name(test_empty_file_name))


def test_none_file_name():
  verify_assert_and_no_tracing(RuntimeError, TEST_LOGGER, None,
                               LOG_LEVEL_ERROR, get_log_name(test_none_file_name))


def test_bad_type_log_level():
  name = get_log_name(test_bad_type_log_level)
  verify_assert_and_no_tracing(RuntimeError, TEST_LOGGER, name, 5, name)


def test_bad_value_log_level():
  name = get_log_name(test_bad_value_log_level)
  verify_assert_and_no_tracing(RuntimeError, TEST_LOGGER, name, "5", name)


def test_none_log_level():
  name = get_log_name(test_none_log_level)
  verify_assert_and_no_tracing(RuntimeError, TEST_LOGGER, name, None, name)
