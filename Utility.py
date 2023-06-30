from dataclasses import dataclass
from typing import Type
import Tracing

@dataclass
class DieRoll:
    numRoles: int
    dieType: int

def parseDie(die, tracing: Type[Tracing.LogTrace]):
    try:
        tracing.info("Parsing: " + die)
        parts = str.split(die,'d')
        if len(parts) != 2:
            tracing.error("Unable to parse die due to bad format: " + die)
            return None
        return DieRoll(numRoles=int(parts[0]), dieType=int(parts[1]))
    except Exception as e:
        tracing.error(f"An exception occurred: {type(e).__name__} - {str(e)}")
        return None

if __name__ == "__main__":
    tracer = Tracing.LogTrace('test_tracer', "Local_test_file.txt", Tracing.LOG_LEVEL_DEBUG)
    tracer.info("Quick local test")
    dieRole = parseDie("1d10", tracing=tracer)
    tracer.info("Die role: " + str(dieRole))