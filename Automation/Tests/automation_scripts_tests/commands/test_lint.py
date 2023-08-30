import argparse
import json
import os

import mockito
import pytest

from bhamon_development_toolkit.automation import automation_helpers
from bhamon_development_toolkit.python.python_package import PythonPackage

from automation_scripts.commands.lint import LintCommand
from automation_scripts.configuration.project_configuration import ProjectConfiguration


@pytest.mark.asyncio
async def test_run_with_success(tmpdir):

    def generate_dummy_python_package(python_package: PythonPackage) -> None:
        if python_package.path_to_tests is None:
            raise ValueError("Path to tests must not be none")

        source_directory = os.path.join(python_package.path_to_sources, python_package.name_for_file_system)
        test_directory = os.path.join(python_package.path_to_tests, python_package.name_for_file_system + "_tests")

        os.makedirs(source_directory)
        with open(os.path.join(source_directory, "__init__.py"), mode = "w", encoding = "utf-8") as source_file:
            pass
        with open(os.path.join(source_directory, "my_module.py"), mode = "w", encoding = "utf-8") as source_file:
            source_file.write("\"\"\"Sample module\"\"\"\n")

        os.makedirs(test_directory)

        with open(os.path.join(test_directory, "__init__.py"), mode = "w", encoding = "utf-8") as source_file:
            pass
        with open(os.path.join(test_directory, "test_my_module.py"), mode = "w", encoding = "utf-8") as source_file:
            source_file.write("\"\"\"Unit tests for sample module\"\"\"\n")

    with automation_helpers.execute_in_workspace(tmpdir):
        project_configuration = mockito.mock(spec = ProjectConfiguration)

        python_package = PythonPackage(
            identifier = "my-python-package",
            path_to_sources = os.path.join("Sources", "my_package"),
            path_to_tests = os.path.join("Tests", "my_package"))

        generate_dummy_python_package(python_package)

        command = LintCommand()
        arguments = argparse.Namespace(run_identifier = "my-run-identifier")

        mockito.when(project_configuration).list_python_packages().thenReturn([ python_package ])

        await command.run_async(arguments, configuration = project_configuration, simulate = False)

        log_file_path = os.path.join("Artifacts", "LintResults", arguments.run_identifier, python_package.identifier + ".log")
        with open(log_file_path, mode = "r", encoding = "utf-8") as log_file:
            assert log_file.read() == ""

        report_file_path = os.path.join("Artifacts", "LintResults", arguments.run_identifier, python_package.identifier + ".json")
        with open(report_file_path, mode = "r", encoding = "utf-8") as report_file:
            assert json.load(report_file) == []

        log_file_path = os.path.join("Artifacts", "LintResults", arguments.run_identifier, python_package.identifier + "-tests.log")
        with open(log_file_path, mode = "r", encoding = "utf-8") as log_file:
            assert log_file.read() == ""

        report_file_path = os.path.join("Artifacts", "LintResults", arguments.run_identifier, python_package.identifier + "-tests.json")
        with open(report_file_path, mode = "r", encoding = "utf-8") as report_file:
            assert json.load(report_file) == []


@pytest.mark.asyncio
async def test_run_with_failure_in_sources(tmpdir):

    def generate_dummy_python_package(python_package: PythonPackage) -> None:
        if python_package.path_to_tests is None:
            raise ValueError("Path to tests must not be none")

        source_directory = os.path.join(python_package.path_to_sources, python_package.name_for_file_system)
        test_directory = os.path.join(python_package.path_to_tests, python_package.name_for_file_system + "_tests")

        os.makedirs(source_directory)
        with open(os.path.join(source_directory, "__init__.py"), mode = "w", encoding = "utf-8") as source_file:
            pass
        with open(os.path.join(source_directory, "my_module.py"), mode = "w", encoding = "utf-8") as source_file:
            source_file.write("def my_function():\n    do_nothing()")

        os.makedirs(test_directory)

        with open(os.path.join(test_directory, "__init__.py"), mode = "w", encoding = "utf-8") as source_file:
            pass
        with open(os.path.join(test_directory, "test_my_module.py"), mode = "w", encoding = "utf-8") as source_file:
            source_file.write("\"\"\"Unit tests for sample module\"\"\"\n")

    with automation_helpers.execute_in_workspace(tmpdir):
        project_configuration = mockito.mock(spec = ProjectConfiguration)

        python_package = PythonPackage(
            identifier = "my-python-package",
            path_to_sources = os.path.join("Sources", "my_package"),
            path_to_tests = os.path.join("Tests", "my_package"))

        generate_dummy_python_package(python_package)

        command = LintCommand()
        arguments = argparse.Namespace(run_identifier = "my-run-identifier")

        mockito.when(project_configuration).list_python_packages().thenReturn([ python_package ])

        with pytest.raises(RuntimeError):
            await command.run_async(arguments, configuration = project_configuration, simulate = False)

        log_file_path = os.path.join("Artifacts", "LintResults", arguments.run_identifier, python_package.identifier + ".log")
        with open(log_file_path, mode = "r", encoding = "utf-8") as log_file:
            assert log_file.read() != ""

        report_file_path = os.path.join("Artifacts", "LintResults", arguments.run_identifier, python_package.identifier + ".json")
        with open(report_file_path, mode = "r", encoding = "utf-8") as report_file:
            assert json.load(report_file) != []

        log_file_path = os.path.join("Artifacts", "LintResults", arguments.run_identifier, python_package.identifier + "-tests.log")
        with open(log_file_path, mode = "r", encoding = "utf-8") as log_file:
            assert log_file.read() == ""

        report_file_path = os.path.join("Artifacts", "LintResults", arguments.run_identifier, python_package.identifier + "-tests.json")
        with open(report_file_path, mode = "r", encoding = "utf-8") as report_file:
            assert json.load(report_file) == []


