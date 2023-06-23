from dataclasses import dataclass

@dataclass
class DieRoll:
    numRoles: int
    dieType: int

def parseDie(die):
    if die == None:
        return None
    try:
        parts = str.split(die,'d')
        if len(parts) != 2:
            return None
        return DieRoll(numRoles=int(parts[0]), dieType=int(parts[1]))
    except:
            return None
