<!-- cspell:words epub pylint pytest -->

# Document Manipulation



## Overview

Document Manipulation is a toolkit and scripts for manipulating text documents. It originates from my need to create EPUB files as part of my publishing activity and as of now remains a work in progress.

The project is open source software. See [About](About.md) for more information.



## Development

The project is developed using Python and should support the usual workflows with `pip`, `pylint` and `pytest`. It is highly recommended to use a Python virtual environment.

Additionally, there are commands to automate development related tasks, as can be found under [Automation](Automation). The script `Automation/Setup/setup.py` sets up a local workspace with a Python virtual environment. After that's done, the commands can be executed through the `Automation/Scripts/automation_scripts/run_command.py` script, which you might want to run as a module using `python -m automation_scripts.run_command`. Use the scripts with the `--help` option for information, as well as the `--simulate` option if you wish to check a command's behavior before actually running it.
