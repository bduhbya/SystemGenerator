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

High level actions are listed below. Each action is described in further detail.

| Key      | Purpose                                                                                                                                                                                                                                                                                                                                                                                                     |
|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `ver`    | Indicates the version of SysGen the configuration file is written for use with. Each file must contain the `ver` key,                                                                                                                                                                                                                                                                                       |
| `step`   | Describes a step in the generation process. A step is typically the top level item in a generation description.<br><br>Steps are composed of the following keys:<br>- name<br>- save<br>- repeat<br>- steps<br>- rolls<br><br>Steps may reference a separate JSON file. This allows splitting a complex generation specification into multiple files.<br><br><br>Link to step section |
| `roll`   | Describes a randomized event accomplished by a die or dice roll.<br><br>Indicates a random value. The random value is generated based on TTRPG nomenclature of a die or dice and modifiers. Examples:<br>- 1d10<br>- 2d4<br>- 1d20+5<br>- 2d10-5<br><br>If a result is not specified for the outcome of a roll, no action is taken.                                                             |
| `result` | The result of a die/dice roll. A result can be a text value or a step. When a result is a:<br>- step: The step matching the result is executed.<br>- text: The result text is recorded<br><br>Result values are single values or ranges:<br>- 1<br>- 0<br>- 0-4                                                                                                                                             |

_Add instructions to repeat steps and reference/save roll values_

### Step
_Important. ALL steps must have a unique name within the same file._ This allows guaranteed referencing of data generated during step processing.

Steps comprise the high level structure of the specification file. Steps are hierarchical and can be broken down into more steps. Rolls are used to generate the random data out of a step. Steps have the option to save the step output as an entry in the output file to allow for using a step to logically separate a specification into steps used only for intermediate calculations which are not saved in the final output.

Steps may be repeated a set number of times or a random number of times.



## Output files
System data is written to JSON and plain text.