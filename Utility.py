from dataclasses import dataclass
from typing import Type
import Tracing


@dataclass
class DieRoll:
  numRoles: int
  dieType: int


@dataclass
class ConfigVersion:
  major: int
  minor: int


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
    return ConfigVersion(major=parsedVersion[0], minor=parsedVersion[1])

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
    parsedDie = parseIntList(die, tracing, 2, 'd', 'parseDie')
    return DieRoll(numRoles=parsedDie[0], dieType=parsedDie[1])
  except Exception as e:
    tracing.error(f'An exception occurred: {type(e).__name__} - {str(e)}')
    return None


if __name__ == "__main__":
  tracer = Tracing.LogTrace('test_tracer', "Local_test_file.txt",
                            Tracing.LOG_LEVEL_DEBUG)
  tracer.info("Quick local test")
  dieRole = parseDie("1d10", tracing=tracer)
  tracer.info("Die role: " + str(dieRole))
