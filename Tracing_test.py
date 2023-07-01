import pytest
from Tracing import LogTrace, LOG_LEVEL_DEBUG
import os

TEST_LOG_FILE = "test_log_file.txt"

def get_file_content():
    try:
        with open(TEST_LOG_FILE, "r") as file:
            content = file.read()
            return content
    except Exception as e:
      print(f"An error occurred: {e}")

def log_contains(value, logContent):
    return value in logContent

@pytest.fixture(autouse=True)
def tracing_test_setup():
    # Code to be executed before each test
    # Perform any necessary setup or initialization here
    try:
        os.remove(TEST_LOG_FILE)
        print("tracing_test_setup, Removed previous test file: " + TEST_LOG_FILE)
    except OSError as e:
        print(f"tracing_test_setup, Error deleting the file: {e}")


def test_error_logging():
    tracer = LogTrace('test_tracer', TEST_LOG_FILE, LOG_LEVEL_DEBUG)
    tracer.error('An error occurred. {error_code}', error_code=123)
    content = get_file_content()
    assert log_contains('An error occurred.', content)
    # assert len(logs) == 1