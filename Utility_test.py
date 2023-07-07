import Utility
import pytest

mocked_LogTrace = None
mocked_instance = None


def clean_mocks():
  global mocked_instance
  global mocked_LogTrace
  mocked_instance = None
  mocked_LogTrace = None


@pytest.fixture(autouse=True)
def mock_handler(mocker):
  global mocked_LogTrace
  global mocked_instance
  mocked_LogTrace = mocker.patch("Tracing.LogTrace")
  mocked_instance = mocked_LogTrace.return_value
  mocked_instance.info.return_value = None
  mocked_instance.error.return_value = None
  yield
  clean_mocks()


def test_empty_argument_parseDie(mocker):
  result = Utility.parseDie('', mocked_instance)
  assert result == None


def test_incorrect_argument_parseDie():
  result = Utility.parseDie('5', mocked_instance)
  assert result == None


def test_none_argument_parseDie():
  result = Utility.parseDie(None, mocked_instance)
  assert result == None


def test_numeric_argument_parseDie():
  result = Utility.parseDie(5, mocked_instance)
  assert result == None


def test_non_numeric_parse_data_argument_parseDie():
  result = Utility.parseDie('sd10', mocked_instance)
  assert result == None


def test_badly_format_parse_data_argument_parseDie():
  result = Utility.parseDie('1d10d5', mocked_instance)
  assert result == None


def test_one_d10_argument_parseDie():
  result = Utility.parseDie('1d10', mocked_instance)
  assert result.numRoles == 1
  assert result.dieType == 10
