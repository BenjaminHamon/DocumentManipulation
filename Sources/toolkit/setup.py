# cspell:words dateutil lxml

import os
import sys

import setuptools

workspace_directory = os.path.abspath(os.path.join("..", ".."))
automation_setup_directory = os.path.join(workspace_directory, "Automation", "Setup")

sys.path.insert(0, automation_setup_directory)

import automation_helpers # pylint: disable = wrong-import-position


def run_setup() -> None:
    project_configuration = automation_helpers.load_project_configuration(workspace_directory)

    setuptools.setup(
		name = "benjaminhamon-document-manipulation-toolkit",
		description = "Toolkit and scripts for manipulating text documents",
        version = project_configuration["ProjectVersionFull"],
        author = project_configuration["Author"],
        author_email = project_configuration["AuthorEmail"],
        url = project_configuration["ProjectUrl"],
        packages = setuptools.find_packages(include = [ "benjaminhamon_document_manipulation_toolkit", "benjaminhamon_document_manipulation_toolkit.*" ]),
        python_requires = "~= 3.9",

        install_requires = [
            "lxml ~= 4.9.3",
            "lxml-stubs ~= 0.4.0",
            "python-dateutil ~= 2.8.2",
            "PyYAML ~= 6.0.1",
        ],
    )


run_setup()
