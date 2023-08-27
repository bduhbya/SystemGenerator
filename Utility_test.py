import Utility
import pytest
import Tracing
import os
from Unit_test_common import get_test_log_file_name

UTIL_LOGGING = 'utility_test'
UTIL_LOGGING_FILE = get_test_log_file_name(UTIL_LOGGING)
TRACE_LEVEL = Tracing.LOG_LEVEL_DEBUG

test_tracer = None

def clear_test_file():
  try:
    os.remove(UTIL_LOGGING_FILE)
    print(f"clear_test_file, Removed previous test file: {UTIL_LOGGING_FILE}")
  except OSError as e:
    print(f"clear_test_file, Error deleting file  {UTIL_LOGGING_FILE}: {type(e).__name__} - {str(e)}")

def setup_logging():
  global test_tracer
  if test_tracer is None:
    test_tracer = Tracing.LogTrace(UTIL_LOGGING, UTIL_LOGGING_FILE, TRACE_LEVEL)


def clean_logging():
  global test_tracer
  if test_tracer != None:
    test_tracer.close()
    test_tracer = None


def verify_die_roll_result(input, expected):
  result = Utility.parseDie(input, test_tracer)
  assert result == expected, f'Expected {expected}, but got {result}'


def verify_version_result(input, expected):
  result = Utility.parseVersion(input, test_tracer)
  assert result == expected, f'Expected {expected}, but got {result}'


def verify_gen_type_result(input, expected):
  result = Utility.parseGenType(input, test_tracer)
  assert result == expected, f'Expected {expected}, but got {result}'

@pytest.fixture(scope="module", autouse=True)
def setup_module():
  clear_test_file()


@pytest.fixture(autouse=True)
def setup_test(mocker):
  setup_logging()
  
  yield
  clean_logging()
 

def test_none_argument_parseGenType():
  verify_gen_type_result(None, None)


def test_numeric_argument_parseGenType():
  verify_gen_type_result(5, None)


def test_incorrect_argument_parseGenType():
  verify_gen_type_result('not valid', None)


def test_step_argument_parseGenType():
  verify_gen_type_result('step', Utility.GenerationUnitType(genType='step'))


# Parse version tests
def test_empty_argument_parseVersion():
  verify_version_result('', None)


def test_incorrect_argument_parseVersion():
  verify_version_result('200', None)


def test_none_argument_parseVersion():
  verify_version_result(None, None)


def test_numeric_argument_parseVersion():
  verify_version_result(1.1, None)


def test_non_numeric_argument_parseVersion():
  verify_version_result('f.0', None)


def test_correct_argumet_parseVersion():
  verify_version_result('0.1', Utility.ConfigVersion(major=0, minor=1))


# Parse die tests
def test_badly_formatted_argument_parseDie():
  verify_die_roll_result('1.2.1', None)


def test_incorrect_argument_parseDie():
  verify_die_roll_result('5', None)


def test_none_argument_parseDie():
  verify_die_roll_result(None, None)


def test_numeric_argument_parseDie():
  verify_die_roll_result(5, None)


def test_non_numeric_parse_data_argument_parseDie():
  verify_die_roll_result('sd10', None)


def test_badly_format_parse_data_argument_parseDie():
  verify_die_roll_result('1d10d5', None)


def test_one_d10_argument_parseDie():
  verify_die_roll_result('1d10', Utility.DieRoll(numRoles=1, dieType=10))
