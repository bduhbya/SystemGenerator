import argparse
import random
import json
import os

VERSION = 0.1
# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Warhammer 40K FFG System Generator version ' + str(VERSION) + \
                                 '. By default allows user to enter each roll result every time a role is required in the instructions. The options allow for various levels of automating the generation.')

# Add arguments to the parser
parser.add_argument('--configFile', help='Configuration file containing generation steps and instructions')
# parser.add_argument('--age', type=int, help='Age of the user')
parser.add_argument('--automatic', action='store_false', help='Make all rolls for generated content internally without user interaction')
parser.add_argument('--promptOutcome', action='store_false', help='Prompt for user acceptance of each role result. If the user does not like the role, the user can ask for a reroll')

current_directory = os.getcwd()
print(current_directory)

#Constants
TMP_PREFIX = "C:\\SystemGenerator\\"
# TMP_PREFIX = "/storage/emulated/0/qpython/projects3/RogueTrader/SystemGenerator/"
SYSTEM_GEN_STEPS = "system_generation_steps.json"
KEYWORDS = {
	"executeOnStep"
	"defineSteps",
	"steps",
	"diceRoll"
}
ALL_ATTRIBUTES_PROMPT = "all system attributes"

# DICE = {
# 	"d5": 5,
# 	"d10": 10,
# 	"d100": 100,
# }

generationSteps = []

#Temp for developing on moble device 
config_file_path = TMP_PREFIX

def askAutomaticGeneration(prompt):
    manual_entry = input("Generate " + prompt + " automatically? [Y/n]: ")
    manual_entry = manual_entry.strip()
    if len(manual_entry) != 0 and \
    (manual_entry[0] == "N" or manual_entry[0] == "n"):
        return False
    else:
        return True

def getRoll(die, numRolls, modifiers, minimum, maximum):
    roll = 0
    for _ in range(numRolls):
        roll += random.randint(1, die)

    if modifiers:
        for mod in modifiers:
            roll = roll + mod
    if roll < minimum:
        roll = minimum
    elif roll > maximum:
        roll = maximum
    
    return roll

#TODO move into modules
def generateSystem(automatic):
    print("Generating system features...")
    # Open the JSON file
    with open(getFullPath(SYSTEM_GEN_STEPS)) as file:
        # Load the JSON data
        data = json.load(file)

    # Access the parsed data
    print(data)
    steps = data["defineSteps"]
    for step in steps:
        generationSteps.append(step)
    
    print(generationSteps)

def getFullPath(file_name):
    return config_file_path + file_name

def main():
    print()
    print("Warhammer 40K FFG Star System Generator version " + str(VERSION))
    print()
    # all_automatic_entries = askAutomaticGeneration(ALL_ATTRIBUTES_PROMPT)
    args = parser.parse_args()
    all_automatic_entries = args.automatic
    print("Proceeding with options. automatic: " + str(all_automatic_entries))
    
    generateSystem(all_automatic_entries)
    #generateSystemFeatures(all_automatic_entries)
    #random_number = random.randint(1, 5)
    #print("Rand: " + str(random_number))
    

if __name__ == "__main__":
    main()