@pytest.mark.asyncio
async def test_run_with_failure_in_tests(tmpdir):

    def generate_dummy_python_package(python_package: PythonPackage) -> None:
        if python_package.path_to_tests is None:
            raise ValueError("Path to tests must not be none")

        source_directory = os.path.join(python_package.path_to_sources, python_package.name_for_file_system)
        test_directory = os.path.join(python_package.path_to_tests, python_package.name_for_file_system + "_tests")

        os.makedirs(source_directory)
        with open(os.path.join(source_directory, "__init__.py"), mode = "w", encoding = "utf-8") as source_file:
            pass
        with open(os.path.join(source_directory, "my_module.py"), mode = "w", encoding = "utf-8") as source_file:
            source_file.write("\"\"\"Sample module\"\"\"\n")

        os.makedirs(test_directory)

        with open(os.path.join(test_directory, "__init__.py"), mode = "w", encoding = "utf-8") as source_file:
            pass
        with open(os.path.join(test_directory, "test_my_module.py"), mode = "w", encoding = "utf-8") as source_file:
            source_file.write("def my_function():\n    do_nothing()")

    with automation_helpers.execute_in_workspace(tmpdir):
        project_configuration = mockito.mock(spec = ProjectConfiguration)

        python_package = PythonPackage(
            identifier = "my-python-package",
            path_to_sources = os.path.join("Sources", "my_package"),
            path_to_tests = os.path.join("Tests", "my_package"))

        generate_dummy_python_package(python_package)

        command = LintCommand()
        arguments = argparse.Namespace(run_identifier = "my-run-identifier")

        mockito.when(project_configuration).list_python_packages().thenReturn([ python_package ])

        with pytest.raises(RuntimeError):
            await command.run_async(arguments, configuration = project_configuration, simulate = False)

        log_file_path = os.path.join("Artifacts", "LintResults", arguments.run_identifier, python_package.identifier + ".log")
        with open(log_file_path, mode = "r", encoding = "utf-8") as log_file:
            assert log_file.read() == ""

        report_file_path = os.path.join("Artifacts", "LintResults", arguments.run_identifier, python_package.identifier + ".json")
        with open(report_file_path, mode = "r", encoding = "utf-8") as report_file:
            assert json.load(report_file) == []

        log_file_path = os.path.join("Artifacts", "LintResults", arguments.run_identifier, python_package.identifier + "-tests.log")
        with open(log_file_path, mode = "r", encoding = "utf-8") as log_file:
            assert log_file.read() != ""

        report_file_path = os.path.join("Artifacts", "LintResults", arguments.run_identifier, python_package.identifier + "-tests.json")
        with open(report_file_path, mode = "r", encoding = "utf-8") as report_file:
            assert json.load(report_file) != []


@pytest.mark.asyncio
async def test_run_with_simulate(tmpdir):
    with automation_helpers.execute_in_workspace(tmpdir):
        project_configuration = mockito.mock(spec = ProjectConfiguration)
        python_package = PythonPackage(identifier = "my-python-package", path_to_sources = "Sources", path_to_tests = "Tests")

        command = LintCommand()
        arguments = argparse.Namespace(run_identifier = "my-run-identifier")

        mockito.when(project_configuration).list_python_packages().thenReturn([ python_package ])

        await command.run_async(arguments, configuration = project_configuration, simulate = True)
