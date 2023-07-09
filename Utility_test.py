import Utility
import pytest

mocked_LogTrace = None
mocked_instance = None


def clean_mocks():
  global mocked_instance
  global mocked_LogTrace
  mocked_instance = None
  mocked_LogTrace = None


def verify_none_result(input):
  result = Utility.parseDie(input, mocked_instance)
  assert result == None, f'Expected None, but got {result}'

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
  verify_none_result('')


def test_incorrect_argument_parseDie():
  verify_none_result('5')


def test_none_argument_parseDie():
  verify_none_result(None)


def test_numeric_argument_parseDie():
  verify_none_result(5)


def test_non_numeric_parse_data_argument_parseDie():
  verify_none_result('sd10')


def test_badly_format_parse_data_argument_parseDie():
  verify_none_result('1d10d5')


def test_one_d10_argument_parseDie():
  result = Utility.parseDie('1d10', mocked_instance)
  assert result.numRoles == 1
  assert result.dieType == 10
