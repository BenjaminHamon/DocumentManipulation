import logging
import os
import platform
from typing import List, Optional

from bhamon_development_toolkit.python import python_helpers as python_helpers_base
from bhamon_development_toolkit.processes.executable_command import ExecutableCommand

# Exposing base functions
from bhamon_development_toolkit.python.python_helpers import find_and_check_system_python_executable # pylint: disable = unused-import
from bhamon_development_toolkit.python.python_helpers import find_system_python_executable # pylint: disable = unused-import
from bhamon_development_toolkit.python.python_helpers import setup_virtual_environment # pylint: disable = unused-import
from bhamon_development_toolkit.python.python_helpers import run_python_command


logger = logging.getLogger("Python")


def get_venv_python_executable(venv_directory: str) -> str:
    return get_venv_executable(venv_directory, "python")


def get_venv_executable(venv_directory: str, executable: str) -> str:
    if platform.system() == "Windows":
        return os.path.join(venv_directory, "scripts", executable + ".exe")
    return os.path.join(venv_directory, "bin", executable)


def install_python_packages(python_executable: str,
        name_or_path_collection: List[str], python_package_repository: Optional[str] = None, simulate: bool = False) -> None:

    install_command = ExecutableCommand(python_executable)
    install_command.add_arguments([ "-m", "pip", "install", "--upgrade" ])

    if python_package_repository is not None:
        install_command.add_arguments([ "--extra-index", python_package_repository ])

    install_command.add_arguments(name_or_path_collection)

    run_python_command(install_command, simulate = simulate)


def install_python_packages_for_development(python_executable: str,
        name_or_path_collection: List[str], python_package_repository: Optional[str] = None, simulate: bool = False) -> None:

    python_helpers_base.install_python_packages(python_executable, name_or_path_collection, python_package_repository, simulate = simulate)
