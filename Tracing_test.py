import pytest
from Tracing import LogTrace, LOG_LEVEL_DEBUG
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

TRACE_STATEMENT = 'info log trace'
TRACE_LINE = '| TRACE |'

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
  assert count_lines(TEST_LOG_FILE) == 1
  log_and_verify(tracer.info, INFO, True)
  assert count_lines(TEST_LOG_FILE) == 2
  log_and_verify(tracer.warning, WARNING, True)
  assert count_lines(TEST_LOG_FILE) == 3
  log_and_verify(tracer.error, ERROR, True)
  assert count_lines(TEST_LOG_FILE) == 4

def test_error_logging():
  tracer = LogTrace('test_tracer', TEST_LOG_FILE, LOG_LEVEL_DEBUG)
  tracer.error('An error occurred. {error_code}', error_code=123)
  content = get_file_content()
  assert log_contains('An error occurred. 123', content)
  assert log_contains('| ERROR |', content)
  assert count_lines(TEST_LOG_FILE) == 1
