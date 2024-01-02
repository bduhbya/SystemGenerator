# SystemGenerator

The System Generator is intended to generate star System data for Warhammer 40K Rogue Trader and related TTRPG games.

To make customization easier, creation of the star system elements is coded into JSON configuration files. The standard configuration files are adapted from the Rogue Trader Stars of Inequity source book.

The generated system is saved as JSON and as plain text.

## Usage

_TBD_

_Considering options for:_
- Automatically roll all random values
- Automatically roll and ask user to confirm or reroll
- Let user pick each value
- Generate plain text from JSON file

Run with -h to get usage documentation from the script.

## Input files

JSON template 

## Parsing language

_TBD_

### Generator actions

High level descriptions of the supported parser actions are listed below. Each action is described in further detail in it's dedicated section.

| Key      | Purpose                                                                                                                                                                                                                                                                                                                                                                                                     |
|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `ver`    | Indicates the version of SysGen the configuration file is written for use with. Each file must contain the `ver` key,                                                                                                                                                                                                                                                                                       |
| `step`   | Describes a step in the generation process. A step is typically the top level item in a generation description.<br>Link to step section |
| `roll`   | Describes a randomized event accomplished by a die or dice roll.                                                             |
| `result` | The result of a die/dice roll. A result can be a text value or a step. When a result is a:<br>- step: The step matching the result is executed.<br>- text: The result text is recorded<br><br>Result values are single values or ranges:<br>- 1<br>- 0<br>- 0-4                                                                                                                                             |
| `save` | Save the step as an object in output hierarchy |
| `repeat` | Repeat the step or result generation the specified number of times  |

_Add instructions to repeat steps and reference/save roll values_

### Step
_Important. ALL steps must have a unique name within the same file._ This allows guaranteed referencing of data generated during step processing.

Steps comprise the high level structure of the specification file. Steps are hierarchical and can be broken down into more steps. sub-steps create a hierarchical json output generation object.

Rolls are used to generate the random data out of a step. Steps have the option to save the step output as an entry in the output file to allow for using a step to logically separate a specification into steps used only for intermediate calculations which are not saved in the final output.

Steps may be repeated a set number of times or a random number of times. Repeated steps generate an array.

Step composition:

| Entry    | Required | Value                                                 | Generation Entity Output                                                                                                                                         | Description                                                                                                                                                                                                                                                     |
|----------|----------|-------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `name`   | Y        | Any string                                            | If `save` requested, Json object with:<br>-key: `name`<br>-field name as `name`<br><br>Note that duplicate names may have the generation file attached if needed | File unique name of step                                                                                                                                                                                                                                        |
| `save`   | Y        | -`y`<br>-`n`                                          | If `y`, create json object as described in `name` description                                                                                                    | Should the step itself be saved as an output object.<br>-`y`: save the step as a unique generation entity<br>-`n`: do save the step itself as a unique generation entity                                                                                        |
| `repeat` | N        | - Any integer<br>- die/dice roll string in format xdx | Create json array of roll results within the object based repetition value                                                                                       | Repeats the step as requested                                                                                                                                                                                                                                   |
| `step`   | N        | - A step entry<br>- File path to input file           | Processes the step as a json object within this step as applicable to step processing.                                                                           | The result of a die/dice roll. A result can be a text value or a step. When a result is a:<br>- step: The step matching the result is executed.<br>- text: The result text is recorded<br><br>Result values are single values or ranges:<br>- 1<br>- 0<br>- 0-4 |
| `roll`   | N        | Xdx+n                                                 | Creates a json key-value pair based on the roll result                                                                                                           | Describes a randomized event accomplish by a die or dice roll as described by the `roll` section.                                                                                                                                                               |


## Output files
System data is written to JSON and plain text.