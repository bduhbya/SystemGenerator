import pytest
from Tracing import LogTrace, LOG_LEVEL_DEBUG, LOG_LEVEL_INFO, LOG_LEVEL_WARNING, LOG_LEVEL_ERROR
import os
from pathlib import Path

TEST_LOG_FILE = 'test_log_file.txt'
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


def get_file_content():
  try:
    with open(TEST_LOG_FILE, "r") as file:
      content = file.read()
      return content
  except Exception as e:
    print(f"An error occurred: {e}")


def get_file_content_2(fileName):
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


def log_and_verify_file(traceFun, type, shouldLog, method):
  fileName = method.__name__ + "_" + TEST_LOG_FILE
  line = LOG_TEST_DATA[type].get('LOG_LINE')
  lineType = LOG_TEST_DATA[type].get('LINE_TYPE')
  traceFun(line)
  content = get_file_content_2(fileName)
  assert log_contains(
    line, content) == shouldLog, f"Expected {line} in log to be {shouldLog}"
  assert log_contains(
    lineType,
    content) == shouldLog, f"Expected {lineType} in log to be {shouldLog}"


def log_and_verify(traceFun, type, shouldLog):
  line = LOG_TEST_DATA[type].get('LOG_LINE')
  lineType = LOG_TEST_DATA[type].get('LINE_TYPE')
  traceFun(line)
  content = get_file_content()
  assert log_contains(
    line, content) == shouldLog, f"Expected {line} in log to be {shouldLog}"
  assert log_contains(
    lineType,
    content) == shouldLog, f"Expected {lineType} in log to be {shouldLog}"


def check_line_count(logFile, count):
  actual = count_lines(logFile)
  assert actual == count, f"Expected {count} lines in {logFile}, found {actual}"


def check_line_count_2(method, count):
  logFile = method.__name__ + "_" + TEST_LOG_FILE
  actual = count_lines(logFile)
  assert actual == count, f"Expected {count} lines in {logFile}, found {actual}"


def verify_assert_and_no_tracing(expectedAssert, testLogger, logFile, level):
  tracer = None
  with pytest.raises(expectedAssert):
    tracer = LogTrace(testLogger, logFile, level)

  file_path = Path(TEST_LOG_FILE)
  assert tracer == None, "Expected tracer to be None"
  assert file_path.exists(
  ) == False, f"Expected file {TEST_LOG_FILE} to not exist"



def clear_test_file(name):
  try:
    os.remove(name)
    print(f"clear_test_file, Removed previous test file: {name}")
  except OSError as e:
    print(f"clear_test_file, Error deleting file  {name}: {type(e).__name__} - {str(e)}")


def get_logger_and_clean_previous(method, logLevel):
  fileName = method.__name__ + "_" + TEST_LOG_FILE
  clear_test_file(fileName)
  return LogTrace(method, fileName, logLevel)


# def setup_logging():
#   global test_tracer
#   if test_tracer is None:
#     test_tracer = Tracing.LogTrace(UTIL_LOGGING, UTIL_LOGGING_FILE, TRACE_LEVEL)


@pytest.fixture(autouse=True)
def tracing_test_setup():
  # Code to be executed before each test
  try:
    os.remove(TEST_LOG_FILE)
    print("tracing_test_setup, Removed previous test file: " + TEST_LOG_FILE)
  except OSError as e:
    print(f"tracing_test_setup, Error deleting the file: {e}")


def test_debug_logging():
  tracer = get_logger_and_clean_previous(test_debug_logging, LOG_LEVEL_DEBUG)
  log_and_verify_file(tracer.debug, DEBUG, True, test_debug_logging)
  check_line_count_2(test_debug_logging, 1)
  log_and_verify_file(tracer.info, INFO, True, test_debug_logging)
  check_line_count_2(test_debug_logging, 2)
  log_and_verify_file(tracer.warning, WARNING, True, test_debug_logging)
  check_line_count_2(test_debug_logging, 3)
  log_and_verify_file(tracer.error, ERROR, True, test_debug_logging)
  check_line_count_2(test_debug_logging, 4)


def test_info_logging():
  tracer = LogTrace(TEST_LOGGER, TEST_LOG_FILE, LOG_LEVEL_INFO)
  log_and_verify(tracer.debug, DEBUG, False)
  check_line_count(TEST_LOG_FILE, 0)
  log_and_verify(tracer.info, INFO, True)
  check_line_count(TEST_LOG_FILE, 1)
  log_and_verify(tracer.warning, WARNING, True)
  check_line_count(TEST_LOG_FILE, 2)
  log_and_verify(tracer.error, ERROR, True)
  check_line_count(TEST_LOG_FILE, 3)


def test_warn_logging():
  tracer = LogTrace(TEST_LOGGER, TEST_LOG_FILE, LOG_LEVEL_WARNING)
  log_and_verify(tracer.debug, DEBUG, False)
  check_line_count(TEST_LOG_FILE, 0)
  log_and_verify(tracer.info, INFO, False)
  check_line_count(TEST_LOG_FILE, 0)
  log_and_verify(tracer.warning, WARNING, True)
  check_line_count(TEST_LOG_FILE, 1)
  log_and_verify(tracer.error, ERROR, True)
  check_line_count(TEST_LOG_FILE, 2)


def test_error_logging():
  tracer = LogTrace(TEST_LOGGER, TEST_LOG_FILE, LOG_LEVEL_ERROR)
  log_and_verify(tracer.debug, DEBUG, False)
  check_line_count(TEST_LOG_FILE, 0)
  log_and_verify(tracer.info, INFO, False)
  check_line_count(TEST_LOG_FILE, 0)
  log_and_verify(tracer.warning, WARNING, False)
  check_line_count(TEST_LOG_FILE, 0)
  log_and_verify(tracer.error, ERROR, True)
  check_line_count(TEST_LOG_FILE, 1)


def test_empty_logger_name():
  tracer = LogTrace('', TEST_LOG_FILE, LOG_LEVEL_ERROR)
  file_path = Path(TEST_LOG_FILE)
  assert file_path.exists() == True, f"Expected file {TEST_LOG_FILE} to exist"


def test_none_logger_name():
  tracer = LogTrace(None, TEST_LOG_FILE, LOG_LEVEL_ERROR)
  file_path = Path(TEST_LOG_FILE)
  assert file_path.exists() == True, f"Expected file {TEST_LOG_FILE} to exist"


def test_empty_file_name():
  verify_assert_and_no_tracing(IsADirectoryError, TEST_LOGGER, '',
                               LOG_LEVEL_ERROR)


def test_none_file_name():
  verify_assert_and_no_tracing(RuntimeError, TEST_LOGGER, None,
                               LOG_LEVEL_ERROR)


def test_bad_type_log_level():
  verify_assert_and_no_tracing(RuntimeError, TEST_LOGGER, TEST_LOG_FILE, 5)


def test_bad_value_log_level():
  verify_assert_and_no_tracing(RuntimeError, TEST_LOGGER, TEST_LOG_FILE, "5")


def test_none_log_level():
  verify_assert_and_no_tracing(RuntimeError, TEST_LOGGER, TEST_LOG_FILE, None)
