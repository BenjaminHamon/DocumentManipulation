import json
import os

from bhamon_development_toolkit.automation.project_version import ProjectVersion
from bhamon_development_toolkit.python.python_package import PythonPackage
from bhamon_development_toolkit.revision_control.git_client import GitClient

from automation_scripts.configuration.application_development_configuration import ApplicationDevelopmentConfiguration
from automation_scripts.configuration.automation_configuration import AutomationConfiguration
from automation_scripts.configuration.project_metadata import ProjectMetadata
from automation_scripts.configuration.python_development_configuration import PythonDevelopmentConfiguration
from automation_scripts.configuration.workspace_environment import WorkspaceEnvironment
from automation_scripts.toolkit.applications.application_package_configuration import ApplicationPackageConfiguration


def load_automation_configuration() -> AutomationConfiguration:
    automation_python_package = PythonPackage(
        identifier = "automation-scripts",
        path_to_sources = os.path.join("Automation", "Scripts"),
        path_to_tests = os.path.join("Automation", "Tests"))

    return AutomationConfiguration(
        project_metadata = load_project_metadata(),
        python_development_configuration = load_python_development_configuration(),
        application_development_configuration = load_application_development_configuration(),
        workspace_environment = load_workspace_environment(),
        automation_python_package = automation_python_package,
    )


def load_project_metadata() -> ProjectMetadata:
    json_file_path = "ProjectConfiguration.json"
    with open(json_file_path, mode = "r", encoding = "utf-8") as json_file:
        project_configuration_as_dict = json.load(json_file)

    return ProjectMetadata(
        identifier = project_configuration_as_dict["ProjectIdentifier"],
        display_name = project_configuration_as_dict["ProjectDisplayName"],
        version = load_project_version(project_configuration_as_dict["ProjectVersionIdentifier"]),
        copyright_text = project_configuration_as_dict["Copyright"],
        author = project_configuration_as_dict["Author"],
        author_email = project_configuration_as_dict["AuthorEmail"],
        project_url = project_configuration_as_dict["ProjectUrl"],
    )


def load_project_version(identifier: str) -> ProjectVersion:
    git_client = GitClient("git")

    revision = git_client.get_current_revision()
    revision_date = git_client.get_revision_date(revision)
    branch = git_client.get_current_branch()

    return ProjectVersion(
        identifier = identifier,
        revision = revision,
        revision_date = revision_date,
        branch = branch,
    )


def load_python_development_configuration() -> PythonDevelopmentConfiguration:
    return PythonDevelopmentConfiguration(
        venv_directory = ".venv",
        package_collection = [
            PythonPackage(
                identifier = "benjaminhamon-document-manipulation-application",
                path_to_sources = os.path.join("Sources", "application"),
                path_to_tests = os.path.join("Tests", "application")),

            PythonPackage(
                identifier = "benjaminhamon-document-manipulation-scripts",
                path_to_sources = os.path.join("Sources", "scripts"),
                path_to_tests = os.path.join("Tests", "scripts")),

            PythonPackage(
                identifier = "benjaminhamon-document-manipulation-toolkit",
                path_to_sources = os.path.join("Sources", "toolkit"),
                path_to_tests = os.path.join("Tests", "toolkit")),
        ]
    )


def load_application_development_configuration() -> ApplicationDevelopmentConfiguration:
    return ApplicationDevelopmentConfiguration(
        python_package_identifier = "benjaminhamon-document-manipulation-application",
        package_configuration_collection = [
            ApplicationPackageConfiguration(
                configuration_identifier = "LinuxApplication",
                target_operating_system = "Linux",
                target_application_environment = "Linux",
                files_to_include = [
                    ("About.md", "About.md"),
                    ("Artifacts/Binaries/Linux/DocumentManipulation", "DocumentManipulation"),
                    ("Documentation/Application/ReadMe.md", "ReadMe.md"),
                    ("License.txt", "License.txt"),
                ]),

            ApplicationPackageConfiguration(
                configuration_identifier = "WindowsApplication",
                target_operating_system = "Windows",
                target_application_environment = "Windows",
                files_to_include = [
                    ("About.md", "About.md"),
                    ("Artifacts/Binaries/Windows/DocumentManipulation.exe", "DocumentManipulation.exe"),
                    ("Documentation/Application/ReadMe.md", "ReadMe.md"),
                    ("License.txt", "License.txt"),
                ]),
            ]
        )


def load_workspace_environment() -> WorkspaceEnvironment:
    return WorkspaceEnvironment()
