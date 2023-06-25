import Utility

def test_empty_argument_parseDie():
    result = Utility.parseDie('')
    assert result == None

def test_incorrect_argument_parseDie():
    result = Utility.parseDie('5')
    assert result == None

def test_none_argument_parseDie():
    result = Utility.parseDie(None)
    assert result == None

def test_numeric_argument_parseDie():
    result = Utility.parseDie(5)
    assert result == None

def test_non_numeric_parse_data_argument_parseDie():
    result = Utility.parseDie('sd10')
    assert result == None

def test_badly_format_parse_data_argument_parseDie():
    result = Utility.parseDie('1d10d5')
    assert result == None

def test_one_d10_argument_parseDie():
    result = Utility.parseDie('1d10')
    assert result.numRoles == 1
    assert result.dieType == 10
