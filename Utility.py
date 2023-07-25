from dataclasses import dataclass
from typing import Type
import Tracing


GENERATION_UNIT_TYPES = [
  'step',
  'roll',
  'result'
]

@dataclass
class DieRoll:
  numRoles: int
  dieType: int


@dataclass
class ConfigVersion:
  major: int
  minor: int


@dataclass
class GenerationUnitType:
 genType: str


def parseIntList(strValue: str, tracing: Type[Tracing.LogTrace], numParts: int,
                 split: str, source: str):
  """
  This function divides a string into integer parts. NO exception handling is provided.
  Callers are expected to deal with exceptions.

  Parameters:
  
  strValue: str - String to split
  tracing: Type[Tracing.LogTrace] - Tracing object
  numParts: int - expected number of parts
  split: str - Key for splitting string
  source: str - caller info for tracing

  Return:

  List of int containing converted values or throws exception
  """
  tracing.info(f'Parsing: {strValue} for {source}')
  parts = str.split(strValue, split)
  if len(parts) != numParts:
    tracing.error(
      f'Unable to parse for {source} due to bad format: {strValue}')
    return None

  returnList = []
  for value in parts:
    returnList.append(int(value))
  return returnList


def validateGenType(genType: str, tracing: Type[Tracing.LogTrace]):
  """
  This function validates if the generation unit type is present in the acceptable
  types. 

  Parameters:
  
  strValue: str - Generation unit to validate
  tracing: Type[Tracing.LogTrace] - Tracing object

  Return:

  boolean: true for valid type, false otherwise. Throws exception on
  bad input types
  """
  tracing.info(f'Validating input: {genType}')
  if genType in GENERATION_UNIT_TYPES:
    tracing.info(f'{genType} is valid type')
    return True
  else:
    tracing.warning(f'{genType} not valid. Valid types: {GENERATION_UNIT_TYPES}')
    return False


def parseVersion(versionStr: str, tracing: Type[Tracing.LogTrace]):
  '''
  Parses file version from json version key's value

  Parameters

  versionStr: str - version value in string form of x.x
  tracing: Type[Tracing.LogTrace] - tracing object

  Return

  DieRoll object or None
  '''
  try:
    tracing.info(f'Parsing: {versionStr}')
    parsedVersion = parseIntList(versionStr, tracing, 2, '.', 'parseVersion')
    retVal = ConfigVersion(major=parsedVersion[0], minor=parsedVersion[1])
    tracing.info(f'Parsed successfully: {retVal}')
    return retVal

  except Exception as e:
    tracing.error(f'An exception occurred: {type(e).__name__} - {str(e)}')
    return None


def parseDie(die: str, tracing: Type[Tracing.LogTrace]):
  '''
  Parses die roll from die json key's value

  Parameters

  die: str - die roll in string form of xdx
  tracing: Type[Tracing.LogTrace] - tracing object

  Return

  ConfigVersion object or None
  '''
  try:
    tracing.info(f'Parsing: {die}')
    parsedDie = parseIntList(die, tracing, 2, 'd', 'parseDie')
    retVal = DieRoll(numRoles=parsedDie[0], dieType=parsedDie[1])
    tracing.info(f'Parsed successfully: {retVal}')
    return retVal
  except Exception as e:
    tracing.error(f'An exception occurred: {type(e).__name__} - {str(e)}')
    return None

def parseGenType(genType: str, tracing: Type[Tracing.LogTrace]):
  '''
  Parses the generation unit type.

  Parameters

  genType: str - Generation unit type
  tracing: Type[Tracing.LogTrace] - tracing object

  Return

  Str object or None
  '''
  try:
    tracing.info(f'Parsing: {genType}')
    if validateGenType(genType, tracing):
      tracing.info(f'Parsed successfully: {genType}')
      return GenerationUnitType(genType=genType)
    else:
      tracing.warning(f'{genType} is not a supported generation unit type')
      return None
  except Exception as e:
    tracing.error(f'An exception occurred: {type(e).__name__} - {str(e)}')
    return None


if __name__ == "__main__":
  tracer = Tracing.LogTrace('test_tracer', "Local_test_file.txt",
                            Tracing.LOG_LEVEL_DEBUG)
  tracer.info("Quick local test")
  dieRole = parseDie("1d10", tracing=tracer)
  tracer.info("Die role: " + str(dieRole))
