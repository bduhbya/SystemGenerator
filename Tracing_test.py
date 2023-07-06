import pytest
from Tracing import LogTrace, LOG_LEVEL_DEBUG, LOG_LEVEL_INFO, LOG_LEVEL_WARNING, LOG_LEVEL_ERROR
import os

TEST_LOG_FILE = 'test_log_file.txt'

ERROR = 0
WARNING = 1
INFO = 2
DEBUG = 3
LOG_TEST_DATA = [
  {
    'LOG_LINE':'error log trace',
    'LINE_TYPE':'| ERROR |'
  },
  {
    'LOG_LINE':'warning log trace',
    'LINE_TYPE':'| WARNING |'
  },
  {
    'LOG_LINE':'info log trace',
    'LINE_TYPE':'| INFO |'
  },
  {
    'LOG_LINE':'debug log trace',
    'LINE_TYPE':'| DEBUG |'
  }
]

def get_file_content():
  try:
    with open(TEST_LOG_FILE, "r") as file:
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

def log_and_verify(traceFun, type, shouldLog):
  line = LOG_TEST_DATA[type].get('LOG_LINE')
  lineType = LOG_TEST_DATA[type].get('LINE_TYPE')
  traceFun(line)
  content = get_file_content()
  assert log_contains(line, content) == shouldLog, f"Expected {line} in log to be {shouldLog}"
  assert log_contains(lineType, content) == shouldLog, f"Expected {lineType} in log to be {shouldLog}"

def check_line_count(logFile, count):
  actual = count_lines(logFile)
  assert actual == count, f"Expected {count} lines in {logFile}, found {actual}"

@pytest.fixture(autouse=True)
def tracing_test_setup():
  # Code to be executed before each test
  # Perform any necessary setup or initialization here
  try:
    os.remove(TEST_LOG_FILE)
    print("tracing_test_setup, Removed previous test file: " + TEST_LOG_FILE)
  except OSError as e:
    print(f"tracing_test_setup, Error deleting the file: {e}")

def test_debug_logging():
  tracer = LogTrace('test_tracer', TEST_LOG_FILE, LOG_LEVEL_DEBUG)
  log_and_verify(tracer.debug, DEBUG, True)
  check_line_count(TEST_LOG_FILE, 1)
  log_and_verify(tracer.info, INFO, True)
  check_line_count(TEST_LOG_FILE, 2)
  log_and_verify(tracer.warning, WARNING, True)
  check_line_count(TEST_LOG_FILE, 3)
  log_and_verify(tracer.error, ERROR, True)
  check_line_count(TEST_LOG_FILE, 4)

def test_info_logging():
  tracer = LogTrace('test_tracer', TEST_LOG_FILE, LOG_LEVEL_INFO)
  log_and_verify(tracer.debug, DEBUG, False)
  check_line_count(TEST_LOG_FILE, 0)
  log_and_verify(tracer.info, INFO, True)
  check_line_count(TEST_LOG_FILE, 1)
  log_and_verify(tracer.warning, WARNING, True)
  check_line_count(TEST_LOG_FILE, 2)
  log_and_verify(tracer.error, ERROR, True)
  check_line_count(TEST_LOG_FILE, 3)

def test_warn_logging():
  tracer = LogTrace('test_tracer', TEST_LOG_FILE, LOG_LEVEL_WARNING)
  log_and_verify(tracer.debug, DEBUG, False)
  check_line_count(TEST_LOG_FILE, 0)
  log_and_verify(tracer.info, INFO, False)
  check_line_count(TEST_LOG_FILE, 0)
  log_and_verify(tracer.warning, WARNING, True)
  check_line_count(TEST_LOG_FILE, 1)
  log_and_verify(tracer.error, ERROR, True)
  check_line_count(TEST_LOG_FILE, 2)

def test_error_logging():
  tracer = LogTrace('test_tracer', TEST_LOG_FILE, LOG_LEVEL_ERROR)
  log_and_verify(tracer.debug, DEBUG, False)
  check_line_count(TEST_LOG_FILE, 0)
  log_and_verify(tracer.info, INFO, False)
  check_line_count(TEST_LOG_FILE, 0)
  log_and_verify(tracer.warning, WARNING, False)
  check_line_count(TEST_LOG_FILE, 0)
  log_and_verify(tracer.error, ERROR, True)
  check_line_count(TEST_LOG_FILE, 1)
